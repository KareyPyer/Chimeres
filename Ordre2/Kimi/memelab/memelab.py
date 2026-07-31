#!/usr/bin/env python3
"""
MemeLab Viz & Mining — Exploration visuelle & quantitative de dynamiques mémétiques
Auteur : spécialiste mémétique (style Blackmore / Rushkoff)
Usage : python memelab_viz.py  (placez tous les CSV dans le même dossier ou indiquez data_dir)
"""

import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr, spearmanr
from scipy.spatial.distance import pdist, squareform

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
DATA_DIR = Path(".")          # ou Path("/home/workdir/attachments")
OUTPUT_DIR = Path("memelab_output")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use("dark_background")
sns.set_palette("magma")
pio.templates.default = "plotly_dark"

# ------------------------------------------------------------------
# 1. CHARGEMENT ROBUSTE
# ------------------------------------------------------------------
def safe_read(name, **kwargs):
    path = DATA_DIR / name
    if not path.exists() or path.stat().st_size == 0:
        print(f"[WARN] {name} manquant ou vide → DataFrame vide")
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, **kwargs)
        print(f"[OK] {name}: {len(df)} lignes, {len(df.columns)} colonnes")
        return df
    except Exception as e:
        print(f"[ERR] {name}: {e}")
        return pd.DataFrame()

print("=== Chargement des artefacts mémétiques ===")
artefacts     = safe_read("artefacts.csv")
resonance     = safe_read("symbolic_resonance.csv")
episodic      = safe_read("episodic_memory.csv")
alliances     = safe_read("alliances.csv")
factions      = safe_read("factions.csv")
semantic_drift= safe_read("semantic_drift.csv")
chronicle     = safe_read("chronicle.csv")
myths         = safe_read("myths.csv")
interactions  = safe_read("interactions.csv")
random_events = safe_read("random_events.csv")
narrative_ev  = safe_read("narrative_events.csv")
daily         = safe_read("daily_metrics.csv")
strains       = safe_read("strains_state.csv")
agents        = safe_read("agents_state.csv")

# ------------------------------------------------------------------
# 2. NETTOYAGE & FEATURE ENGINEERING LÉGER
# ------------------------------------------------------------------
if not daily.empty:
    daily = daily.sort_values("timestamp")

if not agents.empty:
    # Dernier état de chaque agent (snapshot final)
    agents_last = agents.sort_values("timestamp").groupby("agent_id").last().reset_index()
    # États au fil du temps (pour animations / heatmaps)
    agents["status"] = agents["status"].astype(str)

if not strains.empty:
    strains = strains.sort_values(["timestamp", "strain_id"])

if not interactions.empty:
    interactions["transmission_occurred"] = interactions["transmission_occurred"].astype(int)

# ------------------------------------------------------------------
# 3. STATISTIQUES DESCRIPTIVES + MATRICES (Data Mining ready)
# ------------------------------------------------------------------
def compute_basic_stats():
    stats = {}
    if not daily.empty:
        stats["daily_summary"] = daily.describe().T
        stats["final_compartments"] = daily.iloc[-1][["cult_S","cult_E","cult_I","cult_A","cult_R","cult_D"]].to_dict()
        stats["peak_I"] = daily["cult_I"].max()
        stats["mean_Rt"] = daily["rt"].mean()

    if not agents_last.empty:
        stats["status_dist"] = agents_last["status"].value_counts().to_dict()
        stats["guild_dist"]  = agents_last["guild"].value_counts().to_dict()
        stats["zone_dist"]   = agents_last["zone"].value_counts().to_dict()
        stats["strain_dist"] = agents_last["strain_id"].value_counts().to_dict()

    if not strains.empty:
        last_strains = strains.groupby("strain_id").last()
        stats["strains_final"] = last_strains[["contagion_power","dogma_intensity","total_adherents","prevalence"]].to_dict()

    return stats

stats = compute_basic_stats()
pd.Series(stats).to_json(OUTPUT_DIR / "basic_stats.json", indent=2)
print("[OK] Stats de base exportées")

# Matrice de corrélation sur métriques journalières
if not daily.empty and len(daily) > 5:
    corr_daily = daily.select_dtypes(include=[np.number]).corr()
    corr_daily.to_csv(OUTPUT_DIR / "corr_daily_metrics.csv")
    print("[OK] Matrice corrélation daily_metrics")

