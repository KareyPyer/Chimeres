# 🧬 Chimeres — Hybridation de codes par LLM

> *Expériences de croisement de scripts Python générés/enrichis par IA : deux "organismes-code" parents sont fusionnés pour produire des "chimères" — des programmes hybrides qui héritent, recombinent et mutent les mécanismes de leurs parents.*

Ce dépôt est un laboratoire proto : chaque script est un simulateur multi-agents complet (souvent 1000+ lignes, zéro dépendance obligatoire au-delà de la stdlib), écrit en français, avec une esthétique CLI très marquée (bannières ASCII/RetroWave, affichages "Feng-Shui"). L'idée directrice est double :

1. **ArcheoEpidemic** — un modèle épidémiologique (façon SEIR) appliqué à la propagation de récits/mèmes dans une population d'agents culturels.
2. **SymbolicDNA_Forge** — un moteur évolutif qui génère des "artefacts symboliques" (glyphe paléolithique + mantra + couleur + vecteur émotionnel) via algorithme génétique.

Les chimères d'**Ordre 2** (`Kimi.py`, `QweN.py`) fusionnent les deux paradigmes : la contagion narrative ne transmet plus un simple texte, mais un artefact symbolique complet qui évolue et dont l'attrait esthétique pilote la contagion.

---

## Sommaire

