#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memetic_explorer.py
====================

Corpus Vauvillensis / Latent Fracturo Studio — Memetic DataViz & Data Mining Toolkit
--------------------------------------------------------------------------------------

Un instrument d'exploration pour les sorties du simulateur épidémio-mémétique
(agents, souches (strains), factions, artefacts, mythes, événements).

Philosophie
-----------
Ce module traite les données non comme de simples logs, mais comme la trace
fossile d'un écosystème de réplicateurs culturels (au sens de Blackmore/Dawkins) :
    - FIDÉLITÉ  -> stabilité du mantra / cohérence narrative
    - FÉCONDITÉ -> contagion_power, meme_virulence, taux de transmission
    - LONGÉVITÉ -> prevalence dans le temps, résistance au désenchantement

Chaque visualisation cherche un équilibre entre lisibilité analytique
(un chercheur doit pouvoir lire un chiffre) et lisibilité *sensible*
(un pattern doit pouvoir être *senti* avant d'être mesuré) — dans l'esprit
d'un tableau de bord d'épidémiologiste culturel à la Rushkoff.

Usage rapide
------------
    from memetic_explorer import MemeticExplorer

    mx = MemeticExplorer(data_dir="/path/to/csvs", output_dir="/path/to/output")
    mx.run_full_pipeline()          # génère TOUTES les visus + tout le data mining
    mx.generate_dashboard()         # une seule planche de synthèse (overview)

Chaque méthode `plot_*` peut aussi être appelée isolément pour l'exploration
interactive en notebook Jupyter (cohérent avec le reste de l'écosystème LFS).

Dépendances : pandas, numpy, matplotlib, seaborn, networkx, scikit-learn, scipy
(aucune dépendance réseau, tout est calculé localement).
"""

from __future__ import annotations

import ast
import json
import os
import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyArrowPatch
import matplotlib.gridspec as gridspec
import seaborn as sns
import networkx as nx

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy import stats

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ----------------------------------------------------------------------------
# ESTHÉTIQUE — palette "glitch-rituel" cohérente avec l'univers Corpus 2075
# ----------------------------------------------------------------------------

BG = "#0b0d12"
FG = "#e8e6df"
GRID = "#262a35"
ACCENT = ["#c5fb38", "#ff5fa2", "#38d1fb", "#ffaa00", "#a06bff", "#ff3838", "#38fbb0"]

STATUS_COLORS = {
    "S": "#38d1fb",  # Receptive / susceptible
    "E": "#ffaa00",  # Exposed
    "I": "#ff3838",  # Evangelist (infectious)
    "A": "#a06bff",  # Silent carrier (asymptomatic)
    "R": "#38fbb0",  # Disenchanted (recovered/resistant)
    "D": "#5a5f6e",  # Dormant/dead (if present)
}
STATUS_LABELS = {
    "S": "Réceptifs",
    "E": "Exposés",
    "I": "Évangélistes",
    "A": "Porteurs silencieux",
    "R": "Désenchantés",
    "D": "Dormants",
}


def _apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "axes.edgecolor": GRID,
        "axes.labelcolor": FG,
        "axes.titlecolor": FG,
        "xtick.color": FG,
        "ytick.color": FG,
        "text.color": FG,
        "grid.color": GRID,
        "grid.alpha": 0.5,
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "savefig.facecolor": BG,
        "figure.dpi": 130,
        "axes.grid": True,
        "grid.linestyle": ":",
        "legend.facecolor": "#12141c",
        "legend.edgecolor": GRID,
    })


_apply_dark_theme()
_MEME_CMAP = mcolors.LinearSegmentedColormap.from_list(
    "meme_glitch", ["#0b0d12", "#38d1fb", "#c5fb38", "#ffaa00", "#ff3838"]
)


def _safe_literal(x):
    """Parse une chaîne dict/list "à la Python" (issue de repr()) en objet."""
    if isinstance(x, (dict, list)):
        return x
    if not isinstance(x, str) or not x.strip():
        return None
    try:
        return ast.literal_eval(x)
    except (ValueError, SyntaxError):
        try:
            return json.loads(x)
        except Exception:
            return None


def _safe_json(x):
    if isinstance(x, (dict, list)):
        return x
    if not isinstance(x, str) or not x.strip():
        return None
    try:
        return json.loads(x)
    except Exception:
        return _safe_literal(x)


class MemeticExplorer:
    """
    Point d'entrée unique pour explorer un run du simulateur mémétique.

    Charge tous les CSV attendus (silencieusement tolérant aux fichiers
    manquants ou vides — un run court peut ne pas produire de mythes,
    par exemple), et expose :
      - des méthodes `plot_*`  -> figures PNG (viz)
      - des méthodes `compute_*` -> tables de data mining (CSV/JSON)
      - `run_full_pipeline()` -> tout génère, avec rapport de synthèse.
    """

    FILES = [
        "agents_state", "artefacts", "symbolic_resonance", "episodic_memory",
        "alliances", "factions", "semantic_drift", "chronicle", "myths",
        "interactions", "random_events", "narrative_events", "daily_metrics",
        "strains_state",
    ]

    def __init__(self, data_dir: str, output_dir: str = "./memetic_output"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.fig_dir = self.output_dir / "figures"
        self.mining_dir = self.output_dir / "data_mining"
        for d in (self.output_dir, self.fig_dir, self.mining_dir):
            d.mkdir(parents=True, exist_ok=True)

        self.df: dict[str, pd.DataFrame] = {}
        self._load_all()
        self._preprocess()

    # ------------------------------------------------------------------
    # CHARGEMENT
    # ------------------------------------------------------------------

    def _load_all(self):
        for name in self.FILES:
            path = self.data_dir / f"{name}.csv"
            if path.exists():
                try:
                    df = pd.read_csv(path)
                except Exception as e:
                    warnings.warn(f"Impossible de lire {name}.csv : {e}")
                    df = pd.DataFrame()
            else:
                df = pd.DataFrame()
            self.df[name] = df

    def _preprocess(self):
        # --- agents_state : colonnes numériques de trait ---
        a = self.df.get("agents_state", pd.DataFrame())
        self.trait_cols = [c for c in [
            "narrative_fluency", "charisma", "memory_depth", "intelligence",
            "skepticism", "dogma_risk", "expressiveness", "influence_potential",
            "mobility", "altruism", "social_compliance", "curiosity",
            "narrative_recovery",
        ] if c in a.columns]
        self.symbolic_cols = [c for c in [
            "symbolic_complexity", "symbolic_symmetry", "symbolic_glitch",
            "symbolic_entropy", "artefact_fitness",
        ] if c in a.columns]
        # colonnes dynamiques (varient réellement dans le temps / entre agents ;
        # certains runs laissent les traits psycho-cognitifs figés à leur défaut,
        # ces colonnes servent alors de filet de sécurité pour PCA/clustering)
        self.dynamic_cols = [c for c in [
            "narrative_coherence", "meme_virulence", "receptivity", "influence_score",
        ] if c in a.columns]

        # --- artefacts : parse dict fitness_breakdown ---
        art = self.df.get("artefacts", pd.DataFrame())
        if not art.empty and "fitness_breakdown" in art.columns:
            parsed = art["fitness_breakdown"].apply(_safe_literal)
            expand = pd.json_normalize(parsed).add_prefix("fit_")
            self.df["artefacts"] = pd.concat(
                [art.reset_index(drop=True), expand.reset_index(drop=True)], axis=1
            )

        # --- random_events : parse affected_agents + impact (JSON-ish) ---
        re_df = self.df.get("random_events", pd.DataFrame())
        if not re_df.empty:
            if "impact" in re_df.columns:
                re_df["impact_parsed"] = re_df["impact"].apply(_safe_json)
            if "affected_agents" in re_df.columns:
                re_df["affected_agents_list"] = re_df["affected_agents"].apply(
                    lambda s: [int(x) for x in str(s).split(",") if x.strip().isdigit()]
                    if pd.notna(s) else []
                )
            self.df["random_events"] = re_df

        # --- status code normalisation (ordre logique du cycle) ---
        self.status_order = [s for s in ["S", "E", "I", "A", "R", "D"] if
                              s in self.df.get("agents_state", pd.DataFrame()).get("status_code", pd.Series(dtype=str)).unique()
                              or s in [c.replace("cult_", "") for c in self.df.get("daily_metrics", pd.DataFrame()).columns if c.startswith("cult_")]]

    # ------------------------------------------------------------------
    # UTIL
    # ------------------------------------------------------------------

    def _feature_cols_for_clustering(self, df: pd.DataFrame) -> list[str]:
        """Sélectionne, parmi traits + dynamiques + symboliques, les colonnes à
        variance non nulle — évite les PCA/clustering dégénérés quand un run n'a
        pas individualisé certains traits (restés à leur valeur par défaut)."""
        candidates = list(dict.fromkeys(self.trait_cols + self.dynamic_cols + self.symbolic_cols))
        candidates = [c for c in candidates if c in df.columns]
        return [c for c in candidates if df[c].nunique(dropna=True) > 1]

    def _save(self, fig, name: str):
        path = self.fig_dir / f"{name}.png"
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        return path

    def _empty_ax_msg(self, ax, msg="Données insuffisantes pour ce run"):
        ax.text(0.5, 0.5, msg, ha="center", va="center", color="#666a77",
                 fontsize=11, style="italic", transform=ax.transAxes)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    # ------------------------------------------------------------------
    # 1. DYNAMIQUE ÉPIDÉMIQUE — courbes SEIAR-D
    # ------------------------------------------------------------------

    def plot_epidemic_curves(self, save=True):
        """Courbes de compartiments culturels (cult_S/E/I/A/R/D) dans le temps,
        + taux de reproduction effectif rt en second axe — la 'météo' de l'épidémie."""
        dm = self.df.get("daily_metrics", pd.DataFrame())
        fig, ax1 = plt.subplots(figsize=(11, 6))
        if dm.empty:
            self._empty_ax_msg(ax1)
            return self._save(fig, "01_epidemic_curves") if save else fig

        cult_cols = [c for c in dm.columns if c.startswith("cult_")]
        for c in cult_cols:
            code = c.replace("cult_", "")
            color = STATUS_COLORS.get(code, "#999999")
            label = STATUS_LABELS.get(code, code)
            ax1.plot(dm["timestamp"], dm[c], label=label, color=color, linewidth=2.2)
            ax1.fill_between(dm["timestamp"], dm[c], alpha=0.06, color=color)

        ax1.set_xlabel("Temps (pas de simulation)")
        ax1.set_ylabel("Nombre d'agents")
        ax1.set_title("Dynamique épidémio-mémétique — compartiments culturels (SEIAR-D)",
                       fontsize=13, fontweight="bold")
        ax1.legend(loc="upper left", frameon=True, ncol=2, fontsize=9)

        if "rt" in dm.columns:
            ax2 = ax1.twinx()
            ax2.plot(dm["timestamp"], dm["rt"], color="#ff5fa2", linewidth=1.2,
                      linestyle="--", alpha=0.85, label="Rt (taux repro. effectif)")
            ax2.axhline(1.0, color="#ff5fa2", linewidth=0.6, alpha=0.4)
            ax2.set_ylabel("Rt effectif", color="#ff5fa2")
            ax2.tick_params(axis="y", colors="#ff5fa2")
            ax2.grid(False)

        fig.tight_layout()
        return self._save(fig, "01_epidemic_curves") if save else fig

    # ------------------------------------------------------------------
    # 2. PHYLOGÉNIE DES SOUCHES — arbre de mutation mémétique
    # ------------------------------------------------------------------

    def plot_strain_phylogeny(self, save=True):
        """Arbre généalogique des souches (strains) : noeud = souche à son pic,
        taille = adhérents totaux max, couleur = puissance de contagion."""
        ss = self.df.get("strains_state", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(10, 7))
        if ss.empty:
            self._empty_ax_msg(ax)
            return self._save(fig, "02_strain_phylogeny") if save else fig

        agg = ss.groupby("strain_id").agg(
            parent_id=("parent_id", "first"),
            generation=("generation", "first"),
            contagion_power=("contagion_power", "max"),
            dogma_intensity=("dogma_intensity", "mean"),
            total_adherents=("total_adherents", "max"),
            mutation_count=("mutation_count", "max"),
            emergence_time=("emergence_time", "min"),
            theme=("mantra_theme", "first"),
        ).reset_index()

        G = nx.DiGraph()
        for _, row in agg.iterrows():
            G.add_node(row["strain_id"], **row.to_dict())
        for _, row in agg.iterrows():
            if pd.notna(row["parent_id"]) and row["parent_id"] in G.nodes:
                G.add_edge(row["parent_id"], row["strain_id"])

        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        except Exception:
            # fallback : layout par génération (x) / hash stable (y)
            pos = {}
            gen_counts = {}
            for n in G.nodes:
                g = G.nodes[n]["generation"]
                gen_counts[g] = gen_counts.get(g, 0) + 1
                idx = gen_counts[g]
                pos[n] = (g * 3.0, idx * 1.6 - 0.5)

        sizes = [200 + 60 * G.nodes[n].get("total_adherents", 1) for n in G.nodes]
        colors = [G.nodes[n].get("contagion_power", 0.5) for n in G.nodes]

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#4a4f5e", arrows=True,
                                 arrowstyle="-|>", arrowsize=14, width=1.4,
                                 connectionstyle="arc3,rad=0.08")
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color=colors,
                                         cmap=_MEME_CMAP, vmin=0, vmax=1,
                                         edgecolors="#e8e6df", linewidths=1.0)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color=FG,
                                  font_family="monospace")

        cbar = fig.colorbar(nodes, ax=ax, shrink=0.7, pad=0.02)
        cbar.set_label("Puissance de contagion")
        ax.set_title("Phylogénie mémétique — arbre de mutation des souches",
                      fontsize=13, fontweight="bold")
        ax.set_axis_off()
        fig.tight_layout()
        return self._save(fig, "02_strain_phylogeny") if save else fig

    # ------------------------------------------------------------------
    # 3. RÉSEAU DE FACTIONS — alliances
    # ------------------------------------------------------------------

    def plot_faction_network(self, save=True):
        fa = self.df.get("factions", pd.DataFrame())
        al = self.df.get("alliances", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(9, 8))
        if fa.empty:
            self._empty_ax_msg(ax)
            return self._save(fig, "03_faction_network") if save else fig

        G = nx.Graph()
        for _, row in fa.iterrows():
            G.add_node(row["faction_id"], **row.to_dict())
        if not al.empty:
            for _, row in al.iterrows():
                if row["faction_id"] in G.nodes and row["ally_id"] in G.nodes:
                    G.add_edge(row["faction_id"], row["ally_id"], t=row.get("timestamp"))

        pos = nx.spring_layout(G, seed=42, k=1.4)
        sizes = [300 + 120 * G.nodes[n].get("member_count", 1) for n in G.nodes]
        node_colors = [G.nodes[n].get("color", "#c5fb38") for n in G.nodes]

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#ff5fa2", width=1.6, alpha=0.7)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color=node_colors,
                                 edgecolors="#e8e6df", linewidths=1.2)
        labels = {n: G.nodes[n].get("name", n)[:22] for n in G.nodes}
        nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, font_size=8, font_color=FG)

        ax.set_title("Réseau des factions — alliances émergentes", fontsize=13, fontweight="bold")
        ax.set_axis_off()
        fig.tight_layout()
        return self._save(fig, "03_faction_network") if save else fig

    # ------------------------------------------------------------------
    # 4. RÉSEAU D'INTERACTIONS SOCIALES (agents) — support de transmission
    # ------------------------------------------------------------------

    def plot_interaction_network(self, save=True, only_transmissions=False):
        it = self.df.get("interactions", pd.DataFrame())
        ag = self.df.get("agents_state", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(10, 9))
        if it.empty:
            self._empty_ax_msg(ax)
            return self._save(fig, "04_interaction_network") if save else fig

        data = it[it["transmission_occurred"] == 1] if only_transmissions else it
        G = nx.Graph()
        for _, row in data.iterrows():
            G.add_edge(int(row["agent_a"]), int(row["agent_b"]),
                       weight=row.get("intensity", 1.0),
                       transmitted=bool(row.get("transmission_occurred", 0)))

        # dernier statut connu par agent, pour la couleur
        last_status = {}
        if not ag.empty:
            last = ag.sort_values("timestamp").groupby("agent_id").last()
            last_status = last["status_code"].to_dict()

        pos = nx.spring_layout(G, seed=7, k=0.6 / max(1, np.sqrt(len(G.nodes))))
        node_colors = [STATUS_COLORS.get(last_status.get(n, ""), "#666a77") for n in G.nodes]
        edge_colors = ["#ff5fa2" if G[u][v].get("transmitted") else "#2c3040" for u, v in G.edges]
        edge_widths = [0.4 + 1.6 * G[u][v].get("weight", 1) / (data["intensity"].max() or 1)
                        for u, v in G.edges]

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=edge_widths, alpha=0.6)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=90, node_color=node_colors,
                                 edgecolors="#0b0d12", linewidths=0.5)

        handles = [plt.Line2D([0], [0], marker="o", color="w", label=STATUS_LABELS[k],
                                markerfacecolor=v, markersize=8)
                   for k, v in STATUS_COLORS.items() if k in last_status.values()]
        if handles:
            ax.legend(handles=handles, loc="upper left", fontsize=8, frameon=True)

        title = "Réseau de transmission (contagion réalisée)" if only_transmissions \
            else "Réseau social — toutes interactions (rose = transmission réussie)"
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_axis_off()
        fig.tight_layout()
        name = "04b_transmission_network" if only_transmissions else "04_interaction_network"
        return self._save(fig, name) if save else fig

    # ------------------------------------------------------------------
    # 5. PAYSAGE SYMBOLIQUE — carte de résonance mémétique
    # ------------------------------------------------------------------

    def plot_symbolic_landscape(self, save=True):
        """Carte spatiale des souches dans l'espace de résonance symbolique :
        position = coordonnées de résonance, taille = masse mémétique,
        halo = rayon d'influence."""
        sr = self.df.get("symbolic_resonance", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(9, 9))
        if sr.empty:
            self._empty_ax_msg(ax)
            return self._save(fig, "05_symbolic_landscape") if save else fig

        for _, row in sr.iterrows():
            halo = plt.Circle((row["position_x"], row["position_y"]), row["influence_radius"] * 8,
                                color=ACCENT[hash(row["strain_id"]) % len(ACCENT)], alpha=0.10)
            ax.add_patch(halo)
            ax.scatter(row["position_x"], row["position_y"], s=200 + 400 * row["mass"],
                       color=ACCENT[hash(row["strain_id"]) % len(ACCENT)],
                       edgecolors="white", linewidths=1.0, zorder=5)
            ax.annotate(row["strain_id"], (row["position_x"], row["position_y"]),
                        textcoords="offset points", xytext=(8, 8), fontsize=9,
                        color=FG, fontfamily="monospace")

        ax.set_title("Paysage symbolique — carte de résonance mémétique", fontsize=13, fontweight="bold")
        ax.set_xlabel("position_x (espace symbolique)")
        ax.set_ylabel("position_y (espace symbolique)")
        ax.set_aspect("equal", adjustable="datalim")
        fig.tight_layout()
        return self._save(fig, "05_symbolic_landscape") if save else fig

    # ------------------------------------------------------------------
    # 6. PROFIL PSYCHO-COGNITIF DES AGENTS — coordonnées parallèles
    # ------------------------------------------------------------------

    def plot_agent_trait_parallel(self, save=True, sample: Optional[int] = 400, group_by="status_code"):
        """Coordonnées parallèles des traits psycho-cognitifs des agents,
        colorées par statut épidémique — révèle les profils-types de récepteurs/évangélistes."""
        ag = self.df.get("agents_state", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(13, 6))
        cols = self.trait_cols
        if ag.empty or not cols:
            self._empty_ax_msg(ax)
            return self._save(fig, "06_agent_trait_parallel") if save else fig

        last = ag.sort_values("timestamp").groupby("agent_id").last().reset_index()
        if sample and len(last) > sample:
            last = last.sample(sample, random_state=0)

        norm = last[cols].copy()
        for c in cols:
            rng = norm[c].max() - norm[c].min()
            norm[c] = (norm[c] - norm[c].min()) / rng if rng > 0 else 0.5

        x = np.arange(len(cols))
        for _, row in norm.iterrows():
            code = last.loc[row.name, group_by] if group_by in last.columns else None
            color = STATUS_COLORS.get(code, "#888888")
            ax.plot(x, row[cols].values, color=color, alpha=0.25, linewidth=0.8)

        ax.set_xticks(x)
        ax.set_xticklabels(cols, rotation=35, ha="right", fontsize=8)
        ax.set_ylabel("Valeur normalisée [0,1]")
        ax.set_title("Profils psycho-cognitifs des agents (coordonnées parallèles)",
                      fontsize=13, fontweight="bold")
        handles = [plt.Line2D([0], [0], color=v, label=STATUS_LABELS[k], linewidth=2)
                   for k, v in STATUS_COLORS.items() if k in last[group_by].unique()]
        if handles:
            ax.legend(handles=handles, loc="upper right", fontsize=8, ncol=2)
        fig.tight_layout()
        return self._save(fig, "06_agent_trait_parallel") if save else fig

    # ------------------------------------------------------------------
    # 7. ÉVOLUTION DES STATUTS — aires empilées (proportion, par pas de temps)
    # ------------------------------------------------------------------

    def plot_status_stream(self, save=True):
        ag = self.df.get("agents_state", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(11, 5.5))
        if ag.empty:
            self._empty_ax_msg(ax)
            return self._save(fig, "07_status_stream") if save else fig

        pivot = ag.groupby(["timestamp", "status_code"]).size().unstack(fill_value=0)
        codes = [c for c in ["S", "E", "I", "A", "R", "D"] if c in pivot.columns]
        pivot = pivot[codes]
        colors = [STATUS_COLORS[c] for c in codes]
        ax.stackplot(pivot.index, pivot.T.values, labels=[STATUS_LABELS[c] for c in codes],
                     colors=colors, alpha=0.85)
        ax.set_xlabel("Temps"); ax.set_ylabel("Nb agents (empilé)")
        ax.set_title("Flux des statuts culturels — vue empilée", fontsize=13, fontweight="bold")
        ax.legend(loc="upper left", fontsize=8, ncol=2)
        fig.tight_layout()
        return self._save(fig, "07_status_stream") if save else fig

    # ------------------------------------------------------------------
    # 8. MÉMOIRE ÉPISODIQUE — heatmap type d'événement x temps (pondérée impact)
    # ------------------------------------------------------------------

    def plot_episodic_memory_heatmap(self, save=True, n_bins=20):
        ep = self.df.get("episodic_memory", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(11, 5))
        if ep.empty:
            self._empty_ax_msg(ax)
            return self._save(fig, "08_episodic_memory_heatmap") if save else fig

        ep = ep.copy()
        ep["t_bin"] = pd.cut(ep["timestamp"], bins=min(n_bins, ep["timestamp"].nunique() or 1))
        pivot = ep.pivot_table(index="event_type", columns="t_bin", values="impact",
                                aggfunc="sum", observed=False).fillna(0)
        sns.heatmap(pivot, ax=ax, cmap=_MEME_CMAP, cbar_kws={"label": "Impact cumulé"},
                    linewidths=0.3, linecolor=BG)
        ax.set_xlabel("Fenêtre temporelle")
        ax.set_ylabel("Type d'événement")
        ax.set_title("Mémoire épisodique collective — intensité par type et période",
                      fontsize=13, fontweight="bold")
        ax.set_xticklabels([f"{int(iv.left)}-{int(iv.right)}" for iv in pivot.columns],
                            rotation=45, ha="right", fontsize=7)
        fig.tight_layout()
        return self._save(fig, "08_episodic_memory_heatmap") if save else fig

    # ------------------------------------------------------------------
    # 9. PAYSAGE DE FITNESS DES ARTEFACTS — esthétique vs structure symbolique
    # ------------------------------------------------------------------

    def plot_artefact_fitness_landscape(self, save=True):
        art = self.df.get("artefacts", pd.DataFrame())
        fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
        if art.empty:
            for ax in axes:
                self._empty_ax_msg(ax)
            return self._save(fig, "09_artefact_fitness") if save else fig

        ax = axes[0]
        emotions = art["dominant_emotion"].astype(str).unique() if "dominant_emotion" in art else []
        cmap_e = {e: ACCENT[i % len(ACCENT)] for i, e in enumerate(emotions)}
        for e in emotions:
            sub = art[art["dominant_emotion"] == e]
            ax.scatter(sub["complexity"], sub["aesthetic_score"], s=60 + 300 * sub.get("glitch_factor", 0.2),
                      color=cmap_e[e], alpha=0.75, edgecolors="white", linewidths=0.4, label=e)
        ax.set_xlabel("Complexité symbolique"); ax.set_ylabel("Score esthétique")
        ax.set_title("Fitness des artefacts — complexité vs esthétique\n(taille = facteur de glitch)",
                     fontsize=11, fontweight="bold")
        ax.legend(fontsize=7, loc="best")

        ax2 = axes[1]
        if "fit_linguistic_fitness" in art.columns and "fit_visual_score" in art.columns:
            sc = ax2.scatter(art["fit_linguistic_fitness"], art["fit_visual_score"],
                             c=art["aesthetic_score"], cmap=_MEME_CMAP, s=70,
                             edgecolors="white", linewidths=0.4)
            cbar = fig.colorbar(sc, ax=ax2); cbar.set_label("Score esthétique global")
            ax2.set_xlabel("Fitness linguistique"); ax2.set_ylabel("Score visuel")
            ax2.set_title("Décomposition de la fitness (linguistique vs visuelle)",
                          fontsize=11, fontweight="bold")
        else:
            self._empty_ax_msg(ax2)

        fig.tight_layout()
        return self._save(fig, "09_artefact_fitness") if save else fig

    # ------------------------------------------------------------------
    # 10. CHRONOLOGIE NARRATIVE — timeline multi-échelle des événements
    # ------------------------------------------------------------------

    def plot_narrative_timeline(self, save=True):
        """Frise combinant chronicle (événements structurels), myths (naissance de
        mythes) et random_events (événements aléatoires) sur un même axe temporel."""
        chr_ = self.df.get("chronicle", pd.DataFrame())
        myths = self.df.get("myths", pd.DataFrame())
        rnd = self.df.get("random_events", pd.DataFrame())

        fig, ax = plt.subplots(figsize=(12, 4.5))
        tracks = []
        if not chr_.empty:
            tracks.append(("Chronique", chr_["timestamp"], chr_["event_type"], "#38d1fb", 2))
        if not myths.empty:
            tracks.append(("Mythes", myths["created_at"], myths["title"], "#c5fb38", 1))
        if not rnd.empty:
            tracks.append(("Événements aléatoires", rnd["timestamp"], rnd["event_type"], "#ff5fa2", 0))

        if not tracks:
            self._empty_ax_msg(ax)
            return self._save(fig, "10_narrative_timeline") if save else fig

        for label, times, texts, color, y in tracks:
            ax.scatter(times, [y] * len(times), color=color, s=90, zorder=5, edgecolors="white", linewidths=0.5)
            for t, txt in zip(times, texts):
                ax.annotate(str(txt)[:28], (t, y), textcoords="offset points", xytext=(0, 10),
                            ha="center", fontsize=6.5, color=color, rotation=25)

        ax.set_yticks([y for *_, y in tracks])
        ax.set_yticklabels([t[0] for t in tracks])
        ax.set_xlabel("Temps")
        ax.set_ylim(-1, len(tracks))
        ax.set_title("Chronologie narrative — chronique, mythes, événements aléatoires",
                      fontsize=13, fontweight="bold")
        fig.tight_layout()
        return self._save(fig, "10_narrative_timeline") if save else fig

    # ------------------------------------------------------------------
    # 11. MATRICES DE CORRÉLATION — traits, souches, artefacts
    # ------------------------------------------------------------------

    def plot_correlation_matrix(self, df_name: str, cols: list[str], title: str, save=True):
        df = self.df.get(df_name, pd.DataFrame())
        fig, ax = plt.subplots(figsize=(8, 7))
        cols = [c for c in cols if c in df.columns]
        if df.empty or len(cols) < 2:
            self._empty_ax_msg(ax)
            return self._save(fig, f"11_corr_{df_name}") if save else fig

        corr = df[cols].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        sns.heatmap(corr, ax=ax, cmap="RdBu_r", vmin=-1, vmax=1, mask=mask,
                    annot=corr.shape[0] <= 15, fmt=".2f", annot_kws={"size": 7},
                    linewidths=0.4, linecolor=BG, cbar_kws={"label": "Corrélation (Pearson)"})
        ax.set_title(title, fontsize=12, fontweight="bold")
        plt.setp(ax.get_xticklabels(), rotation=40, ha="right", fontsize=8)
        plt.setp(ax.get_yticklabels(), fontsize=8)
        fig.tight_layout()
        return self._save(fig, f"11_corr_{df_name}") if save else fig

    # ------------------------------------------------------------------
    # 12. PCA + CLUSTERING DES AGENTS — typologie comportementale
    # ------------------------------------------------------------------

    def plot_agent_pca_clusters(self, save=True, k_range=range(2, 7)):
        ag = self.df.get("agents_state", pd.DataFrame())
        fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
        if ag.empty:
            for ax in axes:
                self._empty_ax_msg(ax)
            return self._save(fig, "12_agent_pca_clusters") if save else fig

        last = ag.sort_values("timestamp").groupby("agent_id").last().reset_index()
        cols = self._feature_cols_for_clustering(last)
        if len(cols) < 2:
            for ax in axes:
                self._empty_ax_msg(ax, "Traits constants sur ce run — variance nulle (PCA impossible)")
            return self._save(fig, "12_agent_pca_clusters") if save else fig
        X = last[cols].fillna(last[cols].mean())
        Xs = StandardScaler().fit_transform(X)

        pca = PCA(n_components=2, random_state=0)
        coords = pca.fit_transform(Xs)

        best_k, best_score, best_labels = 2, -1, None
        for k in k_range:
            if len(last) <= k:
                continue
            km = KMeans(n_clusters=k, random_state=0, n_init=10).fit(Xs)
            if len(set(km.labels_)) < 2:
                continue
            score = silhouette_score(Xs, km.labels_)
            if score > best_score:
                best_k, best_score, best_labels = k, score, km.labels_

        ax = axes[0]
        if best_labels is not None:
            sc = ax.scatter(coords[:, 0], coords[:, 1], c=best_labels, cmap="tab10",
                            s=45, edgecolors="white", linewidths=0.3)
            ax.set_title(f"PCA des traits d'agents — {best_k} clusters (silhouette={best_score:.2f})",
                        fontsize=11, fontweight="bold")
        else:
            ax.scatter(coords[:, 0], coords[:, 1], color=ACCENT[0], s=45)
            ax.set_title("PCA des traits d'agents", fontsize=11, fontweight="bold")
        var = pca.explained_variance_ratio_
        ax.set_xlabel(f"PC1 ({var[0]*100:.1f}% var.)")
        ax.set_ylabel(f"PC2 ({var[1]*100:.1f}% var.)")

        ax2 = axes[1]
        loadings = pca.components_.T
        for i, col in enumerate(cols):
            ax2.arrow(0, 0, loadings[i, 0], loadings[i, 1], color=ACCENT[i % len(ACCENT)],
                      head_width=0.02, alpha=0.85)
            ax2.annotate(col, (loadings[i, 0], loadings[i, 1]), fontsize=7, color=FG)
        ax2.axhline(0, color=GRID, linewidth=0.5); ax2.axvline(0, color=GRID, linewidth=0.5)
        ax2.set_title("Cercle des corrélations (loadings PCA)", fontsize=11, fontweight="bold")
        ax2.set_xlim(-1, 1); ax2.set_ylim(-1, 1)
        ax2.set_aspect("equal")

        fig.tight_layout()

        self._last_pca_clusters = None
        if best_labels is not None:
            out = last[["agent_id"]].copy()
            out["cluster"] = best_labels
            out["pc1"], out["pc2"] = coords[:, 0], coords[:, 1]
            self._last_pca_clusters = out

        return self._save(fig, "12_agent_pca_clusters") if save else fig

    # ------------------------------------------------------------------
    # 13. DENDROGRAMME DES SOUCHES — similarité symbolique hiérarchique
    # ------------------------------------------------------------------

    def plot_strain_dendrogram(self, save=True):
        ss = self.df.get("strains_state", pd.DataFrame())
        fig, ax = plt.subplots(figsize=(9, 5))
        feat_cols = [c for c in ["contagion_power", "dogma_intensity", "symbolic_complexity",
                                   "symbolic_symmetry", "artefact_fitness", "latency_period"]
                     if c in ss.columns]
        if ss.empty or len(feat_cols) < 2:
            self._empty_ax_msg(ax)
            return self._save(fig, "13_strain_dendrogram") if save else fig

        agg = ss.groupby("strain_id")[feat_cols].mean()
        if len(agg) < 2:
            self._empty_ax_msg(ax, "Une seule souche — pas de hiérarchie à construire")
            return self._save(fig, "13_strain_dendrogram") if save else fig

        Xs = StandardScaler().fit_transform(agg)
        Z = linkage(Xs, method="ward")
        dendrogram(Z, labels=agg.index.tolist(), ax=ax, color_threshold=0.7 * max(Z[:, 2]),
                   above_threshold_color="#4a4f5e")
        ax.set_title("Dendrogramme des souches — similarité symbolique (Ward)",
                     fontsize=12, fontweight="bold")
        ax.set_ylabel("Distance")
        fig.tight_layout()
        return self._save(fig, "13_strain_dendrogram") if save else fig

    # ==================================================================
    # DATA MINING — tables exploitables pour la phase suivante
    # ==================================================================

    def compute_correlation_matrices(self):
        """Exporte les matrices de corrélation (Pearson) des traits d'agents,
        des souches et des artefacts en CSV, prêtes pour analyse hardcore."""
        out = {}
        specs = {
            "agents_traits": ("agents_state", self.trait_cols + self.symbolic_cols),
            "strains": ("strains_state", ["contagion_power", "dogma_intensity", "latency_period",
                                            "carrier_count", "total_adherents", "prevalence",
                                            "mutation_count", "symbolic_complexity", "symbolic_symmetry",
                                            "artefact_fitness"]),
            "artefacts": ("artefacts", ["aesthetic_score", "complexity", "symmetry",
                                          "glitch_factor", "entropy_level"]),
            "daily_metrics": ("daily_metrics", [c for c in self.df.get("daily_metrics", pd.DataFrame()).columns
                                                  if c != "timestamp"]),
        }
        for key, (dfname, cols) in specs.items():
            df = self.df.get(dfname, pd.DataFrame())
            cols = [c for c in cols if c in df.columns]
            if df.empty or len(cols) < 2:
                continue
            corr = df[cols].corr()
            path = self.mining_dir / f"correlation_{key}.csv"
            corr.to_csv(path)
            out[key] = str(path)
        return out

    def compute_strain_similarity(self):
        """Matrice de similarité cosinus entre souches, basée sur leur signature
        symbolique (contagion, dogme, complexité, symétrie, fitness) — utile pour
        détecter les 'espèces mémétiques' convergentes malgré une généalogie distincte."""
        ss = self.df.get("strains_state", pd.DataFrame())
        feat_cols = [c for c in ["contagion_power", "dogma_intensity", "symbolic_complexity",
                                   "symbolic_symmetry", "artefact_fitness", "latency_period"]
                     if c in ss.columns]
        if ss.empty or len(feat_cols) < 2:
            return None
        agg = ss.groupby("strain_id")[feat_cols].mean()
        Xs = StandardScaler().fit_transform(agg)
        sim = cosine_similarity(Xs)
        sim_df = pd.DataFrame(sim, index=agg.index, columns=agg.index)
        path = self.mining_dir / "strain_similarity_matrix.csv"
        sim_df.to_csv(path)
        return str(path)

    def compute_agent_clustering(self, k_range=range(2, 7)):
        """KMeans + PCA sur les traits psycho-cognitifs des agents : assignation
        de cluster, coordonnées PCA, score de silhouette — exporté par agent."""
        ag = self.df.get("agents_state", pd.DataFrame())
        if ag.empty:
            return None
        last = ag.sort_values("timestamp").groupby("agent_id").last().reset_index()
        cols = self._feature_cols_for_clustering(last)
        if len(cols) < 2:
            return None
        X = last[cols].fillna(last[cols].mean())
        Xs = StandardScaler().fit_transform(X)

        pca = PCA(n_components=min(3, len(cols)), random_state=0)
        coords = pca.fit_transform(Xs)

        best_k, best_score, best_labels = None, -1, None
        for k in k_range:
            if len(last) <= k:
                continue
            km = KMeans(n_clusters=k, random_state=0, n_init=10).fit(Xs)
            if len(set(km.labels_)) < 2:
                continue
            score = silhouette_score(Xs, km.labels_)
            if score > best_score:
                best_k, best_score, best_labels = k, score, km.labels_

        out = last[["agent_id", "status_code", "faction_id", "strain_id"]].copy()
        for i in range(coords.shape[1]):
            out[f"pc{i+1}"] = coords[:, i]
        out["cluster"] = best_labels if best_labels is not None else -1
        path = self.mining_dir / "agent_clusters.csv"
        out.to_csv(path, index=False)

        meta = {
            "best_k": int(best_k) if best_k else None,
            "silhouette_score": float(best_score) if best_score > -1 else None,
            "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
            "features_used": cols,
        }
        with open(self.mining_dir / "agent_clusters_meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        return str(path)

    def compute_network_metrics(self):
        """Centralités (degré, intermédiarité, eigenvector) sur le réseau
        d'interactions et sur le réseau d'alliances de factions."""
        results = {}
        it = self.df.get("interactions", pd.DataFrame())
        if not it.empty:
            G = nx.Graph()
            for _, row in it.iterrows():
                G.add_edge(int(row["agent_a"]), int(row["agent_b"]),
                          weight=row.get("intensity", 1.0))
            deg = dict(G.degree())
            btw = nx.betweenness_centrality(G, weight="weight")
            try:
                eig = nx.eigenvector_centrality(G, max_iter=500, weight="weight")
            except Exception:
                eig = {n: np.nan for n in G.nodes}
            df_net = pd.DataFrame({
                "agent_id": list(G.nodes),
                "degree": [deg[n] for n in G.nodes],
                "betweenness": [btw[n] for n in G.nodes],
                "eigenvector_centrality": [eig[n] for n in G.nodes],
            }).sort_values("betweenness", ascending=False)
            path = self.mining_dir / "network_metrics_agents.csv"
            df_net.to_csv(path, index=False)
            results["agents"] = str(path)

        fa = self.df.get("factions", pd.DataFrame())
        al = self.df.get("alliances", pd.DataFrame())
        if not fa.empty:
            Gf = nx.Graph()
            for _, row in fa.iterrows():
                Gf.add_node(row["faction_id"])
            if not al.empty:
                for _, row in al.iterrows():
                    Gf.add_edge(row["faction_id"], row["ally_id"])
            deg = dict(Gf.degree())
            df_f = pd.DataFrame({"faction_id": list(Gf.nodes), "degree": [deg[n] for n in Gf.nodes]})
            path = self.mining_dir / "network_metrics_factions.csv"
            df_f.to_csv(path, index=False)
            results["factions"] = str(path)
        return results

    def compute_meme_fitness_stats(self):
        """Statistiques de fitness mémétique par souche (proxy Fidélité/Fécondité/
        Longévité à la Blackmore) : pic de prévalence, temps au pic, vitesse de
        croissance initiale, décroissance, nombre de mutations émises."""
        ss = self.df.get("strains_state", pd.DataFrame())
        if ss.empty:
            return None
        rows = []
        for sid, g in ss.groupby("strain_id"):
            g = g.sort_values("timestamp")
            peak_idx = g["prevalence"].idxmax()
            peak_t = g.loc[peak_idx, "timestamp"]
            peak_val = g.loc[peak_idx, "prevalence"]
            emergence = g["emergence_time"].iloc[0]
            # vitesse de croissance initiale (pente sur les 5 premiers pas dispo)
            early = g.head(5)
            growth = (np.polyfit(early["timestamp"], early["prevalence"], 1)[0]
                      if len(early) >= 2 else np.nan)
            late = g.tail(5)
            decay = (np.polyfit(late["timestamp"], late["prevalence"], 1)[0]
                     if len(late) >= 2 else np.nan)
            rows.append({
                "strain_id": sid,
                "theme": g["mantra_theme"].iloc[0] if "mantra_theme" in g else None,
                "emergence_time": emergence,
                "peak_time": peak_t,
                "peak_prevalence": peak_val,
                "final_prevalence": g["prevalence"].iloc[-1],
                "mean_contagion_power": g["contagion_power"].mean(),
                "mean_dogma_intensity": g["dogma_intensity"].mean(),
                "growth_rate_early": growth,
                "decay_rate_late": decay,
                "mutation_count_max": g["mutation_count"].max(),
                "longevity_steps": g["timestamp"].max() - emergence,
            })
        out = pd.DataFrame(rows).sort_values("peak_prevalence", ascending=False)
        path = self.mining_dir / "meme_fitness_stats.csv"
        out.to_csv(path, index=False)
        return str(path)

    def compute_transmission_stats(self):
        """Probabilité empirique de transmission par tranche d'intensité/risque,
        et taux de transmission global — pour calibrer un futur modèle prédictif."""
        it = self.df.get("interactions", pd.DataFrame())
        if it.empty:
            return None
        it = it.copy()
        it["intensity_bin"] = pd.qcut(it["intensity"], q=min(5, it["intensity"].nunique()),
                                        duplicates="drop")
        summary = it.groupby("intensity_bin", observed=False).agg(
            n=("transmission_occurred", "size"),
            transmission_rate=("transmission_occurred", "mean"),
            mean_risk=("transmission_risk", "mean"),
        ).reset_index()
        path = self.mining_dir / "transmission_stats_by_intensity.csv"
        summary.to_csv(path, index=False)

        # corrélation risque déclaré vs transmission réalisée
        if it["transmission_risk"].nunique() > 1:
            r, p = stats.pointbiserialr(it["transmission_occurred"], it["transmission_risk"])
            with open(self.mining_dir / "transmission_risk_correlation.json", "w") as f:
                json.dump({"point_biserial_r": float(r), "p_value": float(p),
                           "global_transmission_rate": float(it["transmission_occurred"].mean())}, f, indent=2)
        return str(path)

    def compute_descriptive_stats(self):
        """Statistiques descriptives complètes (describe + skew/kurtosis) pour
        chaque table numérique — base pour le data mining ultérieur."""
        paths = {}
        for name, df in self.df.items():
            num = df.select_dtypes(include=[np.number])
            if num.empty:
                continue
            desc = num.describe().T
            desc["skew"] = num.skew()
            desc["kurtosis"] = num.kurtosis()
            path = self.mining_dir / f"describe_{name}.csv"
            desc.to_csv(path)
            paths[name] = str(path)
        return paths

    def export_master_summary(self):
        """JSON de synthèse — un point d'entrée unique pour la phase de data
        mining hardcore : compte les entités, pics épidémiques, souche dominante, etc."""
        dm = self.df.get("daily_metrics", pd.DataFrame())
        ag = self.df.get("agents_state", pd.DataFrame())
        ss = self.df.get("strains_state", pd.DataFrame())
        fa = self.df.get("factions", pd.DataFrame())
        myths = self.df.get("myths", pd.DataFrame())

        summary = {
            "n_timesteps": int(dm["timestamp"].nunique()) if not dm.empty else None,
            "n_agents": int(ag["agent_id"].nunique()) if not ag.empty else None,
            "n_strains": int(ss["strain_id"].nunique()) if not ss.empty else None,
            "n_factions": int(fa["faction_id"].nunique()) if not fa.empty else None,
            "n_myths": int(myths["myth_id"].nunique()) if not myths.empty else None,
            "peak_rt": float(dm["rt"].max()) if "rt" in dm.columns and not dm.empty else None,
            "peak_infected": int(dm["cult_I"].max()) if "cult_I" in dm.columns and not dm.empty else None,
            "peak_infected_time": int(dm.loc[dm["cult_I"].idxmax(), "timestamp"])
                if "cult_I" in dm.columns and not dm.empty else None,
            "final_disenchanted": int(dm["cult_R"].iloc[-1]) if "cult_R" in dm.columns and not dm.empty else None,
        }
        if not ss.empty:
            dominant = ss.groupby("strain_id")["total_adherents"].max().idxmax()
            summary["dominant_strain"] = dominant
        path = self.mining_dir / "master_summary.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        return summary

    # ==================================================================
    # DASHBOARD DE SYNTHÈSE — une planche, tout le run en un regard
    # ==================================================================

    def generate_dashboard(self, save=True):
        fig = plt.figure(figsize=(18, 11))
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.55, wspace=0.35)
        fig.suptitle("Corpus Vauvillensis — Tableau de bord épidémio-mémétique",
                     fontsize=16, fontweight="bold", color=ACCENT[0], y=0.98)

        dm = self.df.get("daily_metrics", pd.DataFrame())
        ag = self.df.get("agents_state", pd.DataFrame())
        ss = self.df.get("strains_state", pd.DataFrame())

        # (1) courbes épidémiques
        ax1 = fig.add_subplot(gs[0, :2])
        if not dm.empty:
            for c in [c for c in dm.columns if c.startswith("cult_")]:
                code = c.replace("cult_", "")
                ax1.plot(dm["timestamp"], dm[c], color=STATUS_COLORS.get(code, "#999"),
                        label=STATUS_LABELS.get(code, code), linewidth=1.8)
            ax1.legend(fontsize=6.5, ncol=3, loc="upper left")
            ax1.set_title("Compartiments culturels", fontsize=10, fontweight="bold")
        else:
            self._empty_ax_msg(ax1)

        # (2) KPIs texte
        ax2 = fig.add_subplot(gs[0, 2]); ax2.axis("off")
        summ = self.export_master_summary()
        kpi_text = "\n".join([f"{k.replace('_',' ').capitalize()}: {v}" for k, v in summ.items()])
        ax2.text(0.02, 0.98, "MÉTRIQUES CLÉS", fontsize=11, fontweight="bold",
                 color=ACCENT[0], va="top", transform=ax2.transAxes)
        ax2.text(0.02, 0.85, kpi_text, fontsize=8, va="top", family="monospace",
                 color=FG, transform=ax2.transAxes)

        # (3) status stream
        ax3 = fig.add_subplot(gs[1, 0])
        if not ag.empty:
            pivot = ag.groupby(["timestamp", "status_code"]).size().unstack(fill_value=0)
            codes = [c for c in ["S", "E", "I", "A", "R", "D"] if c in pivot.columns]
            ax3.stackplot(pivot.index, pivot[codes].T.values,
                         colors=[STATUS_COLORS[c] for c in codes], alpha=0.85)
            ax3.set_title("Flux des statuts", fontsize=10, fontweight="bold")
        else:
            self._empty_ax_msg(ax3)

        # (4) symbolic landscape mini
        ax4 = fig.add_subplot(gs[1, 1])
        sr = self.df.get("symbolic_resonance", pd.DataFrame())
        if not sr.empty:
            ax4.scatter(sr["position_x"], sr["position_y"], s=200 * sr["mass"],
                       c=range(len(sr)), cmap=_MEME_CMAP, edgecolors="white")
            for _, row in sr.iterrows():
                ax4.annotate(row["strain_id"], (row["position_x"], row["position_y"]), fontsize=6)
            ax4.set_title("Paysage symbolique", fontsize=10, fontweight="bold")
        else:
            self._empty_ax_msg(ax4)

        # (5) strain prevalence over time
        ax5 = fig.add_subplot(gs[1, 2])
        if not ss.empty:
            for sid, g in ss.groupby("strain_id"):
                ax5.plot(g["timestamp"], g["prevalence"], label=sid, linewidth=1.6)
            ax5.legend(fontsize=6.5)
            ax5.set_title("Prévalence par souche", fontsize=10, fontweight="bold")
        else:
            self._empty_ax_msg(ax5)

        # (6) agent trait correlation mini
        ax6 = fig.add_subplot(gs[2, 0])
        cols = self.trait_cols[:8]
        if not ag.empty and len(cols) >= 2:
            corr = ag[cols].corr()
            sns.heatmap(corr, ax=ax6, cmap="RdBu_r", vmin=-1, vmax=1, cbar=False,
                       xticklabels=False, yticklabels=[c[:10] for c in cols])
            ax6.set_title("Corrélation traits (extrait)", fontsize=10, fontweight="bold")
            plt.setp(ax6.get_yticklabels(), fontsize=6)
        else:
            self._empty_ax_msg(ax6)

        # (7) artefact aesthetic distribution
        ax7 = fig.add_subplot(gs[2, 1])
        art = self.df.get("artefacts", pd.DataFrame())
        if not art.empty and "aesthetic_score" in art.columns:
            ax7.hist(art["aesthetic_score"], bins=15, color=ACCENT[2], alpha=0.85, edgecolor=BG)
            ax7.set_title("Distribution fitness artefacts", fontsize=10, fontweight="bold")
        else:
            self._empty_ax_msg(ax7)

        # (8) network mini
        ax8 = fig.add_subplot(gs[2, 2])
        it = self.df.get("interactions", pd.DataFrame())
        if not it.empty:
            G = nx.Graph()
            for _, row in it.iterrows():
                G.add_edge(int(row["agent_a"]), int(row["agent_b"]))
            pos = nx.spring_layout(G, seed=1)
            nx.draw_networkx_edges(G, pos, ax=ax8, edge_color="#2c3040", width=0.6, alpha=0.6)
            nx.draw_networkx_nodes(G, pos, ax=ax8, node_size=25, node_color=ACCENT[4])
            ax8.set_title("Réseau social (aperçu)", fontsize=10, fontweight="bold")
            ax8.set_axis_off()
        else:
            self._empty_ax_msg(ax8)

        return self._save(fig, "00_dashboard_overview") if save else fig

    # ==================================================================
    # PIPELINE COMPLET
    # ==================================================================

    def run_full_pipeline(self, verbose=True):
        """Génère toutes les visualisations + tout le data mining en une passe,
        et produit un rapport markdown de synthèse."""
        if verbose:
            print("→ Génération des visualisations...")
        viz_fns = [
            self.generate_dashboard, self.plot_epidemic_curves, self.plot_strain_phylogeny,
            self.plot_faction_network, self.plot_interaction_network,
            lambda: self.plot_interaction_network(only_transmissions=True),
            self.plot_symbolic_landscape, self.plot_agent_trait_parallel, self.plot_status_stream,
            self.plot_episodic_memory_heatmap, self.plot_artefact_fitness_landscape,
            self.plot_narrative_timeline,
            lambda: self.plot_correlation_matrix("agents_state", self.trait_cols + self.symbolic_cols,
                                                   "Corrélation — traits psycho-cognitifs des agents"),
            lambda: self.plot_correlation_matrix("strains_state",
                    ["contagion_power", "dogma_intensity", "latency_period", "carrier_count",
                     "total_adherents", "prevalence", "mutation_count", "symbolic_complexity",
                     "symbolic_symmetry", "artefact_fitness"], "Corrélation — dynamique des souches"),
            lambda: self.plot_correlation_matrix("artefacts",
                    ["aesthetic_score", "complexity", "symmetry", "glitch_factor", "entropy_level"],
                    "Corrélation — structure des artefacts"),
            self.plot_agent_pca_clusters, self.plot_strain_dendrogram,
        ]
        generated = []
        for fn in viz_fns:
            try:
                generated.append(str(fn()))
            except Exception as e:
                warnings.warn(f"Échec visu {getattr(fn, '__name__', 'lambda')}: {e}")

        if verbose:
            print("→ Extraction data mining...")
        mining = {
            "correlations": self.compute_correlation_matrices(),
            "strain_similarity": self.compute_strain_similarity(),
            "agent_clusters": self.compute_agent_clustering(),
            "network_metrics": self.compute_network_metrics(),
            "meme_fitness_stats": self.compute_meme_fitness_stats(),
            "transmission_stats": self.compute_transmission_stats(),
            "descriptive_stats": self.compute_descriptive_stats(),
            "master_summary": self.export_master_summary(),
        }

        self._write_report(generated, mining)
        if verbose:
            print(f"→ Terminé. Figures : {self.fig_dir}\n  Data mining : {self.mining_dir}")
        return {"figures": generated, "mining": mining}

    def _write_report(self, generated, mining):
        lines = ["# Rapport de synthèse — exploration mémétique\n"]
        lines.append("## Métriques clés\n")
        for k, v in mining["master_summary"].items():
            lines.append(f"- **{k}** : {v}")
        lines.append("\n## Figures générées\n")
        for g in generated:
            lines.append(f"- `{Path(g).name}`")
        lines.append("\n## Tables de data mining (`data_mining/`)\n")
        for k, v in mining.items():
            if k == "master_summary":
                continue
            lines.append(f"- **{k}** : `{v}`")
        with open(self.output_dir / "REPORT.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "./memetic_output"
    mx = MemeticExplorer(data_dir=data_dir, output_dir=out_dir)
    mx.run_full_pipeline()
