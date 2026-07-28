# Pack de données — Corpus Vauvillensis Edition

Pack JSON externe pour `ArcheoEpidemic_Chimera4a1.py` (v2.2 DATA_ORACLE_EXTENDED).
Vocabulaire, thèmes et factions ancrés dans le **Corpus Vauvillensis / Normandie
fractale 2075** : Modèle du Temps Tissé, coefficient Δ, Caen-Profonde, la Hague,
WORM-ᚦESSUS, Tisserands de Brume, Sans-Marques, Codex Stein, OMEGA-REFLECT.

## Fichiers

| Fichier | Contenu |
|---|---|
| `oniric_lexicon.json` | Vocabulaire onirique enrichi (adjectifs, noms, actions, symboles, tags `<delta>` `<hague>` `<tissage>`...) ancré dans les paysages normands/2075 |
| `themes.json` | Les 6 thèmes d'origine (protection, voyage, rituel, silence, émergence, déclin) **augmentés**, + 6 thèmes inédits : `convergence`, `biocodéologie`, `résistance_analogique`, `tissage`, `delta_modulation`, `sans-marques` |
| `cultural_genomes.json` | Espèces (Tisserand, Delta-Codeur, Glyphomancien...), guildes (dont `Tisserands_de_Brume`, `Sans-Marques`) avec `guild_lore` narratif, glyphes |
| `event_types.json` | Types d'événements enrichis (`convergence_pulse`, `delta_surge`, `hague_transmission`, `worm_awakening`, `tisserand_pact`) + poids narratif |
| `simulation_config.json` | 5 scénarios prêts à l'emploi avec presets de paramètres CLI (Caen-Profonde, Convergence 2077, Sans-Marques, Delta intense, Biocodéologie lente) |

## Usage

```bash
python3 ArcheoEpidemic_Chimera4a1.py --data-dir archeoepidemic_data \
  --steps 60 --pop-total 150 --nb-zones 6 --root-theme émergence \
  --mutation-prob 0.03 --myth-generation-period 15 --no-retro
```

Export complet (CSV + Neo4J) :

```bash
python3 ArcheoEpidemic_Chimera4a1.py --data-dir archeoepidemic_data \
  --steps 100 --pop-total 200 --export-csv out_csv --export-neo4j out_neo4j
```

## ⚠️ Limitation native du script (pas du pack)

`--root-theme` construit sa liste de choix **avant** le chargement de `--data-dir`
(le parser argparse est bâti avec les données internes par défaut). Résultat :
en CLI, `--root-theme` n'accepte que les 6 clés d'origine
(`protection`, `voyage`, `rituel`, `silence`, `émergence`, `déclin`) — même si
`themes.json` en définit davantage.

Les thèmes inédits (`convergence`, `biocodéologie`, `résistance_analogique`,
`tissage`, `delta_modulation`, `sans-marques`) restent pleinement actifs :
- comme `preferred_theme` aléatoire des agents (`CulturalGenome`)
- si tu passes `root_theme` directement en Python via `params={"root_theme": "convergence", ...}`
  plutôt que par le CLI

Pour débloquer ces thèmes en CLI, il suffit de déplacer l'appel à
`get_themes_list()` dans `build_arg_parser()` après le parsing de `--data-dir`
(ou de retirer la contrainte `choices=`) — je peux faire ce patch si tu veux.

## Exemple d'usage direct en Python

```python
from ArcheoEpidemic_Chimera4a1 import run_cultural_epidemic_simulation

params = {
    "seed": 2077, "pop_total": 300, "nb_zones": 9, "initial_believers": 5,
    "root_theme": "convergence", "r0_base": 3.2, "disenchant_rate": 0.02,
    "oblivion_rate": 0.002, "mutation_prob": 0.015, "dogma_rate": 0.008,
    "latency_period": 4.0, "random_event_prob": 0.02,
    "myth_generation_period": 25, "max_myths": 6,
}
sim = run_cultural_epidemic_simulation(
    params, steps=150, retro_display=False,
    data_dir="archeoepidemic_data", export_csv="out_csv",
)
```

Ceci correspond au scénario `convergence_2077` de `simulation_config.json`.