# Matrice de similarité textuelle des mantras (artefacts)
if not artefacts.empty and "mantra_text" in artefacts.columns:
    texts = artefacts["mantra_text"].fillna("").astype(str).tolist()
    if len(texts) > 1:
        tfidf = TfidfVectorizer(max_features=200, ngram_range=(1,2), min_df=1)
        X = tfidf.fit_transform(texts)
        sim = cosine_similarity(X)
        sim_df = pd.DataFrame(sim, index=artefacts.index, columns=artefacts.index)
        sim_df.to_csv(OUTPUT_DIR / "mantra_cosine_similarity.csv")
        print("[OK] Matrice similarité cosinus des mantras")

# Graphe d’infection (NetworkX) + degrés, centralité
G = nx.DiGraph()
if not interactions.empty:
    for _, row in interactions.iterrows():
        if row["transmission_occurred"] == 1:
            G.add_edge(row["agent_a"], row["agent_b"],
                       weight=row["intensity"],
                       risk=row["transmission_risk"],
                       t=row["timestamp"])
    # Ajout des infections déclarées dans episodic_memory
    if not episodic.empty:
        for _, row in episodic[episodic["event_type"]=="infection"].iterrows():
            # parsing grossier "Infecté par Agent#X"
            content = str(row["content"])
            if "Agent#" in content:
                try:
                    src = int(content.split("Agent#")[1].split()[0])
                    G.add_edge(src, row["agent_id"], t=row["timestamp"], type="declared")
                except:
                    pass

    nx.write_gexf(G, OUTPUT_DIR / "infection_network.gexf")
    degree_df = pd.DataFrame(dict(G.degree(weight="weight")).items(), columns=["agent","weighted_degree"])
    degree_df.to_csv(OUTPUT_DIR / "infection_degrees.csv", index=False)
    print(f"[OK] Réseau d’infection : {G.number_of_nodes()} nœuds, {G.number_of_edges()} arcs")

# ------------------------------------------------------------------
# 4. VISUALISATIONS INTERACTIVES (Plotly)
# ------------------------------------------------------------------
def plot_daily_dashboard():
    if daily.empty:
        return
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=("Compartiments culturels (S-E-I-A-R-D)", "Rₜ effectif",
                        "Nombre de strains / myths / factions", "Prévalence & adhérents",
                        "Événements narratifs cumulés", "Heatmap corrélation"),
        specs=[[{}, {}], [{}, {}], [{}, {}]]
    )

    # 1. Compartiments
    for col, name in [("cult_S","S"),("cult_E","E"),("cult_I","I"),
                      ("cult_A","A"),("cult_R","R"),("cult_D","D")]:
        if col in daily.columns:
            fig.add_trace(go.Scatter(x=daily["timestamp"], y=daily[col],
                                     name=name, mode="lines"), row=1, col=1)

    # 2. Rₜ
    if "rt" in daily.columns:
        fig.add_trace(go.Scatter(x=daily["timestamp"], y=daily["rt"],
                                 name="Rₜ", line=dict(color="orange")), row=1, col=2)

    # 3. Compteurs
    for col, name in [("nb_strains","strains"),("nb_myths","myths"),("nb_factions","factions")]:
        if col in daily.columns:
            fig.add_trace(go.Scatter(x=daily["timestamp"], y=daily[col],
                                     name=name, mode="lines+markers"), row=2, col=1)

    # 4. Placeholder pour prévalence (à enrichir avec strains)
    fig.add_trace(go.Scatter(x=daily["timestamp"], y=daily.get("cult_I",0),
                             name="Infectés (proxy)", fill="tozeroy"), row=2, col=2)

    # 5. Événements (si narrative_events)
    if not narrative_ev.empty:
        cum = narrative_ev.groupby("timestamp").size().cumsum().reset_index(name="cum_events")
        fig.add_trace(go.Scatter(x=cum["timestamp"], y=cum["cum_events"],
                                 name="Événements narratifs", fill="tozeroy"), row=3, col=1)

    # 6. Heatmap corrélation
    if not daily.empty:
        num = daily.select_dtypes(include=[np.number])
        if num.shape[1] > 1:
            corr = num.corr()
            fig.add_trace(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns,
                                     colorscale="RdBu", zmid=0), row=3, col=2)

    fig.update_layout(height=1100, title_text="MemeLab — Dashboard épidémiologie culturelle",
                      showlegend=True)
    fig.write_html(OUTPUT_DIR / "dashboard_daily.html")
    fig.show()
    print("[OK] Dashboard daily sauvegardé")

plot_daily_dashboard()

