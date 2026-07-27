
╔═══════════════════════════════════════════════════════════════════╗
║          📊 DONNÉES CSV — ARCHEOEPIDEMIC CHIMERA v2.1            ║
║                     Pour traitement KNIME                        ║
╚═══════════════════════════════════════════════════════════════════╝

📁 FICHIERS DISPONIBLES
───────────────────────────────────────────────────────────────────

1. agents_state.csv
   └─ État longitudinal des agents (1 ligne par agent × pas de temps)
   └─ Colonnes: timestamp, agent_id, zone, guild, status, strain_id, ...
   └─ Analyse: trajectoires individuelles, survie, conversion

2. strains_state.csv
   └─ État longitudinal des souches (1 ligne par souche × pas de temps)
   └─ Colonnes: timestamp, strain_id, parent_id, generation, carrier_count, ...
   └─ Analyse: évolution des souches, dominance, mutations

3. daily_metrics.csv
   └─ Métriques agrégées par pas de temps
   └─ Colonnes: timestamp, rt, cult_S, cult_E, cult_I, cult_A, cult_R, cult_D, ...
   └─ Analyse: dynamique globale, Rt, proportions

4. narrative_events.csv
   └─ Événements narratifs individuels (expositions, désenchantements, ...)
   └─ Analyse: séries temporelles, propagation

5. random_events.csv
   └─ Événements aléatoires (schismes, prophéties, censures, ...)
   └─ Analyse: impact des événements sur la dynamique

6. interactions.csv
   └─ Toutes les tentatives de transmission
   └─ Colonnes: timestamp, agent_a, agent_b, intensity, transmission_risk, occurred
   └─ Analyse: réseau de propagation, efficacité

7. relics.csv
   └─ Reliques préservées
   └─ Analyse: conservation des mantras, rôle des Anachorètes

8. myths.csv
   └─ Mythes fondateurs générés
   └─ Analyse: agrégation narrative, convergence culturelle

9. chronicle.csv
   └─ Chronologie des événements majeurs
   └─ Analyse: séquence narrative, rythme

10. semantic_drift.csv
    └─ Dérive sémantique (parent → enfant)
    └─ Analyse: arbre des mutations, évolution linguistique

🔗 TYPES DE JOINTURES POSSIBLES
───────────────────────────────────────────────────────────────────

• agents_state + narrative_events (agent_id)
• agents_state + interactions (agent_a, agent_b)
• strains_state + agents_state (strain_id)
• strains_state + semantic_drift (parent_strain, child_strain)
• daily_metrics + random_events (timestamp)

📊 MÉTRIQUES CLÉS POUR KNIME
───────────────────────────────────────────────────────────────────

• Rt → taux de reproduction effectif
• cult_I → nombre d'évangélistes
• cult_A → porteurs silencieux
• prevalence → proportion d'adhérents par souche
• narrative_coherence → cohérence narrative
• influence_score → influence accumulée

🔄 WORKFLOW KNIME RECOMMANDÉ
───────────────────────────────────────────────────────────────────

1. CSV Reader → agents_state.csv
2. GroupBy → aggrégation par timestamp
3. Line Plot → évolution des statuts
4. CSV Reader → interactions.csv
5. Network Creator → graphe de transmission
6. Network Analyzer → centralité, composantes

✨ BONNE ANALYSE ! 
