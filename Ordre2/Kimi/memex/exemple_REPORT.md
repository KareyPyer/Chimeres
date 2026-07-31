# Rapport de synthèse — exploration mémétique

## Métriques clés

- **n_timesteps** : 100
- **n_agents** : 80
- **n_strains** : 3
- **n_factions** : 2
- **n_myths** : 2
- **peak_rt** : 2.0
- **peak_infected** : 18
- **peak_infected_time** : 64
- **final_disenchanted** : 63
- **dominant_strain** : M-001

## Figures générées

- `00_dashboard_overview.png`
- `01_epidemic_curves.png`
- `02_strain_phylogeny.png`
- `03_faction_network.png`
- `04_interaction_network.png`
- `04b_transmission_network.png`
- `05_symbolic_landscape.png`
- `06_agent_trait_parallel.png`
- `07_status_stream.png`
- `08_episodic_memory_heatmap.png`
- `09_artefact_fitness.png`
- `10_narrative_timeline.png`
- `11_corr_agents_state.png`
- `11_corr_strains_state.png`
- `11_corr_artefacts.png`
- `12_agent_pca_clusters.png`
- `13_strain_dendrogram.png`

## Tables de data mining (`data_mining/`)

- **correlations** : `{'agents_traits': 'outputs/data_mining/correlation_agents_traits.csv', 'strains': 'outputs/data_mining/correlation_strains.csv', 'artefacts': 'outputs/data_mining/correlation_artefacts.csv', 'daily_metrics': 'outputs/data_mining/correlation_daily_metrics.csv'}`
- **strain_similarity** : `outputs/data_mining/strain_similarity_matrix.csv`
- **agent_clusters** : `outputs/data_mining/agent_clusters.csv`
- **network_metrics** : `{'agents': 'outputs/data_mining/network_metrics_agents.csv', 'factions': 'outputs/data_mining/network_metrics_factions.csv'}`
- **meme_fitness_stats** : `outputs/data_mining/meme_fitness_stats.csv`
- **transmission_stats** : `outputs/data_mining/transmission_stats_by_intensity.csv`
- **descriptive_stats** : `{'agents_state': 'outputs/data_mining/describe_agents_state.csv', 'artefacts': 'outputs/data_mining/describe_artefacts.csv', 'symbolic_resonance': 'outputs/data_mining/describe_symbolic_resonance.csv', 'episodic_memory': 'outputs/data_mining/describe_episodic_memory.csv', 'alliances': 'outputs/data_mining/describe_alliances.csv', 'factions': 'outputs/data_mining/describe_factions.csv', 'chronicle': 'outputs/data_mining/describe_chronicle.csv', 'myths': 'outputs/data_mining/describe_myths.csv', 'interactions': 'outputs/data_mining/describe_interactions.csv', 'random_events': 'outputs/data_mining/describe_random_events.csv', 'narrative_events': 'outputs/data_mining/describe_narrative_events.csv', 'daily_metrics': 'outputs/data_mining/describe_daily_metrics.csv', 'strains_state': 'outputs/data_mining/describe_strains_state.csv'}`