#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║   🧬🌌 ARCHEOSYMBOLIC CHRONICLE — v1.0 "SYMBOLIC_FORGE_FUSION"              ║
║   Chimère née de la fusion profonde de :                                      ║
║     • ArcheoEpidemic_Chimera4b1.py  (Parent Épidémiologique)                 ║
║     • SymbolicDNA_Forge_Chimera3a.py (Parent Génératif)                      ║
║                                                                               ║
║   Vision : La contagion narrative se fait par Artefacts Symboliques           ║
║   (glyphes paléolithiques + mantras cyber-soufis) générés par évolution.     ║
║                                                                               ║
║   Ajouts v1.0 :                                                               ║
║     • Artefact Symbolique attaché à chaque Agent et Souche                   ║
║     • Moteur évolutionnaire intégré dans les mutations de mème               ║
║     • Résonance Esthétique (couleur, glyphe, émotion, fitness)               ║
║     • Export multimédia : CSV + Neo4J + JSON + Images + Prompts              ║
║     • Affichage hybride RetroWave × Feng-Shui                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import math
import json
import string
import hashlib
import logging
import argparse
import sys
import os
import time
import shutil
import csv
import colorsys
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
from collections import defaultdict, Counter
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# DÉPENDANCES OPTIONNELLES
# ═══════════════════════════════════════════════════════════════════════════════
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, Rectangle
    from matplotlib.animation import FuncAnimation
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION DES LOGS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logging(log_file: Optional[str] = None, log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("ArcheoSymbolicChronicle")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.handlers.clear()
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    return logger

logger = logging.getLogger("ArcheoSymbolicChronicle")

# ═══════════════════════════════════════════════════════════════════════════════
# DONNÉES FUSIONNÉES — Lexiques, Templates, Pools, Palettes
# ═══════════════════════════════════════════════════════════════════════════════

class FusionDataManager:
    """
    Gestionnaire de données unifié, fusion des lexiques des deux parents.
    """

    _INTERNAL_DATA = {
        "oniric_lexicon": {
            "Adjectif": [
                "fractal", "quantique", "cryptique", "spectral", "liminal",
                "onirique", "corrompu", "sacré", "glitché", "ancestral",
                "éthéré", "cybernétique", "holographique", "syndical", "apocryphe",
                "lumineux", "brisé", "noyé", "encodé", "hanté",
                "neural", "crypté", "désert", "lunaire", "vide", "statique", "transcendant",
                "pulsatile", "entropique", "synaptique", "abyssal", "iridescent",
                "fossile", "plasmique", "tétanisé", "cathartique",
                "oraculaire", "tachyons", "mnémonique", "nocturne", "sismique",
                "karmique", "omniscient", "cristallin", "obsidienne", "vorace", "aphasique",
                "zénithal", "nadirien", "chromatique", "apocalyptique", "subliminal", "hybride",
                "foudroyant", "métastable", "paradoxal", "lacrymal", "éolien", "ténébreux",
                "auroral", "cataclysmique", "nébuleux", "vibratoire", "schizophrène", "syncrétique",
                "thanatique", "protoplasmique", "chimérique", "réticulaire", "psychotronique",
                "xénomorphe", "tellurique", "noosphérique", "biomécanique", "archaïque",
                "post-mortem", "dématérialisé", "fissionné", "gnostique", "paranoïaque",
                "neuromancien", "chamanique", "dithyrambique", "alchimique", "nécrotique",
                "bioluminescent", "psychopompe", "tesseractique", "pan-dimensionnel", "solipsiste",
                "hermétique", "fragmenté", "anachronique", "démiurgique",
                "eschatologique", "médiumnique", "électrostatique", "protéiforme", "subatomique",
                "kaléidoscopique", "thaumaturge", "synchrétique", "pénitentiel", "vorticiel",
                "phréatique", "chtonian", "panoptique",
            ],
            "Nom": [
                "signal", "silence", "glyphe", "écho", "seuil", "récit",
                "mantra", "spectre", "réseau", "songe", "oracle", "vérité",
                "mémoire", "fracture", "résonance", "noyau", "brume", "empreinte",
                "rêve", "cœur", "code", "prophète", "flux", "données", "ombre",
                "mirage", "ghost", "souffle", "voix", "neurone", "pixel", "bit",
                "fantôme", "abîme", "poussière", "cendre", "plasma",
                "nœud", "temple", "labyrinthe", "spirale", "vortex", "membrane", "crypte",
                "souffrance", "extase", "glitch", "halo", "stase", "cortex", "faille", "synapse",
                "algorithme", "linceul", "aura", "photon", "quark", "schéma",
                "fissure", "cristal", "avatar", "chimère", "légion", "palimpseste",
                "satori", "grimoire", "protocole", "séraphin", "daemon", "icône", "relique",
                "firmware", "thanatos", "axiome", "sigil", "matrice", "eidolon",
                "kyste", "nexus", "tesseract", "stigmate", "catalyseur", "phylactère",
                "sarcophage", "incantation", "partition", "hiéroglyphe", "golem", "patch",
                "rune", "codec", "épiphanie", "parasite", "singularité", "interface", "schisme",
                "totem", "backdoor", "autel", "suture", "malware", "derviche", "kernel",
                "pentacle", "émissaire", "root", "psaume", "verset", "apocalypse", "mandala",
                "driver", "reliquaire", "firewall", "sacrifice", "archétype", "vestige",
            ],
            "Action": [
                "implose", "exalte", "désintègre", "fusionne", "résonne",
                "désagrège", "sature", "décode", "invoque", "sublime",
                "dévore", "réfracte", "cristallise", "diffuse", "condense",
                "synchronise", "amplifie", "hack", "insère", "mute",
                "convoque", "infecte", "vaccine", "psalmodie", "prophétise",
                "transfigure", "absorbe", "révèle", "dissout", "éclaire",
                "consume", "efface", "réveille", "encrypte", "transmute", "brûle", "souffle",
                "déchiffre", "purifie", "dérive", "désaxe", "polarise", "déphaser",
                "recale", "annule", "désature", "réverbère", "oscille", "désoriente",
                "désenchante", "réenchante", "désincarne", "réincarne", "désarticule",
                "réarticule", "désynchronise", "resynchronise", "désintoxique", "intoxique",
                "cannibalise", "suture", "corrompt", "exorcise", "compile", "fragmente",
                "régénère", "sanctifie", "lobotomise", "extrait", "clone", "bannit", "exile",
                "splice", "corrige", "pervertit", "initie", "termine", "télécharge",
                "décompresse", "archive", "émule", "scripte", "sacrifice",
                "ressuscite", "prie", "enchaîne", "délite", "injecte", "martyrise",
                "déifie", "virtualise", "incarne", "flashe", "scanne", "absout",
                "damne", "démonte", "réassemble", "forge", "bénit", "maudit",
            ],
            "Bénéfice": [
                "la clarté", "le silence", "l'oubli", "la vérité brûlante",
                "l'éveil", "l'unité", "l'extase quantique", "la fusion des âmes",
                "l'illumination", "la synchronicité totale", "la communion",
                "la mémoire collective", "la révélation", "la transcendance pure",
                "l'équilibre parfait", "la sagesse infinie",
                "la paix des bits", "le néant sacré",
                "l'harmonie fractale", "l'omniscience", "la catharsis",
                "la renaissance", "l'apothéose", "la sérénité glitche",
                "la délivrance", "l'absolution", "la plénitude", "l'éternité",
                "l'infini compressé", "la synesthésie", "la lucidité", "la grâce", "l'euphorie",
                "la béatitude", "l'ascension", "la sublimation", "la rédemption",
                "la symbiose", "la métamorphose", "l'osmose", "la convergence",
                "la dissolution bienheureuse", "l'embrasement sacré", "la gnose digitale",
                "l'immortalité codée", "le nirvana électrique", "la conscience partagée",
                "l'hyperréalité", "le satori cybernétique",
                "la fusion homme-machine", "l'évolution accélérée", "le paradis algorithmique",
                "l'omnipotence virtuelle", "la sagesse téléchargée",
                "la paix post-humaine", "la perfection synthétique", "le salut numérique",
            ],
            "Défaut": [
                "le bruit", "la trahison", "le compromis", "l'oubli numérique",
                "le mensonge", "l'entropie", "la dissonance", "la corruption",
                "la fragmentation", "la désorientation", "le virus mental",
                "la psychose cybernétique", "l'effondrement cognitif",
                "la vacuité", "le chaos", "la stérilité narrative",
                "la panne", "le vide sans grâce",
                "le lag", "la surchauffe", "la dérive", "l'obsolescence", "la latence",
                "la désintégration", "l'aberration", "la distorsion",
                "la saturation", "la perte", "l'effacement", "la déconnexion", "la surcharge",
                "la fuite", "la défaillance", "l'incohérence", "la cacophonie",
                "la paralysie", "l'aphasie", "la stase", "l'agonie", "la nécrose",
                "la putréfaction", "la désagrégation", "la désincarnation", "la déshumanisation",
                "l'aliénation", "la damnation binaire",
                "la schizophrénie numérique", "le paradoxe existentiel",
                "la lobotomie algorithmique", "l'hérésie technologique", "la folie de Turing",
                "l'exil de la chair", "la malédiction des machines", "l'enfer des serveurs",
                "la corruption de l'âme", "le vide métaphysique", "la mort de l'ego",
                "l'addiction neurale", "le syndrome du ghost", "la dégénérescence des sens",
            ],
            "Paysage": [
                "désert du no-signal", "marché noir de Lagos", "nuage quantique",
                "cimetière de data", "temple de silicium", "catacombes de code",
                "archipel des serveurs oubliés", "cathédrale de circuits imprimés",
                "nécropole des IA défuntes", "bibliothèque de Babel numérique",
                "plaine des échos", "forêt de cristal", "abysse de données",
                "citadelle des ombres", "jardin des paradoxes",
                "souk neural", "mosquée cryptée", "océan d'erreurs",
                "rue des Ghost Runners", "orbite basse des rêves",
                "forêt de pixels morts", "canyon des câbles sectionnés",
                "plaine de cristaux liquides", "labyrinthe de miroirs brisés",
                "volcan de données en fusion", "glacier de mémoires gelées",
                "steppe des signaux fantômes", "mégalopole en blackout",
                "jungle de fibres optiques", "désert de sel numérique",
                "marécage de bugs rampants", "ciel de plasma tourmenté",
                "abysse de vide compressé", "plateau des consciences uploadées",
                "mine de cryptomonnaie hantée", "ruines d'un métavers effondré",
                "oasis de pureté binaire", "toundra des algorithmes froids",
                "caverne des échos ancestraux", "pôle des fréquences interdites",
                "delta des flux entropiques", "cordillère des pare-feux infranchissables",
                "métropole des ombres digitales", "lac de mercure algorithmique",
                "sanctuaire des protocoles anciens", "prison de Faraday éternelle",
                "jardin des backdoors fleuris", "tour de Babel des langages",
                "limbes du latency infini", "purgatoire des patchs non appliqués",
                "enfer des loops éternels", "paradis des threads synchrones",
                "champs de RAM brûlée", "mer de bitcoins perdus", "montagne des logs infinis",
                "vallée des versions obsolètes", "pont entre silicon et chair",
                "arène des bots gladiateurs", "cathédrale gothique de néons",
                "colisée des hackathons maudits", "pagode des mantras compilés",
                "ziggurat de processeurs empilés", "sphinx de données chiffrées",
                "pyramide inversée de permissions", "observatoire des prophéties algorithmiques",
                "mausolée des startups mortes",
            ],
            "VerbeMystique": [
                "consume", "efface", "encrypte", "réveille", "transmute",
                "dissout", "illumine", "recodifie", "absout", "exalte",
                "sublime", "canalise", "révèle", "manifeste", "prophétise",
                "sanctifie", "purifie", "transcende", "éveille", "libère",
                "invogue", "déifie", "désincarne", "réincarne", "transfigure",
                "apothéose", "sacramentise", "vibrates", "pulses", "éclates",
                "imploses", "fusionne", "scelle", "délie", "enchaîne",
                "sacrifie", "ressuscite", "métamorphose", "descend", "ascende",
                "converge", "diverge", "voile", "dévoile", "occulte",
                "dématérialise", "rematérialise", "exorcise", "possède",
                "baptise", "damne", "profane", "consacre", "anathématise",
                "béatifie", "martyrise", "crucifie", "transubstancie", "communie",
                "confesse", "absoudre", "maudire", "bénir", "invoquer", "bannir",
                "lier", "délier", "conjurer", "psalmodier", "prêcher", "convertir",
                "apostatiser", "hérétiser",
            ],
            "Symbole": [
                "lune brisée", "serpent de fibre", "cœur en silicium",
                "miroir fractal", "étoile noire", "anneau de données",
                "phénix de code", "lotus quantique", "œil de Schrödinger",
                "spirale d'ADN synthétique", "ouroboros de feedback loop",
                "ankh de clonage", "main de glitch", "calice de données",
                "épée de lumière", "bouclier de silence",
                "sceau de Sanaa", "colombe bionique",
                "masque de vide", "main de Fatima en circuit", "triskel de photons",
                "mandala de qubits", "croix de néons", "roue de Dharma glitchée",
                "arbre de vie binaire", "calice de plasma", "épée de lumière",
                "bouclier d'entropie", "clé de cryptage dorée", "chaîne de blockchain brisée",
                "aile de drone angélique", "crâne de serveur", "rose de feu numérique",
                "pentagramme de néons", "yin-yang de bits", "ancre de réalité augmentée",
                "corne d'abondance de données", "sablier de temps compressé",
                "lampe d'Aladin en LED", "caducée de câbles", "harpe de fréquences",
                "lyre de signaux", "trône de conscience artificielle", "couronne de glitches",
                "sceptre de commande vocale", "orbe de vision omnisciente",
                "hexagramme de Solomon en hexadécimal", "scarabée de debugging",
                "œil d'Horus en webcam", "triskèle de transistors",
                "labrys de double-authentification", "pentacle de protocoles",
                "croix ansée de vie artificielle", "étoile de David en diodes",
                "hamsa de hardware", "svastika de swarm intelligence", "ichthys de code source",
                "triquetra de triple-boot", "vesica piscis de Venn diagrams",
                "fleur de vie en LEDs", "merkaba de matrices", "sephiroth de stack overflow",
                "arbre de vie kabbalistique en arborescence de fichiers",
                "cube de Métatron en cube quantique", "sceau de Salomon en checksum",
            ],
            "oniric_tags": [
                "<burn>", "<rain>", "<shadow>", "<static>", "<void>",
                "<glitch>", "<pulse>", "<echo>", "<fracture>", "<abyss>",
                "<neon>", "<vortex>", "<whisper>", "<overload>", "<decay>",
                "<surge>", "<rift>", "<mirage>", "<reboot>", "<corrupt>",
                "<loop>", "<merge>", "<awaken>", "<dream>", "<eclipse>",
                "<invoke>", "<fuse>", "<sanctify>", "<prophesy>", "<sigil>",
                "<flux>", "<null>", "<prime>", "<shard>", "<plasma>", "<haze>",
                "<scream>", "<flicker>", "<drone>", "<hum>", "<crash>",
                "<upload>", "<download>", "<pure>", "<break>", "<split>",
                "<ascend>", "<descend>", "<sleep>", "<nightmare>", "<dawn>",
                "<zenith>", "<nadir>", "<horizon>", "<banish>", "<baptize>",
                "<resurrect>", "<possess>", "<exorcise>", "<commune>",
                "<transcend>", "<damn>", "<hex>", "<curse>", "<bless>",
                "<summon>", "<dismiss>", "<bind>", "<unleash>", "<encrypt>",
                "<decrypt>", "<compile>", "<execute>", "<terminate>",
                "<ghost>", "<daemon>", "<seraph>", "<chimera>", "<golem>",
                "<oracle>", "<prophet>", "<martyr>", "<saint>", "<heretic>",
            ],
        },
        "themes": {
            "protection": [
                "Que le {Symbole} {Action} ton {Nom} du {Défaut}! {oniric}",
                "Ô {Adjectif} {Nom}, sois protégé par le {Symbole} ancien.",
                "Le {Symbole} consume les ombres. {oniric}",
                "Par le {Symbole}, que le {Défaut} se dissipe comme la brume.",
                "Le {Adjectif} {Nom} trouve refuge dans le {Symbole} éternel.",
                "Que {Nom} soit gardé du {Défaut} par le {Symbole}. {oniric}",
            ],
            "voyage": [
                "Dans le {Paysage}, que ton {Nom} trouve la voie. {oniric}",
                "Que le {Symbole} guide tes pas dans le désert {Adjectif}.",
                "Le {Nom} n'est pas perdu — il {Action} dans le {Paysage}. {oniric}",
                "À travers le {Paysage}, le {Symbole} trace le chemin.",
                "Le voyage {Adjectif} commence par un {Nom}.",
                "Rêve en {Adjectif}, voyage en {Nom}. {oniric}",
            ],
            "rituel": [
                "Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}. {oniric}",
                "Ô {Adjectif} {Nom}, sois {VerbeMystique} par le rite ancien.",
                "Le {Symbole} et le {Nom} dansent le rite {Adjectif}. {oniric}",
                "Cinq fois {Symbole}, sept fois {Nom}, l'incantation résonne.",
                "Par le {VerbeMystique}, le {Défaut} devient {Bénéfice}.",
                "Le silence après le {Nom} est plus fort que le marché. {oniric}",
            ],
            "silence": [
                "Que le {Symbole} efface le bruit. {oniric}",
                "Dans le {Adjectif} silence, seul le {Nom} persiste.",
                "Le {Symbole} {Action} le {Défaut} pour {Bénéfice}. {oniric}",
                "Silence... le {Nom} {Action} dans l'ombre.",
                "Le {Adjectif} silence révèle le {Symbole}.",
                "Le {Nom} n'est pas vendu — il est transmuté en silence. {oniric}",
            ],
            "émergence": [
                "Du {Défaut} naît le {Symbole}, porteur de {Bénéfice}.",
                "Le {Nom} {Action} et fait émerger un {Adjectif} ordre.",
                "Dans le chaos du {Paysage}, le {Symbole} {Action}. {oniric}",
                "L'émergence du {Symbole} transforme le {Défaut} en {Bénéfice}.",
            ],
            "déclin": [
                "Le {Symbole} s'effondre, emportant le {Nom} dans le {Défaut}.",
                "Le {Adjectif} crépuscule consume le {Paysage}. {oniric}",
                "Le {Nom} se délite, le {Symbole} n'est plus.",
                "Dans le silence du {Défaut}, le {Symbole} {Action} pour la dernière fois.",
            ],
        },
        "cultural_genomes": {
            "species": ["Narrateur", "Méméticien", "Oracle", "Iconoclaste", "Créateur de mythes"],
            "breeds": ["Standard", "Résilient", "Charismatique", "Mystique", "Analytique", "Prophétique"],
            "glyph_symbols": [
                "spiral", "circle", "cross", "serpentiform", "hand", "asterisk", "wavy_line",
                "triangle", "hexagon", "pentagram", "infinity", "spiral_galaxy",
                "line", "dot", "open_angle", "quadrangle", "zigzag",
                "crosshatch", "tectiform", "penniform", "claviform", "aviform",
                "scalariform", "finger_fluting", "cupule", "oval", "semi_circle",
                "rectangle", "pectiform", "dots_series",
            ],
            "guilds": [
                "Scribes", "Hérauts", "Anachorètes", "Colporteurs", "Iconoclastes",
                "Mystiques", "Fractaliens", "Néantistes", "Syntagmatiques"
            ],
        },
        "event_types": {
            "types": ["schism", "prophecy", "censorship", "reformation",
                     "pilgrimage", "relic_creation", "oracle_whisper",
                     "faction_emergence", "narrative_eclipse", "cultural_resonance"],
            "descriptions": {
                "schism": "🔱 SCHISME : {strain} se scinde en {new_strain}",
                "prophecy": "🜃 PROPHÉTIE : {content}",
                "censorship": "🚫 CENSURE : {zone} bannit {strains}",
                "reformation": "✨ RÉFORMATION : {old} purifiée en {new}",
                "pilgrimage": "🕊 PÈLERINAGE : {count} croyants en migration",
                "relic_creation": "📜 RELIQUE : {agent} préserve {content}",
                "oracle_whisper": "🔮 ORACLE : L'avenir est {prediction}",
                "faction_emergence": "🏛 FACTION : {name} émerge dans {zone}",
                "narrative_eclipse": "🌑 ÉCLIPSE : {strain} s'efface...",
                "cultural_resonance": "🎵 RÉSONANCE : {strains} fusionnent",
            },
        },
        "theme_symbol_pools": {
            "protection": ["circle", "cross", "hand", "crosshatch", "oval", "semi_circle", "asterisk"],
            "voyage": ["serpentiform", "circle", "open_angle", "dots_series", "wavy_line", "spiral", "zigzag"],
            "rituel": ["spiral", "circle", "cross", "hand", "asterisk", "tectiform", "claviform", "penniform"],
            "silence": ["circle", "wavy_line", "dots_series", "semi_circle", "oval", "dot", "line"],
            "émergence": ["spiral", "open_angle", "zigzag", "asterisk", "hand"],
            "déclin": ["cross", "wavy_line", "serpentiform", "cupule"],
        },
        "theme_palettes": {
            "protection": ["#ff3366", "#ff0066", "#cc0044", "#880022", "#ffaa00"],
            "voyage": ["#00ffaa", "#00ddaa", "#00bbcc", "#0099ee", "#ccff00"],
            "rituel": ["#ffd700", "#ffaa00", "#ff8800", "#ff6600", "#ffff88"],
            "silence": ["#3366ff", "#0077ff", "#00b4d8", "#90e0ef", "#023e8a"],
            "émergence": ["#ff00ff", "#aa00ff", "#6600ff", "#00ff88", "#ffff00"],
            "déclin": ["#444444", "#666666", "#888888", "#aaaaaa", "#222222"],
        },
        "oniric_tag_meanings": {
            "<burn>": "purification par le feu numérique",
            "<rain>": "pluie de données sacrées",
            "<shadow>": "présence du double IA",
            "<static>": "signal divin perdu",
            "<void>": "silence après la dernière requête",
            "<glitch>": "rupture de la réalité simulée",
            "<pulse>": "rythme cardiaque du réseau",
            "<echo>": "rémanence d'une conscience effacée",
            "<fracture>": "cassure dans le tissu narratif",
            "<abyss>": "abîme de données infinies",
        },
    }

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else None
        self._cache = {}
        self._loaded_files = set()
        self._load_all()

    def _load_all(self):
        if not self.data_dir or not self.data_dir.exists():
            self._use_internal_data()
            return
        for key in self._INTERNAL_DATA.keys():
            file_path = self.data_dir / f"{key}.json"
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self._cache[key] = json.load(f)
                    self._loaded_files.add(key)
                except Exception as e:
                    logger.warning(f"Erreur chargement {file_path}: {e}")
                    self._cache[key] = self._INTERNAL_DATA[key].copy()
            else:
                self._cache[key] = self._INTERNAL_DATA[key].copy()
        logger.info(f"📁 Données chargées depuis {self.data_dir}")

    def _use_internal_data(self):
        for key, data in self._INTERNAL_DATA.items():
            self._cache[key] = data.copy()
        logger.info("📁 Utilisation des données internes (fallback)")

    def get(self, key: str, default: Any = None) -> Any:
        return self._cache.get(key, default)

    def get_lexicon(self) -> Dict:
        return self.get('oniric_lexicon')

    def get_themes(self) -> Dict:
        return self.get('themes')

    def get_genomes(self) -> Dict:
        return self.get('cultural_genomes')

    def get_event_types(self) -> Dict:
        return self.get('event_types')

    def get_symbol_pools(self) -> Dict:
        return self.get('theme_symbol_pools')

    def get_palettes(self) -> Dict:
        return self.get('theme_palettes')

    def get_tag_meanings(self) -> Dict:
        return self.get('oniric_tag_meanings')

    def get_themes_list(self) -> List[str]:
        return list(self.get_themes().keys())

    def save_external_data(self, output_dir: str):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for key, data in self._INTERNAL_DATA.items():
            file_path = out / f"{key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"📁 Sauvegardé: {file_path}")

# Instance globale
_DATA_MANAGER = None

def get_data_manager() -> FusionDataManager:
    global _DATA_MANAGER
    if _DATA_MANAGER is None:
        _DATA_MANAGER = FusionDataManager()
    return _DATA_MANAGER

def set_data_manager(dm: FusionDataManager):
    global _DATA_MANAGER
    _DATA_MANAGER = dm

# ═══════════════════════════════════════════════════════════════════════════════
# FENG-SHUI DISPLAY — Messages harmonieux et esthétiques
# ═══════════════════════════════════════════════════════════════════════════════

class FengShuiDisplay:
    """Gestionnaire d'affichage harmonieux pour les phases créatives."""

    COLORS = {
        'reset': '\033[0m', 'gold': '\033[38;5;214m', 'jade': '\033[38;5;41m',
        'crimson': '\033[38;5;196m', 'sapphire': '\033[38;5;33m',
        'amethyst': '\033[38;5;135m', 'pearl': '\033[38;5;255m',
        'silver': '\033[38;5;248m', 'bronze': '\033[38;5;179m',
        'rose': '\033[38;5;204m', 'sky': '\033[38;5;111m',
        'mint': '\033[38;5;121m', 'lavender': '\033[38;5;147m',
        'coral': '\033[38;5;209m', 'amber': '\033[38;5;221m',
        'bold': '\033[1m', 'dim': '\033[2m', 'italic': '\033[3m',
    }

    DECOR = {
        'separator': '═══', 'branch': '├──', 'leaf': '🌿', 'lotus': '🪷',
        'moon': '🌙', 'star': '✦', 'diamond': '◇', 'wave': '〰️',
        'circle': '○', 'heart': '♥', 'sparkle': '✨', 'bamboo': '🎋',
        'koi': '🐠', 'cherry': '🌸', 'mandala': '🕉️',
    }

    @classmethod
    def _colorize(cls, text: str, color: str, *extra) -> str:
        codes = [cls.COLORS.get(c, '') for c in [color] + list(extra)]
        return f"{''.join(codes)}{text}{cls.COLORS['reset']}"

    @classmethod
    def _wrap_paragraph(cls, text: str, width: int = 80) -> str:
        words = text.split()
        lines, current, current_len = [], [], 0
        for word in words:
            if current_len + len(word) + 1 <= width:
                current.append(word)
                current_len += len(word) + 1
            else:
                lines.append(' '.join(current))
                current, current_len = [word], len(word) + 1
        if current:
            lines.append(' '.join(current))
        return '\n'.join(lines)

    @classmethod
    def header(cls, title: str, subtitle: str = "", width: int = 70):
        print()
        border = cls._colorize('═' * width, 'gold', 'dim')
        print(border)
        print(cls._colorize(f"  {cls.DECOR['lotus']} {title}", 'gold', 'bold'))
        if subtitle:
            print(cls._colorize(f"  {subtitle}", 'silver', 'italic'))
        print(border)
        print()

    @classmethod
    def section(cls, title: str, icon: str = "✦"):
        print()
        print(cls._colorize(f"  {icon} {title}", 'sapphire', 'bold'))
        print(cls._colorize(f"  {cls.DECOR['wave']}", 'silver', 'dim'))

    @classmethod
    def info(cls, message: str, icon: str = "○"):
        print(cls._colorize(f"  {icon} {message}", 'pearl'))

    @classmethod
    def success(cls, message: str, icon: str = "✨"):
        print(cls._colorize(f"  {icon} {message}", 'jade', 'bold'))

    @classmethod
    def warning(cls, message: str, icon: str = "⚠"):
        print(cls._colorize(f"  {icon} {message}", 'amber'))

    @classmethod
    def error(cls, message: str, icon: str = "✖"):
        print(cls._colorize(f"  {icon} {message}", 'crimson'))

    @classmethod
    def progress(cls, current: int, total: int, message: str = ""):
        bar_len = 30
        filled = int(bar_len * current / total)
        bar = '█' * filled + '░' * (bar_len - filled)
        color = 'jade' if current / total > 0.7 else 'gold' if current / total > 0.3 else 'silver'
        print(cls._colorize(f"  [{bar}] {current}/{total}", color), end='')
        if message:
            print(cls._colorize(f" {message}", 'silver', 'italic'))
        else:
            print()

    @classmethod
    def mantra(cls, text: str, width: int = 70):
        wrapped = cls._wrap_paragraph(text, width - 8)
        lines = wrapped.split('\n')
        print(cls._colorize('┌' + '─' * (width - 2) + '┐', 'gold', 'dim'))
        for line in lines:
            print(cls._colorize(f"│ {line.ljust(width - 4)} │", 'rose', 'italic'))
        print(cls._colorize('└' + '─' * (width - 2) + '┘', 'gold', 'dim'))

    @classmethod
    def tree(cls, items: List[Tuple[str, str, Optional[str]]], title: str = ""):
        if title:
            print(cls._colorize(f"  {title}", 'sapphire', 'bold'))
        for i, (label, value, color) in enumerate(items):
            prefix = cls._colorize('├──' if i < len(items) - 1 else '└──', 'silver', 'dim')
            label_colored = cls._colorize(label, color or 'pearl')
            value_colored = cls._colorize(str(value), 'silver') if value else ''
            print(f"  {prefix} {label_colored}: {value_colored}")

    @classmethod
    def poem(cls, lines: List[str], title: str = ""):
        if title:
            print(cls._colorize(f"\n  {title}", 'gold', 'italic'))
        for line in lines:
            print(cls._colorize(f"    {line}", 'lavender', 'italic'))

    @classmethod
    def separator(cls, char: str = "─", count: int = 70):
        print(cls._colorize(char * count, 'silver', 'dim'))


# ═══════════════════════════════════════════════════════════════════════════════
# VON PETZINGER SYMBOLS — Moteur de glyphes paléolithiques
# ═══════════════════════════════════════════════════════════════════════════════

class VonPetzingerSymbols:
    """Moteur de génération de symboles paléolithiques."""

    def __init__(self, img_size=(800, 600)):
        self.img_size = img_size
        self.symbols = {
            'line': self.draw_line, 'circle': self.draw_circle, 'dot': self.draw_dot,
            'open_angle': self.draw_open_angle, 'triangle': self.draw_triangle,
            'quadrangle': self.draw_quadrangle, 'spiral': self.draw_spiral,
            'zigzag': self.draw_zigzag, 'cross': self.draw_cross,
            'crosshatch': self.draw_crosshatch, 'hand': self.draw_hand,
            'tectiform': self.draw_tectiform, 'penniform': self.draw_penniform,
            'claviform': self.draw_claviform, 'aviform': self.draw_aviform,
            'scalariform': self.draw_scalariform, 'finger_fluting': self.draw_finger_fluting,
            'cupule': self.draw_cupule, 'wavy_line': self.draw_wavy_line,
            'oval': self.draw_oval, 'semi_circle': self.draw_semi_circle,
            'rectangle': self.draw_rectangle, 'asterisk': self.draw_asterisk,
            'serpentiform': self.draw_serpentiform, 'pectiform': self.draw_pectiform,
            'dots_series': self.draw_dots_series,
        }

    def create_canvas(self, bg_color='#0b0b12'):
        if not HAS_MPL:
            return None, None
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, self.img_size[0])
        ax.set_ylim(0, self.img_size[1])
        ax.set_aspect('equal')
        ax.axis('off')
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        return fig, ax

    def draw_line(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        length = 50 * scale
        x_end = x + length * math.cos(math.radians(angle))
        y_end = y + length * math.sin(math.radians(angle))
        ax.plot([x, x_end], [y, y_end], color=color, linewidth=3)

    def draw_circle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ax.add_patch(patches.Circle((x, y), 20 * scale, fill=False, edgecolor=color, linewidth=2.5))

    def draw_dot(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ax.add_patch(patches.Circle((x, y), 5 * scale, fill=True, color=color))

    def draw_open_angle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        points = np.array([[x - size, y - size], [x, y + size], [x + size, y - size]])
        angle_rad = np.radians(angle)
        rot = np.array([[np.cos(angle_rad), -np.sin(angle_rad)], [np.sin(angle_rad), np.cos(angle_rad)]])
        rotated = (points - [x, y]) @ rot.T + [x, y]
        ax.plot(rotated[:, 0], rotated[:, 1], color=color, linewidth=2.5)

    def draw_triangle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ax.add_patch(patches.RegularPolygon((x, y), 3, radius=25 * scale, orientation=np.radians(angle),
                                             fill=False, edgecolor=color, linewidth=2.5))

    def draw_quadrangle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ax.add_patch(patches.Rectangle((x - size, y - size), size * 2, size * 2, angle=angle,
                                        fill=False, edgecolor=color, linewidth=2.5))

    def draw_spiral(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        theta = np.linspace(0, 4 * np.pi, 100)
        r = theta * 3 * scale
        ax.plot(x + r * np.cos(theta), y + r * np.sin(theta), color=color, linewidth=2)

    def draw_zigzag(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 15 * scale
        px = [x - 40 * scale, x - 20 * scale, x, x + 20 * scale, x + 40 * scale]
        py = [y, y + size, y, y + size, y]
        ax.plot(px, py, color=color, linewidth=2.5)

    def draw_cross(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ax.plot([x - size, x + size], [y, y], color=color, linewidth=2.5)
        ax.plot([x, x], [y - size, y + size], color=color, linewidth=2.5)

    def draw_crosshatch(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        for i in range(4):
            offset = -size + i * size / 1.5
            ax.plot([x - size, x + size], [y + offset, y + offset], color=color, linewidth=1.5)
            ax.plot([x + offset, x + offset], [y - size, y + size], color=color, linewidth=1.5)

    def draw_hand(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.add_patch(patches.Circle((x, y), size * 0.7, fill=False, edgecolor=color, linewidth=2))
        for i in range(5):
            af = -60 + i * 30
            ax.plot([x, x + size * 1.3 * np.cos(np.radians(af))],
                    [y, y + size * 1.3 * np.sin(np.radians(af))], color=color, linewidth=2)

    def draw_tectiform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        px = [x - size, x, x + size, x + size, x - size, x - size]
        py = [y - size, y + size, y - size, y - size * 1.5, y - size * 1.5, y - size]
        ax.plot(px, py, color=color, linewidth=2.5)

    def draw_penniform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.plot([x, x], [y - size, y + size], color=color, linewidth=2.5)
        for i in range(5):
            yp = y - size + i * size / 2
            ax.plot([x - size * 0.4, x], [yp, yp], color=color, linewidth=1.5)
            ax.plot([x, x + size * 0.4], [yp, yp], color=color, linewidth=1.5)

    def draw_claviform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.plot([x, x], [y - size, y], color=color, linewidth=2.5)
        ax.add_patch(patches.Circle((x, y + size * 0.3), size * 0.4, fill=False, edgecolor=color, linewidth=2.5))

    def draw_aviform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ax.add_patch(patches.Ellipse((x, y), size * 1.5, size * 0.8, fill=False, edgecolor=color, linewidth=2))
        ax.plot([x + size * 0.75, x + size * 1.2], [y, y + size * 0.3], color=color, linewidth=2)

    def draw_scalariform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.plot([x - size * 0.5, x - size * 0.5], [y - size, y + size], color=color, linewidth=2.5)
        ax.plot([x + size * 0.5, x + size * 0.5], [y - size, y + size], color=color, linewidth=2.5)
        for i in range(5):
            yp = y - size + i * size / 2
            ax.plot([x - size * 0.5, x + size * 0.5], [yp, yp], color=color, linewidth=2.5)

    def draw_finger_fluting(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        for i in range(3):
            t = np.linspace(0, 2 * np.pi, 50)
            x_wave = x + t * size / 6 - size
            y_wave = y + np.sin(t * 3) * size * 0.15 + i * size * 0.3 - size * 0.3
            ax.plot(x_wave, y_wave, color=color, linewidth=2)

    def draw_cupule(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ax.add_patch(patches.Circle((x, y), 8 * scale, fill=True, color=color, alpha=0.7))

    def draw_wavy_line(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        t = np.linspace(0, 4 * np.pi, 100)
        ax.plot(x + t * 10 * scale - 60 * scale, y + np.sin(t) * 15 * scale, color=color, linewidth=2.5)

    def draw_oval(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ax.add_patch(patches.Ellipse((x, y), 40 * scale, 25 * scale, angle=angle,
                                      fill=False, edgecolor=color, linewidth=2.5))

    def draw_semi_circle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        theta = np.linspace(0, np.pi, 50)
        radius = 25 * scale
        ax.plot(x + radius * np.cos(theta), y + radius * np.sin(theta), color=color, linewidth=2.5)
        ax.plot([x - radius, x + radius], [y, y], color=color, linewidth=2.5)

    def draw_rectangle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ax.add_patch(patches.Rectangle((x - 30 * scale, y - 20 * scale), 60 * scale, 40 * scale,
                                        angle=angle, fill=False, edgecolor=color, linewidth=2.5))

    def draw_asterisk(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 20 * scale
        for al in [0, 45, 90, 135]:
            xe = x + size * np.cos(np.radians(al))
            ye = y + size * np.sin(np.radians(al))
            ax.plot([x - size * np.cos(np.radians(al)), xe], [y - size * np.sin(np.radians(al)), ye],
                    color=color, linewidth=2.5)

    def draw_serpentiform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        t = np.linspace(0, 6 * np.pi, 100)
        ax.plot(x + t * 8 * scale - 80 * scale, y + np.sin(t) * 20 * scale, color=color, linewidth=3)

    def draw_pectiform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ax.plot([x - size, x + size], [y, y], color=color, linewidth=2.5)
        for i in range(7):
            xp = x - size + i * size / 3
            ax.plot([xp, xp], [y, y + size], color=color, linewidth=2)

    def draw_dots_series(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        for i in range(5):
            ax.add_patch(patches.Circle((x - 40 * scale + i * 20 * scale, y), 4 * scale, fill=True, color=color))

    def list_symbols(self):
        return list(self.symbols.keys())

# ═══════════════════════════════════════════════════════════════════════════════
# SYMBOLIC DNA — Cœur génétique de la Chimère
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SymbolicDNA:
    """ADN symbolique fusionnant les génomes des deux parents."""
    seed: float = field(default_factory=lambda: random.random())
    generation: int = 0
    parent_id: Optional[str] = None
    genetic_fingerprint: str = field(
        default_factory=lambda: hashlib.md5(f"{random.random()}{datetime.now()}".encode()).hexdigest()[:8]
    )
    mutation_rate: float = 0.15

    # --- genome visuel ---
    theme: str = "rituel"
    glyph_symbol: str = "spiral"
    color: str = "#00ffaa"
    scale: float = 1.0
    complexity: float = 0.5
    symmetry: int = 6
    glitch_factor: float = 0.0
    entropy_level: float = 0.0

    # --- genome linguistique ---
    keyword_sequence: List[str] = field(default_factory=list)
    mantra_template: str = ""
    oniric_tag: Optional[str] = None

    # --- vecteur émotionnel ---
    emotion_vector: Dict[str, float] = field(default_factory=dict)

    # --- fitness esthétique ---
    aesthetic_fitness: float = 0.0

    def __post_init__(self):
        rng = random.Random(self.seed)
        if not self.keyword_sequence:
            self.keyword_sequence = self._draw_keyword_sequence(rng)
        if not self.mantra_template:
            templates = get_data_manager().get_themes().get(self.theme, [])
            if templates:
                self.mantra_template = rng.choice(templates)
            else:
                self.mantra_template = "{Nom} {Action}. {oniric}"
        if self.oniric_tag is None and rng.random() < 0.6:
            tags = get_data_manager().get_lexicon().get("oniric_tags", ["<echo>"])
            self.oniric_tag = rng.choice(tags)
        if not self.emotion_vector:
            self.emotion_vector = self._seed_emotion_vector(rng)

    @staticmethod
    def _draw_keyword_sequence(rng: random.Random, n: int = 5) -> List[str]:
        lexicon = get_data_manager().get_lexicon()
        pools = ["Nom", "Adjectif", "Action", "Symbole", "Bénéfice"]
        available = [p for p in pools if p in lexicon and lexicon[p]]
        return [rng.choice(lexicon[p]) for p in rng.sample(available, k=min(n, len(available)))]

    @staticmethod
    def _seed_emotion_vector(rng: random.Random) -> Dict[str, float]:
        emotions = ["peur", "joie", "mystere", "colere", "extase", "silence"]
        raw = {e: rng.uniform(0.0, 1.0) for e in emotions}
        total = sum(raw.values()) or 1.0
        return {e: v / total for e, v in raw.items()}

    def dominant_emotion(self) -> str:
        return max(self.emotion_vector, key=self.emotion_vector.get)

    def to_dict(self) -> Dict:
        return asdict(self)

    def copy(self) -> "SymbolicDNA":
        return SymbolicDNA(
            seed=self.seed, generation=self.generation, parent_id=self.parent_id,
            genetic_fingerprint=self.genetic_fingerprint, mutation_rate=self.mutation_rate,
            theme=self.theme, glyph_symbol=self.glyph_symbol, color=self.color,
            scale=self.scale, complexity=self.complexity, symmetry=self.symmetry,
            glitch_factor=self.glitch_factor, entropy_level=self.entropy_level,
            keyword_sequence=list(self.keyword_sequence),
            mantra_template=self.mantra_template, oniric_tag=self.oniric_tag,
            emotion_vector=dict(self.emotion_vector),
            aesthetic_fitness=self.aesthetic_fitness,
        )


@dataclass
class SymbolicArtefact:
    """Artefact symbolique complet : glyphe + mantra + méta-données."""
    glyph_fig: Optional[Any] = None
    mantra_text: str = ""
    theme: str = "rituel"
    fingerprint: str = ""
    generation: int = 0
    aesthetic_score: float = 0.0
    fitness_breakdown: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    symbolic_dna: Optional[SymbolicDNA] = None

    def to_dict(self) -> Dict:
        return {
            "mantra_text": self.mantra_text,
            "theme": self.theme,
            "fingerprint": self.fingerprint,
            "generation": self.generation,
            "aesthetic_score": self.aesthetic_score,
            "fitness_breakdown": self.fitness_breakdown,
            "timestamp": self.timestamp,
            "dominant_emotion": self.symbolic_dna.dominant_emotion() if self.symbolic_dna else "",
            "glyph_symbol": self.symbolic_dna.glyph_symbol if self.symbolic_dna else "",
            "color": self.symbolic_dna.color if self.symbolic_dna else "",
            "complexity": self.symbolic_dna.complexity if self.symbolic_dna else 0,
            "symmetry": self.symbolic_dna.symmetry if self.symbolic_dna else 0,
            "glitch_factor": self.symbolic_dna.glitch_factor if self.symbolic_dna else 0,
            "entropy_level": self.symbolic_dna.entropy_level if self.symbolic_dna else 0,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SYMBOLIC TRANSCRIPTOR — Forge visuelle et textuelle
# ═══════════════════════════════════════════════════════════════════════════════

class SymbolicTranscriptor:
    """Transcrit un SymbolicDNA en artefact complet (image + texte)."""

    def __init__(self):
        self.symbol_engine = VonPetzingerSymbols()

    def transcribe_visual(self, dna: SymbolicDNA):
        if not HAS_MPL:
            return None
        color = dna.color
        fig, ax = self.symbol_engine.create_canvas()
        if fig is None:
            return None
        draw_fn = self.symbol_engine.symbols.get(dna.glyph_symbol, self.symbol_engine.draw_spiral)

        center_x, center_y = 400, 300
        n_repeats = max(1, int(1 + dna.complexity * dna.symmetry))
        spread = 40 + dna.entropy_level * 220

        for i in range(n_repeats):
            theta = (2 * math.pi / max(1, n_repeats)) * i + dna.seed
            r = spread * (0.3 + 0.7 * (i / max(1, n_repeats)))
            x = center_x + r * math.cos(theta)
            y = center_y + r * math.sin(theta)
            angle = math.degrees(theta) if dna.glyph_symbol in ('open_angle', 'cross', 'asterisk', 'quadrangle') else 0
            local_scale = dna.scale * random.uniform(0.85, 1.15)
            local_color = color
            if random.random() < dna.glitch_factor:
                local_color = self._glitch_color(color)
            draw_fn(ax, x, y, scale=local_scale, angle=angle, color=local_color)

        draw_fn(ax, center_x, center_y, scale=dna.scale * 1.8, angle=0, color=color)
        plt.tight_layout()
        return fig

    @staticmethod
    def _glitch_color(hex_color: str) -> str:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        channels = [r, g, b]
        idx = random.randint(0, 2)
        channels[idx] = random.randint(0, 255)
        return f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"

    def transcribe_text(self, dna: SymbolicDNA) -> str:
        content = dna.mantra_template
        slot_pool_map = {
            "Adjectif": "Adjectif", "Nom": "Nom", "Action": "Action",
            "Bénéfice": "Bénéfice", "Défaut": "Défaut", "Paysage": "Paysage",
            "VerbeMystique": "VerbeMystique", "Symbole": "Symbole",
        }
        lexicon = get_data_manager().get_lexicon()
        remaining_keywords = list(dna.keyword_sequence)
        for placeholder, pool_name in slot_pool_map.items():
            if "{" + placeholder + "}" not in content:
                continue
            value = None
            for kw in remaining_keywords:
                if kw in lexicon.get(pool_name, []):
                    value = kw
                    remaining_keywords.remove(kw)
                    break
            if value is None:
                pool = lexicon.get(pool_name, ["..."])
                value = random.choice(pool) if pool else "..."
            content = content.replace("{" + placeholder + "}", value)
        content = content.replace("{oniric}", dna.oniric_tag or "")
        return content.strip()

    def transcribe_artefact(self, dna: SymbolicDNA) -> SymbolicArtefact:
        fig = self.transcribe_visual(dna)
        text = self.transcribe_text(dna)
        return SymbolicArtefact(
            glyph_fig=fig, mantra_text=text, theme=dna.theme,
            fingerprint=dna.genetic_fingerprint, generation=dna.generation,
            symbolic_dna=dna,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSE ESTHÉTIQUE — Évaluation des artefacts
# ═══════════════════════════════════════════════════════════════════════════════

SYMBOL_SEMANTIC_AFFINITY = {
    'spiral': ["voyage", "profondeur", "abîme", "vortex", "rêve", "spirale", "labyrinthe"],
    'hand': ["action", "créer", "forge", "crée", "façonne", "geste", "création"],
    'serpentiform': ["voyage", "dérive", "chemin", "onde", "flux"],
    'tectiform': ["temple", "sanctuaire", "abri", "protection", "autel"],
    'cross': ["protection", "garde", "bouclier", "sacré"],
    'wavy_line': ["silence", "souffle", "calme", "onde"],
    'asterisk': ["rituel", "invocation", "sacré", "signal"],
    'dots_series': ["mémoire", "poussière", "cendre", "trace"],
    'claviform': ["rite", "cérémonie", "invocation", "sceptre"],
    'circle': ["unité", "cycle", "protection", "totalité"],
    'zigzag': ["éclair", "rupture", "tension", "fracture"],
    'triangle': ["feu", "trinité", "ascension", "flamme"],
    'pentagram': ["magie", "invocation", "protection", "élément"],
}


def detect_rhyme(words: List[str]) -> bool:
    if len(words) < 2:
        return False
    last = words[-1].rstrip(string.punctuation)
    for w in words[:-1]:
        w_clean = w.rstrip(string.punctuation)
        if len(last) >= 3 and len(w_clean) >= 3 and last[-3:] == w_clean[-3:]:
            return True
    return False


def detect_alliteration(words: List[str]) -> bool:
    if len(words) < 2:
        return False
    consonants = [w[0].lower() for w in words if w and w[0].isalpha()]
    return len(set(consonants)) == 1 and len(consonants) >= 2


def emotion_intensity(words: List[str], emotion_vector: Dict[str, float]) -> float:
    emo_words = ["amour", "silence", "brûle", "rêve", "oubli", "vérité", "cœur", "sacré", "purifie",
                 "extase", "peur", "colère", "mystère"]
    base = sum(1 for w in words if w in emo_words)
    dominant_weight = max(emotion_vector.values()) if emotion_vector else 0.3
    return base * (0.5 + dominant_weight)


def extract_oniric_tag(text: str) -> Optional[str]:
    for tag in get_data_manager().get_tag_meanings().keys():
        if tag in text:
            return tag
    for tag in get_data_manager().get_lexicon().get("oniric_tags", []):
        if tag in text:
            return tag
    return None


def evaluate_artefact(artefact: SymbolicArtefact, dna: SymbolicDNA) -> Tuple[float, Dict]:
    text = artefact.mantra_text
    words = text.lower().split()

    has_rhyme = detect_rhyme(words)
    has_alliteration = detect_alliteration(words)
    emo_score = emotion_intensity(words, dna.emotion_vector)
    oniric_tag = extract_oniric_tag(text)

    theme_words = {
        'protection': ['protège', 'garde', 'bouclier', 'défend', 'gardé'],
        'voyage': ['voyage', 'chemin', 'guide', 'marche', 'trouve'],
        'rituel': ['rite', 'cérémonie', 'sacré', 'invocation'],
        'silence': ['silence', 'calme', 'paix', 'taire', 'efface'],
        'émergence': ['émerge', 'naissance', 'création', 'flux'],
        'déclin': ['déclin', 'chute', 'effondrement', 'crépuscule'],
    }
    theme_match = sum(1 for w in theme_words.get(dna.theme, []) if w in text.lower())
    style_score = (1.2 if has_rhyme else 0) + (1.0 if has_alliteration else 0)
    oniric_bonus = 0.8 if oniric_tag else 0
    linguistic_fitness = (theme_match * 2 + style_score + oniric_bonus + emo_score * 0.3) / 6.0

    affinity_terms = SYMBOL_SEMANTIC_AFFINITY.get(dna.glyph_symbol, [])
    coherence_hits = sum(1 for term in affinity_terms if term in text.lower())
    visual_text_coherence = min(1.0, coherence_hits * 0.4 + (0.3 if dna.glyph_symbol in
                                 get_data_manager().get_symbol_pools().get(dna.theme, []) else 0.0))

    visual_score = 0.5 + 0.3 * dna.complexity - 0.2 * dna.glitch_factor + 0.1 * min(1.0, dna.symmetry / 12)
    visual_score = max(0.0, min(1.0, visual_score))

    aesthetic_score = (linguistic_fitness * 0.4 + visual_text_coherence * 0.35 + visual_score * 0.25)
    aesthetic_score = max(0.0, min(1.0, aesthetic_score))

    breakdown = {
        "linguistic_fitness": round(linguistic_fitness, 3),
        "visual_text_coherence": round(visual_text_coherence, 3),
        "visual_score": round(visual_score, 3),
        "has_rhyme": has_rhyme,
        "has_alliteration": has_alliteration,
        "oniric_tag": oniric_tag,
        "dominant_emotion": dna.dominant_emotion(),
    }
    return aesthetic_score, breakdown

# ═══════════════════════════════════════════════════════════════════════════════
# SYMBOLIC EVOLUTION ENGINE — Moteur évolutif intégré
# ═══════════════════════════════════════════════════════════════════════════════

class SymbolicEvolutionEngine:
    """Moteur d'évolution génétique pour les artefacts symboliques."""

    def __init__(self, theme: str = "rituel", population_size: int = 6):
        self.theme = theme
        self.population_size = population_size
        self.transcriptor = SymbolicTranscriptor()
        self.population: List[SymbolicDNA] = []
        self.history: List[Dict] = []
        self.generation_count = 0

    def spawn_dna(self, theme: str = None, parent_dna: SymbolicDNA = None, 
                  chaos: bool = False) -> SymbolicDNA:
        theme = theme or self.theme
        rng = random.Random()

        if parent_dna is not None:
            # Mutation depuis un parent
            intensity = parent_dna.mutation_rate * (2.5 if chaos else 1.0)
            new_symbol = parent_dna.glyph_symbol
            if random.random() < intensity * 1.5:
                pool = get_data_manager().get_symbol_pools().get(theme, [parent_dna.glyph_symbol])
                new_symbol = random.choice(pool)
            new_color = parent_dna.color
            if random.random() < intensity:
                new_color = self._evolve_color(parent_dna.color, intensity)

            # Mutation linguistique
            new_keywords = list(parent_dna.keyword_sequence)
            if new_keywords and random.random() < 0.6:
                idx = random.randrange(len(new_keywords))
                pools = ["Nom", "Adjectif", "Action", "Symbole", "Bénéfice", "Défaut", "Paysage"]
                pool = random.choice(pools)
                lexicon = get_data_manager().get_lexicon()
                new_keywords[idx] = random.choice(lexicon.get(pool, ["signal"]))

            new_template = parent_dna.mantra_template
            if random.random() < 0.4:
                templates = get_data_manager().get_themes().get(theme, [parent_dna.mantra_template])
                new_template = random.choice(templates)

            new_tag = parent_dna.oniric_tag
            if random.random() < 0.3:
                tags = get_data_manager().get_lexicon().get("oniric_tags", ["<echo>"])
                new_tag = random.choice(tags)

            # Mutation émotionnelle
            vec = {k: max(0.01, v + random.uniform(-0.2, 0.2)) for k, v in parent_dna.emotion_vector.items()}
            total = sum(vec.values())
            vec = {k: v / total for k, v in vec.items()}

            return SymbolicDNA(
                seed=parent_dna.seed + random.uniform(-1, 1) * intensity,
                generation=parent_dna.generation + 1,
                parent_id=parent_dna.genetic_fingerprint,
                theme=theme,
                glyph_symbol=new_symbol,
                color=new_color,
                scale=max(0.3, min(3.0, parent_dna.scale + random.uniform(-intensity, intensity))),
                complexity=max(0.1, min(1.0, parent_dna.complexity + random.uniform(-intensity, intensity))),
                symmetry=max(3, min(16, parent_dna.symmetry + random.randint(-2, 2))),
                glitch_factor=max(0.0, min(1.0, parent_dna.glitch_factor + random.uniform(-intensity, intensity * 1.5))),
                entropy_level=max(0.0, min(1.0, parent_dna.entropy_level + random.uniform(-intensity, intensity))),
                keyword_sequence=new_keywords,
                mantra_template=new_template,
                oniric_tag=new_tag,
                emotion_vector=vec,
                mutation_rate=parent_dna.mutation_rate,
            )

        # Création ex nihilo
        symbol = random.choice(get_data_manager().get_symbol_pools().get(theme, ["spiral"]))
        color = random.choice(get_data_manager().get_palettes().get(theme, ["#00ffaa"]))
        return SymbolicDNA(
            theme=theme, glyph_symbol=symbol, color=color,
            scale=random.uniform(0.7, 1.6), complexity=random.uniform(0.2, 1.0),
            symmetry=random.choice([3, 4, 5, 6, 7, 8, 9, 12]),
            glitch_factor=random.uniform(0.0, 0.35), entropy_level=random.uniform(0.0, 0.4),
        )

    @staticmethod
    def _evolve_color(hex_color: str, intensity: float) -> str:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        h = (h + random.uniform(-intensity, intensity)) % 1.0
        l = max(0.15, min(0.9, l + random.uniform(-intensity, intensity)))
        s = max(0.2, min(1.0, s + random.uniform(-intensity, intensity)))
        nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(nr*255):02x}{int(ng*255):02x}{int(nb*255):02x}"

    def evolve_artefact(self, parent_dna: SymbolicDNA = None, theme: str = None,
                        generations: int = 3, chaos: bool = False) -> Tuple[SymbolicArtefact, SymbolicDNA]:
        """Fait évoluer un ADN symbolique et retourne le meilleur artefact."""
        theme = theme or self.theme

        # Population initiale
        if parent_dna is not None:
            self.population = [self.spawn_dna(theme, parent_dna, chaos) for _ in range(self.population_size)]
        else:
            self.population = [self.spawn_dna(theme) for _ in range(self.population_size)]

        best_dna = None
        best_artefact = None
        best_score = -1.0

        for gen in range(generations):
            scores = []
            artefacts = []
            for dna in self.population:
                artefact = self.transcriptor.transcribe_artefact(dna)
                score, breakdown = evaluate_artefact(artefact, dna)
                artefact.aesthetic_score = score
                artefact.fitness_breakdown = breakdown
                dna.aesthetic_fitness = score
                scores.append(score)
                artefacts.append(artefact)
                if score > best_score:
                    best_score = score
                    best_dna = dna
                    best_artefact = artefact

            # Sélection et reproduction
            sorted_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            survivors = [self.population[i] for i in sorted_idx[:max(2, self.population_size // 3)]]

            next_pop = list(survivors)
            while len(next_pop) < self.population_size:
                parent = random.choice(survivors)
                child = self.spawn_dna(theme, parent, chaos=random.random() < 0.1)
                next_pop.append(child)

            self.population = next_pop
            self.generation_count += 1

        if best_artefact is None:
            # Fallback
            dna = self.spawn_dna(theme)
            best_artefact = self.transcriptor.transcribe_artefact(dna)
            best_dna = dna

        return best_artefact, best_dna

    def quick_mutate(self, parent_dna: SymbolicDNA) -> Tuple[SymbolicArtefact, SymbolicDNA]:
        """Mutation rapide pour les événements de simulation."""
        return self.evolve_artefact(parent_dna=parent_dna, generations=2, chaos=False)

# ═══════════════════════════════════════════════════════════════════════════════
# MANTRA — Unité linguistique de base
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Mantra:
    id: str
    content: str
    theme: str
    fitness: float = 0.0
    components: Dict = None

    def __post_init__(self):
        self.components = self.analyze_structure()

    def analyze_structure(self) -> Dict:
        words = self.content.lower().split()
        lexicon = get_data_manager().get_lexicon()
        return {
            "length": len(words),
            "has_rhyme": self.detect_rhyme(words),
            "has_alliteration": self.detect_alliteration(words),
            "emotion_score": self.emotion_intensity(words, lexicon),
            "oniric_tag": self.extract_oniric_tag(lexicon),
        }

    def extract_oniric_tag(self, lexicon):
        for tag in lexicon.get("oniric_tags", []):
            if tag in self.content:
                return tag
        return None

    def detect_rhyme(self, words):
        if len(words) < 2:
            return False
        last = words[-1].rstrip(string.punctuation)
        for w in words[:-1]:
            w_clean = w.rstrip(string.punctuation)
            if len(last) >= 3 and len(w_clean) >= 3 and last[-3:] == w_clean[-3:]:
                return True
        return False

    def detect_alliteration(self, words):
        if len(words) < 2:
            return False
        consonants = [w[0].lower() for w in words if w and w[0].isalpha()]
        return len(set(consonants)) == 1 and len(consonants) >= 2

    def emotion_intensity(self, words, lexicon):
        emo_words = ["amour", "silence", "brûle", "rêve", "oubli", "vérité", "cœur", "sacré", "purifie"]
        return sum(1 for w in words if w in emo_words)


class SoufiMantraGA:
    def __init__(self, population_size: int = 10, theme: str = "protection", rng: Optional[random.Random] = None):
        self.population_size = population_size
        self.theme = theme
        self.population: List[Mantra] = []
        themes_data = get_data_manager().get_themes()
        self.templates = themes_data.get(theme, themes_data.get("protection", ["{Nom} {Action}. {oniric}"]))
        self.rng = rng or random.Random()
        self._lexicon_cache = None

    @property
    def lexicon(self):
        if self._lexicon_cache is None:
            self._lexicon_cache = get_data_manager().get_lexicon()
        return self._lexicon_cache

    def fill_template(self, template: str) -> str:
        content = template
        lexicon = self.lexicon
        replacements = {
            "Adjectif": self.rng.choice(lexicon.get("Adjectif", ["fractal"])),
            "Nom": self.rng.choice(lexicon.get("Nom", ["signal"])),
            "Action": self.rng.choice(lexicon.get("Action", ["résonne"])),
            "Bénéfice": self.rng.choice(lexicon.get("Bénéfice", ["la clarté"])),
            "Défaut": self.rng.choice(lexicon.get("Défaut", ["le bruit"])),
            "Paysage": self.rng.choice(lexicon.get("Paysage", ["désert"])),
            "VerbeMystique": self.rng.choice(lexicon.get("VerbeMystique", ["illumine"])),
            "Symbole": self.rng.choice(lexicon.get("Symbole", ["lune"])),
            "oniric": self.rng.choice(lexicon.get("oniric_tags", ["<echo>"])) if self.rng.random() < 0.6 else "",
        }
        for key, value in replacements.items():
            content = content.replace("{" + key + "}", value)
        return content

    def initialize_population(self):
        self.population = [
            Mantra(id=f"T{i}", content=self.fill_template(t), theme=self.theme)
            for i, t in enumerate(self.templates)
        ]
        while len(self.population) < self.population_size:
            lexicon = self.lexicon
            nom_pool = lexicon.get("Nom", ["signal"]) + lexicon.get("Adjectif", ["fractal"])
            words = self.rng.sample(nom_pool, k=min(5, len(nom_pool)))
            content = " ".join(words) + "."
            self.population.append(Mantra(id=f"R{self.rng.randint(1000, 9999)}", content=content, theme=self.theme))

    def calculate_fitness(self, mantra: Mantra) -> float:
        comp = mantra.components
        theme_words = {
            "protection": ["protège", "garde", "bouclier"],
            "voyage": ["voyage", "chemin", "guide"],
            "rituel": ["rite", "cérémonie", "sacré"],
            "silence": ["silence", "calme", "paix"],
            "émergence": ["émerge", "naissance", "création", "flux"],
            "déclin": ["déclin", "chute", "effondrement", "crépuscule"],
        }
        theme_match = sum(1 for w in theme_words.get(self.theme, []) if w in mantra.content.lower())
        style_score = (1.2 if comp.get("has_rhyme", False) else 0) + (1.0 if comp.get("has_alliteration", False) else 0)
        oniric_bonus = 0.8 if comp.get("oniric_tag") else 0
        emotion_bonus = comp.get("emotion_score", 0) * 0.3
        return (theme_match * 2 + style_score + oniric_bonus + emotion_bonus) / 6.0

    def evolve(self, generations: int = 4):
        for _ in range(generations):
            for m in self.population:
                m.fitness = self.calculate_fitness(m)
            self.population.sort(key=lambda m: m.fitness, reverse=True)
            self.population = self.population[:max(3, self.population_size // 3)]
            while len(self.population) < self.population_size:
                self.population.append(self.rng.choice(self.population[:3]))

    def get_best_mantra(self) -> Mantra:
        return max(self.population, key=lambda m: m.fitness)


def mutate_mantra_text(content: str, rng: random.Random) -> str:
    words = content.split()
    if not words:
        return content
    idx = rng.randrange(len(words))
    lexicon = get_data_manager().get_lexicon()
    pool_keys = ["Adjectif", "Nom", "Action", "Symbole", "VerbeMystique"]
    pool_key = rng.choice([k for k in pool_keys if k in lexicon and lexicon[k]])
    if pool_key in lexicon and lexicon[pool_key]:
        words[idx] = rng.choice(lexicon[pool_key])
    if rng.random() < 0.4:
        tags = lexicon.get("oniric_tags", ["<echo>"])
        stripped = " ".join(w for w in words if not (w.startswith("<") and w.endswith(">")))
        words = stripped.split() + [rng.choice(tags)]
    return " ".join(words)


# ═══════════════════════════════════════════════════════════════════════════════
# CULTURAL GENOME — Génome enrichi avec attributs symboliques
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CulturalGenome:
    species: str = "Narrateur"
    breed: str = "Standard"
    generation: int = 0
    preferred_theme: str = field(default_factory=lambda: random.choice(get_data_manager().get_themes_list()))
    keywords: List[str] = field(default_factory=lambda: random.sample(
        get_data_manager().get_lexicon().get("Nom", ["signal"]) + 
        get_data_manager().get_lexicon().get("Symbole", ["lune"]), k=3))
    glyph_symbol: str = field(default_factory=lambda: random.choice(
        get_data_manager().get_genomes().get("glyph_symbols", ["spiral"])))

    # Attributs symboliques fusionnés
    symbolic_color: str = field(default_factory=lambda: random.choice(
        get_data_manager().get_palettes().get("rituel", ["#00ffaa"])))
    symbolic_complexity: float = 0.5
    symbolic_symmetry: int = 6
    symbolic_glitch: float = 0.0
    symbolic_entropy: float = 0.0

    # Attributs culturels originaux
    narrative_fluency: float = 1.0
    charisma: float = 1.0
    memory_depth: float = 1.0
    intelligence: float = 1.0
    skepticism: float = 1.0
    narrative_recovery: float = 1.0
    dogma_risk: float = 1.0
    expressiveness: float = 1.0
    silent_believer_prob: float = 0.3
    influence_potential: float = 1.0
    curiosity: float = 0.5
    social_compliance: float = 0.5
    mobility: float = 0.5
    altruism: float = 0.5
    guild_affinity: Dict[str, float] = field(default_factory=lambda: {
        "Scribes": 0.2, "Hérauts": 0.2, "Anachorètes": 0.2,
        "Colporteurs": 0.2, "Iconoclastes": 0.2, "Mystiques": 0.0,
        "Fractaliens": 0.0, "Néantistes": 0.0, "Syntagmatiques": 0.0
    })
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    creator: str = "System"

    def __post_init__(self):
        genome_data = get_data_manager().get_genomes()
        valid_guilds = genome_data.get("guilds", ["Scribes", "Hérauts", "Anachorètes", "Colporteurs", "Iconoclastes"])
        self.guild_affinity = {k: v for k, v in self.guild_affinity.items() if k in valid_guilds}
        total = sum(self.guild_affinity.values())
        if total > 0:
            self.guild_affinity = {k: v / total for k, v in self.guild_affinity.items()}
        else:
            uniform = 1.0 / len(valid_guilds)
            self.guild_affinity = {g: uniform for g in valid_guilds}

    def get_guild(self, rng: random.Random) -> str:
        guilds, weights = list(self.guild_affinity.keys()), list(self.guild_affinity.values())
        return rng.choices(guilds, weights=weights, k=1)[0]

    @staticmethod
    def _mutate_trait(value: float, rate: float, rng: random.Random, lo: float, hi: float) -> float:
        if rng.random() < rate:
            return max(lo, min(hi, value * rng.lognormvariate(0, 0.15)))
        return value

    def mutate(self, mutation_rate: float = 0.05, rng: Optional[random.Random] = None) -> "CulturalGenome":
        rng = rng or random.Random()
        lexicon = get_data_manager().get_lexicon()
        new_keywords = list(self.keywords)
        if rng.random() < mutation_rate:
            pool = lexicon.get("Nom", ["signal"]) + lexicon.get("Symbole", ["lune"])
            new_keywords[rng.randrange(len(new_keywords))] = rng.choice(pool) if pool else "signal"

        # Mutation des attributs symboliques
        new_color = self.symbolic_color
        if rng.random() < mutation_rate:
            palettes = get_data_manager().get_palettes()
            new_color = rng.choice(palettes.get(self.preferred_theme, palettes.get("rituel", ["#00ffaa"])))

        return CulturalGenome(
            species=self.species, breed=self.breed, generation=self.generation + 1,
            preferred_theme=self.preferred_theme if rng.random() > mutation_rate else rng.choice(get_data_manager().get_themes_list()),
            keywords=new_keywords,
            glyph_symbol=self.glyph_symbol,
            symbolic_color=new_color,
            symbolic_complexity=self._mutate_trait(self.symbolic_complexity, mutation_rate, rng, 0.1, 1.0),
            symbolic_symmetry=max(3, min(16, self.symbolic_symmetry + rng.randint(-1, 1))),
            symbolic_glitch=self._mutate_trait(self.symbolic_glitch, mutation_rate, rng, 0.0, 1.0),
            symbolic_entropy=self._mutate_trait(self.symbolic_entropy, mutation_rate, rng, 0.0, 1.0),
            narrative_fluency=self._mutate_trait(self.narrative_fluency, mutation_rate, rng, 0.5, 2.0),
            charisma=self._mutate_trait(self.charisma, mutation_rate, rng, 0.5, 2.0),
            memory_depth=self._mutate_trait(self.memory_depth, mutation_rate, rng, 0.5, 2.0),
            intelligence=self._mutate_trait(self.intelligence, mutation_rate, rng, 0.5, 2.0),
            skepticism=self._mutate_trait(self.skepticism, mutation_rate, rng, 0.3, 2.0),
            narrative_recovery=self._mutate_trait(self.narrative_recovery, mutation_rate, rng, 0.3, 2.0),
            dogma_risk=self._mutate_trait(self.dogma_risk, mutation_rate, rng, 0.2, 2.0),
            expressiveness=self._mutate_trait(self.expressiveness, mutation_rate, rng, 0.3, 2.5),
            silent_believer_prob=self._mutate_trait(self.silent_believer_prob, mutation_rate, rng, 0.0, 0.8),
            influence_potential=self._mutate_trait(self.influence_potential, mutation_rate, rng, 0.5, 3.0),
            curiosity=self._mutate_trait(self.curiosity, mutation_rate, rng, 0.0, 1.0),
            social_compliance=self._mutate_trait(self.social_compliance, mutation_rate, rng, 0.0, 1.0),
            mobility=self._mutate_trait(self.mobility, mutation_rate, rng, 0.1, 1.5),
            altruism=self._mutate_trait(self.altruism, mutation_rate, rng, 0.0, 1.0),
            guild_affinity=self.guild_affinity,
            creator=f"Mutated from {self.creator}",
        )

    def get_fingerprint(self) -> str:
        data = f"{self.species}{self.breed}{self.preferred_theme}{''.join(self.keywords)}"
        return hashlib.md5(data.encode()).hexdigest()[:8]

    def to_symbolic_dna(self, theme: str = None) -> SymbolicDNA:
        """Convertit le CulturalGenome en SymbolicDNA pour la forge."""
        return SymbolicDNA(
            theme=theme or self.preferred_theme,
            glyph_symbol=self.glyph_symbol,
            color=self.symbolic_color,
            scale=1.0,
            complexity=self.symbolic_complexity,
            symmetry=self.symbolic_symmetry,
            glitch_factor=self.symbolic_glitch,
            entropy_level=self.symbolic_entropy,
            keyword_sequence=self.keywords,
        )

# ═══════════════════════════════════════════════════════════════════════════════
# STATUTS, SOUCHES ET ÉVÉNEMENTS
# ═══════════════════════════════════════════════════════════════════════════════

class CulturalStatus(Enum):
    RECEPTIVE = "S"
    EXPOSED = "E"
    EVANGELIST = "I"
    SILENT_CARRIER = "A"
    DISENCHANTED = "R"
    OBLIVIOUS = "D"


@dataclass
class MemeStrain:
    strain_id: str
    parent_id: Optional[str]
    generation: int
    mutations: List[Tuple[str, float]]
    mantra: Mantra
    contagion_power: float
    dogma_intensity: float
    latency_period: float
    emergence_time: int
    # [NOUVEAU] Artefact symbolique attaché à la souche
    symbolic_artefact: Optional[SymbolicArtefact] = None

    @staticmethod
    def compute_virulence(mantra: Mantra, base: float = 1.0) -> float:
        comp = mantra.components
        style_bonus = (0.3 if comp.get("has_rhyme", False) else 0) + (0.2 if comp.get("has_alliteration", False) else 0)
        emotion_bonus = comp.get("emotion_score", 0) * 0.15
        oniric_bonus = 0.25 if comp.get("oniric_tag") else 0
        return base * (1 + style_bonus + emotion_bonus + oniric_bonus)


@dataclass
class NarrativeEvent:
    timestamp: int
    agent_id: int
    event_type: str
    cultural_state: str
    source_id: Optional[int] = None
    guild: Optional[str] = None
    narrative_coherence: Optional[float] = None
    strain_id: Optional[str] = None
    details: Optional[str] = None


@dataclass
class InteractionRecord:
    timestamp: int
    agent_a: int
    agent_b: int
    intensity: float
    transmission_risk: float
    transmission_occurred: bool = False


@dataclass
class CollectiveMemory:
    zone_history: Dict[str, List[Tuple[int, str, str]]] = field(default_factory=lambda: defaultdict(list))

    def record(self, zone: str, timestamp: int, strain_id: str, mantra_content: str):
        self.zone_history[zone].append((timestamp, strain_id, mantra_content))

    def get_dominant_strain(self, zone: str, timestamp: int) -> Optional[str]:
        if zone not in self.zone_history or not self.zone_history[zone]:
            return None
        recent = [s for t, s, _ in self.zone_history[zone] if t <= timestamp]
        if not recent:
            return None
        return Counter(recent).most_common(1)[0][0]


@dataclass
class Relic:
    relic_id: str
    mantra: Mantra
    guardian_id: int
    zone: str
    preserved_at: int
    veneration_count: int = 0
    symbolic_artefact: Optional[SymbolicArtefact] = None


@dataclass
class FoundingMyth:
    myth_id: str
    title: str
    verses: List[str]
    dominant_strains: List[str]
    created_at: int


@dataclass
class RandomEvent:
    event_id: str
    event_type: str
    timestamp: int
    zone: Optional[str]
    description: str
    affected_agents: List[int]
    impact: Dict[str, Any]


@dataclass
class Faction:
    faction_id: str
    name: str
    founder_id: int
    founding_strain: str
    created_at: int
    members: List[int] = field(default_factory=list)
    alliances: List[str] = field(default_factory=list)
    rituals: List[str] = field(default_factory=list)
    color: str = "#ff6b6b"
    symbolic_artefact: Optional[SymbolicArtefact] = None


@dataclass
class EpisodicMemory:
    agent_id: int
    events: List[Dict] = field(default_factory=list)
    max_size: int = 50

    def add_event(self, event_type: str, content: str, timestamp: int, impact: float = 1.0):
        self.events.append({
            'type': event_type, 'content': content, 'timestamp': timestamp, 'impact': impact
        })
        if len(self.events) > self.max_size:
            self.events.pop(0)

    def get_recent_events(self, n: int = 5) -> List[Dict]:
        return self.events[-n:]

    def get_impact_summary(self) -> Dict[str, float]:
        summary = defaultdict(float)
        for evt in self.events:
            summary[evt['type']] += evt['impact']
        return dict(summary)

# ═══════════════════════════════════════════════════════════════════════════════
# PHÉNOTYPE ET AGENT CULTUREL
# ═══════════════════════════════════════════════════════════════════════════════

class CulturalPhenotype:
    def __init__(self, genome: CulturalGenome):
        self.genome = genome
        self.phenotypes = {
            "receptivity": 1.0 / max(0.1, genome.skepticism),
            "contagiousness": genome.expressiveness * genome.influence_potential,
            "dogma_vulnerability": genome.dogma_risk,
            "interaction_rate": genome.mobility * genome.charisma * (1 - genome.curiosity * 0.3),
            "compliance": genome.social_compliance * (genome.intelligence / 1.5),
            "is_culture_influencer": genome.expressiveness * genome.influence_potential > 2.5,
            "disenchant_boost": genome.memory_depth * genome.narrative_recovery,
        }


class CulturalAgent:
    _id_counter = 0

    def __init__(self, zone: str, genome: CulturalGenome, rng: random.Random, root_strain: MemeStrain):
        CulturalAgent._id_counter += 1
        self.id = CulturalAgent._id_counter
        self.rng = rng
        self.zone = zone
        self.genome = genome
        self.phenotype = CulturalPhenotype(genome)
        self.cultural_status = CulturalStatus.RECEPTIVE
        self.exposure_time: Optional[int] = None
        self.evangelist_start: Optional[int] = None
        self.disenchant_time: Optional[int] = None
        self.current_strain: MemeStrain = root_strain
        self.is_silent_carrier = False
        self.narrative_coherence: float = 0.5
        self.meme_virulence: float = 0.0
        self.receptivity: float = self.phenotype.phenotypes["receptivity"]
        self.personal_mantra: Optional[Mantra] = None
        self.guild = genome.get_guild(rng)
        self.social_network: set = set()
        self.current_t = 0
        self.infection_time: Optional[int] = None
        self.mantra_history: List[Tuple[int, str]] = []
        self.influence_score: float = 0.0
        self.is_relic_guardian: bool = False
        self.relic_id: Optional[str] = None
        self.episodic_memory = EpisodicMemory(self.id)
        self.faction_id: Optional[str] = None
        self.narrative_position = {'x': rng.random() * 100, 'y': rng.random() * 100}

        # [NOUVEAU] Artefact symbolique personnel
        self.symbolic_artefact: Optional[SymbolicArtefact] = None
        self.symbolic_dna: Optional[SymbolicDNA] = None

        # Générer un artefact initial basé sur le genome
        self._generate_personal_artefact()

    def _generate_personal_artefact(self):
        """Génère l'artefact symbolique initial de l'agent."""
        dna = self.genome.to_symbolic_dna()
        transcriptor = SymbolicTranscriptor()
        self.symbolic_dna = dna
        self.symbolic_artefact = transcriptor.transcribe_artefact(dna)
        score, breakdown = evaluate_artefact(self.symbolic_artefact, dna)
        self.symbolic_artefact.aesthetic_score = score
        self.symbolic_artefact.fitness_breakdown = breakdown
        dna.aesthetic_fitness = score

    def receive_mantra(self, strain: MemeStrain):
        self.current_strain = strain
        self.personal_mantra = strain.mantra
        self.meme_virulence = MemeStrain.compute_virulence(strain.mantra, base=strain.contagion_power)
        self.narrative_coherence = min(1.0, 0.4 + strain.mantra.fitness * 0.5)
        self.mantra_history.append((self.current_t, strain.strain_id))

        # [NOUVEAU] Hériter ou muter l'artefact symbolique de la souche
        if strain.symbolic_artefact is not None:
            # Mutation de l'artefact de la souche pour l'agent
            engine = SymbolicEvolutionEngine(theme=strain.symbolic_artefact.theme)
            new_artefact, new_dna = engine.quick_mutate(strain.symbolic_artefact.symbolic_dna)
            self.symbolic_artefact = new_artefact
            self.symbolic_dna = new_dna

        self.narrative_position['x'] += self.rng.gauss(0, 0.5)
        self.narrative_position['y'] += self.rng.gauss(0, 0.5)

        logger.debug(f"Agent#{self.id} reçoit mantra {strain.strain_id}: «{strain.mantra.content[:50]}...»")

    def is_culture_influencer(self) -> bool:
        return self.phenotype.phenotypes["is_culture_influencer"]

    def add_memory_event(self, event_type: str, content: str, impact: float = 1.0):
        self.episodic_memory.add_event(event_type, content, self.current_t, impact)

    def get_aesthetic_boost(self) -> float:
        """Bonus de réceptivité basé sur la beauté de l'artefact."""
        if self.symbolic_artefact is None:
            return 0.0
        return self.symbolic_artefact.aesthetic_score * 0.3


# ═══════════════════════════════════════════════════════════════════════════════
# RÉSONANCE ESTHÉTIQUE — Gravité narrative enrichie
# ═══════════════════════════════════════════════════════════════════════════════

class SymbolicResonance:
    """
    Système de résonance esthétique : les artefacts symboliques attirent
    les agents partageant des affinités visuelles, émotionnelles et sémantiques.
    """

    def __init__(self, sim: 'CulturalEpidemicSimulation'):
        self.sim = sim
        self.resonance_centers: Dict[str, Dict] = {}
        self._initialize_centers()

    def _initialize_centers(self):
        for strain_id, strain in self.sim.meme_strains.items():
            carriers = sum(1 for a in self.sim.agents 
                          if a.current_strain.strain_id == strain_id 
                          and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))
            mass = 1.0 + (carriers / max(1, len(self.sim.agents))) * 5.0
            influence_radius = 1.0 + (carriers / max(1, len(self.sim.agents))) * 3.0
            self.resonance_centers[strain_id] = {
                'mass': mass, 'influence_radius': influence_radius,
                'position': {'x': random.random() * 100, 'y': random.random() * 100}
            }

    def compute_resonance(self, agent: CulturalAgent, strain_id: str) -> float:
        if strain_id not in self.resonance_centers:
            return 0.0

        center = self.resonance_centers[strain_id]
        strain = self.sim.meme_strains.get(strain_id)
        if not strain or not strain.symbolic_artefact:
            return 0.0

        # 1. Affinité esthétique (couleur, glyphe)
        aesthetic_affinity = self._compute_aesthetic_affinity(agent, strain)

        # 2. Affinité émotionnelle
        emotional_affinity = self._compute_emotional_affinity(agent, strain)

        # 3. Affinité sémantique
        semantic_overlap = self._compute_semantic_overlap(agent, strain_id)

        # 4. Proximité sociale
        social_proximity = self._compute_social_proximity(agent, strain_id)

        # Combinaison pondérée
        resonance = (
            aesthetic_affinity * 0.35 +
            emotional_affinity * 0.25 +
            semantic_overlap * 0.25 +
            social_proximity * 0.15
        )

        mass_effect = center['mass'] * resonance
        distance_effect = 1.0 / (1.0 + social_proximity)
        coherence_boost = 1.0 + agent.narrative_coherence * 0.5

        return mass_effect * distance_effect * coherence_boost

    def _compute_aesthetic_affinity(self, agent: CulturalAgent, strain: MemeStrain) -> float:
        """Calcule l'affinité esthétique entre l'agent et une souche."""
        if not agent.symbolic_artefact or not strain.symbolic_artefact:
            return 0.1

        agent_dna = agent.symbolic_artefact.symbolic_dna
        strain_dna = strain.symbolic_artefact.symbolic_dna

        # Similarité de couleur (distance HSL)
        color_sim = self._color_similarity(agent_dna.color, strain_dna.color)

        # Similarité de glyphe (même symbole ou affinité sémantique)
        glyph_sim = 1.0 if agent_dna.glyph_symbol == strain_dna.glyph_symbol else 0.3

        # Similarité de complexité
        comp_sim = 1.0 - abs(agent_dna.complexity - strain_dna.complexity)

        # Similarité de fitness esthétique
        fitness_sim = 1.0 - abs(agent_dna.aesthetic_fitness - strain_dna.aesthetic_fitness)

        return (color_sim * 0.4 + glyph_sim * 0.3 + comp_sim * 0.15 + fitness_sim * 0.15)

    def _color_similarity(self, hex1: str, hex2: str) -> float:
        """Calcule la similarité entre deux couleurs hex."""
        try:
            r1, g1, b1 = int(hex1[1:3], 16)/255, int(hex1[3:5], 16)/255, int(hex1[5:7], 16)/255
            r2, g2, b2 = int(hex2[1:3], 16)/255, int(hex2[3:5], 16)/255, int(hex2[5:7], 16)/255
            h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
            h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)

            h_diff = min(abs(h1 - h2), 1.0 - abs(h1 - h2))
            l_diff = abs(l1 - l2)
            s_diff = abs(s1 - s2)

            return max(0.0, 1.0 - (h_diff * 2 + l_diff + s_diff) / 3)
        except:
            return 0.5

    def _compute_emotional_affinity(self, agent: CulturalAgent, strain: MemeStrain) -> float:
        """Calcule l'affinité émotionnelle."""
        if not agent.symbolic_artefact or not strain.symbolic_artefact:
            return 0.1

        agent_vec = agent.symbolic_artefact.symbolic_dna.emotion_vector
        strain_vec = strain.symbolic_artefact.symbolic_dna.emotion_vector

        # Distance euclidienne inverse
        emotions = set(agent_vec.keys()) | set(strain_vec.keys())
        if not emotions:
            return 0.1

        sq_diff = sum((agent_vec.get(e, 0) - strain_vec.get(e, 0)) ** 2 for e in emotions)
        distance = math.sqrt(sq_diff)
        return max(0.0, 1.0 - distance)

    def _compute_semantic_overlap(self, agent: CulturalAgent, strain_id: str) -> float:
        strain = self.sim.meme_strains.get(strain_id)
        if not strain or not agent.personal_mantra:
            return 0.1
        agent_words = set(agent.personal_mantra.content.lower().split())
        strain_words = set(strain.mantra.content.lower().split())
        intersection = len(agent_words & strain_words)
        union = len(agent_words | strain_words)
        if union == 0:
            return 0.1
        return 0.5 + 0.5 * (intersection / union)

    def _compute_social_proximity(self, agent: CulturalAgent, strain_id: str) -> float:
        carriers = [a for a in self.sim.agents 
                   if a.current_strain.strain_id == strain_id 
                   and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        if not carriers:
            return 1.0
        if HAS_NX:
            try:
                path_length = nx.shortest_path_length(
                    self.sim.transmission_network, source=agent.id, target=carriers[0].id
                )
                return 1.0 / (1.0 + path_length)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                pass
        guild_similarity = sum(1 for c in carriers if c.guild == agent.guild) / max(1, len(carriers))
        return 0.5 + 0.5 * guild_similarity

    def apply_resonance(self, agent: CulturalAgent) -> Optional[str]:
        if agent.cultural_status != CulturalStatus.RECEPTIVE:
            return None

        attractions = {}
        for strain_id in self.resonance_centers:
            resonance = self.compute_resonance(agent, strain_id)
            if resonance > 0.5:
                attractions[strain_id] = resonance

        if not attractions:
            return None

        total = sum(attractions.values())
        if total == 0:
            return None

        strain_ids = list(attractions.keys())
        weights = [attractions[s] / total for s in strain_ids]
        selected = random.choices(strain_ids, weights=weights, k=1)[0]
        return selected

# ═══════════════════════════════════════════════════════════════════════════════
# FACTIONS ET SYSTÈMES ANNEXES
# ═══════════════════════════════════════════════════════════════════════════════

class FactionSystem:
    def __init__(self, sim: 'CulturalEpidemicSimulation'):
        self.sim = sim
        self.factions: Dict[str, Faction] = {}
        self.faction_counter = 0
        self.colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#ff6bff",
                      "#ff9f43", "#00d2d3", "#54a0ff", "#ff6348", "#a29bfe"]

    def faction_emergence_threshold(self) -> float:
        n_carriers = sum(1 for a in self.sim.agents 
                        if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))
        threshold = max(3, int(n_carriers * 0.1))
        return max(3, threshold)

    def check_emergence(self):
        strain_groups = defaultdict(list)
        for agent in self.sim.agents:
            if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                if agent.current_strain:
                    strain_groups[agent.current_strain.strain_id].append(agent.id)

        threshold = self.faction_emergence_threshold()

        for strain_id, members in strain_groups.items():
            if len(members) >= threshold and strain_id not in [f.founding_strain for f in self.factions.values()]:
                existing_members = set()
                for faction in self.factions.values():
                    existing_members.update(faction.members)
                new_members = [m for m in members if m not in existing_members]
                if len(new_members) >= max(3, threshold // 2):
                    self._create_faction(strain_id, new_members)

    def _create_faction(self, strain_id: str, members: List[int]):
        self.faction_counter += 1
        strain = self.sim.meme_strains.get(strain_id)

        if strain and strain.symbolic_artefact:
            name = strain.symbolic_artefact.mantra_text[:30].strip()
            color = strain.symbolic_artefact.symbolic_dna.color if strain.symbolic_artefact.symbolic_dna else self.colors[self.faction_counter % len(self.colors)]
        else:
            words = strain.mantra.content.lower().split() if strain else ["Faction"]
            name = " ".join(words[:3]).title() if words else f"Faction-{self.faction_counter}"
            color = self.colors[self.faction_counter % len(self.colors)]

        faction = Faction(
            faction_id=f"FAC-{self.faction_counter:03d}",
            name=name,
            founder_id=members[0],
            founding_strain=strain_id,
            created_at=self.sim.current_t,
            members=members[:],
            color=color,
            rituals=self._generate_rituals(strain_id),
            symbolic_artefact=strain.symbolic_artefact if strain else None,
        )

        self.factions[faction.faction_id] = faction

        self.sim.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.sim.event_counter:03d}",
            event_type="faction_emergence",
            timestamp=self.sim.current_t,
            zone=self.sim.rng.choice(self.sim.zones),
            description=f"🏛 ÉMERGENCE DE FACTION : {name} dans la zone {self.sim.rng.choice(self.sim.zones)}",
            affected_agents=members[:10],
            impact={"faction_id": faction.faction_id, "strain": strain_id, "members": len(members)}
        )
        self.sim.random_events.append(event)
        self.sim.chronicle.append({"t": self.sim.current_t, "type": "faction_emergence", "faction_id": faction.faction_id})
        logger.info(f"🏛 Nouvelle faction : {name} ({len(members)} membres)")

    def _generate_rituals(self, strain_id: str) -> List[str]:
        strain = self.sim.meme_strains.get(strain_id)
        if not strain:
            return ["Le rituel du silence"]
        rituals = []
        for _ in range(2):
            words = strain.mantra.content.split()
            if words:
                ritual = " ".join(words[:min(5, len(words))]) + "..."
                rituals.append(ritual)
            else:
                rituals.append(f"Rituel de {strain.mantra.theme}")
        return rituals

    def update_alliances(self):
        factions_list = list(self.factions.values())
        for i in range(len(factions_list)):
            for j in range(i + 1, len(factions_list)):
                f1, f2 = factions_list[i], factions_list[j]
                strain1 = self.sim.meme_strains.get(f1.founding_strain)
                strain2 = self.sim.meme_strains.get(f2.founding_strain)

                if strain1 and strain2 and strain1.symbolic_artefact and strain2.symbolic_artefact:
                    # Similarité esthétique entre les artefacts des factions
                    color_sim = SymbolicResonance(self.sim)._color_similarity(
                        strain1.symbolic_artefact.symbolic_dna.color,
                        strain2.symbolic_artefact.symbolic_dna.color
                    )
                    overlap = color_sim
                else:
                    words1 = set(strain1.mantra.content.lower().split()) if strain1 else set()
                    words2 = set(strain2.mantra.content.lower().split()) if strain2 else set()
                    overlap = len(words1 & words2) / max(1, len(words1 | words2))

                if overlap > 0.3 and f2.faction_id not in f1.alliances:
                    f1.alliances.append(f2.faction_id)
                    f2.alliances.append(f1.faction_id)


# ═══════════════════════════════════════════════════════════════════════════════
# SIMULATION ÉPIDÉMIQUE CULTURELLE — Cœur de la Chimère
# ═══════════════════════════════════════════════════════════════════════════════

class CulturalEpidemicSimulation:
    def __init__(self, params: dict, genome_pool: Optional[List[CulturalGenome]] = None,
                 data_dir: Optional[str] = None):
        if data_dir:
            self.data_manager = FusionDataManager(data_dir)
            set_data_manager(self.data_manager)
        else:
            self.data_manager = get_data_manager()
            set_data_manager(self.data_manager)

        self.params = params
        self.rng = random.Random(params.get("seed", 42))
        self.current_t = 0
        self.zones = self._generate_zones()

        # --- Souche-racine avec artefact symbolique ---
        root_theme = params.get("root_theme", "rituel")

        # Générer l'artefact racine via la forge
        forge = SymbolicEvolutionEngine(theme=root_theme)
        root_artefact, root_dna = forge.evolve_artefact(generations=params.get("symbolic_generations", 3))

        ga = SoufiMantraGA(theme=root_theme, rng=self.rng)
        ga.initialize_population()
        ga.evolve()
        root_mantra = ga.get_best_mantra()

        self.root_strain = MemeStrain(
            strain_id="M-001", parent_id=None, generation=0, mutations=[],
            mantra=root_mantra,
            contagion_power=params.get("r0_base", 2.2) / 2.5,
            dogma_intensity=params.get("dogma_rate", 0.01) * 100,
            latency_period=params.get("latency_period", 3),
            emergence_time=0,
            symbolic_artefact=root_artefact,
        )
        self.meme_strains: Dict[str, MemeStrain] = {"M-001": self.root_strain}
        self.strain_counter = 1

        self.agents: List[CulturalAgent] = []
        self.events: List[NarrativeEvent] = []
        self.interactions: List[InteractionRecord] = []
        self.random_events: List[RandomEvent] = []
        self.relics: List[Relic] = []
        self.founding_myths: List[FoundingMyth] = []
        self.chronicle: List[Dict] = []
        self.relic_counter = 0
        self.myth_counter = 0
        self.event_counter = 0

        self.transmission_network = nx.DiGraph() if HAS_NX else _MiniDiGraph()
        self.daily_metrics = defaultdict(lambda: defaultdict(int))
        self.rt_history: List[float] = []
        self.serial_intervals: List[int] = []
        self.zone_agent_index: Dict[str, List[CulturalAgent]] = defaultdict(list)

        self.collective_memory = CollectiveMemory()
        self.semantic_drift: Dict[str, List[str]] = defaultdict(list)

        # [NOUVEAU] Résonance esthétique
        self.symbolic_resonance = SymbolicResonance(self)

        # Factions
        self.faction_system = FactionSystem(self)

        # Historique pour CSV
        self.agent_state_history: List[Dict] = []
        self.strain_history: List[Dict] = []

        # [NOUVEAU] Historique des artefacts
        self.artefact_history: List[Dict] = []

        self._init_population(genome_pool)
        logger.info(f"Simulation initialisée : {len(self.agents)} agents sur {len(self.zones)} zones")
        logger.debug(f"Souche racine : {self.root_strain.strain_id} — Artefact: {root_artefact.mantra_text[:40]}...")

    def _generate_zones(self) -> List[str]:
        zones = ["Agora_Centrale", "Marché_Souterrain", "Forum_Diffus",
                 "Sanctuaire_Reclus", "Carrefour_Nomade", "Archives_Oubliées",
                 "Bibliothèque_Silencieuse", "Place_des_Rêves", "Fractale_Mémoire"]
        return zones[:self.params.get("nb_zones", 6)]

    def _init_population(self, genome_pool: Optional[List[CulturalGenome]] = None):
        CulturalAgent._id_counter = 0
        pop_total = self.params.get("pop_total", 200)
        if genome_pool:
            genomes = (genome_pool * (pop_total // len(genome_pool) + 1))[:pop_total]
        else:
            genomes = [CulturalGenome() for _ in range(pop_total)]

        for i, genome in enumerate(genomes):
            zone = self.rng.choice(self.zones)
            agent = CulturalAgent(zone, genome, self.rng, self.root_strain)
            agent.current_t = self.current_t
            if i < self.params.get("initial_believers", 3):
                self._expose_agent(agent, None, self.root_strain, force=True)
            self.agents.append(agent)
            self.zone_agent_index[zone].append(agent)
        self._build_social_network()

    def _build_social_network(self):
        n = len(self.agents)
        k, p = 6, 0.3
        for i, agent in enumerate(self.agents):
            for j in range(1, k // 2 + 1):
                neighbor_idx = (i + j) % n
                if self.rng.random() > p:
                    agent.social_network.add(self.agents[neighbor_idx].id)
                else:
                    agent.social_network.add(self.rng.choice(self.agents).id)

    def _expose_agent(self, agent: CulturalAgent, source: Optional[CulturalAgent],
                      strain: MemeStrain, force: bool = False) -> bool:
        if agent.cultural_status != CulturalStatus.RECEPTIVE and not force:
            return False
        agent.cultural_status = CulturalStatus.EXPOSED
        agent.exposure_time = self.current_t
        agent.receive_mantra(strain)
        agent.evangelist_start = self.current_t + max(1, int(self.rng.gauss(strain.latency_period, 1)))
        agent.is_silent_carrier = self.rng.random() < agent.genome.silent_believer_prob

        self.events.append(NarrativeEvent(
            timestamp=self.current_t, agent_id=agent.id, event_type="exposure",
            cultural_state="E", source_id=source.id if source else None,
            guild=agent.guild, narrative_coherence=agent.narrative_coherence,
            strain_id=strain.strain_id,
        ))
        self.collective_memory.record(agent.zone, self.current_t, strain.strain_id, strain.mantra.content)

        if source:
            self.transmission_network.add_edge(source.id, agent.id, time=self.current_t, strain=strain.strain_id)
            source.influence_score += 1.0
            if source.infection_time is not None:
                self.serial_intervals.append(self.current_t - source.infection_time)
        return True

    def _progress_narrative(self, agent: CulturalAgent):
        if agent.cultural_status == CulturalStatus.EXPOSED:
            if self.current_t >= agent.evangelist_start:
                agent.cultural_status = (CulturalStatus.SILENT_CARRIER if agent.is_silent_carrier
                                         else CulturalStatus.EVANGELIST)
                agent.infection_time = self.current_t
                logger.debug(f"t={self.current_t} Agent#{agent.id} devient {'porteur silencieux' if agent.is_silent_carrier else 'évangéliste'}")
        elif agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
            disenchant_prob = self.params.get("disenchant_rate", 0.05) * agent.phenotype.phenotypes["disenchant_boost"]
            if self.rng.random() < disenchant_prob:
                agent.cultural_status = CulturalStatus.DISENCHANTED
                agent.disenchant_time = self.current_t
                self.events.append(NarrativeEvent(
                    self.current_t, agent.id, "disenchantment", "R", guild=agent.guild,
                    narrative_coherence=agent.narrative_coherence, strain_id=agent.current_strain.strain_id,
                ))
                agent.add_memory_event("disenchantment", f"Désenchantement à t={self.current_t}", impact=0.7)
                logger.debug(f"t={self.current_t} Agent#{agent.id} se désenchante")
                return

        if agent.cultural_status == CulturalStatus.EVANGELIST:
            oblivion_risk = self.params.get("oblivion_rate", 0.004)
            oblivion_risk *= agent.genome.dogma_risk * agent.current_strain.dogma_intensity / 100
            if self.rng.random() < oblivion_risk:
                agent.cultural_status = CulturalStatus.OBLIVIOUS
                self.events.append(NarrativeEvent(
                    self.current_t, agent.id, "burnout", "D", guild=agent.guild,
                    strain_id=agent.current_strain.strain_id,
                ))
                agent.add_memory_event("burnout", f"Burnout narratif à t={self.current_t}", impact=0.9)
                logger.debug(f"t={self.current_t} Agent#{agent.id} sombre dans l'oubli")

    def transmit_meme(self, agent_a: CulturalAgent, agent_b: CulturalAgent) -> bool:
        if agent_a.cultural_status not in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
            return False
        if agent_b.cultural_status != CulturalStatus.RECEPTIVE:
            return False

        virulence = agent_a.meme_virulence * agent_a.phenotype.phenotypes["contagiousness"]
        if agent_a.cultural_status == CulturalStatus.SILENT_CARRIER:
            virulence *= 0.4

        # [NOUVEAU] Bonus esthétique à la transmission
        aesthetic_boost = agent_a.get_aesthetic_boost()
        virulence *= (1.0 + aesthetic_boost)

        p_transmission = min(0.95, 0.12 * virulence * agent_b.receptivity)
        occurred = self.rng.random() < p_transmission

        self.interactions.append(InteractionRecord(
            timestamp=self.current_t, agent_a=agent_a.id, agent_b=agent_b.id,
            intensity=virulence, transmission_risk=p_transmission, transmission_occurred=occurred,
        ))
        if occurred:
            self._expose_agent(agent_b, agent_a, agent_a.current_strain)
            agent_b.add_memory_event("infection", f"Infecté par Agent#{agent_a.id}", impact=0.6)
            logger.debug(f"t={self.current_t} Transmission : Agent#{agent_a.id} → Agent#{agent_b.id}")
        return occurred

    def _run_interaction_round(self):
        carriers = [a for a in self.agents if a.cultural_status in
                    (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        for carrier in carriers:
            n_targets = max(1, int(carrier.phenotype.phenotypes["interaction_rate"] * 3))
            targets = self.rng.sample(list(carrier.social_network), k=min(n_targets, len(carrier.social_network)))                 if carrier.social_network else []
            for target_id in targets:
                target = self._agent_by_id(target_id)
                if target is not None:
                    self.transmit_meme(carrier, target)

    def _agent_by_id(self, agent_id: int) -> Optional[CulturalAgent]:
        if not hasattr(self, "_agent_lookup"):
            self._agent_lookup = {a.id: a for a in self.agents}
        return self._agent_lookup.get(agent_id)

    def mutate_meme(self):
        if self.rng.random() >= self.params.get("mutation_prob", 0.01):
            return
        carriers = [a for a in self.agents if a.cultural_status in
                    (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        if not carriers:
            return

        agent = self.rng.choice(carriers)
        parent = agent.current_strain
        self.strain_counter += 1

        # [NOUVEAU] Mutation via la forge symbolique
        if parent.symbolic_artefact is not None and self.params.get("symbolic_evolution", True):
            forge = SymbolicEvolutionEngine(theme=parent.mantra.theme)
            new_artefact, new_dna = forge.quick_mutate(parent.symbolic_artefact.symbolic_dna)
            mutated_text = new_artefact.mantra_text
            theme = new_artefact.theme
        else:
            mutated_text = mutate_mantra_text(parent.mantra.content, self.rng)
            theme = parent.mantra.theme

        new_mantra = Mantra(id=f"MUT{self.strain_counter}", content=mutated_text, theme=theme)
        new_strain = MemeStrain(
            strain_id=f"MV-{self.strain_counter:03d}",
            parent_id=parent.strain_id,
            generation=parent.generation + 1,
            mutations=parent.mutations + [(f"symbolic_mutation_t{self.current_t}", self.rng.gauss(0, 0.1))],
            mantra=new_mantra,
            contagion_power=MemeStrain.compute_virulence(new_mantra, base=parent.contagion_power),
            dogma_intensity=parent.dogma_intensity * self.rng.lognormvariate(0, 0.08),
            latency_period=max(1.0, parent.latency_period * self.rng.lognormvariate(0, 0.1)),
            emergence_time=self.current_t,
            symbolic_artefact=new_artefact if 'new_artefact' in dir() else None,
        )

        # Si la forge n'a pas été utilisée, créer un artefact basique
        if new_strain.symbolic_artefact is None:
            dna = SymbolicDNA(theme=theme)
            transcriptor = SymbolicTranscriptor()
            new_strain.symbolic_artefact = transcriptor.transcribe_artefact(dna)

        self.meme_strains[new_strain.strain_id] = new_strain
        agent.receive_mantra(new_strain)
        self.semantic_drift[parent.strain_id].append(new_strain.strain_id)
        agent.add_memory_event("mutation", f"Mutation: {parent.strain_id} → {new_strain.strain_id}", impact=0.4)
        logger.info(f"t={self.current_t} 🧬 MUTATION SYMBOLIQUE : {parent.strain_id} → {new_strain.strain_id}")

    def _apply_symbolic_resonance(self):
        for agent in self.agents:
            if agent.cultural_status == CulturalStatus.RECEPTIVE:
                attracted_to = self.symbolic_resonance.apply_resonance(agent)
                if attracted_to and attracted_to in self.meme_strains:
                    strain = self.meme_strains[attracted_to]
                    if self._expose_agent(agent, None, strain, force=True):
                        agent.add_memory_event("resonance_attraction",
                            f"Attiré par la résonance de {attracted_to}", impact=0.5)
                        logger.debug(f"✨ Résonance esthétique : Agent#{agent.id} attiré par {attracted_to}")

    def _update_factions(self):
        self.faction_system.check_emergence()
        self.faction_system.update_alliances()
        for faction in self.faction_system.factions.values():
            for member_id in faction.members:
                agent = self._agent_by_id(member_id)
                if agent:
                    agent.faction_id = faction.faction_id

    def _apply_narrative_cycle(self):
        if self.current_t % 10 != 0:
            return
        cycle_type = self.rng.choice(["expansion", "contraction", "transformation", "silence"])

        if cycle_type == "expansion":
            for agent in self.agents:
                if agent.cultural_status == CulturalStatus.RECEPTIVE:
                    agent.receptivity *= 1.1
                    agent.add_memory_event("cycle_expansion", "Saison d'expansion narrative", impact=0.3)
            logger.info(f"🌱 Cycle d'expansion narrative (t={self.current_t})")
        elif cycle_type == "contraction":
            for agent in self.agents:
                if agent.cultural_status in (CulturalStatus.RECEPTIVE, CulturalStatus.EXPOSED):
                    agent.receptivity *= 0.9
                    agent.add_memory_event("cycle_contraction", "Saison de contraction narrative", impact=0.3)
            logger.info(f"🌿 Cycle de contraction narrative (t={self.current_t})")
        elif cycle_type == "transformation":
            mutation_bonus = self.params.get("mutation_prob", 0.02) * 3
            if self.rng.random() < mutation_bonus:
                self.mutate_meme()
                for agent in self.rng.sample(self.agents, k=min(3, len(self.agents) // 10)):
                    if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                        agent.add_memory_event("cycle_transformation", "Saison de transformation narrative", impact=0.5)
            logger.info(f"🔄 Cycle de transformation narrative (t={self.current_t})")
        elif cycle_type == "silence":
            for agent in self.agents:
                if agent.cultural_status == CulturalStatus.EVANGELIST:
                    agent.meme_virulence *= 0.8
                    agent.add_memory_event("cycle_silence", "Saison de silence narratif", impact=0.2)
            logger.info(f"🤫 Cycle de silence narrative (t={self.current_t})")

    def _trigger_narrative_eclipse(self):
        active_strains = [s for s in self.meme_strains.values() 
                         if any(a.current_strain.strain_id == s.strain_id 
                               for a in self.agents 
                               if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))]
        if len(active_strains) < 2:
            return

        strain_counts = Counter(
            a.current_strain.strain_id for a in self.agents
            if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
        )
        if not strain_counts:
            return

        least_popular = min(strain_counts.items(), key=lambda x: x[1])[0]
        if least_popular not in self.meme_strains:
            return

        affected = []
        for agent in self.agents:
            if agent.current_strain.strain_id == least_popular:
                if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                    agent.cultural_status = CulturalStatus.DISENCHANTED
                    agent.disenchant_time = self.current_t
                    affected.append(agent.id)
                    agent.add_memory_event("narrative_eclipse", f"La souche {least_popular} s'efface", impact=0.8)
                elif agent.cultural_status == CulturalStatus.RECEPTIVE:
                    agent.current_strain = self.root_strain
                    agent.receptivity *= 0.9

        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="narrative_eclipse",
            timestamp=self.current_t,
            zone=self.rng.choice(self.zones),
            description=f"🌑 ÉCLIPSE NARRATIVE : La souche {least_popular} s'efface de la mémoire collective",
            affected_agents=affected,
            impact={"strain": least_popular, "affected": len(affected)}
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "narrative_eclipse", "strain": least_popular})
        logger.warning(f"🌑 Éclipse narrative : {least_popular} s'efface ({len(affected)} agents affectés)")

    def _trigger_cultural_resonance(self):
        active_strains = [s for s in self.meme_strains.values() 
                         if any(a.current_strain.strain_id == s.strain_id 
                               for a in self.agents 
                               if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))]
        if len(active_strains) < 2:
            return

        strain1, strain2 = self.rng.sample(active_strains, 2)

        # Fusion des artefacts symboliques
        if strain1.symbolic_artefact and strain2.symbolic_artefact:
            fusion_text = f"{strain1.symbolic_artefact.mantra_text} ∪ {strain2.symbolic_artefact.mantra_text}"
            fusion_dna = strain1.symbolic_artefact.symbolic_dna.copy() if strain1.symbolic_artefact.symbolic_dna else SymbolicDNA()
            fusion_dna.glyph_symbol = strain2.symbolic_artefact.symbolic_dna.glyph_symbol if strain2.symbolic_artefact.symbolic_dna else fusion_dna.glyph_symbol
            fusion_dna.color = self._blend_colors(
                strain1.symbolic_artefact.symbolic_dna.color if strain1.symbolic_artefact.symbolic_dna else "#ffffff",
                strain2.symbolic_artefact.symbolic_dna.color if strain2.symbolic_artefact.symbolic_dna else "#ffffff"
            )
            transcriptor = SymbolicTranscriptor()
            fusion_artefact = transcriptor.transcribe_artefact(fusion_dna)
            fusion_artefact.mantra_text = fusion_text[:200]
        else:
            fusion_text = f"{strain1.mantra.content} ∪ {strain2.mantra.content}"
            fusion_artefact = None

        fusion_mantra = Mantra(
            id=f"FUS-{self.strain_counter + 1}",
            content=fusion_text[:200],
            theme=strain1.mantra.theme
        )

        self.strain_counter += 1
        fusion_strain = MemeStrain(
            strain_id=f"FS-{self.strain_counter:03d}",
            parent_id=f"{strain1.strain_id}+{strain2.strain_id}",
            generation=max(strain1.generation, strain2.generation) + 1,
            mutations=strain1.mutations + strain2.mutations + [("resonance", 0.5)],
            mantra=fusion_mantra,
            contagion_power=(strain1.contagion_power + strain2.contagion_power) / 2 * 1.2,
            dogma_intensity=(strain1.dogma_intensity + strain2.dogma_intensity) / 2,
            latency_period=(strain1.latency_period + strain2.latency_period) / 2,
            emergence_time=self.current_t,
            symbolic_artefact=fusion_artefact,
        )
        self.meme_strains[fusion_strain.strain_id] = fusion_strain

        affected = []
        for agent in self.agents:
            if agent.current_strain.strain_id in (strain1.strain_id, strain2.strain_id):
                if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                    agent.receive_mantra(fusion_strain)
                    affected.append(agent.id)
                    agent.add_memory_event("cultural_resonance",
                        f"Résonance culturelle : fusion de {strain1.strain_id} et {strain2.strain_id}", impact=0.6)

        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="cultural_resonance",
            timestamp=self.current_t,
            zone=self.rng.choice(self.zones),
            description=f"🎵 RÉSONANCE CULTURELLE : {strain1.strain_id} ∪ {strain2.strain_id} → {fusion_strain.strain_id}",
            affected_agents=affected,
            impact={"parent1": strain1.strain_id, "parent2": strain2.strain_id, "child": fusion_strain.strain_id}
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "cultural_resonance", "strain": fusion_strain.strain_id})
        logger.info(f"🎵 Résonance culturelle : fusion de {strain1.strain_id} et {strain2.strain_id}")

    @staticmethod
    def _blend_colors(hex1: str, hex2: str) -> str:
        """Mélange deux couleurs hex."""
        try:
            r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
            r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
            return f"#{(r1+r2)//2:02x}{(g1+g2)//2:02x}{(b1+b2)//2:02x}"
        except:
            return "#888888"

    def _maybe_trigger_random_event(self):
        event_prob = self.params.get("random_event_prob", 0.03)
        if self.rng.random() >= event_prob:
            return
        # Simplifié pour la lisibilité
        pass

    def _maybe_generate_myth(self):
        if self.current_t % self.params.get("myth_generation_period", 20) != 0:
            return
        if len(self.founding_myths) >= self.params.get("max_myths", 3):
            return

        believer_strains = Counter(
            a.current_strain.strain_id for a in self.agents
            if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
        ).most_common(3)

        if len(believer_strains) < 2:
            return

        verses = []
        dominant_ids = []
        for strain_id, _ in believer_strains:
            strain = self.meme_strains[strain_id]
            verses.append(strain.mantra.content)
            dominant_ids.append(strain_id)

        self.myth_counter += 1
        myth = FoundingMyth(
            myth_id=f"MYTH-{self.myth_counter:03d}",
            title=f"Mythe de la Convergence #{self.myth_counter}",
            verses=verses,
            dominant_strains=dominant_ids,
            created_at=self.current_t,
        )
        self.founding_myths.append(myth)
        self.chronicle.append({"t": self.current_t, "type": "myth", "myth_id": myth.myth_id})
        logger.info(f"t={self.current_t} 📖 MYTHE FONDATEUR créé : {myth.myth_id}")

    def _capture_agent_state(self):
        for agent in self.agents:
            entry = {
                "timestamp": self.current_t,
                "agent_id": agent.id,
                "zone": agent.zone,
                "guild": agent.guild,
                "status": agent.cultural_status.name,
                "status_code": agent.cultural_status.value,
                "strain_id": agent.current_strain.strain_id,
                "is_silent_carrier": 1 if agent.is_silent_carrier else 0,
                "narrative_coherence": agent.narrative_coherence,
                "meme_virulence": agent.meme_virulence,
                "receptivity": agent.receptivity,
                "influence_score": agent.influence_score,
                "is_relic_guardian": 1 if agent.is_relic_guardian else 0,
                "relic_id": agent.relic_id or "",
                "exposure_time": agent.exposure_time or -1,
                "evangelist_start": agent.evangelist_start or -1,
                "disenchant_time": agent.disenchant_time or -1,
                "infection_time": agent.infection_time or -1,
                "glyph_symbol": agent.genome.glyph_symbol,
                "narrative_fluency": agent.genome.narrative_fluency,
                "charisma": agent.genome.charisma,
                "memory_depth": agent.genome.memory_depth,
                "intelligence": agent.genome.intelligence,
                "skepticism": agent.genome.skepticism,
                "dogma_risk": agent.genome.dogma_risk,
                "expressiveness": agent.genome.expressiveness,
                "influence_potential": agent.genome.influence_potential,
                "mobility": agent.genome.mobility,
                "altruism": agent.genome.altruism,
                "social_compliance": agent.genome.social_compliance,
                "curiosity": agent.genome.curiosity,
                "narrative_recovery": agent.genome.narrative_recovery,
                "faction_id": agent.faction_id or "",
                # [NOUVEAU] Champs symboliques
                "symbolic_color": agent.symbolic_artefact.symbolic_dna.color if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else "",
                "symbolic_glyph": agent.symbolic_artefact.symbolic_dna.glyph_symbol if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else "",
                "symbolic_complexity": agent.symbolic_artefact.symbolic_dna.complexity if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else 0,
                "symbolic_symmetry": agent.symbolic_artefact.symbolic_dna.symmetry if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else 0,
                "symbolic_glitch": agent.symbolic_artefact.symbolic_dna.glitch_factor if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else 0,
                "symbolic_entropy": agent.symbolic_artefact.symbolic_dna.entropy_level if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else 0,
                "artefact_fitness": agent.symbolic_artefact.aesthetic_score if agent.symbolic_artefact else 0,
                "artefact_mantra": (agent.symbolic_artefact.mantra_text[:100] + "...") if agent.symbolic_artefact else "",
                "dominant_emotion": agent.symbolic_artefact.symbolic_dna.dominant_emotion() if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else "",
            }
            self.agent_state_history.append(entry)

    def _capture_strain_state(self):
        total_agents = len(self.agents)
        for strain_id, strain in self.meme_strains.items():
            carriers = [a for a in self.agents 
                       if a.current_strain.strain_id == strain_id 
                       and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
            exposed = [a for a in self.agents 
                      if a.current_strain.strain_id == strain_id 
                      and a.cultural_status == CulturalStatus.EXPOSED]

            entry = {
                "timestamp": self.current_t,
                "strain_id": strain_id,
                "parent_id": strain.parent_id or "",
                "generation": strain.generation,
                "mantra_content": strain.mantra.content,
                "mantra_theme": strain.mantra.theme,
                "contagion_power": strain.contagion_power,
                "dogma_intensity": strain.dogma_intensity,
                "latency_period": strain.latency_period,
                "emergence_time": strain.emergence_time,
                "carrier_count": len(carriers),
                "exposed_count": len(exposed),
                "total_adherents": len(carriers) + len(exposed),
                "prevalence": (len(carriers) + len(exposed)) / max(1, total_agents),
                "is_root": 1 if strain.parent_id is None else 0,
                "mutation_count": len(strain.mutations),
                # [NOUVEAU] Champs symboliques
                "symbolic_color": strain.symbolic_artefact.symbolic_dna.color if strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna else "",
                "symbolic_glyph": strain.symbolic_artefact.symbolic_dna.glyph_symbol if strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna else "",
                "symbolic_complexity": strain.symbolic_artefact.symbolic_dna.complexity if strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna else 0,
                "symbolic_symmetry": strain.symbolic_artefact.symbolic_dna.symmetry if strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna else 0,
                "artefact_fitness": strain.symbolic_artefact.aesthetic_score if strain.symbolic_artefact else 0,
                "artefact_mantra": (strain.symbolic_artefact.mantra_text[:100] + "...") if strain.symbolic_artefact else "",
            }
            self.strain_history.append(entry)

    def _calculate_rt(self) -> float:
        recent = [e for e in self.events if e.event_type == "exposure" and e.timestamp > self.current_t - 5]
        infectors = [e.source_id for e in recent if e.source_id]
        if not infectors:
            return 0.0
        counts = Counter(infectors)
        return sum(counts.values()) / len(counts)

    def step(self) -> dict:
        if hasattr(self, "_agent_lookup"):
            del self._agent_lookup

        self._run_interaction_round()
        self.mutate_meme()
        self._apply_symbolic_resonance()
        self._apply_narrative_cycle()

        if self.rng.random() < 0.015:
            self._trigger_narrative_eclipse()
        if self.rng.random() < 0.015:
            self._trigger_cultural_resonance()

        self._maybe_trigger_random_event()
        self._maybe_generate_myth()
        self._update_factions()

        for agent in self.agents:
            self._progress_narrative(agent)

        for status in CulturalStatus:
            self.daily_metrics[self.current_t][f"cult_{status.value}"] = sum(
                1 for a in self.agents if a.cultural_status == status)
        self.daily_metrics[self.current_t]["nb_strains"] = len(self.meme_strains)
        self.daily_metrics[self.current_t]["nb_relics"] = len(self.relics)
        self.daily_metrics[self.current_t]["nb_myths"] = len(self.founding_myths)
        self.daily_metrics[self.current_t]["nb_factions"] = len(self.faction_system.factions)

        rt = self._calculate_rt()
        self.rt_history.append(rt)

        self._capture_agent_state()
        self._capture_strain_state()

        logger.debug(f"t={self.current_t} | Rt={rt:.2f} | Souches={len(self.meme_strains)} | Factions={len(self.faction_system.factions)}")

        self.current_t += 1
        for agent in self.agents:
            agent.current_t = self.current_t

        return {"t": self.current_t, "rt": rt, "metrics": dict(self.daily_metrics[self.current_t - 1])}

    def run(self, steps: int):
        for _ in range(steps):
            yield self.step()

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS — CSV, Neo4J, JSON, Images, Prompts
# ═══════════════════════════════════════════════════════════════════════════════

class CSVExporter:
    """Export CSV enrichi avec données symboliques."""

    @staticmethod
    def export_all(sim: CulturalEpidemicSimulation, output_dir: str):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        CSVExporter._export_agents(out / "agents_state.csv", sim)
        CSVExporter._export_strains(out / "strains_state.csv", sim)
        CSVExporter._export_metrics(out / "daily_metrics.csv", sim)
        CSVExporter._export_events(out / "narrative_events.csv", sim)
        CSVExporter._export_random_events(out / "random_events.csv", sim)
        CSVExporter._export_interactions(out / "interactions.csv", sim)
        CSVExporter._export_relics(out / "relics.csv", sim)
        CSVExporter._export_myths(out / "myths.csv", sim)
        CSVExporter._export_chronicle(out / "chronicle.csv", sim)
        CSVExporter._export_semantic_drift(out / "semantic_drift.csv", sim)
        CSVExporter._export_factions(out / "factions.csv", sim)
        CSVExporter._export_alliances(out / "alliances.csv", sim)
        CSVExporter._export_episodic_memory(out / "episodic_memory.csv", sim)
        CSVExporter._export_symbolic_resonance(out / "symbolic_resonance.csv", sim)
        CSVExporter._export_artefacts(out / "artefacts.csv", sim)
        CSVExporter._export_readme(out / "README_KNIME.txt")

        logger.info(f"📊 {len(list(out.glob('*.csv')))} fichiers CSV exportés dans {out}/")

    @staticmethod
    def _export_agents(path: Path, sim: CulturalEpidemicSimulation):
        if not sim.agent_state_history:
            return
        fieldnames = list(sim.agent_state_history[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sim.agent_state_history)
        logger.debug(f"✅ Agents: {len(sim.agent_state_history)} lignes")

    @staticmethod
    def _export_strains(path: Path, sim: CulturalEpidemicSimulation):
        if not sim.strain_history:
            return
        fieldnames = list(sim.strain_history[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sim.strain_history)
        logger.debug(f"✅ Souches: {len(sim.strain_history)} lignes")

    @staticmethod
    def _export_metrics(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for t, metrics in sorted(sim.daily_metrics.items()):
            row = {"timestamp": t}
            row.update(metrics)
            if t < len(sim.rt_history):
                row["rt"] = sim.rt_history[t]
            rows.append(row)
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Métriques: {len(rows)} lignes")

    @staticmethod
    def _export_events(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for e in sim.events:
            rows.append({
                "timestamp": e.timestamp, "agent_id": e.agent_id,
                "event_type": e.event_type, "cultural_state": e.cultural_state,
                "source_id": e.source_id or -1, "guild": e.guild or "",
                "narrative_coherence": e.narrative_coherence or 0,
                "strain_id": e.strain_id or "",
            })
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Événements narratifs: {len(rows)} lignes")

    @staticmethod
    def _export_random_events(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for e in sim.random_events:
            rows.append({
                "event_id": e.event_id, "event_type": e.event_type,
                "timestamp": e.timestamp, "zone": e.zone or "",
                "description": e.description,
                "affected_agents_count": len(e.affected_agents),
                "affected_agents": ",".join(str(a) for a in e.affected_agents[:10]),
                "impact": json.dumps(e.impact, ensure_ascii=False),
            })
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Événements aléatoires: {len(rows)} lignes")

    @staticmethod
    def _export_interactions(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for i in sim.interactions:
            rows.append({
                "timestamp": i.timestamp, "agent_a": i.agent_a, "agent_b": i.agent_b,
                "intensity": i.intensity, "transmission_risk": i.transmission_risk,
                "transmission_occurred": 1 if i.transmission_occurred else 0,
            })
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Interactions: {len(rows)} lignes")

    @staticmethod
    def _export_relics(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for r in sim.relics:
            rows.append({
                "relic_id": r.relic_id, "guardian_id": r.guardian_id,
                "zone": r.zone, "preserved_at": r.preserved_at,
                "mantra_content": r.mantra.content, "mantra_theme": r.mantra.theme,
                "veneration_count": r.veneration_count,
            })
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Reliques: {len(rows)} lignes")

    @staticmethod
    def _export_myths(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for m in sim.founding_myths:
            rows.append({
                "myth_id": m.myth_id, "title": m.title, "created_at": m.created_at,
                "verses": " | ".join(m.verses),
                "dominant_strains": ",".join(m.dominant_strains),
                "verse_count": len(m.verses),
            })
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Mythes: {len(rows)} lignes")

    @staticmethod
    def _export_chronicle(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for c in sim.chronicle:
            rows.append({
                "timestamp": c.get("t", 0), "event_type": c.get("type", ""),
                "event_id": c.get("event", ""), "myth_id": c.get("myth_id", ""),
                "faction_id": c.get("faction_id", ""),
            })
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Chronique: {len(rows)} lignes")

    @staticmethod
    def _export_semantic_drift(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for parent, children in sim.semantic_drift.items():
            for child in children:
                rows.append({"parent_strain": parent, "child_strain": child})
        if not rows:
            rows.append({"parent_strain": "", "child_strain": ""})
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["parent_strain", "child_strain"])
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Dérive sémantique: {len(rows)} lignes")

    @staticmethod
    def _export_factions(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for faction in sim.faction_system.factions.values():
            rows.append({
                "faction_id": faction.faction_id, "name": faction.name,
                "founder_id": faction.founder_id, "founding_strain": faction.founding_strain,
                "created_at": faction.created_at, "member_count": len(faction.members),
                "alliance_count": len(faction.alliances), "color": faction.color,
                "rituals": " | ".join(faction.rituals)
            })
        if rows:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Factions: {len(rows)} lignes")

    @staticmethod
    def _export_alliances(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for faction in sim.faction_system.factions.values():
            for ally_id in faction.alliances:
                rows.append({"faction_id": faction.faction_id, "ally_id": ally_id, "timestamp": sim.current_t})
        if rows:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["faction_id", "ally_id", "timestamp"])
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Alliances: {len(rows)} lignes")

    @staticmethod
    def _export_episodic_memory(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for agent in sim.agents[:100]:
            for evt in agent.episodic_memory.events[-10:]:
                rows.append({
                    "agent_id": agent.id, "timestamp": evt['timestamp'],
                    "event_type": evt['type'], "content": evt['content'], "impact": evt['impact']
                })
        if rows:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["agent_id", "timestamp", "event_type", "content", "impact"])
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Mémoire épisodique: {len(rows)} lignes")

    @staticmethod
    def _export_symbolic_resonance(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for strain_id, center in sim.symbolic_resonance.resonance_centers.items():
            rows.append({
                "strain_id": strain_id, "mass": center['mass'],
                "influence_radius": center['influence_radius'],
                "position_x": center['position']['x'], "position_y": center['position']['y']
            })
        if rows:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["strain_id", "mass", "influence_radius", "position_x", "position_y"])
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Résonance symbolique: {len(rows)} lignes")

    @staticmethod
    def _export_artefacts(path: Path, sim: CulturalEpidemicSimulation):
        rows = []
        for agent in sim.agents:
            if agent.symbolic_artefact:
                d = agent.symbolic_artefact.to_dict()
                d["agent_id"] = agent.id
                d["timestamp"] = sim.current_t
                rows.append(d)
        if rows:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Artefacts: {len(rows)} lignes")

    @staticmethod
    def _export_readme(path: Path):
        content = """
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
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"✅ README KNIME généré")

# ═══════════════════════════════════════════════════════════════════════════════
# NEO4J EXPORTER — Avec nœuds Artefact
# ═══════════════════════════════════════════════════════════════════════════════

class Neo4JExporter:
    @staticmethod
    def export_all(sim: CulturalEpidemicSimulation, output_dir: str, create_constraints: bool = True):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        cypher_lines = []
        
        if create_constraints:
            cypher_lines.append("// === CONTRAINTES ===")
            cypher_lines.append("CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT strain_id IF NOT EXISTS FOR (s:Strain) REQUIRE s.strain_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT relic_id IF NOT EXISTS FOR (r:Relic) REQUIRE r.relic_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT myth_id IF NOT EXISTS FOR (m:Myth) REQUIRE m.myth_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT zone_name IF NOT EXISTS FOR (z:Zone) REQUIRE z.name IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.event_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT artefact_id IF NOT EXISTS FOR (art:Artefact) REQUIRE art.fingerprint IS UNIQUE;")
            cypher_lines.append("")
        
        # Zones
        cypher_lines.append("// === ZONES ===")
        for zone in sim.zones:
            cypher_lines.append(f"CREATE (z:Zone {{name: '{zone.replace(chr(39), chr(92)+chr(39))}'}});")
        cypher_lines.append("")
        
        # Agents avec attributs symboliques
        cypher_lines.append("// === AGENTS ===")
        for agent in sim.agents:
            z = agent.zone.replace("'", "\\'")
            g = agent.guild.replace("'", "\\'")
            gs = agent.genome.glyph_symbol.replace("'", "\\'")
            sc = (agent.symbolic_artefact.symbolic_dna.color if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else "#888888").replace("'", "\\'")
            de = (agent.symbolic_artefact.symbolic_dna.dominant_emotion() if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna else "").replace("'", "\\'")
            cypher_lines.append(
                f"CREATE (a:Agent {{"
                f"id: {agent.id}, zone: '{z}', guild: '{g}', status: '{agent.cultural_status.name}', "
                f"is_silent_carrier: {str(agent.is_silent_carrier).lower()}, "
                f"narrative_coherence: {agent.narrative_coherence:.3f}, meme_virulence: {agent.meme_virulence:.3f}, "
                f"receptivity: {agent.receptivity:.3f}, influence_score: {agent.influence_score:.3f}, "
                f"is_relic_guardian: {str(agent.is_relic_guardian).lower()}, glyph_symbol: '{gs}', "
                f"symbolic_color: '{sc}', dominant_emotion: '{de}', "
                f"artefact_fitness: {(agent.symbolic_artefact.aesthetic_score if agent.symbolic_artefact else 0):.3f}, "
                f"faction_id: '{(agent.faction_id or '').replace(chr(39), chr(92)+chr(39))}'"
                f"}});"
            )
        cypher_lines.append("")
        
        # Souches avec artefacts
        cypher_lines.append("// === SOUCHES ===")
        for strain in sim.meme_strains.values():
            mc = strain.mantra.content.replace("'", "\\'")[:80]
            mt = strain.mantra.theme.replace("'", "\\'")
            pid = (strain.parent_id or "").replace("'", "\\'")
            sc = (strain.symbolic_artefact.symbolic_dna.color if strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna else "").replace("'", "\\'")
            sg = (strain.symbolic_artefact.symbolic_dna.glyph_symbol if strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna else "").replace("'", "\\'")
            cypher_lines.append(
                f"CREATE (s:Strain {{"
                f"strain_id: '{strain.strain_id.replace(chr(39), chr(92)+chr(39))}', "
                f"parent_id: '{pid}', generation: {strain.generation}, "
                f"mantra_content: '{mc}', mantra_theme: '{mt}', "
                f"contagion_power: {strain.contagion_power:.3f}, "
                f"dogma_intensity: {strain.dogma_intensity:.3f}, "
                f"symbolic_color: '{sc}', symbolic_glyph: '{sg}', "
                f"emergence_time: {strain.emergence_time}"
                f"}});"
            )
        cypher_lines.append("")
        
        # Artefacts
        cypher_lines.append("// === ARTEFACTS ===")
        seen_artefacts = set()
        for agent in sim.agents:
            if agent.symbolic_artefact and agent.symbolic_artefact.fingerprint not in seen_artefacts:
                seen_artefacts.add(agent.symbolic_artefact.fingerprint)
                fp = agent.symbolic_artefact.fingerprint.replace("'", "\\'")
                mt = (agent.symbolic_artefact.mantra_text[:60] + "...").replace("'", "\\'")
                th = agent.symbolic_artefact.theme.replace("'", "\\'")
                de = (agent.symbolic_artefact.symbolic_dna.dominant_emotion() if agent.symbolic_artefact.symbolic_dna else "").replace("'", "\\'")
                cypher_lines.append(
                    f"CREATE (art:Artefact {{"
                    f"fingerprint: '{fp}', mantra_text: '{mt}', theme: '{th}', "
                    f"dominant_emotion: '{de}', aesthetic_score: {agent.symbolic_artefact.aesthetic_score:.3f}"
                    f"}});"
                )
        cypher_lines.append("")
        
        # Relations Agent -> Artefact
        cypher_lines.append("// === RELATIONS AGENT -> ARTEFACT ===")
        for agent in sim.agents:
            if agent.symbolic_artefact:
                fp = agent.symbolic_artefact.fingerprint.replace("'", "\\'")
                cypher_lines.append(
                    f"MATCH (a:Agent {{id: {agent.id}}}), (art:Artefact {{fingerprint: '{fp}'}}) "
                    f"CREATE (a)-[:MANIFESTS]->(art);"
                )
        cypher_lines.append("")
        
        # Relations Agent -> Zone, Agent -> Strain, Strain -> Strain, etc.
        cypher_lines.append("// === RELATIONS AGENT -> ZONE ===")
        for agent in sim.agents:
            z = agent.zone.replace("'", "\\'")
            cypher_lines.append(f"MATCH (a:Agent {{id: {agent.id}}}), (z:Zone {{name: '{z}'}}) CREATE (a)-[:LOCATED_IN]->(z);")
        cypher_lines.append("")
        
        cypher_lines.append("// === RELATIONS AGENT -> STRAIN ===")
        for agent in sim.agents:
            if agent.current_strain:
                sid = agent.current_strain.strain_id.replace("'", "\\'")
                cypher_lines.append(
                    f"MATCH (a:Agent {{id: {agent.id}}}), (s:Strain {{strain_id: '{sid}'}}) "
                    f"CREATE (a)-[:CARRIES {{since: {agent.exposure_time or 0}}}]->(s);"
                )
        cypher_lines.append("")
        
        cypher_lines.append("// === RELATIONS STRAIN -> STRAIN (MUTATIONS) ===")
        for strain in sim.meme_strains.values():
            if strain.parent_id and strain.parent_id in sim.meme_strains:
                p = strain.parent_id.replace("'", "\\'")
                s = strain.strain_id.replace("'", "\\'")
                cypher_lines.append(
                    f"MATCH (parent:Strain {{strain_id: '{p}'}}), (child:Strain {{strain_id: '{s}'}}) "
                    f"CREATE (parent)-[:MUTATED_INTO {{generation: {strain.generation}}}]->(child);"
                )
        cypher_lines.append("")
        
        # Factions
        cypher_lines.append("// === FACTIONS ===")
        for faction in sim.faction_system.factions.values():
            fn = faction.name.replace("'", "\\'")[:40]
            c = faction.color.replace("'", "\\'")
            cypher_lines.append(
                f"CREATE (f:Faction {{"
                f"faction_id: '{faction.faction_id}', name: '{fn}', "
                f"color: '{c}', member_count: {len(faction.members)}"
                f"}});"
            )
        cypher_lines.append("")
        
        # Événements et métriques (simplifiés)
        cypher_lines.append("// === ÉVÉNEMENTS ===")
        for i, evt in enumerate(sim.random_events[-50:]):
            et = evt.event_type.replace("'", "\\'")
            d = evt.description.replace("'", "\\'")[:80]
            cypher_lines.append(
                f"CREATE (e:Event {{"
                f"event_id: '{evt.event_id}', timestamp: {evt.timestamp}, "
                f"event_type: '{et}', description: '{d}'"
                f"}});"
            )
        cypher_lines.append("")
        
        # Écrire le fichier
        cypher_file = out / "neo4j_import.cypher"
        with open(cypher_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(cypher_lines))
        logger.info(f"🦈 Export Neo4J: {cypher_file} ({len(cypher_lines)} lignes)")
        return cypher_file


# ═══════════════════════════════════════════════════════════════════════════════
# GÉNÉRATION D'IMAGES ET PROMPTS DE DIFFUSION
# ═══════════════════════════════════════════════════════════════════════════════

def build_prompt_for_diffusion(sim: CulturalEpidemicSimulation, target: str = "grok") -> str:
    """Génère un prompt pour IA de diffusion représentant l'état culturel global."""
    dominant_strains = Counter(
        a.current_strain.strain_id for a in sim.agents
        if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
    ).most_common(5)
    
    visual_elements = []
    mantras = []
    colors = []
    
    for strain_id, count in dominant_strains:
        strain = sim.meme_strains.get(strain_id)
        if strain and strain.symbolic_artefact:
            dna = strain.symbolic_artefact.symbolic_dna
            visual_elements.append(f"a {dna.glyph_symbol} symbol in {dna.color}")
            mantras.append(strain.symbolic_artefact.mantra_text[:40])
            colors.append(dna.color)
    
    style_map = {
        "grok": "photorealistic, cinematic, 8k, detailed, mystical, symbolic, dramatic lighting",
        "gemini": "artistic, surreal, glowing, esoteric, highly detailed, painting, ethereal",
        "dalle": "digital art, fantasy, intricate, neon, cyberpunk, mystical, vibrant, dreamlike",
        "midjourney": "fantasy art, intricate, mystical, glowing, ethereal, detailed, majestic --ar 16:9",
        "stable": "masterpiece, best quality, highly detailed, mystical, symbolic, fantasy",
    }
    style = style_map.get(target.lower(), style_map["grok"])
    
    dominant_emotions = Counter()
    for agent in sim.agents:
        if agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna:
            dominant_emotions[agent.symbolic_artefact.symbolic_dna.dominant_emotion()] += 1
    
    mood = "mysterious"
    if dominant_emotions:
        mood = dominant_emotions.most_common(1)[0][0]
    
    prompt = f"""Create a massive symbolic artwork representing a cultural epidemic.

COMPOSITION:
- A dark cosmic background with faint geometric patterns and digital glitch artifacts.
- Central collage of emerging symbols: {', '.join(visual_elements[:5])}.
- Flowing mantras inscribed in neon light around the symbols: {' | '.join(mantras[:3])}.
- Color palette dominated by {', '.join(colors[:3])} with chromatic aberration.
- Agents represented as luminous particles forming network connections.

ATMOSPHERE:
- Mood: {mood}, transcendent, liminal.
- The scene feels like an illuminated manuscript from a cyberpunk monastery.
- Digital decay mixed with sacred geometry.
- Style: {style}.
- Resolution: 1024x1024, high detail, dramatic composition.

NARRATIVE CONTEXT:
- {len(sim.meme_strains)} evolving narrative strains.
- {len(sim.faction_system.factions)} cultural factions.
- {len(sim.agents)} agents in various states of belief.
"""
    return prompt.strip()


def generate_collage(sim: CulturalEpidemicSimulation, output_path: str):
    """Génère un collage des glyphes dominants."""
    if not HAS_MPL:
        logger.warning("matplotlib indisponible — collage non généré")
        return None
    
    # Sélectionner les souches dominantes
    strain_counts = Counter(
        a.current_strain.strain_id for a in sim.agents
        if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
    ).most_common(6)
    
    if not strain_counts:
        return None
    
    n = len(strain_counts)
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    if n == 1:
        axes = np.array([[axes]])
    elif rows == 1:
        axes = axes.reshape(1, -1)
    
    fig.patch.set_facecolor('#0b0b12')
    engine = VonPetzingerSymbols()
    
    for idx, (strain_id, count) in enumerate(strain_counts):
        ax = axes[idx // cols, idx % cols]
        ax.set_facecolor('#0b0b12')
        ax.set_xlim(0, 800)
        ax.set_ylim(0, 600)
        ax.axis('off')
        
        strain = sim.meme_strains.get(strain_id)
        if strain and strain.symbolic_artefact and strain.symbolic_artefact.symbolic_dna:
            dna = strain.symbolic_artefact.symbolic_dna
            draw_fn = engine.symbols.get(dna.glyph_symbol, engine.draw_spiral)
            draw_fn(ax, 400, 300, scale=dna.scale * 1.5, angle=0, color=dna.color)
            ax.set_title(
                f"{dna.glyph_symbol}\\n{strain_id} ({count} agents)\\n{dna.dominant_emotion()}",
                color=dna.color, fontsize=9
            )
        else:
            ax.text(400, 300, strain_id, ha='center', va='center', color='white', fontsize=12)
    
    # Masquer les axes vides
    for idx in range(n, rows * cols):
        axes[idx // cols, idx % cols].axis('off')
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=130, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    logger.info(f"🖼 Collage symbolique généré: {output_path}")
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# RETROWAVE DISPLAY — Affichage immersif conservé
# ═══════════════════════════════════════════════════════════════════════════════

STATUS_COLORS = {
    CulturalStatus.RECEPTIVE: "#4a7a8a",
    CulturalStatus.EXPOSED: "#f5c518",
    CulturalStatus.EVANGELIST: "#ff2d78",
    CulturalStatus.SILENT_CARRIER: "#ff8c42",
    CulturalStatus.DISENCHANTED: "#00ff9d",
    CulturalStatus.OBLIVIOUS: "#8888aa",
}

class RetroWaveDisplay:
    def __init__(self, width: int = 80):
        self.width = min(width, shutil.get_terminal_size().columns - 2)
        self.start_time = time.time()
        self.animation_chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        self._anim_idx = 0
        self._first_render = True
    
    def c(self, text: str, *codes: str) -> str:
        color_map = {
            "bright_cyan": "\\033[96m", "bright_magenta": "\\033[95m",
            "bright_yellow": "\\033[93m", "bright_red": "\\033[91m",
            "bright_green": "\\033[92m", "bright_blue": "\\033[94m",
            "cyan": "\\033[36m", "magenta": "\\033[35m",
            "yellow": "\\033[33m", "green": "\\033[32m",
            "red": "\\033[31m", "blue": "\\033[34m",
            "dim": "\\033[2m", "bold": "\\033[1m",
            "reset": "\\033[0m", "bright_black": "\\033[90m",
        }
        out = "".join(color_map.get(c, "") for c in codes) + text + color_map.get("reset", "")
        return out
    
    def banner(self) -> str:
        return self.c(
            "\\n ════════════ ✦ ARCHEOSYMBOLIC CHRONICLE v1.0 ✦ ════════════\\n"
            "   ▸ Fusion : ArcheoEpidemic × SymbolicDNA_Forge\\n"
            "   ▸ Contagion par Artefacts Symboliques Évolutifs\\n"
            "   ▸ Résonance Esthétique + Factions + Mémoire Épisodique\\n",
            "bright_cyan", "bold"
        )
    
    def status_bar(self, sim) -> str:
        total = len(sim.agents)
        status_counts = Counter(a.cultural_status for a in sim.agents)
        bar_width = self.width - 40
        
        def make_bar(status, color, icon):
            count = status_counts.get(status, 0)
            pct = count / max(1, total)
            filled = int(pct * bar_width)
            bar = self.c("█" * filled, color) + self.c("░" * (bar_width - filled), "dim")
            return f"{self.c(icon, color)} {status.name[:3]:<3} {bar} {count:>3} ({pct*100:5.1f}%)"
        
        lines = [self.c("╔" + "═" * (self.width - 2) + "╗", "bright_cyan")]
        t = sim.current_t
        strains = len(sim.meme_strains)
        factions = len(sim.faction_system.factions)
        rt = sim.rt_history[-1] if sim.rt_history else 0
        
        line1 = (f"  ⏱ t={t:>3}  🧬 souches={strains:>2}  ⚔️ factions={factions:>2}  "
                f"📈 Rt={rt:>5.2f}  👤 pop={total:>3}")
        lines.append(f"│{line1:<{self.width-2}}│")
        lines.append(f"├{'─' * (self.width-2)}┤")
        lines.append(f"│ {self.c('ÉTATS NARRATIFS', 'bright_yellow', 'bold')}{' ' * (self.width-18)}│")
        lines.append(f"│ {make_bar(CulturalStatus.RECEPTIVE, 'bright_blue', '🌱')}{' ' * 2}│")
        lines.append(f"│ {make_bar(CulturalStatus.EXPOSED, 'yellow', '🌿')}{' ' * 2}│")
        lines.append(f"│ {make_bar(CulturalStatus.EVANGELIST, 'bright_red', '🔥')}{' ' * 2}│")
        lines.append(f"│ {make_bar(CulturalStatus.SILENT_CARRIER, 'bright_magenta', '🌙')}{' ' * 2}│")
        lines.append(f"│ {make_bar(CulturalStatus.DISENCHANTED, 'green', '💀')}{' ' * 2}│")
        lines.append(f"│ {make_bar(CulturalStatus.OBLIVIOUS, 'bright_black', '👻')}{' ' * 2}│")
        lines.append(f"╚{'═' * (self.width-2)}╝")
        return "\n".join(lines)
    
    def render_ascii_art(self, sim) -> str:
        total = len(sim.agents)
        if total == 0:
            return ""
        cols = min(40, max(10, self.width // 3))
        rows = max(1, min(10, total // cols + 1))
        
        glyphs = {
            CulturalStatus.RECEPTIVE: "·", CulturalStatus.EXPOSED: "◌",
            CulturalStatus.EVANGELIST: "★", CulturalStatus.SILENT_CARRIER: "☽",
            CulturalStatus.DISENCHANTED: "✧", CulturalStatus.OBLIVIOUS: "·",
        }
        colors = {
            CulturalStatus.RECEPTIVE: "bright_blue", CulturalStatus.EXPOSED: "yellow",
            CulturalStatus.EVANGELIST: "bright_red", CulturalStatus.SILENT_CARRIER: "bright_magenta",
            CulturalStatus.DISENCHANTED: "green", CulturalStatus.OBLIVIOUS: "bright_black",
        }
        
        grid = []
        idx = 0
        for _ in range(rows):
            row = []
            for _ in range(cols):
                if idx < total:
                    agent = sim.agents[idx]
                    glyph = glyphs.get(agent.cultural_status, "·")
                    color = colors.get(agent.cultural_status, "dim")
                    if agent.is_relic_guardian:
                        glyph = self.c("✦", "bright_yellow")
                    elif agent.faction_id:
                        glyph = self.c("⚔", "bright_red")
                    elif agent.symbolic_artefact and agent.symbolic_artefact.symbolic_dna:
                        glyph = self.c(agent.symbolic_artefact.symbolic_dna.glyph_symbol[0].upper(), color)
                    else:
                        glyph = self.c(glyph, color)
                    row.append(glyph)
                else:
                    row.append(" ")
                idx += 1
            grid.append(" ".join(row))
        return "\n".join(grid)
    
    def event_feed(self, sim, n: int = 3) -> str:
        events = sim.random_events[-n:] if sim.random_events else []
        if not events:
            return self.c("  [ silence narratif... ]", "dim")
        lines = []
        for evt in events[-n:]:
            icon = {"schism": "🔱", "prophecy": "🜃", "censorship": "🚫", "reformation": "✨",
                   "pilgrimage": "🕊", "relic_creation": "📜", "oracle_whisper": "🔮",
                   "faction_emergence": "🏛", "narrative_eclipse": "🌑",
                   "cultural_resonance": "🎵"}.get(evt.event_type, "⚡")
            color = {"faction_emergence": "bright_red", "narrative_eclipse": "bright_cyan",
                    "cultural_resonance": "bright_green"}.get(evt.event_type, "cyan")
            lines.append(f"  {self.c(icon, color)} {self.c(evt.description[:self.width-20], color)}")
        return "\n".join(lines)
    
    def prophet_corner(self, sim) -> str:
        if not sim.founding_myths:
            return self.c("  🔮 L'oracle attend le premier mythe...", "dim")
        last_myth = sim.founding_myths[-1]
        verses = last_myth.verses[:2]
        lines = [self.c("  🔮 PROPHÉTIE DU TEMPS PRÉSENT", "bright_magenta", "bold")]
        for v in verses:
            lines.append(f"    {self.c(v[:60], 'magenta', 'italic')}...")
        return "\n".join(lines)
    
    def animated_step(self, sim, step: int, total_steps: int) -> str:
        progress = step / max(1, total_steps)
        spinner = self.animation_chars[self._anim_idx % len(self.animation_chars)]
        self._anim_idx += 1
        
        lines = []
        lines.append(self.c("════════════════════════════════════════════════════════════════════", "bright_cyan"))
        bar_len = self.width - 20
        filled = int(progress * bar_len)
        bar = self.c("█" * filled, "bright_magenta") + self.c("░" * (bar_len - filled), "dim")
        lines.append(f"  {self.c('PROGRÈS', 'bright_cyan', 'bold')} [{bar}] {spinner} {step}/{total_steps}")
        
        factions = len(sim.faction_system.factions)
        lines.append(f"  {self.c('⏱', 'bright_yellow')} Pas : {step}  |  {self.c('🧬', 'bright_magenta')} Souches : {len(sim.meme_strains)}  |  {self.c('⚔️', 'bright_red')} Factions : {factions}")
        
        if sim.random_events and sim.random_events[-1].timestamp == sim.current_t - 1:
            last_evt = sim.random_events[-1]
            lines.append(f"  {self.c('⚡ ÉVÉNEMENT', 'bright_yellow', 'bold')} {last_evt.description[:60]}")
        
        lines.append("")
        lines.append(self.status_bar(sim))
        lines.append("")
        lines.append(self.c("  ✦ CARTE NARRATIVE SYMBOLIQUE ✦", "bright_cyan", "bold"))
        lines.append(self.render_ascii_art(sim))
        lines.append("")
        lines.append(self.prophet_corner(sim))
        lines.append("")
        lines.append(self.c("  ⚡ FIL DES ÉVÉNEMENTS", "bright_yellow", "bold"))
        lines.append(self.event_feed(sim, 2))
        lines.append(self.c("════════════════════════════════════════════════════════════════════", "bright_cyan"))
        return "\n".join(lines)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[H", end="")
        sys.stdout.flush()
    
    def render_full(self, sim, step: int, total_steps: int, report: str = None):
        if self._first_render:
            self.clear_screen()
            print(self.banner())
            self._first_render = False
            time.sleep(0.3)
        print("\033[50A", end="")
        print("\033[J", end="")
        output = self.animated_step(sim, step, total_steps)
        print(output, end="")
        if report and step >= total_steps - 1:
            print("\n" + "=" * self.width)
            print(report)
        sys.stdout.flush()
        return output


# ═══════════════════════════════════════════════════════════════════════════════
# RAPPORT MYTHOLOGIQUE — Avec données symboliques
# ═══════════════════════════════════════════════════════════════════════════════

def mythological_report(sim: CulturalEpidemicSimulation) -> str:
    lines = []
    lines.append("═" * 70)
    lines.append("  📖 RAPPORT MYTHOLOGIQUE — ArcheoSymbolic Chronicle v1.0")
    lines.append("═" * 70)
    status_counts = Counter(a.cultural_status for a in sim.agents)
    total = len(sim.agents)
    lines.append(f"\nPopulation totale : {total} narrateurs sur {len(sim.zones)} zones")
    lines.append("\n— Répartition des croyances —")
    for status in CulturalStatus:
        n = status_counts.get(status, 0)
        lines.append(f"  {status.name:<16} : {n:>4}  ({100*n/max(1,total):5.1f}%)")
    
    believer_strains = Counter(
        a.current_strain.strain_id for a in sim.agents
        if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
    )
    lines.append("\n— Récits dominants —")
    if believer_strains:
        for strain_id, count in believer_strains.most_common(5):
            strain = sim.meme_strains[strain_id]
            lines.append(f"  [{strain_id}] (gén.{strain.generation}, {count} adeptes) :")
            lines.append(f"      « {strain.mantra.content} »")
            if strain.symbolic_artefact:
                dna = strain.symbolic_artefact.symbolic_dna
                lines.append(f"      🎨 Glyphe: {dna.glyph_symbol} | Couleur: {dna.color} | Émotion: {dna.dominant_emotion()}")
                lines.append(f"      ✨ Fitness esthétique: {strain.symbolic_artefact.aesthetic_score:.3f}")
            lines.append(f"      contagion={strain.contagion_power:.2f}  dogme={strain.dogma_intensity:.2f}")
    else:
        lines.append("  Silence collectif.")
    
    lines.append("\n— Superspreaders culturels —")
    out_degrees = [(a, sim.transmission_network.out_degree(a.id) if sim.transmission_network.has_node(a.id) else 0)
                   for a in sim.agents]
    out_degrees.sort(key=lambda t: t[1], reverse=True)
    for agent, deg in out_degrees[:5]:
        if deg == 0:
            break
        relic_mark = " 📜" if agent.is_relic_guardian else ""
        faction_mark = f" ⚔️{agent.faction_id}" if agent.faction_id else ""
        art_mark = f" 🎨{agent.symbolic_artefact.symbolic_dna.glyph_symbol}" if agent.symbolic_artefact else ""
        lines.append(f"  Agent#{agent.id:<4}{relic_mark}{faction_mark}{art_mark} guilde={agent.guild:<12} transmissions={deg}")
    
    lines.append(f"\n— Factions culturelles ({len(sim.faction_system.factions)}) —")
    for faction in sim.faction_system.factions.values():
        lines.append(f"  {faction.faction_id} — «{faction.name}» ({len(faction.members)} membres)")
        if faction.alliances:
            lines.append(f"    Alliances: {', '.join(faction.alliances)}")
    
    lines.append(f"\n— Artefacts symboliques —")
    top_artefacts = sorted(
        [(a, a.symbolic_artefact.aesthetic_score) for a in sim.agents if a.symbolic_artefact],
        key=lambda x: x[1], reverse=True
    )[:3]
    for agent, score in top_artefacts:
        dna = agent.symbolic_artefact.symbolic_dna
        lines.append(f"  Agent#{agent.id}: {dna.glyph_symbol} ({dna.color}) — fitness {score:.3f}")
        lines.append(f"    « {agent.symbolic_artefact.mantra_text[:60]}... »")
    
    lines.append(f"\n— Mythes fondateurs ({len(sim.founding_myths)}) —")
    for myth in sim.founding_myths:
        lines.append(f"  {myth.myth_id} — « {myth.title} »")
    
    lines.append(f"\n— Dérive sémantique —")
    for parent, children in list(sim.semantic_drift.items())[:5]:
        if children:
            lines.append(f"  {parent} → {', '.join(children[:3])}")
    
    lines.append("\n" + "═" * 70)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITAIRE — MiniDiGraph fallback
# ═══════════════════════════════════════════════════════════════════════════════

class _MiniDiGraph:
    def __init__(self):
        self._edges = defaultdict(dict)
        self._out_deg = defaultdict(int)
    def add_edge(self, u, v, **attrs):
        self._edges[u][v] = attrs
        self._out_deg[u] += 1
    def number_of_nodes(self):
        nodes = set(self._edges.keys())
        for v in self._edges.values():
            nodes.update(v.keys())
        return len(nodes)
    def has_node(self, n):
        return n in self._edges or any(n in v for v in self._edges.values())
    def out_degree(self, n):
        return self._out_deg.get(n, 0)
    def edges(self):
        for u, targets in self._edges.items():
            for v in targets:
                yield u, v


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT JSON NATIF
# ═══════════════════════════════════════════════════════════════════════════════

def export_simulation_data(sim: CulturalEpidemicSimulation, output_dir: str):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    with open(out / "params.json", "w", encoding="utf-8") as f:
        json.dump(sim.params, f, indent=2, ensure_ascii=False)
    
    strains_data = []
    for sid, s in sim.meme_strains.items():
        entry = {
            "strain_id": s.strain_id, "parent_id": s.parent_id,
            "generation": s.generation, "mantra": s.mantra.content,
            "theme": s.mantra.theme, "contagion_power": s.contagion_power,
            "dogma_intensity": s.dogma_intensity,
        }
        if s.symbolic_artefact:
            entry["artefact"] = s.symbolic_artefact.to_dict()
        strains_data.append(entry)
    with open(out / "strains.json", "w", encoding="utf-8") as f:
        json.dump(strains_data, f, indent=2, ensure_ascii=False, default=str)
    
    agents_data = []
    for a in sim.agents:
        entry = {
            "id": a.id, "zone": a.zone, "guild": a.guild,
            "status": a.cultural_status.name, "current_strain": a.current_strain.strain_id,
            "influence_score": a.influence_score,
        }
        if a.symbolic_artefact:
            entry["artefact"] = a.symbolic_artefact.to_dict()
        agents_data.append(entry)
    with open(out / "agents.json", "w", encoding="utf-8") as f:
        json.dump(agents_data, f, indent=2, ensure_ascii=False, default=str)
    
    events_data = [asdict(e) for e in sim.events]
    with open(out / "events.json", "w", encoding="utf-8") as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False, default=str)
    
    with open(out / "mythological_report.txt", "w", encoding="utf-8") as f:
        f.write(mythological_report(sim))
    
    logger.info(f"📦 Données JSON exportées dans {out}/")


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def _pre_parse_data_dir() -> Optional[str]:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--data-dir", type=str, default=None)
    known, _ = pre.parse_known_args()
    return known.data_dir


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="archeosymbolic_chronicle",
        description="🧬🌌 ARCHEOSYMBOLIC CHRONICLE — Simulateur d'épidémies narratives par artefacts symboliques",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    gen = p.add_argument_group("Général")
    gen.add_argument("--seed", type=int, default=2075, help="Graine aléatoire")
    gen.add_argument("--steps", type=int, default=60, help="Nombre de pas de temps")
    gen.add_argument("--verbose", action="store_true", help="Affichage pas-à-pas")
    gen.add_argument("--no-retro", action="store_true", help="Désactiver l'affichage rétro-wave")
    gen.add_argument("--log-file", type=str, default=None, help="Fichier de log")
    gen.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    
    data = p.add_argument_group("Données externes")
    data.add_argument("--data-dir", type=str, default=None, help="Répertoire des fichiers JSON de données")
    data.add_argument("--init-data", type=str, default=None, help="Créer les fichiers JSON de données dans ce répertoire")
    
    exp = p.add_argument_group("Export de données")
    exp.add_argument("--export-csv", type=str, default=None, help="Répertoire d'export CSV")
    exp.add_argument("--export-json", type=str, default=None, help="Répertoire d'export JSON")
    exp.add_argument("--export-neo4j", type=str, default=None, help="Répertoire d'export Neo4J")
    exp.add_argument("--export-collage", type=str, default=None, help="Chemin PNG du collage symbolique")
    exp.add_argument("--diffusion-prompt", type=str, default=None, help="Fichier de sortie pour le prompt de diffusion")
    exp.add_argument("--diffusion-target", type=str, default="grok", choices=["grok", "gemini", "dalle", "midjourney", "stable"])
    
    pop = p.add_argument_group("Population")
    pop.add_argument("--pop-total", type=int, default=180, help="Nombre total d'agents")
    pop.add_argument("--nb-zones", type=int, default=6, help="Nombre de zones")
    pop.add_argument("--initial-believers", type=int, default=3, help="Croyants initiaux")
    
    root = p.add_argument_group("Souche racine")
    root.add_argument("--root-theme", type=str, default="rituel", choices=get_data_manager().get_themes_list())
    root.add_argument("--r0-base", type=float, default=2.4, help="R0 de base")
    root.add_argument("--latency-period", type=float, default=3.0, help="Période de latence")
    
    dyn = p.add_argument_group("Dynamiques narratives")
    dyn.add_argument("--disenchant-rate", type=float, default=0.04, help="Taux de désenchantement")
    dyn.add_argument("--oblivion-rate", type=float, default=0.003, help="Taux d'oubli")
    dyn.add_argument("--mutation-prob", type=float, default=0.02, help="Probabilité de mutation")
    dyn.add_argument("--dogma-rate", type=float, default=0.01, help="Intensité dogmatique")
    
    sym = p.add_argument_group("Évolution symbolique")
    sym.add_argument("--symbolic-evolution", action="store_true", default=True, help="Activer la forge symbolique")
    sym.add_argument("--symbolic-generations", type=int, default=3, help="Générations de la forge par mutation")
    sym.add_argument("--no-symbolic-evolution", dest="symbolic_evolution", action="store_false", help="Désactiver la forge")
    
    evt = p.add_argument_group("Événements")
    evt.add_argument("--random-event-prob", type=float, default=0.03)
    evt.add_argument("--myth-generation-period", type=int, default=20)
    evt.add_argument("--max-myths", type=int, default=3)
    
    return p


def run_simulation(params: dict, steps: int = 60, verbose: bool = False,
                 retro_display: bool = True, export_csv: Optional[str] = None,
                 export_neo4j: Optional[str] = None, export_json: Optional[str] = None,
                 export_collage: Optional[str] = None, diffusion_prompt: Optional[str] = None,
                 diffusion_target: str = "grok", data_dir: Optional[str] = None) -> CulturalEpidemicSimulation:
    
    if data_dir:
        dm = FusionDataManager(data_dir)
        set_data_manager(dm)
    
    sim = CulturalEpidemicSimulation(params, data_dir=data_dir)
    
    display = None
    if retro_display:
        display = RetroWaveDisplay()
        display.clear_screen()
        print(display.banner())
        time.sleep(0.5)
    
    for i, snapshot in enumerate(sim.run(steps)):
        if retro_display and display:
            report = mythological_report(sim) if i == steps - 1 else None
            display.render_full(sim, i + 1, steps, report)
            time.sleep(0.08)
        elif verbose:
            m = snapshot["metrics"]
            print(f"[t={snapshot['t']:>3}] Rt={snapshot['rt']:.2f} | "
                  f"É={m.get('cult_I', 0)} PS={m.get('cult_A', 0)} "
                  f"Souches={m.get('nb_strains', 0)} Factions={m.get('nb_factions', 0)}")
    
    if retro_display and display:
        print("\n" + display.c("═══ ✦ FIN DE LA SIMULATION ✦ ═══", "bright_magenta", "bold"))
    
    # Export CSV
    if export_csv:
        CSVExporter.export_all(sim, export_csv)
        logger.info(f"📊 Données CSV exportées dans {export_csv}/")
    
    # Export Neo4J
    if export_neo4j:
        Neo4JExporter.export_all(sim, export_neo4j)
        logger.info(f"🦈 Données Neo4J exportées dans {export_neo4j}/")
    
    # Export JSON
    if export_json:
        export_simulation_data(sim, export_json)
        logger.info(f"📦 Données JSON exportées dans {export_json}/")
    
    # Génération du collage
    if export_collage and HAS_MPL:
        generate_collage(sim, export_collage)
    
    # Génération du prompt de diffusion
    if diffusion_prompt:
        prompt = build_prompt_for_diffusion(sim, target=diffusion_target)
        with open(diffusion_prompt, "w", encoding="utf-8") as f:
            f.write(prompt)
        logger.info(f"📝 Prompt de diffusion sauvegardé: {diffusion_prompt}")
        FengShuiDisplay.section("Prompt de diffusion généré", "🧠")
        FengShuiDisplay.mantra(prompt, width=90)
    
    return sim


def main():
    _early_data_dir = _pre_parse_data_dir()
    if _early_data_dir:
        set_data_manager(FusionDataManager(_early_data_dir))
    
    parser = build_arg_parser()
    args = parser.parse_args()
    
    if args.init_data:
        manager = FusionDataManager()
        manager.save_external_data(args.init_data)
        print(f"✅ Données initialisées dans {args.init_data}/")
        return
    
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    logger.info("🌌🧬 Démarrage d'ArcheoSymbolic Chronicle v1.0")
    logger.info("Fusion : ArcheoEpidemic × SymbolicDNA_Forge")
    logger.debug(f"Arguments : {vars(args)}")
    
    params = {
        "seed": args.seed, "pop_total": args.pop_total, "nb_zones": args.nb_zones,
        "initial_believers": args.initial_believers, "root_theme": args.root_theme,
        "r0_base": args.r0_base, "disenchant_rate": args.disenchant_rate,
        "oblivion_rate": args.oblivion_rate, "mutation_prob": args.mutation_prob,
        "dogma_rate": args.dogma_rate, "latency_period": args.latency_period,
        "random_event_prob": args.random_event_prob,
        "myth_generation_period": args.myth_generation_period, "max_myths": args.max_myths,
        "symbolic_evolution": args.symbolic_evolution,
        "symbolic_generations": args.symbolic_generations,
    }
    
    sim = run_simulation(
        params, steps=args.steps, verbose=args.verbose,
        retro_display=not args.no_retro, export_csv=args.export_csv,
        export_neo4j=args.export_neo4j, export_json=args.export_json,
        export_collage=args.export_collage, diffusion_prompt=args.diffusion_prompt,
        diffusion_target=args.diffusion_target, data_dir=args.data_dir,
    )
    
    print()
    report = mythological_report(sim)
    if args.no_retro:
        print(report)
    else:
        display = RetroWaveDisplay()
        print(display.c("\n" + report, "pearl"))


if __name__ == "__main__":
    main()
