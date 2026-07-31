# Memetic Explorer — Corpus Vauvillensis / LFS

Outil de DataViz + Data Mining pour les sorties du simulateur épidémio-mémétique
(agents, souches, factions, artefacts, mythes, événements narratifs).

## Installation

Dépendances (toutes locales, aucun appel réseau) :

```bash
pip install pandas numpy matplotlib seaborn networkx scikit-learn scipy --break-system-packages
```

`networkx` tentera d'utiliser `graphviz` pour la phylogénie des souches (arbre
propre) ; s'il n'est pas installé, un layout de repli par génération est utilisé
automatiquement — aucune action requise.

## Usage

### En ligne de commande — pipeline complet

```bash
python3 memetic_explorer.py /chemin/vers/les/csv ./sortie
```

Génère :
- `sortie/figures/` — 17 visualisations PNG (voir liste ci-dessous)
- `sortie/data_mining/` — matrices de corrélation, similarité, clustering, stats
- `sortie/REPORT.md` — rapport de synthèse

### En notebook Jupyter — exploration à la carte

```python
from memetic_explorer import MemeticExplorer

mx = MemeticExplorer(data_dir="/chemin/vers/les/csv", output_dir="./sortie")

mx.plot_epidemic_curves()        # courbes SEIAR-D
mx.plot_strain_phylogeny()       # arbre de mutation des souches
mx.plot_symbolic_landscape()     # carte de résonance mémétique
mx.plot_agent_pca_clusters()     # typologie comportementale des agents
mx.generate_dashboard()          # planche de synthèse
```

Chaque `plot_*` renvoie le chemin du PNG sauvegardé (ou la `Figure` matplotlib
si `save=False`, pratique pour itérer dans un notebook sans spammer le disque).

## Catalogue des visualisations

| # | Méthode | Ce qu'elle montre |
|---|---------|---|
| 00 | `generate_dashboard` | Planche de synthèse — tout le run en un regard |
| 01 | `plot_epidemic_curves` | Compartiments culturels S/E/I/A/R/D + Rt effectif |
| 02 | `plot_strain_phylogeny` | Arbre de mutation des souches (généalogie mémétique) |
| 03 | `plot_faction_network` | Graphe d'alliances entre factions |
| 04 | `plot_interaction_network` | Réseau social complet (+ variante transmissions réalisées) |
| 05 | `plot_symbolic_landscape` | Carte spatiale de résonance des souches (masse, rayon d'influence) |
| 06 | `plot_agent_trait_parallel` | Coordonnées parallèles des profils psycho-cognitifs |
| 07 | `plot_status_stream` | Flux empilé des statuts culturels dans le temps |
| 08 | `plot_episodic_memory_heatmap` | Intensité des souvenirs collectifs (type × période) |
| 09 | `plot_artefact_fitness_landscape` | Fitness esthétique des artefacts (linguistique vs visuelle) |
| 10 | `plot_narrative_timeline` | Frise chronique / mythes / événements aléatoires |
| 11 | `plot_correlation_matrix` | Matrices de corrélation (traits, souches, artefacts) |
| 12 | `plot_agent_pca_clusters` | PCA + KMeans — typologie comportementale des agents |
| 13 | `plot_strain_dendrogram` | Hiérarchie de similarité symbolique entre souches |

## Catalogue du data mining (`data_mining/`)

- **`correlation_*.csv`** — matrices de Pearson (traits d'agents, souches, artefacts, métriques journalières)
- **`strain_similarity_matrix.csv`** — similarité cosinus entre souches (signature symbolique) : détecte les "espèces mémétiques" convergentes malgré une généalogie distincte
- **`agent_clusters.csv` + `_meta.json`** — assignation de cluster (KMeans, k optimal par silhouette) + coordonnées PCA par agent
- **`network_metrics_agents.csv` / `_factions.csv`** — centralités (degré, intermédiarité, eigenvector) : qui sont les super-diffuseurs ?
- **`meme_fitness_stats.csv`** — par souche : pic de prévalence, vitesse de croissance initiale, décroissance, longévité (proxy Fidélité/Fécondité/Longévité à la Blackmore)
- **`transmission_stats_by_intensity.csv` + `transmission_risk_correlation.json`** — taux de transmission empirique par tranche d'intensité, corrélation risque déclaré / transmission réalisée
- **`describe_*.csv`** — statistiques descriptives complètes (moyenne, écart-type, skew, kurtosis) pour chaque table numérique
- **`master_summary.json`** — point d'entrée unique : comptages, pics épidémiques, souche dominante

## Notes de robustesse

- Le module tolère les fichiers vides/absents (ex : un run court sans mythe) —
  chaque figure affiche alors un message plutôt que de planter.
- Les colonnes `fitness_breakdown` (artefacts) et `impact`/`affected_agents`
  (random_events) sont auto-parsées depuis leur représentation Python/JSON.
- Pour le PCA/clustering des agents, si les traits psycho-cognitifs sont figés
  à leur valeur par défaut sur un run donné (variance nulle — ça peut arriver
  selon la config du simulateur), le module bascule automatiquement sur les
  colonnes dynamiques (`narrative_coherence`, `meme_virulence`, `receptivity`,
  `influence_score`) et symboliques plutôt que de produire une PCA dégénérée.

## Prochaine étape suggérée

Les tables de `data_mining/` sont pensées comme point de départ pour une phase
d'analyse plus poussée : tests d'hypothèses sur les corrélations trait ↔
statut épidémique, modèles prédictifs de transmission (régression logistique
sur `transmission_stats_by_intensity.csv`), analyse de survie des souches
(Kaplan-Meier sur `longevity_steps`), ou détection de communautés sur le
réseau d'interactions (Louvain/Leiden) à partir de `network_metrics_agents.csv`.
