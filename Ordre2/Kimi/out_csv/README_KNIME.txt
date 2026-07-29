
╔═══════════════════════════════════════════════════════════════════╗
║          📊 DONNÉES CSV — ARCHEOSYMBOLIC CHRONICLE v1.0         ║
║                     Pour traitement KNIME                        ║
╚═══════════════════════════════════════════════════════════════════╝

📁 FICHIERS DISPONIBLES
───────────────────────────────────────────────────────────────────
1. agents_state.csv       → État longitudinal des agents (avec champs symboliques)
2. strains_state.csv      → État longitudinal des souches (avec champs symboliques)
3. daily_metrics.csv      → Métriques agrégées par pas de temps
4. narrative_events.csv   → Événements narratifs individuels
5. random_events.csv      → Événements aléatoires
6. interactions.csv       → Tentatives de transmission
7. relics.csv             → Reliques préservées
8. myths.csv              → Mythes fondateurs
9. chronicle.csv          → Chronologie des événements majeurs
10. semantic_drift.csv    → Dérive sémantique
11. factions.csv          → Factions émergentes
12. alliances.csv         → Alliances entre factions
13. episodic_memory.csv   → Mémoire épisodique des agents
14. symbolic_resonance.csv→ Centres de résonance esthétique
15. artefacts.csv         → Artefacts symboliques des agents

🔗 TYPES DE JOINTURES
───────────────────────────────────────────────────────────────────
• agents_state + artefacts (agent_id)
• agents_state + factions (faction_id)
• strains_state + artefacts (strain_id via artefact_mantra)
• factions + alliances (faction_id, ally_id)

📊 MÉTRIQUES CLÉS SYMBOLIQUES
───────────────────────────────────────────────────────────────────
• artefact_fitness → score esthétique de l'artefact
• symbolic_color → couleur dominante de l'artefact
• symbolic_glyph → glyphe paléolithique
• symbolic_complexity / symbolic_symmetry → attributs visuels
• dominant_emotion → émotion dominante de l'artefact
