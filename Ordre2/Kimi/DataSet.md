---

## 🏛️ Vue d'ensemble du système et des données

Le simulateur modélise la **propagation épidémiologique et l'évolution de mèmes/artefacts symboliques** au sein d'une population d'agents virtuels distribués par zones. Les données générées retracent l'état des agents, l'évolution génétique des mantras et glyphes (ADN symbolique), les métriques épidémiologiques quotidiennes, la dynamique des factions/alliances, la dérive sémantique et la gravité narrative (résonance symbolique).

---

## 📂 Description fichier par fichier

### 1. `agents_state.csv`

* **Contenu** : Cartographie complète de l'état individuel des agents à la fin de la simulation.
* **Colonnes principales** :
* `agent_id` : Identifiant unique de l'agent.
* `zone` : Zone géographique ou réseau d'appartenance.
* `cultural_status` : Statut épidémiologique (`S` = Réceptif, `E` = Exposé, `I` = Évangéliste, `A` = Porteur silencieux, `R` = Désenchanté, `D` = Inconscient/Ignorant).
* `guild` : Guilde d'appartenance (`Scribes`, `Hérauts`, `Anachorètes`, `Colporteurs`, `Iconoclastes`, `Mystiques`, `Fractaliens`, etc.).
* `current_strain` : Identifiant de la souche mématique actuellement véhiculée.
* `narrative_coherence` : Niveau de cohérence narrative interne de l'agent ($[0.0, 1.0]$).
* `meme_virulence` : Virulence perçue du mème porté.
* `receptivity` : Sensibilité ou perméabilité à l'infection mématique.
* `influence_score` : Score de leadership/capacité d'influence dans le réseau social.
* `faction_id` : Identifiant de la faction d'appartenance.
* `aesthetic_score` & `dominant_emotion` : Attributs issus de l'artefact symbolique propre à l'agent.
* `pos_x`, `pos_y` : Coordonnées spatiales dans l'espace mématique.



---

### 2. `strains_state.csv`

* **Contenu** : Registre généalogique et caractéristiques des souches mématiques apparues au cours de la simulation.
* **Colonnes principales** :
* `strain_id` : Identifiant unique de la souche (ex. `ST_0`, `ST_1`).
* `parent_id` : Souche parente (permet de reconstruire l'arbre phylogénétique des mèmes).
* `generation` : Rang générationnel de la mutation.
* `contagion_power` : Pouvoir de contagion de base.
* `dogma_intensity` : Rigidité/dogmatisme de la souche.
* `mantra_content` : Texte du mantra généré/évolué associé à la souche.
* `theme` & `glyph_symbol` : Thème esthétique (`protection`, `voyage`, `rituel`, `silence`, `émergence`, `déclin`) et forme du glyphe associé.
* `aesthetic_score` : Score d'évaluation esthétique globales de l'artefact de la souche.



---

### 3. `daily_metrics.csv`

* **Contenu** : Séries temporelles agrégées jour par jour sur l'état global du système.
* **Colonnes principales** :
* `timestamp` / `day` : Numéro du cycle ou jour de simulation.
* `count_S`, `count_E`, `count_I`, `count_A`, `count_R`, `count_D` : Décompte de la population par statut SEIARD.
* `active_strains_count` : Nombre de souches en circulation.
* `dominant_strain` : Souche occupant la plus grande part de marché cognitif.
* `global_narrative_coherence` : Moyenne de cohérence narrative de la population.
* `mean_aesthetic_score` : Score esthétique moyen des mèmes actifs.



---

### 4. `interactions.csv`

* **Contenu** : Log détaillé des rencontres inter-agents ayant servi de vecteur potentiel de contagion.
* **Colonnes principales** :
* `timestamp` : Cycle où l'interaction s'est produite.
* `agent_a`, `agent_b` : Identifiants des deux agents impliqués.
* `intensity` : Force ou durée du lien d'échange.
* `transmission_risk` : Probabilité théorique de transmission lors de l'échange.
* `transmission_occurred` : Booléen (`True`/`False`) indiquant si une infection mématique a eu lieu.



---

### 5. `narrative_events.csv` & `random_events.csv`

* **Contenu** : Événements marquants et micro-crises ayant influencé la dynamique culturelle.
* **Typologie d'événements** :
* **Narrative Events** : Schismes (`schism`), prophéties (`prophecy`), censures (`censorship`), réformations (`reformation`), pèlerinages (`pilgrimage`), création de reliques (`relic_creation`), éclipses narratives.
* **Random Events** : Incidents stochastiques affectant des zones géographiques ou des sous-groupes d'agents.



---

### 6. `artefacts.csv`

* **Contenu** : Catalogue des artefacts symboliques générés (combinaison d'un glyphe paléolithique, d'une palette chromatique et d'un mantra).
* **Colonnes principales** :
* `fingerprint` : Empreinte ADN hachée de l'artefact (`genetic_fingerprint`).
* `mantra_text` : Mantra transcrit.
* `theme`, `color`, `glyph_symbol` : Propriétés visuelles.
* `complexity`, `symmetry`, `glitch_factor`, `entropy_level` : Paramètres génératifs du visuel.
* `aesthetic_score`, `linguistic_fitness`, `visual_text_coherence` : Mesures détaillées des composants d'évaluation.



---

### 7. `factions.csv` & `alliances.csv`

* **Contenu** : Structure politique et groupements sociaux émergents de la contagion mématique.
* **Caractéristiques** :
* **Factions** : Identifiant, nom, fondateur (`founder_id`), souche fondatrice (`founding_strain`), liste des membres et rituels associés.
* **Alliances** : Paires de factions partageant une affinité idéologique ou mématique et pactes de non-agression/synergie.



---

### 8. `semantic_drift.csv`

* **Contenu** : Suivi des dérives sémantiques et linguistiques au fur et à mesure des transmissions et mutations de mèmes.
* **Informations** : Mesure de la distance ou distorsion du sens entre la souche originelle (racine) et ses déclinaisons mutées au fil des cycles.

---

### 9. `symbolic_resonance.csv`

* **Contenu** : Matrice ou métriques d'attraction/gravité narrative générée par la résonance esthétique des artefacts.
* **Information** : Force d'attraction exercée par les centres mématiques majeurs sur les agents selon leur proximité sociale, affinité de couleurs, glyphes et vecteurs émotionnels (`peur`, `joie`, `mystere`, `colere`, `extase`, `silence`).

---

### 10. `chronicle.csv`, `myths.csv` & `episodic_memory.csv`

* **Contenu** : Archivage textuel et mémoriel de la simulation.
* `myths.csv` : Mythes fondateurs créés à partir des mantras dominants et versets sacrés.
* `episodic_memory.csv` : Historique individuel de mémoire à court/moyen terme propre à chaque agent.
* `chronicle.csv` : Résumé historiographique global assemblant les événements majeurs de la simulation sous forme de récit.