- [Structure du dépôt](#structure-du-dépôt)
- [Concepts transverses](#concepts-transverses)
- [1. ArcheoEpidemic_Chimera4b1.py](#1-archeoepidemic_chimera4b1py)
- [2. SymbolicDNA_Forge_Chimera3a.py](#2-symbolicdna_forge_chimera3apy)
- [3. FengShui_JSON_Editor.py](#3-fengshui_json_editorpy)
- [4. Ordre2/Kimi/Kimi.py — SYMBOLIC_FORGE_FUSION](#4-ordre2kimikimipy--symbolic_forge_fusion)
- [5. Ordre2/Qwen/QweN.py — AESTHETIC_RESONANCE](#5-ordre2qwenqwenpy--aesthetic_resonance)
- [Comparatif des chimères](#comparatif-des-chimères)
- [Dépendances](#dépendances)
- [Installation rapide](#installation-rapide)
- [Recettes d'invocation](#recettes-dinvocation)
- [Formats d'export](#formats-dexport)
- [Limitations connues](#limitations-connues)
- [Pistes d'évolution (v3.0)](#pistes-dévolution-v30)

---

## Structure du dépôt

```
Chimeres/
├── ArcheoEpidemic/
│   ├── ArcheoEpidemic_Chimera4b1.py   # Simulateur épidémiologique narratif (v2.2 DATA_ORACLE_EXTENDED)
│   ├── launch2.sh                     # Exemple d'invocation à grande échelle (1000 agents, 500 pas)
│   ├── genotheque_json_lab.html       # Visualisation / labo pour les données JSON externalisées
│   ├── data/                          # Pack de données externe (lexique, thèmes, génomes, événements…)
│   ├── data_knime/                    # Exports CSV multi-tables prêts pour KNIME
│   ├── logs/                          # Logs d'exécution
│   └── output/                        # Exports JSON natifs + PNG réseau
│
├── SymbolicDNA/
│   ├── SymbolicDNA_Forge_Chimera3a.py # Moteur évolutif d'artefacts symboliques (v2.0)
│   ├── FengShui_JSON_Editor.py        # Éditeur JSON interactif pour les fichiers de données
│   ├── data/                          # Lexique onirique, gabarits de thèmes, palettes, pools de symboles
│   └── symbolic_forge_output/         # Sorties (PNG, JSON, prompts de diffusion)
│
└── Ordre2/                            # Chimères de "second ordre" (fusion des deux parents ci-dessus)
    ├── Kimi/
    │   ├── Kimi.py                    # ARCHEOSYMBOLIC CHRONICLE — SYMBOLIC_FORGE_FUSION (v1.0)
    │   ├── lauch_kimi.sh
    │   └── out_csv/
    └── Qwen/
        ├── QweN.py                    # ARCHEOSYMBOLIC CHRONICLE — AESTHETIC_RESONANCE (v1.0)
        ├── Tuto-QweN.txt              # "Grimoire d'invocation" — recettes de simulation commentées
        ├── lauch_qwen.sh
        └── output/
```

Aucun des scripts n'expose de package installable (`pip install -e .`) : ce sont des scripts autonomes en `__main__`, à exécuter directement avec `python3 <script>.py [options]` depuis leur propre dossier (les chemins de sortie par défaut sont relatifs au répertoire courant).

---

## Concepts transverses

Les cinq scripts partagent un socle conceptuel commun, avec des variantes d'un fichier à l'autre :

| Concept | Rôle |
|---|---|
| **`CulturalGenome`** (`@dataclass`) | Traits hérités d'un agent : `narrative_fluency`, `charisma`, `skepticism`, `dogma_risk`, `expressiveness`, `influence_potential`, `mobility`, `altruism`, `social_compliance`, `curiosity`, `memory_depth`... Chaque trait module un phénotype effectif via `CulturalPhenotype`. |
| **`CulturalStatus`** (`Enum`, notation type SEIR) | `RECEPTIVE (S)` → `EXPOSED (E)` → `EVANGELIST (I)` / `SILENT_CARRIER (A)` → `DISENCHANTED (R)` → `OBLIVIOUS (D)`. Modélise la trajectoire d'un individu face à un mème : exposition, latence, propagation active ou silencieuse, rejet conscient, oubli. |
| **`MemeStrain` / `Mantra`** | Une "souche" narrative = un texte (mantra) généré par algorithme génétique (`SoufiMantraGA`), doté d'un pouvoir de contagion (`compute_virulence`) qui dépend de propriétés structurelles (rimes, allitérations), émotionnelles et symboliques du texte — pas de sa "vérité". |
| **`SymbolicDNA` / `SymbolicArtefact`** | ADN à deux brins (visuel : glyphe + couleur + complexité/symétrie/glitch/entropie ; linguistique : mots-clés, gabarit, tag onirique, vecteur émotionnel). Transcrit en artefact (image matplotlib + texte + score de fitness) par `SymbolicTranscriptor`. |
| **`SymbolicEvolutionEngine`** | Algorithme génétique générique : population → mutation (`mutate_visual`, `mutate_linguistic`, `mutate_emotional`, `mutate_organism`) → évaluation (`evaluate_organism`/`evaluate_artefact`) → sélection élitiste sur générations, avec probabilité de "chaos mutate". |
| **`NarrativeGravity` / `AestheticResonance` / `SymbolicResonance`** | Système d'attraction pondérée qui détermine, à chaque pas, quelle souche "capture" un agent réceptif — combinant affinité esthétique, affinité émotionnelle, recouvrement sémantique et proximité sociale. |
| **`FactionSystem`** | Émergence endogène de factions quand une souche dépasse un seuil de porteurs (par défaut 10 % de la population croyante), avec génération de rituels et gestion d'alliances/rivalités entre factions. |
| **`EpisodicMemory`** | Journal d'événements marquants par agent (infection, conversion, désenchantement…) avec un score d'impact cumulé. |
| **Génération de mythes / reliques / éclipses narratives** | Mécanismes narratifs de plus haut niveau : `_maybe_generate_myth()` crée des "méta-mèmes" fondateurs ; `_trigger_narrative_eclipse()` efface une souche minoritaire de la mémoire collective ; les `Relic` sont des objets porteurs de mémoire culturelle gardés par un agent. |
| **Exports** | CSV multi-tables (souvent pensés pour KNIME), export Cypher/Neo4J (nœuds `Agent`, `Strain`, `Zone`, `Relic`, `Myth`, `Event` + relations), JSON natif (sans dépendance), PNG (réseau de transmission via `networkx`+`matplotlib`), et — pour les branches liées à SymbolicDNA — prompts texte pour moteurs de diffusion d'image (Grok, Gemini, DALL·E, Midjourney, Stable Diffusion). |
| **Affichage terminal** | Deux styles d'habillage CLI coexistent : `RetroWaveDisplay` (bannières néon ASCII, barre de statut, "coin du prophète", art ASCII animé) et `FengShuiDisplay` (messages apaisants, arbres de paramètres, "mantras" encadrés) — parfois combinés dans une même chimère. |

Toutes les dépendances lourdes (`numpy`, `matplotlib`, `networkx`) sont **optionnelles** : chaque script les importe dans un bloc `try/except` et bascule sur des fallbacks internes (`HAS_NUMPY`, `HAS_MPL`, `HAS_NX`) ou désactive silencieusement les fonctionnalités concernées (rendu d'image, export réseau, calcul de plus court chemin).

---

## 1. `ArcheoEpidemic_Chimera4b1.py`

**Rôle** : simulateur d'« épidémies narratives » — comment un récit/rituel se propage, mute, fait émerger des factions, génère des mythes et finit par s'éteindre ou se figer en dogme dans une population d'agents culturels.

### Architecture interne

- **`JSONDataManager`** — charge un pack de données externe (`--data-dir`) contenant `oniric_lexicon.json`, `themes.json`, `cultural_genomes.json`, `event_types.json` ; sinon retombe sur des données internes (6 thèmes : `protection`, `voyage`, `rituel`, `silence`, `émergence`, `déclin`). Peut aussi **générer** ce pack (`--init-data <dir>`).
- **`Neo4JExporter`** — génère un script Cypher complet : contraintes d'unicité (`Agent.id`, `Strain.strain_id`, `Relic.relic_id`, `Myth.myth_id`, `Zone.name`, `Event.event_id`), création des nœuds `Zone`, `Agent` (avec tous les traits de génome et de phénotype), `Strain`, `Relic`, `Myth`, `Event`, puis des relations de transmission/appartenance. Un README Neo4J est généré automatiquement (`_generate_neo4j_readme`).
- **`NarrativeGravity`** — calcule une "masse" par souche (proportionnelle au nombre de porteurs actifs) et une attraction sur chaque agent réceptif, combinant recouvrement sémantique (`_compute_semantic_overlap`) et proximité sociale dans le réseau de transmission (`_compute_social_proximity`).
- **`FactionSystem`** — `faction_emergence_threshold()` = `max(3, 10 % des porteurs)`. Au-delà, `_create_faction()` nomme la faction d'après les premiers mots du mantra dominant, lui génère des rituels (`_generate_rituals`), et `update_alliances()` maintient des relations inter-factions dans le temps.
- **`EpisodicMemory`** — mémoire d'agent : `add_event`, `get_recent_events(n)`, `get_impact_summary()` (agrégation de l'impact par type d'événement).
- **`SoufiMantraGA`** — mini algorithme génétique qui remplit des gabarits de texte (`fill_template`) à partir du lexique onirique, calcule une fitness (`calculate_fitness`) et fait évoluer une petite population de mantras sur quelques générations (`evolve`).
- **`CulturalGenome`** — dataclass de traits + `mutate()` (mutation gaussienne bornée par trait, taux réglable) + `get_fingerprint()` (hash d'identité génomique).
- **`CulturalEpidemicSimulation`** — cœur de la simulation :
  - `_generate_zones`, `_init_population`, `_build_social_network` (graphe de contacts, `networkx` si disponible sinon `_MiniDiGraph` interne),
  - `_expose_agent` / `transmit_meme` / `_run_interaction_round` — mécanique de contact et transmission,
  - `mutate_meme()` — mutation textuelle (`mutate_mantra_text`) probabiliste des souches actives,
  - `_apply_narrative_gravity`, `_apply_narrative_cycle` (saisons culturelles), `_trigger_narrative_eclipse`, `_trigger_cultural_resonance`, `_maybe_trigger_random_event`, `_maybe_generate_myth`,
  - `_update_factions`, `_calculate_rt()` (nombre de reproduction effectif façon épidémiologie classique),
  - `step()` orchestre un pas de temps complet et retourne un dict de métriques ; `run(steps)` est un générateur qui `yield` un `step()` par itération.
- **`CSVExporterV22`** — 14 tables : `agents_state`, `strains_state`, `daily_metrics`, `narrative_events`, `random_events`, `interactions`, `relics`, `myths`, `chronicle`, `semantic_drift`, `factions`, `alliances`, `episodic_memory`, `narrative_gravity`, plus un `README_KNIME.txt` généré automatiquement.
- **`RetroWaveDisplay`** — habillage terminal néon : bannière, barre de statut, flux d'événements, "coin du prophète" (citations/prédictions), art ASCII, rendu animé pas-à-pas, rapport final encadré.
- **`mythological_report(sim)`** — génère un rapport narratif de fin de simulation (bilan des souches, factions, mythes, reliques).

### CLI (`build_arg_parser`)

```
Général          --seed --steps --verbose --no-retro --log-file --log-level
Données externes --data-dir --init-data
Export           --export-csv --export-json --export-neo4j --export-network
Population       --pop-total --nb-zones --initial-believers
Souche racine    --root-theme {choix internes ou du pack JSON} --r0-base --latency-period
Dynamiques       --disenchant-rate --oblivion-rate --mutation-prob --dogma-rate
Événements       --random-event-prob --myth-generation-period --max-myths
```

⚠️ **Limitation documentée dans `data/README_PACK.md`** : la liste de `--root-theme` est construite **avant** le chargement de `--data-dir` (le parser argparse est bâti avec les données internes par défaut) — en CLI, seuls les 6 thèmes d'origine sont proposés même si un pack JSON en définit davantage. Les thèmes additionnels restent pleinement utilisables :
- comme `preferred_theme` aléatoire tiré dans `CulturalGenome`,
- en appelant directement `run_cultural_epidemic_simulation(params={"root_theme": "convergence", ...})` en Python plutôt que via le CLI.

### Exemple d'invocation (`launch2.sh`)

```bash
python ArcheoEpidemic_Chimera4b1.py \
  --seed 42 --steps 500 --pop-total 1000 --nb-zones 8 \
  --root-theme rituel --r0-base 3.0 --mutation-prob 0.05 \
  --random-event-prob 0.08 \
  --log-file logs/chimera_debug.log --log-level DEBUG \
  --export-json ./output --export-network output/network.png \
  --export-csv ./data_knime --export-neo4j ./data_neo4j \
  --verbose
```

### Pack de données (`data/README_PACK.md`)

Le pack "Corpus Vauvillensis / Normandie fractale 2075" fourni dans `ArcheoEpidemic/data/` illustre l'extensibilité via JSON : lexique onirique enrichi (tags `<delta>`, `<hague>`, `<tissage>`...), 12 thèmes (6 d'origine + 6 inédits : `convergence`, `biocodéologie`, `résistance_analogique`, `tissage`, `delta_modulation`, `sans-marques`), espèces/guildes narratives (`Tisserand`, `Delta-Codeur`, `Glyphomancien`, `Tisserands_de_Brume`, `Sans-Marques`), types d'événements enrichis, et 5 scénarios CLI prêts à l'emploi.

---

## 2. `SymbolicDNA_Forge_Chimera3a.py`

**Rôle** : « la Forge de l'ADN Symbolique » — génère, fait évoluer et exporte des artefacts symboliques (glyphe paléolithique animé façon Von Petzinger + mantra + couleur + émotion), avec un générateur de prompts pour IA de diffusion d'image en sortie.

### Architecture interne

- **`FengShuiDisplay`** — habillage terminal "harmonieux" : en-têtes, sections, arbres de paramètres, mantras encadrés, poèmes de conclusion, barre de progression.
- **`VonPetzingerSymbols`** — bibliothèque de **26 glyphes paléolithiques** (d'après la taxonomie de Genevieve von Petzinger) rendus en `matplotlib` : `line`, `circle`, `dot`, `open_angle`, `triangle`, `quadrangle`, `spiral`, `zigzag`, `cross`, `crosshatch`, `hand`, `tectiform`, `penniform`, `claviform`, `aviform`, `scalariform`, `finger_fluting`, `cupule`, `wavy_line`, `oval`, `semi_circle`, `rectangle`, `asterisk`, `serpentiform`, `pectiform`, `dots_series`.
- **`SymbolicDNA`** (`@dataclass`) — brin d'ADN symbolique : `glyph_symbol`, `color` (hex), `scale`, `complexity`, `symmetry`, `glitch_factor`, `entropy_level` (versant visuel) + mots-clés, gabarit de mantra, tag onirique, vecteur émotionnel (versant linguistique). `dominant_emotion()` retourne l'émotion la plus intense.
- **`SymbolicOrganismGenome`** — un organisme peut porter **plusieurs brins** d'ADN (`strands: List[SymbolicDNA]`), avec des traits organismiques : `creativity`, `self_awareness`, `aesthetic_sense`, `chaos_affinity`, `narrative_coherence`, `mutation_susceptibility`, `species`, `breed`.
- **`SymbolicTranscriptor`** — `transcribe_visual()` (rend le glyphe en image), `transcribe_text()` (génère le mantra à partir du gabarit + lexique), `transcribe_artefact()` (assemble les deux en `SymbolicArtefact`) ; `_glitch_color()` introduit une distorsion chromatique proportionnelle au `glitch_factor`.
- **Analyse de texte** — `detect_rhyme`, `detect_alliteration`, `emotion_intensity`, `extract_oniric_tag` : mesurent des propriétés structurelles et affectives du mantra généré, indépendamment de son sens.
- **`evaluate_artefact()`** — fonction de fitness combinant :
  - `linguistic_fitness = (theme_match*2 + style_score + oniric_bonus + emo_score*0.3) / 6.0`
  - `visual_text_coherence` (accord entre le glyphe/couleur choisis et le champ sémantique du texte)
  - `visual_score` (qualités intrinsèques du rendu graphique)
  → pondération finale approx. 40 % linguistique / 35 % cohérence visuelle-texte / 25 % score visuel (documentée dans l'historique de fusion Ordre 2).
- **`SymbolicEvolutionEngine`** — moteur génétique générique :
  `initialize_population` → `_spawn_organism`/`_spawn_dna` → `mutate_visual` (dont `_evolve_color`, dérive HSL bornée), `mutate_linguistic`, `mutate_emotional`, `mutate_organism` (avec probabilité de **chaos mutate** = mutation à forte intensité) → `evaluate_organism` → `evolve(generations, chaos_probability)` avec sélection élitiste et journalisation par génération.
- **`build_prompt_for_diffusion()`** — traduit un artefact + son ADN en prompt texte optimisé par plateforme cible :
  ```python
  style_map = {
      "grok": "photorealistic, cinematic, 8k, detailed, mystical, symbolic, dramatic lighting",
      "midjourney": "fantasy art, intricate, mystical, glowing, ethereal, detailed, majestic",
      # + gemini, dalle, stable
  }
  ```
- **`render_phylogeny_board()`** — planche visuelle récapitulative de l'arbre phylogénétique des organismes générés au fil des générations.

### CLI (`main`)

```
Généraux        --theme --population --generations --chaos --out --seed --strands --mutation-rate
ADN visuel      --glyph --color --scale --complexity --symmetry --glitch --entropy
ADN linguistique --keywords --template --tag --emotion (JSON)
Organisme       --creativity --self-awareness --aesthetic-sense --chaos-affinity
                --narrative-coherence --mutation-susceptibility --species --breed
Prompt diffusion --diffusion-prompt --diffusion-out --diffusion-target {grok,gemini,dalle,midjourney,stable} --no-visual
```

Deux modes d'exécution :
1. **Évolution générative** (par défaut) : population initiale → `evolve()` sur N générations → export du meilleur organisme.
2. **ADN personnalisé** (dès qu'un paramètre `--glyph/--color/--keywords/...` est fourni) : construction directe d'un `SymbolicDNA` via `build_dna_from_args()`, puis évaluation unique (pas d'évolution).

### Exemples (README intégré au script)

```bash
# Évolution normale
python SymbolicDNA_Forge_Chimera.py --theme voyage --generations 10

# ADN personnalisé + prompt de diffusion
python SymbolicDNA_Forge_Chimera.py --glyph spiral --color "#ff00aa" --complexity 0.8 \
  --glitch 0.5 --keywords "étoile,plasma,chant" \
  --emotion '{"mystere":0.7,"extase":0.3}' --diffusion-prompt

# Prompt seul, sans rendu matplotlib
python SymbolicDNA_Forge_Chimera.py --glyph cross --theme protection --diffusion-prompt --no-visual
```

---

## 3. `FengShui_JSON_Editor.py`

**Rôle** : éditeur JSON interactif en ligne de commande pour maintenir les packs de données (`oniric_lexicon`, `theme_templates`, `theme_symbol_pools`, `theme_palettes`, `oniric_tag_meanings`) consommés par les autres chimères — présenté comme « une expérience de manipulation de données méditative ».

### Architecture interne

- **`FengShuiDisplay`** — variante étendue de l'affichage harmonieux (palette "pierres précieuses").
- **`JSONAnalysis`** — structure de résultat d'analyse (profondeur, nombre d'éléments, clés manquantes, incohérences détectées, recommandations).
- **`FengShuiJSONEditor`** — moteur non-interactif :
  - `REQUIRED_STRUCTURES` — schéma attendu par type de fichier (clés obligatoires),
  - `discover_files()` — scanne `./data/` et le répertoire courant pour lister les JSON disponibles,
  - `detect_file_type()` — reconnaît automatiquement le type d'un fichier chargé selon ses clés,
  - `load()` — chargement avec gestion d'erreurs (`JSONDecodeError` compris) et rapport de taille/structure,
  - `analyze()` — calcule profondeur max, nombre total d'éléments, clés requises manquantes, et formule des `issues`/`recommendations`.
  - Sauvegardes automatiques dans `.backups/` avant modification (best practice de non-destruction).
- **`FengShuiJSONEditorUI`** — boucle interactive (menu terminal) qui orchestre découverte → chargement → analyse → édition → sauvegarde.

### Usage

```bash
python FengShui_JSON_Editor.py
# Lance le menu interactif ; découvre automatiquement les fichiers JSON
# dans ./data/ et le répertoire courant, propose chargement/analyse/édition/sauvegarde.
```

---

## 4. `Ordre2/Kimi/Kimi.py` — SYMBOLIC_FORGE_FUSION

**Rôle** : première chimère de second ordre. Fusionne intégralement `ArcheoEpidemic_Chimera4b1.py` (épidémiologie narrative) et `SymbolicDNA_Forge_Chimera3a.py` (forge génétique) : chaque **agent** et chaque **souche** porte désormais un `SymbolicArtefact` complet, et un moteur évolutif tourne *à l'intérieur* même des mutations de mème.

### Ce qui change par rapport aux parents

- **`CulturalAgent.receive_mantra()`** ne se contente plus de recevoir un texte : il fait **muter son propre artefact symbolique** en héritant de celui de la souche via une évolution rapide (`SymbolicEvolutionEngine.quick_mutate`) :
  ```python
  def receive_mantra(self, strain: MemeStrain):
      self.current_strain = strain
      self.personal_mantra = strain.mantra
      self.meme_virulence = MemeStrain.compute_virulence(...)
      if strain.symbolic_artefact is not None:
          engine = SymbolicEvolutionEngine(theme=strain.symbolic_artefact.theme)
          new_artefact, new_dna = engine.quick_mutate(strain.symbolic_artefact.symbolic_dna)
          self.symbolic_artefact = new_artefact
          self.symbolic_dna = new_dna
  ```
  → l'infection mémétique devient une **transformation esthétique de l'hôte**, pas une simple copie d'information.
- **`SymbolicResonance`** — remplace/étend `NarrativeGravity` avec une pondération explicite à 4 facteurs :
  ```python
  resonance = (
      aesthetic_affinity * 0.35 +   # couleur (similarité HSL) + glyphe + complexité + fitness
      emotional_affinity * 0.25 +   # distance euclidienne inverse sur le vecteur émotionnel
      semantic_overlap * 0.25 +     # recouvrement lexical Jaccard-like mantra agent / souche
      social_proximity * 0.15       # plus court chemin réseau (networkx) ou similarité de guilde
  )
  ```
  puis modulée par la masse du centre de résonance (nombre de porteurs actifs) et la cohérence narrative de l'agent.
- **`FactionSystem`** hérité mais désormais alimenté par les couleurs/mantras des artefacts symboliques (nom et couleur d'une faction dérivés du `symbolic_artefact` de la souche dominante).
- **Exports enrichis** : `CSVExporter`, `Neo4JExporter`, mais aussi `--export-collage` (planche PNG collant les artefacts visuels de la simulation) et `--diffusion-prompt` (génération d'un prompt d'image à partir du meilleur artefact rencontré).

### CLI

Reprend l'essentiel du CLI d'`ArcheoEpidemic` (général, données, population, souche racine, dynamiques, événements) et ajoute :

```
Forge symbolique  --symbolic-evolution / --no-symbolic-evolution --symbolic-generations
Export étendu     --export-collage --diffusion-prompt --diffusion-target {grok,gemini,dalle,midjourney,stable}
```

### Exemple (`lauch_kimi.sh`)

```bash
python Kimi.py --steps 60 --export-csv ./out_csv --export-collage ./collage.png --diffusion-prompt ./prompt.txt
```

---

## 5. `Ordre2/Qwen/QweN.py` — AESTHETIC_RESONANCE

**Rôle** : seconde chimère de second ordre, née de la **même fusion** de parents que Kimi, mais avec une philosophie opposée : là où Kimi est encyclopédique et exhaustif, QweN est volontairement court, dense et élégant (~1000 lignes contre ~3800 pour Kimi) — un outil de prototypage rapide plutôt qu'un laboratoire complet.

### Ce qui la distingue de Kimi

- **`GLYPH_GUILD_MAP`** — taxonomie fixe glyphe → guilde culturelle :
  ```python
  GLYPH_GUILD_MAP = {
      'circle': 'Mystiques', 'spiral': 'Fractaliens', 'cross': 'Hérauts', 'hand': 'Scribes',
      'asterisk': 'Colporteurs', 'wavy_line': 'Néantistes', 'dots_series': 'Anachorètes',
      'serpentiform': 'Syntagmatiques', 'tectiform': 'Iconoclastes', 'claviform': 'Hérauts',
      'penniform': 'Scribes', 'crosshatch': 'Fractaliens', 'zigzag': 'Syntagmatiques',
      'triangle': 'Iconoclastes', 'line': 'Néantistes', 'open_angle': 'Colporteurs',
      'semi_circle': 'Mystiques', 'oval': 'Anachorètes', 'dot': 'Néantistes'
  }
  ```
  Chaque agent a une `guild` **recalculée à chaque `receive_mantra()`** en fonction du glyphe de son artefact courant — modélisant une conversion identitaire immédiate à l'adoption d'un nouveau mème (contrairement à Kimi, où les factions émergent de manière statistique via seuils de population).
- **`AestheticResonance`** (au lieu de `SymbolicResonance`) — 4 facteurs différemment calculés et pondérés :
  ```python
  # 1. Affinité chromatique (distance RGB, pas HSL)
  color_dist = sqrt((r1-r2)^2 + (g1-g2)^2 + (b1-b2)^2) / 441.67   # 441.67 ≈ sqrt(3 * 255^2)
  color_affinity = 1.0 - color_dist
  # 2. Affinité de glyphe (1.0 si identique, 0.2 sinon)
  # 3. Résonance émotionnelle par SIMILARITÉ COSINUS (et non distance euclidienne comme Kimi)
  emotion_affinity = dot(vec1, vec2) / (||vec1|| * ||vec2||)
  # 4. Affinité esthétique = moyenne des scores de fitness des deux artefacts
  affinity = color_affinity*0.3 + glyph_affinity*0.3 + emotion_affinity*0.2 + fitness_affinity*0.2
  ```
  La similarité cosinus mesure l'*alignement* des profils émotionnels plutôt que leur distance absolue — un choix plus proche de la façon dont deux individus peuvent partager une "direction" émotionnelle sans partager la même intensité.
- **Exports** plus sobres : CSV + Neo4J + génération de prompt de diffusion (`generate_diffusion_prompt`), sans collage d'images ni export réseau matplotlib dédié.

### CLI (`main`)

```
Général    --seed --steps --pop-total --nb-zones --root-theme --r0-base --mutation-prob ...
Forge      --symbolic-generations --symbolic-pop
Export     --export-csv --export-neo4j --diffusion-prompt --diffusion-target {grok,gemini,dalle,midjourney,stable}
```

### Exemple (`lauch_qwen.sh`)

```bash
python QweN.py \
    --seed 8888 --steps 50 --pop-total 150 --root-theme rituel --r0-base 2.4 \
    --mutation-prob 0.04 --symbolic-generations 4 --symbolic-pop 8 \
    --export-csv ./output/festin_csv --export-neo4j ./output/festin_neo4j \
    --diffusion-prompt --diffusion-target grok
```

### `Tuto-QweN.txt` — le « Grimoire d'invocation »

Un fichier de recettes commentées livré avec QweN, illustrant plusieurs profils de simulation :

| Invocation | Effet |
|---|---|
| **L'Éveil doux** (`--steps 25 --pop-total 80 --root-theme rituel`) | Découverte rapide, propagation calme dans une petite communauté |
| **L'Explosion créative** (`--mutation-prob 0.08 --root-theme émergence`) | Forte radiation esthétique : de nombreuses souches divergentes naissent |
| **Le Pèlerinage silencieux** (`--root-theme silence --r0-base 1.8`) | Épidémie lente et méditative, glyphes `circle`/`wavy_line`/`dots_series` en teintes bleutées |
| **La Guerre des guildes** (`--root-theme protection --r0-base 3.0 --initial-believers 5`) | Émergence de factions rivales (`Hérauts`, `Mystiques`, `Iconoclastes`) |
| **Le Voyage transcontinental** (`--root-theme voyage --nb-zones 6`) | Diffusion large à travers toutes les zones |

---

## Comparatif des chimères

| Aspect | ArcheoEpidemic (parent) | SymbolicDNA_Forge (parent) | **Kimi** (Ordre 2) | **QweN** (Ordre 2) |
|---|---|---|---|---|
| Lignes de code | ~3480 | ~1670 | ~3800 | ~1030 |
| Unité de contagion | Texte (mantra) | — (génération, pas de contagion) | Artefact symbolique complet | Artefact symbolique complet |
| Structure sociale | Factions émergentes (seuil %) | — | Factions émergentes + artefact | Guildes recalculées par glyphe |
| Moteur évolutif | — | Complet, autonome | Intégré aux mutations de mème | Évolution rapide ciblée |
| Similarité émotionnelle | — | — | Distance euclidienne inverse | Similarité cosinus |
| Export média | CSV, JSON, Neo4J, PNG réseau | PNG, JSON, prompt diffusion | CSV, Neo4J, JSON, collage PNG, prompt | CSV, Neo4J, prompt |
| Philosophie | Épidémiologie narrative | Prototypage esthétique génératif | Encyclopédique, exhaustif | Élégant, minimaliste |
| Usage recommandé | Simulation de mouvements sociaux | Génération d'assets visuels/textuels | Laboratoire de recherche complet | Prototypage rapide d'hypothèses |

---

## Dépendances

Aucune dépendance n'est strictement obligatoire : chaque script dégrade proprement ses fonctionnalités si une bibliothèque manque.

| Bibliothèque | Utilisée pour | Comportement si absente |
|---|---|---|
| `numpy` | Calculs vectoriels, graine aléatoire reproductible | Fallback interne (`HAS_NUMPY = False`) |
| `matplotlib` | Rendu des glyphes, réseau de transmission, planches de phylogénie/collage | Export d'images désactivé, warning loggé |
| `networkx` | Graphe de contacts, plus court chemin (proximité sociale) | Fallback `_MiniDiGraph` (graphe orienté minimal fait maison) |

Stdlib utilisée par ailleurs : `random`, `math`, `json`, `string`, `hashlib`, `logging`, `argparse`, `csv`, `colorsys`, `dataclasses`, `enum`, `collections`, `pathlib`, `datetime`.

### Installation rapide

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy matplotlib networkx
```

Sans installation, tous les scripts restent exécutables en mode dégradé (pas de rendu graphique, graphe social simplifié).

---

## Recettes d'invocation

```bash
# Simulation épidémiologique narrative de base
cd ArcheoEpidemic
python3 ArcheoEpidemic_Chimera4b1.py --seed 2075 --steps 60 --pop-total 180 --root-theme rituel

# Avec pack de données externe + tous les exports
python3 ArcheoEpidemic_Chimera4b1.py --data-dir data --steps 100 --pop-total 200 \
  --root-theme émergence --export-csv out_csv --export-neo4j out_neo4j --export-json output

# Forge symbolique : évolution générative
cd ../SymbolicDNA
python3 SymbolicDNA_Forge_Chimera3a.py --theme voyage --generations 10

# Forge symbolique : ADN personnalisé + prompt pour Midjourney
python3 SymbolicDNA_Forge_Chimera3a.py --glyph spiral --color "#ff00aa" --complexity 0.8 \
  --diffusion-prompt --diffusion-target midjourney

# Chimère Kimi (encyclopédique)
cd ../Ordre2/Kimi
python3 Kimi.py --steps 60 --export-csv out_csv --export-collage collage.png --diffusion-prompt prompt.txt

# Chimère QweN (élégante)
cd ../Qwen
python3 QweN.py --seed 8888 --steps 50 --pop-total 150 --root-theme rituel \
  --symbolic-generations 4 --diffusion-prompt --diffusion-target grok
```

---

## Formats d'export

- **CSV multi-tables** (`--export-csv <dir>`) — pensé pour être rechargé dans **KNIME** : un `README_KNIME.txt`/`README_PACK.md` est généré automatiquement à côté des tables (`agents_state`, `strains_state`, `daily_metrics`, `narrative_events`, `factions`, `alliances`, `episodic_memory`, `narrative_gravity`, etc.).
- **Neo4J / Cypher** (`--export-neo4j <dir>`) — script `.cypher` avec contraintes d'unicité puis création des nœuds (`Zone`, `Agent`, `Strain`, `Relic`, `Myth`, `Event`) et de leurs relations ; un README explicatif est généré à côté.
- **JSON natif** (`--export-json <dir>`) — sans dépendance externe, utile pour rejouer une simulation ou l'inspecter avec `genotheque_json_lab.html`.
- **PNG** — réseau de transmission (`--export-network`, nécessite `matplotlib`+`networkx`), collage d'artefacts symboliques (`--export-collage`, Kimi uniquement), planche de phylogénie (`SymbolicDNA_Forge`).
- **Prompt de diffusion** (`--diffusion-prompt`) — fichier texte prêt à coller dans un outil de génération d'image, avec un style adapté à la cible (`grok`, `gemini`, `dalle`, `midjourney`, `stable`).

---

## Limitations connues

- **`--root-theme` et packs JSON externes** (`ArcheoEpidemic`, hérité par les chimères d'Ordre 2) : la liste de choix du CLI est figée sur les données internes au moment de la construction du parser, *avant* le chargement de `--data-dir`. Les thèmes additionnels d'un pack externe restent utilisables via l'API Python directe (`run_cultural_epidemic_simulation(params={...})`) mais pas via l'argument `--root-theme` en ligne de commande — un patch simple consiste à déplacer l'appel à `get_themes_list()` après le parsing de `--data-dir`, ou à retirer la contrainte `choices=`.
- **Agence des agents** : dans les cinq scripts, les agents sont des vecteurs passifs — ils sont exposés, résonnent, mutent et transmettent selon des probabilités et affinités, mais ne "choisissent" jamais de résister consciemment à un mème séduisant mais superficiel (voir pistes v3.0 ci-dessous).
- **Pondérations non calibrées empiriquement** : les coefficients de `SymbolicResonance`/`AestheticResonance` (0.35/0.25/0.25/0.15 chez Kimi, 0.3/0.3/0.2/0.2 chez QweN) sont des choix de conception, pas des valeurs issues de données réelles.
- **Scripts non paquetés** : pas de `setup.py`/`pyproject.toml`, pas de tests automatisés identifiés dans le dépôt ; chaque script est à lancer depuis son propre dossier pour que les chemins de sortie par défaut (`./data`, `./output`, etc.) soient cohérents.

---

## Pistes d'évolution (v3.0)

Idées de prolongement pour qui souhaite continuer l'hybridation :

- **Longévité mémorielle** — ajouter un paramètre de "durabilité" dans `CulturalGenome`/`MemeStrain` pour distinguer les mèmes éphémères des mèmes qui persistent sur le temps long.
- **Co-évolution hôte-mème** — une fonction `update_cognitive_bias()` qui ajuste les traits de l'agent en fonction de son historique d'exposition (plasticité cognitive), plutôt qu'un génome figé.
- **Recombinaison de mèmes** — au-delà de la dérive lexicale (`mutate_mantra_text`), permettre un croisement entre deux mantras/artefacts porteurs différents (façon mashup).
- **Schisme de factions** — permettre à une `Faction` de se scinder en deux sous-factions quand la divergence sémantique interne dépasse un seuil.
- **Scepticisme esthétique dynamique** (`aesthetic_skepticism`) — moduler l'attraction esthétique effective (`effective_resonance = resonance * (1 - aesthetic_skepticism * 0.5)`) pour modéliser des agents qui résistent à un artefact séduisant mais sémantiquement creux.
- **Module de conscience réflexive** — un `ConsciousnessModule` optionnel qui applique un filtre critique sur la résonance en fonction de la profondeur sémantique perçue d'un mème, pour introduire un minimum d'agence/résistance consciente dans la simulation.

---

*Dépôt à visée exploratoire : ces scripts sont des outils de simulation et de prototypage esthétique/narratif, pas des systèmes de production. Voir le code source de chaque fichier pour le détail exact des implémentations — ce README résume l'architecture observée dans `ArcheoEpidemic_Chimera4b1.py`, `SymbolicDNA_Forge_Chimera3a.py`, `FengShui_JSON_Editor.py`, `Kimi.py` et `QweN.py`.*