# ------------------------------------------------------------------
# 5. RÉSEAU D’INFECTION INTERACTIF
# ------------------------------------------------------------------
def plot_infection_network():
    if G.number_of_nodes() == 0:
        return
    pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42)
    edge_x, edge_y = [], []
    for e in G.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    degrees = [G.degree(n) for n in G.nodes()]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines",
                             line=dict(width=0.5, color="#888"), hoverinfo="none"))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers",
                             marker=dict(size=[d*3+5 for d in degrees],
                                         color=degrees, colorscale="Plasma",
                                         showscale=True, colorbar=dict(title="Degré")),
                             text=[f"Agent {n}<br>degré={G.degree(n)}" for n in G.nodes()],
                             hoverinfo="text"))
    fig.update_layout(title="Réseau de transmission mémétique (infections confirmées)",
                      showlegend=False, height=700)
    fig.write_html(OUTPUT_DIR / "infection_network.html")
    fig.show()
    print("[OK] Réseau interactif sauvegardé")

plot_infection_network()

# ------------------------------------------------------------------
# 6. VISUALISATIONS STATIQUES CLÉS
# ------------------------------------------------------------------
def static_plots():
    # Évolution des compartiments
    if not daily.empty:
        fig, ax = plt.subplots(figsize=(12,6))
        for col in ["cult_S","cult_E","cult_I","cult_A","cult_R","cult_D"]:
            if col in daily.columns:
                ax.plot(daily["timestamp"], daily[col], label=col.replace("cult_",""))
        ax.set_title("Dynamique des compartiments culturels")
        ax.legend()
        ax.set_xlabel("Temps")
        fig.savefig(OUTPUT_DIR / "compartments_timeseries.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Distribution finale des statuts / guildes / zones
    if not agents_last.empty:
        fig, axes = plt.subplots(1,3, figsize=(15,4))
        agents_last["status"].value_counts().plot(kind="bar", ax=axes[0], color="cyan")
        axes[0].set_title("Statuts finaux")
        agents_last["guild"].value_counts().plot(kind="bar", ax=axes[1], color="magenta")
        axes[1].set_title("Guildes")
        agents_last["zone"].value_counts().plot(kind="bar", ax=axes[2], color="yellow")
        axes[2].set_title("Zones")
        plt.tight_layout()
        fig.savefig(OUTPUT_DIR / "final_distributions.png", dpi=150)
        plt.close()

    # Heatmap corrélation agents (attributs numériques)
    if not agents_last.empty:
        num_cols = agents_last.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 3:
            corr = agents_last[num_cols].corr()
            plt.figure(figsize=(10,8))
            sns.heatmap(corr, cmap="coolwarm", center=0, annot=False)
            plt.title("Corrélation attributs agents (snapshot final)")
            plt.savefig(OUTPUT_DIR / "agents_attr_corr.png", dpi=150, bbox_inches="tight")
            plt.close()

static_plots()
print("[OK] Graphiques statiques générés")

# ------------------------------------------------------------------
# 7. EXPORTS SUPPLÉMENTAIRES POUR DATA MINING HARDCORE
# ------------------------------------------------------------------
# Table agent × strain (co-occurrence)
if not agents.empty and "strain_id" in agents.columns:
    agent_strain = pd.crosstab(agents["agent_id"], agents["strain_id"])
    agent_strain.to_csv(OUTPUT_DIR / "agent_strain_crosstab.csv")

# Timeline des mutations / éclipses
if not episodic.empty:
    mut = episodic[episodic["event_type"].isin(["mutation","narrative_eclipse","disenchantment"])]
    mut.to_csv(OUTPUT_DIR / "key_narrative_events.csv", index=False)

# Features textuelles simples des artefacts
if not artefacts.empty and "mantra_text" in artefacts.columns:
    artefacts["mantra_len"] = artefacts["mantra_text"].str.len()
    artefacts["has_tag"] = artefacts["mantra_text"].str.contains(r"<[^>]+>", regex=True).astype(int)
    artefacts[["agent_id","aesthetic_score","complexity","symmetry","glitch_factor","entropy_level",
               "mantra_len","has_tag"]].to_csv(OUTPUT_DIR / "artefact_features.csv", index=False)

print("\n=== MemeLab terminé ===")
print(f"Tous les outputs sont dans : {OUTPUT_DIR.resolve()}")
print("Fichiers clés : dashboard_daily.html, infection_network.html, *.csv, *.png")
print("Prêt pour la phase Data Mining hardcore (clustering de mantras, SIR généralisé,")
print("prédiction de Rₜ, détection de super-spreaders, drift sémantique, etc.)")
