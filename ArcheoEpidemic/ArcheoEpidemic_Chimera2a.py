#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║   🧬🌌 ARCHEOEPIDEMIC CHIMERA — v2.0 "LIBERATED"                            ║
║   Ajouts v2.0 :                                                             ║
║     • CLI exhaustive (argparse) : TOUS les paramètres bidouillables         ║
║     • Logs Debug détaillés (fichier + console)                              ║
║     • Événements aléatoires (schismes, prophéties, censures, réformations)  ║
║     • Mémoire collective par zone + dérive sémantique                       ║
║     • Génération de mythes fondateurs (agrégation de mantras)               ║
║     • Reliques des Anachorètes (mantras préservés)                          ║
║     • Oracle prédictif (tendances narratives)                               ║
║     • Codex final (compilation des mutations)                               ║
║     • Chronique des temps (timeline narrative)                              ║
║     • Pèlerinages (migration vers zones dominantes)                         ║
║     • Saints patrons (superspreaders sacrés)                                ║
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

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
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
    """Configure le système de logs avec sortie console et fichier optionnel."""
    logger = logging.getLogger("ArcheoEpidemicChimera")
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

logger = logging.getLogger("ArcheoEpidemicChimera")

# ═══════════════════════════════════════════════════════════════════════════════
# [PARENT 1] LEXIQUE ONIRIQUE
# ═══════════════════════════════════════════════════════════════════════════════
def load_oniric_lexicon() -> Dict[str, List[str]]:
    return {
        "Adjectif": ["fractal", "quantique", "cryptique", "spectral", "liminal",
                     "onirique", "corrompu", "sacré", "glitché", "ancestral"],
        "Nom": ["signal", "silence", "glyphe", "écho", "seuil", "récit",
                "mantra", "spectre", "réseau", "songe"],
        "Action": ["implose", "exalte", "désintègre", "fusionne", "résonne",
                   "désagrège", "sature", "décode", "invoque", "sublime",
                   "dévore", "réfracte", "cristallise", "diffuse", "condense",
                   "synchronise", "amplifie", "hack", "insère", "mute",
                   "convoque", "infecte", "vaccine", "psalmodie", "prophétise"],
        "Bénéfice": ["la clarté", "le silence", "l'oubli", "la vérité brûlante",
                     "l'éveil", "l'unité", "l'extase quantique", "la fusion des âmes",
                     "l'illumination", "la synchronicité totale", "la communion",
                     "la mémoire collective", "la révélation", "la transcendance pure"],
        "Défaut": ["le bruit", "la trahison", "le compromis", "l'oubli numérique",
                   "le mensonge", "l'entropie", "la dissonance", "la corruption",
                   "la fragmentation", "la désorientation", "le virus mental",
                   "la psychose cybernétique", "l'effondrement cognitif"],
        "Paysage": ["désert du no-signal", "marché noir de Lagos", "nuage quantique",
                    "cimetière de data", "temple de silicium", "catacombes de code",
                    "archipel des serveurs oubliés", "cathédrale de circuits imprimés",
                    "nécropole des IA défuntes", "bibliothèque de Babel numérique"],
        "VerbeMystique": ["consume", "efface", "encrypte", "réveille", "transmute",
                          "dissout", "illumine", "recodifie", "absout", "exalte",
                          "sublime", "canalise", "révèle", "manifeste", "prophétise"],
        "Symbole": ["lune brisée", "serpent de fibre", "cœur en silicium",
                    "miroir fractal", "étoile noire", "anneau de données",
                    "phénix de code", "lotus quantique", "œil de Schrödinger",
                    "spirale d'ADN synthétique", "ouroboros de feedback loop",
                    "ankh de clonage"],
        "oniric_tags": ["<burn>", "<rain>", "<shadow>", "<static>", "<void>",
                        "<glitch>", "<pulse>", "<echo>", "<fracture>", "<abyss>",
                        "<neon>", "<vortex>", "<whisper>", "<overload>", "<decay>",
                        "<surge>", "<rift>", "<mirage>", "<reboot>", "<corrupt>",
                        "<loop>", "<merge>", "<awaken>", "<dream>", "<eclipse>",
                        "<invoke>", "<fuse>", "<sanctify>", "<prophesy>", "<sigil>"],
    }

LEXICON = load_oniric_lexicon()

THEME_TEMPLATES = {
    "protection": [
        "Que le {Symbole} {Action} ton {Nom} du {Défaut}! {oniric}",
        "Ô {Adjectif} {Nom}, sois protégé par le {Symbole} ancien.",
        "Le {Symbole} consume les ombres. {oniric}",
    ],
    "voyage": [
        "Dans le {Paysage}, que ton {Nom} trouve la voie. {oniric}",
        "Que le {Symbole} guide tes pas dans le désert {Adjectif}.",
        "Le {Nom} n'est pas perdu — il {Action} dans le {Paysage}. {oniric}",
    ],
    "rituel": [
        "Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}. {oniric}",
        "Ô {Adjectif} {Nom}, sois {VerbeMystique} par le rite ancien.",
        "Le {Symbole} et le {Nom} dansent le rite {Adjectif}. {oniric}",
    ],
    "silence": [
        "Que le {Symbole} efface le bruit. {oniric}",
        "Dans le {Adjectif} silence, seul le {Nom} persiste.",
        "Le {Symbole} {Action} le {Défaut} pour {Bénéfice}. {oniric}",
    ],
}
THEMES = list(THEME_TEMPLATES.keys())

# ═══════════════════════════════════════════════════════════════════════════════
# [PARENT 1] CLASSES DE BASE (Mantra, SoufiMantraGA)
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
        return {
            "length": len(words),
            "has_rhyme": self.detect_rhyme(words),
            "has_alliteration": self.detect_alliteration(words),
            "emotion_score": self.emotion_intensity(words),
            "oniric_tag": self.extract_oniric_tag(),
        }
    
    def extract_oniric_tag(self):
        for tag in LEXICON["oniric_tags"]:
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
    
    def emotion_intensity(self, words):
        emo_words = ["amour", "silence", "brûle", "rêve", "oubli", "vérité", "cœur", "sacré", "purifie"]
        return sum(1 for w in words if w in emo_words)

class SoufiMantraGA:
    def __init__(self, population_size: int = 10, theme: str = "protection", rng: Optional[random.Random] = None):
        self.population_size = population_size
        self.theme = theme
        self.population: List[Mantra] = []
        self.templates = THEME_TEMPLATES.get(theme, THEME_TEMPLATES["protection"])
        self.rng = rng or random.Random()
    
    def fill_template(self, template: str) -> str:
        content = template
        replacements = {
            "Adjectif": self.rng.choice(LEXICON["Adjectif"]),
            "Nom": self.rng.choice(LEXICON["Nom"]),
            "Action": self.rng.choice(LEXICON["Action"]),
            "Bénéfice": self.rng.choice(LEXICON["Bénéfice"]),
            "Défaut": self.rng.choice(LEXICON["Défaut"]),
            "Paysage": self.rng.choice(LEXICON["Paysage"]),
            "VerbeMystique": self.rng.choice(LEXICON["VerbeMystique"]),
            "Symbole": self.rng.choice(LEXICON["Symbole"]),
            "oniric": self.rng.choice(LEXICON["oniric_tags"]) if self.rng.random() < 0.6 else "",
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
            words = self.rng.sample(LEXICON["Nom"] + LEXICON["Adjectif"], k=min(5, len(LEXICON["Nom"])))
            content = " ".join(words) + "."
            self.population.append(Mantra(id=f"R{self.rng.randint(1000, 9999)}", content=content, theme=self.theme))
    
    def calculate_fitness(self, mantra: Mantra) -> float:
        comp = mantra.components
        theme_words = {
            "protection": ["protège", "garde", "bouclier"],
            "voyage": ["voyage", "chemin", "guide"],
            "rituel": ["rite", "cérémonie", "sacré"],
            "silence": ["silence", "calme", "paix"],
        }
        theme_match = sum(1 for w in theme_words.get(self.theme, []) if w in mantra.content.lower())
        style_score = (1.2 if comp["has_rhyme"] else 0) + (1.0 if comp["has_alliteration"] else 0)
        oniric_bonus = 0.8 if comp["oniric_tag"] else 0
        emotion_bonus = comp["emotion_score"] * 0.3
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
    pool_key = rng.choice(["Adjectif", "Nom", "Action", "Symbole", "VerbeMystique"])
    words[idx] = rng.choice(LEXICON[pool_key])
    if rng.random() < 0.4:
        new_tag = rng.choice(LEXICON["oniric_tags"])
        stripped = " ".join(w for w in words if not (w.startswith("<") and w.endswith(">")))
        words = stripped.split() + [new_tag]
    return " ".join(words)

# ═══════════════════════════════════════════════════════════════════════════════
# [PARENT 2] CulturalGenome
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class CulturalGenome:
    species: str = "Narrateur"
    breed: str = "Standard"
    generation: int = 0
    preferred_theme: str = field(default_factory=lambda: random.choice(THEMES))
    keywords: List[str] = field(default_factory=lambda: random.sample(
        LEXICON["Nom"] + LEXICON["Symbole"], k=3))
    glyph_symbol: str = field(default_factory=lambda: random.choice(
        ["spiral", "circle", "cross", "serpentiform", "hand", "asterisk", "wavy_line"]))
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
        "Scribes": 0.2, "Hérauts": 0.2, "Anachorètes": 0.2, "Colporteurs": 0.2, "Iconoclastes": 0.2
    })
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    creator: str = "System"
    
    def __post_init__(self):
        total = sum(self.guild_affinity.values())
        if total > 0:
            self.guild_affinity = {k: v / total for k, v in self.guild_affinity.items()}
    
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
        new_keywords = list(self.keywords)
        if rng.random() < mutation_rate:
            new_keywords[rng.randrange(len(new_keywords))] = rng.choice(LEXICON["Nom"] + LEXICON["Symbole"])
        return CulturalGenome(
            species=self.species, breed=self.breed, generation=self.generation + 1,
            preferred_theme=self.preferred_theme if rng.random() > mutation_rate else rng.choice(THEMES),
            keywords=new_keywords,
            glyph_symbol=self.glyph_symbol,
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

# ═══════════════════════════════════════════════════════════════════════════════
# [PARENT 2] CulturalStatus et MemeStrain
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
    
    @staticmethod
    def compute_virulence(mantra: Mantra, base: float = 1.0) -> float:
        comp = mantra.components
        style_bonus = (0.3 if comp["has_rhyme"] else 0) + (0.2 if comp["has_alliteration"] else 0)
        emotion_bonus = comp["emotion_score"] * 0.15
        oniric_bonus = 0.25 if comp["oniric_tag"] else 0
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

# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.0] MÉMOIRE COLLECTIVE + RELIQUES + MYTHES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class CollectiveMemory:
    """Trace l'historique des récits dominants par zone."""
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
    """Mantra préservé par un Anachorète — immunisé contre l'oubli."""
    relic_id: str
    mantra: Mantra
    guardian_id: int
    zone: str
    preserved_at: int
    veneration_count: int = 0

@dataclass
class FoundingMyth:
    """Mythe fondateur : agrégation poétique des mantras dominants."""
    myth_id: str
    title: str
    verses: List[str]
    dominant_strains: List[str]
    created_at: int

@dataclass
class RandomEvent:
    """Événement aléatoire : schisme, prophétie, censure, réformation."""
    event_id: str
    event_type: str  # "schism", "prophecy", "censorship", "reformation", "pilgrimage", "relic"
    timestamp: int
    zone: Optional[str]
    description: str
    affected_agents: List[int]
    impact: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] CulturalPhenotype
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

# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] CulturalAgent
# ═══════════════════════════════════════════════════════════════════════════════
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
        self.mantra_history: List[Tuple[int, str]] = []  # [NOUVEAU] historique des mantras portés
        self.influence_score: float = 0.0  # [NOUVEAU] score d'influence accumulé
        self.is_relic_guardian: bool = False  # [NOUVEAU] gardien d'une relique
        self.relic_id: Optional[str] = None
    
    def receive_mantra(self, strain: MemeStrain):
        self.current_strain = strain
        self.personal_mantra = strain.mantra
        self.meme_virulence = MemeStrain.compute_virulence(strain.mantra, base=strain.contagion_power)
        self.narrative_coherence = min(1.0, 0.4 + strain.mantra.fitness * 0.5)
        self.mantra_history.append((self.current_t, strain.strain_id))
        logger.debug(f"Agent#{self.id} reçoit mantra {strain.strain_id}: «{strain.mantra.content[:50]}...»")
    
    def is_culture_influencer(self) -> bool:
        return self.phenotype.phenotypes["is_culture_influencer"]

# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] CulturalEpidemicSimulation — v2.0 avec événements aléatoires
# ═══════════════════════════════════════════════════════════════════════════════
class CulturalEpidemicSimulation:
    def __init__(self, params: dict, genome_pool: Optional[List[CulturalGenome]] = None):
        self.params = params
        self.rng = random.Random(params.get("seed", 42))
        self.current_t = 0
        self.zones = self._generate_zones()
        
        # --- Souche-racine ---
        root_theme = params.get("root_theme", "rituel")
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
        )
        self.meme_strains: Dict[str, MemeStrain] = {"M-001": self.root_strain}
        self.strain_counter = 1
        
        self.agents: List[CulturalAgent] = []
        self.events: List[NarrativeEvent] = []
        self.interactions: List[InteractionRecord] = []
        self.random_events: List[RandomEvent] = []  # [NOUVEAU]
        self.relics: List[Relic] = []  # [NOUVEAU]
        self.founding_myths: List[FoundingMyth] = []  # [NOUVEAU]
        self.chronicle: List[Dict] = []  # [NOUVEAU] chronologie narrative
        self.relic_counter = 0
        self.myth_counter = 0
        self.event_counter = 0
        
        self.transmission_network = nx.DiGraph() if HAS_NX else _MiniDiGraph()
        self.daily_metrics = defaultdict(lambda: defaultdict(int))
        self.rt_history: List[float] = []
        self.serial_intervals: List[int] = []
        self.zone_agent_index: Dict[str, List[CulturalAgent]] = defaultdict(list)
        
        # [NOUVEAU] Systèmes narratifs avancés
        self.collective_memory = CollectiveMemory()
        self.semantic_drift: Dict[str, List[str]] = defaultdict(list)  # évolution des mots par souche
        
        self._init_population(genome_pool)
        logger.info(f"Simulation initialisée : {len(self.agents)} agents sur {len(self.zones)} zones")
        logger.debug(f"Souche racine : {self.root_strain.strain_id} — «{self.root_strain.mantra.content}»")
    
    def _generate_zones(self) -> List[str]:
        zones = ["Agora_Centrale", "Marché_Souterrain", "Forum_Diffus",
                 "Sanctuaire_Reclus", "Carrefour_Nomade", "Archives_Oubliées"]
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
    
    # -------------------------------------------------------------------
    # Exposition + Progression + Transmission
    # -------------------------------------------------------------------
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
                logger.debug(f"t={self.current_t} Agent#{agent.id} sombre dans l'oubli")
    
    def transmit_meme(self, agent_a: CulturalAgent, agent_b: CulturalAgent) -> bool:
        if agent_a.cultural_status not in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
            return False
        if agent_b.cultural_status != CulturalStatus.RECEPTIVE:
            return False
        virulence = agent_a.meme_virulence * agent_a.phenotype.phenotypes["contagiousness"]
        if agent_a.cultural_status == CulturalStatus.SILENT_CARRIER:
            virulence *= 0.4
        p_transmission = min(0.95, 0.12 * virulence * agent_b.receptivity)
        occurred = self.rng.random() < p_transmission
        self.interactions.append(InteractionRecord(
            timestamp=self.current_t, agent_a=agent_a.id, agent_b=agent_b.id,
            intensity=virulence, transmission_risk=p_transmission, transmission_occurred=occurred,
        ))
        if occurred:
            self._expose_agent(agent_b, agent_a, agent_a.current_strain)
            logger.debug(f"t={self.current_t} Transmission : Agent#{agent_a.id} → Agent#{agent_b.id} (souche {agent_a.current_strain.strain_id})")
        return occurred
    
    def _run_interaction_round(self):
        carriers = [a for a in self.agents if a.cultural_status in
                    (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        for carrier in carriers:
            n_targets = max(1, int(carrier.phenotype.phenotypes["interaction_rate"] * 3))
            targets = self.rng.sample(list(carrier.social_network), k=min(n_targets, len(carrier.social_network))) \
                if carrier.social_network else []
            for target_id in targets:
                target = self._agent_by_id(target_id)
                if target is not None:
                    self.transmit_meme(carrier, target)
    
    def _agent_by_id(self, agent_id: int) -> Optional[CulturalAgent]:
        if not hasattr(self, "_agent_lookup"):
            self._agent_lookup = {a.id: a for a in self.agents}
        return self._agent_lookup.get(agent_id)
    
    # -------------------------------------------------------------------
    # Mutation de mème
    # -------------------------------------------------------------------
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
        mutated_text = mutate_mantra_text(parent.mantra.content, self.rng)
        new_mantra = Mantra(id=f"MUT{self.strain_counter}", content=mutated_text, theme=parent.mantra.theme)
        new_strain = MemeStrain(
            strain_id=f"MV-{self.strain_counter:03d}",
            parent_id=parent.strain_id,
            generation=parent.generation + 1,
            mutations=parent.mutations + [(f"lexical_shift_t{self.current_t}", self.rng.gauss(0, 0.1))],
            mantra=new_mantra,
            contagion_power=MemeStrain.compute_virulence(new_mantra, base=parent.contagion_power),
            dogma_intensity=parent.dogma_intensity * self.rng.lognormvariate(0, 0.08),
            latency_period=max(1.0, parent.latency_period * self.rng.lognormvariate(0, 0.1)),
            emergence_time=self.current_t,
        )
        self.meme_strains[new_strain.strain_id] = new_strain
        agent.receive_mantra(new_strain)
        self.semantic_drift[parent.strain_id].append(new_strain.strain_id)
        logger.info(f"t={self.current_t} 🧬 MUTATION : {parent.strain_id} → {new_strain.strain_id} «{new_mantra.content[:40]}...»")
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.0] ÉVÉNEMENTS ALÉATOIRES NARRATIFS
    # -------------------------------------------------------------------
    def _maybe_trigger_random_event(self):
        """Déclenche des événements narratifs rares mais puissants."""
        event_prob = self.params.get("random_event_prob", 0.03)
        if self.rng.random() >= event_prob:
            return
        
        event_type = self.rng.choice([
            "schism", "prophecy", "censorship", "reformation",
            "pilgrimage", "relic_creation", "oracle_whisper"
        ])
        
        if event_type == "schism":
            self._trigger_schism()
        elif event_type == "prophecy":
            self._trigger_prophecy()
        elif event_type == "censorship":
            self._trigger_censorship()
        elif event_type == "reformation":
            self._trigger_reformation()
        elif event_type == "pilgrimage":
            self._trigger_pilgrimage()
        elif event_type == "relic_creation":
            self._trigger_relic_creation()
        elif event_type == "oracle_whisper":
            self._trigger_oracle_whisper()
    
    def _trigger_schism(self):
        """Schisme : une souche dominante se divise en deux variantes rivales."""
        dominant_strains = Counter(
            a.current_strain.strain_id for a in self.agents
            if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
        ).most_common(1)
        if not dominant_strains:
            return
        parent_id = dominant_strains[0][0]
        parent = self.meme_strains[parent_id]
        
        self.strain_counter += 1
        schism_text = mutate_mantra_text(parent.mantra.content, self.rng)
        schism_mantra = Mantra(id=f"SCH{self.strain_counter}", content=schism_text, theme=parent.mantra.theme)
        schism_strain = MemeStrain(
            strain_id=f"SC-{self.strain_counter:03d}",
            parent_id=parent_id, generation=parent.generation + 1,
            mutations=parent.mutations + [("schism", 0.5)],
            mantra=schism_mantra,
            contagion_power=parent.contagion_power * self.rng.uniform(0.8, 1.3),
            dogma_intensity=parent.dogma_intensity * 1.5,
            latency_period=parent.latency_period,
            emergence_time=self.current_t,
        )
        self.meme_strains[schism_strain.strain_id] = schism_strain
        
        # Conversion forcée de 30% des porteurs de la souche parente
        carriers = [a for a in self.agents if a.current_strain.strain_id == parent_id
                    and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        affected = []
        for agent in self.rng.sample(carriers, k=min(len(carriers), max(1, len(carriers) // 3))):
            agent.receive_mantra(schism_strain)
            affected.append(agent.id)
        
        self.event_counter += 1
        zone = self.rng.choice(self.zones)
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="schism",
            timestamp=self.current_t,
            zone=zone,
            description=f"🔱 SCHISME : La souche {parent_id} se scinde. Naissance de {schism_strain.strain_id}",
            affected_agents=affected,
            impact={"parent": parent_id, "child": schism_strain.strain_id},
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "schism", "event": event.event_id})
        logger.warning(f"t={self.current_t} 🔱 SCHISME dans {zone} : {parent_id} → {schism_strain.strain_id} ({len(affected)} convertis)")
    
    def _trigger_prophecy(self):
        """Prophétie : un mantra mystique apparaît et convertit massivement."""
        ga = SoufiMantraGA(theme=self.rng.choice(THEMES), rng=self.rng)
        ga.initialize_population()
        ga.evolve(generations=6)
        prophetic_mantra = ga.get_best_mantra()
        prophetic_mantra.content = "🜃 PROPHÉTIE : " + prophetic_mantra.content
        
        self.strain_counter += 1
        prophetic_strain = MemeStrain(
            strain_id=f"PR-{self.strain_counter:03d}",
            parent_id=None, generation=0,
            mutations=[("prophecy", 1.0)],
            mantra=prophetic_mantra,
            contagion_power=self.params.get("r0_base", 2.2) * 1.5,
            dogma_intensity=50.0,
            latency_period=1.0,
            emergence_time=self.current_t,
        )
        self.meme_strains[prophetic_strain.strain_id] = prophetic_strain
        
        # Exposition massive
        targets = self.rng.sample(self.agents, k=min(len(self.agents) // 4, 30))
        affected = []
        for agent in targets:
            if agent.cultural_status == CulturalStatus.RECEPTIVE:
                self._expose_agent(agent, None, prophetic_strain, force=True)
                affected.append(agent.id)
        
        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="prophecy",
            timestamp=self.current_t,
            zone=None,
            description=f"🜃 PROPHÉTIE : «{prophetic_mantra.content[:60]}...»",
            affected_agents=affected,
            impact={"strain": prophetic_strain.strain_id},
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "prophecy", "event": event.event_id})
        logger.warning(f"t={self.current_t} 🜃 PROPHÉTIE : {len(affected)} nouveaux convertis")
    
    def _trigger_censorship(self):
        """Censure : une zone devient immunisée contre une souche."""
        zone = self.rng.choice(self.zones)
        target_strains = list(self.meme_strains.keys())[:3]
        if not target_strains:
            return
        
        affected = []
        for agent in self.zone_agent_index[zone]:
            if agent.current_strain.strain_id in target_strains:
                if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                    agent.cultural_status = CulturalStatus.DISENCHANTED
                    agent.disenchant_time = self.current_t
                    affected.append(agent.id)
                agent.receptivity *= 0.3  # immunisation partielle
        
        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="censorship",
            timestamp=self.current_t,
            zone=zone,
            description=f"🚫 CENSURE à {zone} : les souches {target_strains} y sont bannies",
            affected_agents=affected,
            impact={"zone": zone, "banned_strains": target_strains},
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "censorship", "event": event.event_id})
        logger.warning(f"t={self.current_t} 🚫 CENSURE à {zone} : {len(affected)} évangélistes réduits au silence")
    
    def _trigger_reformation(self):
        """Réformation : un mantra purifié restaure la cohérence narrative."""
        carriers = [a for a in self.agents if a.cultural_status == CulturalStatus.EVANGELIST]
        if not carriers:
            return
        agent = self.rng.choice(carriers)
        old_strain = agent.current_strain
        
        # Purification du mantra : on garde la structure mais on remplace les mots corrompus
        purified_words = []
        for word in old_strain.mantra.content.split():
            if word.startswith("<") and word.endswith(">"):
                purified_words.append(self.rng.choice(["<sanctify>", "<awaken>", "<reveal>"]))
            else:
                purified_words.append(word)
        purified_text = " ".join(purified_words)
        purified_mantra = Mantra(id=f"REF{self.strain_counter+1}", content=purified_text, theme=old_strain.mantra.theme)
        
        self.strain_counter += 1
        reformed_strain = MemeStrain(
            strain_id=f"RF-{self.strain_counter:03d}",
            parent_id=old_strain.strain_id,
            generation=old_strain.generation + 1,
            mutations=old_strain.mutations + [("reformation", -0.3)],
            mantra=purified_mantra,
            contagion_power=old_strain.contagion_power * 1.2,
            dogma_intensity=old_strain.dogma_intensity * 0.5,
            latency_period=old_strain.latency_period * 0.8,
            emergence_time=self.current_t,
        )
        self.meme_strains[reformed_strain.strain_id] = reformed_strain
        
        # Adoption par tous les évangélistes de la même souche
        affected = []
        for a in self.agents:
            if a.current_strain.strain_id == old_strain.strain_id and a.cultural_status in (
                CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                a.receive_mantra(reformed_strain)
                affected.append(a.id)
        
        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="reformation",
            timestamp=self.current_t,
            zone=agent.zone,
            description=f"✨ RÉFORMATION : {old_strain.strain_id} purifiée en {reformed_strain.strain_id}",
            affected_agents=affected,
            impact={"old": old_strain.strain_id, "new": reformed_strain.strain_id},
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "reformation", "event": event.event_id})
        logger.warning(f"t={self.current_t} ✨ RÉFORMATION : {len(affected)} adeptes adoptent la version purifiée")
    
    def _trigger_pilgrimage(self):
        """Pèlerinage : agents migrent vers la zone où leur souche domine."""
        zone_dominance = {}
        for zone in self.zones:
            dominant = self.collective_memory.get_dominant_strain(zone, self.current_t)
            if dominant:
                zone_dominance[zone] = dominant
        
        if not zone_dominance:
            return
        
        migrants = []
        for agent in self.agents:
            if agent.cultural_status not in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                continue
            if agent.genome.mobility < 0.6:
                continue
            # Cherche la zone où sa souche domine
            target_zone = None
            for z, s in zone_dominance.items():
                if s == agent.current_strain.strain_id and z != agent.zone:
                    target_zone = z
                    break
            if target_zone and self.rng.random() < 0.3:
                self.zone_agent_index[agent.zone].remove(agent)
                agent.zone = target_zone
                self.zone_agent_index[target_zone].append(agent)
                migrants.append(agent.id)
        
        if migrants:
            self.event_counter += 1
            event = RandomEvent(
                event_id=f"EVT-{self.event_counter:03d}",
                event_type="pilgrimage",
                timestamp=self.current_t,
                zone=None,
                description=f"🕊 PÈLERINAGE : {len(migrants)} croyants migrent vers leurs terres saintes",
                affected_agents=migrants,
                impact={"migrants": len(migrants)},
            )
            self.random_events.append(event)
            self.chronicle.append({"t": self.current_t, "type": "pilgrimage", "event": event.event_id})
            logger.info(f"t={self.current_t} 🕊 PÈLERINAGE : {len(migrants)} agents en migration")
    
    def _trigger_relic_creation(self):
        """Création de relique : un Anachorète préserve un mantra ancien."""
        anachoretes = [a for a in self.agents if a.guild == "Anachorètes"
                       and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER, CulturalStatus.DISENCHANTED)
                       and not a.is_relic_guardian]
        if not anachoretes:
            return
        
        guardian = self.rng.choice(anachoretes)
        self.relic_counter += 1
        relic = Relic(
            relic_id=f"REL-{self.relic_counter:03d}",
            mantra=guardian.current_strain.mantra,
            guardian_id=guardian.id,
            zone=guardian.zone,
            preserved_at=self.current_t,
        )
        self.relics.append(relic)
        guardian.is_relic_guardian = True
        guardian.relic_id = relic.relic_id
        guardian.receptivity *= 0.2  # immunisé par la relique
        
        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="relic_creation",
            timestamp=self.current_t,
            zone=guardian.zone,
            description=f"📜 RELIQUE : Agent#{guardian.id} préserve «{relic.mantra.content[:40]}...»",
            affected_agents=[guardian.id],
            impact={"relic": relic.relic_id},
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "relic", "event": event.event_id})
        logger.warning(f"t={self.current_t} 📜 RELIQUE créée par Agent#{guardian.id} à {guardian.zone}")
    
    def _trigger_oracle_whisper(self):
        """Oracle : une voix murmure une tendance future."""
        # Prédiction basée sur les tendances actuelles
        status_counts = Counter(a.cultural_status for a in self.agents)
        dominant_strain = Counter(
            a.current_strain.strain_id for a in self.agents
            if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
        ).most_common(1)
        
        prediction = "silence" if status_counts[CulturalStatus.OBLIVIOUS] > len(self.agents) * 0.3 else \
                     "expansion" if status_counts[CulturalStatus.EVANGELIST] > len(self.agents) * 0.2 else \
                     "stagnation"
        
        self.event_counter += 1
        event = RandomEvent(
            event_id=f"EVT-{self.event_counter:03d}",
            event_type="oracle_whisper",
            timestamp=self.current_t,
            zone=None,
            description=f"🔮 ORACLE murmure : «L'avenir est {prediction}...»",
            affected_agents=[],
            impact={"prediction": prediction, "dominant_strain": dominant_strain[0][0] if dominant_strain else None},
        )
        self.random_events.append(event)
        self.chronicle.append({"t": self.current_t, "type": "oracle", "event": event.event_id})
        logger.info(f"t={self.current_t} 🔮 ORACLE : tendance prédite = {prediction}")
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.0] GÉNÉRATION DE MYTHES FONDATEURS
    # -------------------------------------------------------------------
    def _maybe_generate_myth(self):
        """Agrège les mantras dominants en un mythe fondateur."""
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
        logger.info(f"t={self.current_t} 📖 MYTHE FONDATEUR créé : {myth.myth_id} ({len(verses)} versets)")
    
    # -------------------------------------------------------------------
    # Boucle principale
    # -------------------------------------------------------------------
    def _calculate_rt(self) -> float:
        recent = [e for e in self.events if e.event_type == "exposure" and e.timestamp > self.current_t - 5]
        infectors = [e.source_id for e in recent if e.source_id]
        if not infectors:
            return 0.0
        counts = Counter(infectors)
        return sum(counts.values()) / len(counts)
    
    def step(self) -> dict:
        # Invalider le lookup à chaque step
        if hasattr(self, "_agent_lookup"):
            del self._agent_lookup
        
        self._run_interaction_round()
        self.mutate_meme()
        self._maybe_trigger_random_event()
        self._maybe_generate_myth()
        
        for agent in self.agents:
            self._progress_narrative(agent)
        
        for status in CulturalStatus:
            self.daily_metrics[self.current_t][f"cult_{status.value}"] = sum(
                1 for a in self.agents if a.cultural_status == status)
        self.daily_metrics[self.current_t]["nb_strains"] = len(self.meme_strains)
        self.daily_metrics[self.current_t]["nb_relics"] = len(self.relics)
        self.daily_metrics[self.current_t]["nb_myths"] = len(self.founding_myths)
        
        rt = self._calculate_rt()
        self.rt_history.append(rt)
        
        logger.debug(f"t={self.current_t} | Rt={rt:.2f} | Souches={len(self.meme_strains)} | Reliques={len(self.relics)}")
        
        self.current_t += 1
        for agent in self.agents:
            agent.current_t = self.current_t
        
        return {"t": self.current_t, "rt": rt, "metrics": dict(self.daily_metrics[self.current_t - 1])}
    
    def run(self, steps: int):
        for _ in range(steps):
            yield self.step()


def run_cultural_epidemic_simulation(params: dict, genome_pool: Optional[List[CulturalGenome]] = None,
                                     steps: int = 60, verbose: bool = False) -> CulturalEpidemicSimulation:
    sim = CulturalEpidemicSimulation(params, genome_pool)
    for snapshot in sim.run(steps):
        if verbose:
            m = snapshot["metrics"]
            print(f"[t={snapshot['t']:>3}] Rt={snapshot['rt']:.2f} | "
                  f"É={m.get('cult_I', 0)} PS={m.get('cult_A', 0)} "
                  f"Dés={m.get('cult_R', 0)} Oub={m.get('cult_D', 0)} "
                  f"Souches={m.get('nb_strains', 0)} Reliques={m.get('nb_relics', 0)}")
    return sim


# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] Visualisation
# ═══════════════════════════════════════════════════════════════════════════════
STATUS_COLORS = {
    CulturalStatus.RECEPTIVE: "#4a7a8a",
    CulturalStatus.EXPOSED: "#f5c518",
    CulturalStatus.EVANGELIST: "#ff2d78",
    CulturalStatus.SILENT_CARRIER: "#ff8c42",
    CulturalStatus.DISENCHANTED: "#00ff9d",
    CulturalStatus.OBLIVIOUS: "#8888aa",
}

_GLYPH_DRAWERS = {
    "circle": lambda ax, x, y, s, c: ax.add_patch(patches.Circle((x, y), 20 * s, fill=False, edgecolor=c, linewidth=2)),
    "spiral": None,
    "cross": lambda ax, x, y, s, c: (
        ax.plot([x - 20 * s, x + 20 * s], [y, y], color=c, linewidth=2),
        ax.plot([x, x], [y - 20 * s, y + 20 * s], color=c, linewidth=2)),
    "hand": lambda ax, x, y, s, c: ax.add_patch(patches.Circle((x, y), 15 * s, fill=False, edgecolor=c, linewidth=2)),
    "serpentiform": None,
    "asterisk": lambda ax, x, y, s, c: [
        ax.plot([x, x + 18 * s * math.cos(math.radians(a))], [y, y + 18 * s * math.sin(math.radians(a))],
                color=c, linewidth=2) for a in [0, 45, 90, 135]
    ],
    "wavy_line": None,
}

def render_agent_glyph(agent: CulturalAgent, ax=None):
    color = STATUS_COLORS[agent.cultural_status]
    sym = agent.genome.glyph_symbol
    if not HAS_MPL:
        return f"[{sym}] agent#{agent.id} status={agent.cultural_status.name} color={color}"
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(3, 3))
        fig.patch.set_facecolor("#0b0b12")
        ax.set_facecolor("#0b0b12")
        ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal"); ax.axis("off")
        x, y, scale = 50, 50, 1.5
    else:
        x, y, scale = agent.plot_x, agent.plot_y, 0.6
    drawer = _GLYPH_DRAWERS.get(sym)
    if drawer:
        drawer(ax, x, y, scale, color)
    elif sym == "spiral":
        theta = [i * 0.2 for i in range(60)]
        r = [t * 2.5 * scale for t in theta]
        xs = [x + rr * math.cos(t) for t, rr in zip(theta, r)]
        ys = [y + rr * math.sin(t) for t, rr in zip(theta, r)]
        ax.plot(xs, ys, color=color, linewidth=1.8)
    else:
        ax.add_patch(patches.Circle((x, y), 12 * scale, fill=True, color=color, alpha=0.6))
    if own_fig:
        ax.text(50, 8, agent.personal_mantra.content[:40] + "…" if agent.personal_mantra else "",
                fontsize=6, color=color, ha="center")
        return fig
    return None

def draw_cultural_network(sim: CulturalEpidemicSimulation):
    if not (HAS_MPL and HAS_NX):
        return None
    G = sim.transmission_network
    if G.number_of_nodes() == 0:
        return None
    layout = nx.spring_layout(G, seed=42, k=1.5)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor("#0b0b12"); ax.set_facecolor("#0b0b12"); ax.axis("off")
    for u, v in G.edges():
        x0, y0 = layout[u]; x1, y1 = layout[v]
        ax.plot([x0, x1], [y0, y1], color="#333355", linewidth=0.6, alpha=0.6, zorder=1)
    for a in sim.agents:
        if a.id not in layout:
            continue
        x, y = layout[a.id]
        a.plot_x, a.plot_y = x * 40 + 50, y * 40 + 50
        color = STATUS_COLORS[a.cultural_status]
        size = 60 if a.is_relic_guardian else 40
        ax.scatter([x], [y], s=size, color=color, zorder=2, edgecolors="#111", linewidths=0.4)
    ax.set_title("Réseau narratif — ArcheoEpidemic Chimera v2.0", color="#cccccc", fontsize=11)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION + NOUVEAU] RAPPORT MYTHOLOGIQUE ÉTENDU
# ═══════════════════════════════════════════════════════════════════════════════
def mythological_report(sim: CulturalEpidemicSimulation) -> str:
    lines = []
    lines.append("═" * 70)
    lines.append("  📖 RAPPORT MYTHOLOGIQUE — ArcheoEpidemic Chimera v2.0")
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
            lines.append(f"      contagion={strain.contagion_power:.2f}  dogme={strain.dogma_intensity:.2f}")
    else:
        lines.append("  Silence collectif.")
    
    lines.append("\n— Superspreaders culturels (Saints Patrons) —")
    out_degrees = [(a, sim.transmission_network.out_degree(a.id) if sim.transmission_network.has_node(a.id) else 0)
                   for a in sim.agents]
    out_degrees.sort(key=lambda t: t[1], reverse=True)
    for agent, deg in out_degrees[:5]:
        if deg == 0:
            break
        relic_mark = " 📜" if agent.is_relic_guardian else ""
        lines.append(f"  Agent#{agent.id:<4}{relic_mark} guilde={agent.guild:<12} zone={agent.zone:<18} "
                     f"transmissions={deg}  influence={agent.influence_score:.1f}")
    
    lines.append(f"\n— Évolution narrative —")
    lines.append(f"  Souches totales : {len(sim.meme_strains)}")
    max_gen = max((s.generation for s in sim.meme_strains.values()), default=0)
    lines.append(f"  Générations de mutation : {max_gen}")
    if sim.serial_intervals:
        lines.append(f"  Intervalle sériel moyen : {sum(sim.serial_intervals)/len(sim.serial_intervals):.2f} pas")
    
    # [NOUVEAU] Reliques
    lines.append(f"\n— Reliques sacrées ({len(sim.relics)}) —")
    for relic in sim.relics[:5]:
        lines.append(f"  {relic.relic_id} (préservée t={relic.preserved_at} à {relic.zone})")
        lines.append(f"    Gardien : Agent#{relic.guardian_id}")
        lines.append(f"    « {relic.mantra.content[:60]}... »")
    
    # [NOUVEAU] Mythes fondateurs
    lines.append(f"\n— Mythes fondateurs ({len(sim.founding_myths)}) —")
    for myth in sim.founding_myths:
        lines.append(f"  {myth.myth_id} — « {myth.title} » (t={myth.created_at})")
        for i, verse in enumerate(myth.verses, 1):
            lines.append(f"    {i}. {verse}")
    
    # [NOUVEAU] Événements aléatoires
    lines.append(f"\n— Chronique des événements ({len(sim.random_events)}) —")
    for evt in sim.random_events[-10:]:
        lines.append(f"  [t={evt.timestamp}] {evt.description}")
    
    # [NOUVEAU] Dérive sémantique
    lines.append(f"\n— Dérive sémantique (lignées de mutation) —")
    for parent, children in list(sim.semantic_drift.items())[:5]:
        if children:
            lines.append(f"  {parent} → {', '.join(children[:3])}{'...' if len(children) > 3 else ''}")
    
    lines.append("\n" + "═" * 70)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.0] EXPORT DES DONNÉES
# ═══════════════════════════════════════════════════════════════════════════════
def export_simulation_data(sim: CulturalEpidemicSimulation, output_dir: str):
    """Exporte toutes les données de simulation en JSON."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    # Paramètres
    with open(out / "params.json", "w", encoding="utf-8") as f:
        json.dump(sim.params, f, indent=2, ensure_ascii=False)
    
    # Souches
    strains_data = []
    for sid, s in sim.meme_strains.items():
        strains_data.append({
            "strain_id": s.strain_id,
            "parent_id": s.parent_id,
            "generation": s.generation,
            "mantra": s.mantra.content,
            "theme": s.mantra.theme,
            "contagion_power": s.contagion_power,
            "dogma_intensity": s.dogma_intensity,
            "latency_period": s.latency_period,
            "emergence_time": s.emergence_time,
        })
    with open(out / "strains.json", "w", encoding="utf-8") as f:
        json.dump(strains_data, f, indent=2, ensure_ascii=False)
    
    # Agents
    agents_data = []
    for a in sim.agents:
        agents_data.append({
            "id": a.id,
            "zone": a.zone,
            "guild": a.guild,
            "status": a.cultural_status.name,
            "current_strain": a.current_strain.strain_id,
            "influence_score": a.influence_score,
            "is_relic_guardian": a.is_relic_guardian,
            "mantra_history": a.mantra_history,
            "glyph_symbol": a.genome.glyph_symbol,
        })
    with open(out / "agents.json", "w", encoding="utf-8") as f:
        json.dump(agents_data, f, indent=2, ensure_ascii=False)
    
    # Événements narratifs
    events_data = [asdict(e) for e in sim.events]
    with open(out / "events.json", "w", encoding="utf-8") as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False)
    
    # Événements aléatoires
    random_events_data = [asdict(e) for e in sim.random_events]
    with open(out / "random_events.json", "w", encoding="utf-8") as f:
        json.dump(random_events_data, f, indent=2, ensure_ascii=False)
    
    # Reliques
    relics_data = []
    for r in sim.relics:
        relics_data.append({
            "relic_id": r.relic_id,
            "mantra": r.mantra.content,
            "guardian_id": r.guardian_id,
            "zone": r.zone,
            "preserved_at": r.preserved_at,
        })
    with open(out / "relics.json", "w", encoding="utf-8") as f:
        json.dump(relics_data, f, indent=2, ensure_ascii=False)
    
    # Mythes
    myths_data = [asdict(m) for m in sim.founding_myths]
    with open(out / "myths.json", "w", encoding="utf-8") as f:
        json.dump(myths_data, f, indent=2, ensure_ascii=False)
    
    # Chronique
    with open(out / "chronicle.json", "w", encoding="utf-8") as f:
        json.dump(sim.chronicle, f, indent=2, ensure_ascii=False)
    
    # Métriques quotidiennes
    metrics_data = {str(t): dict(m) for t, m in sim.daily_metrics.items()}
    with open(out / "daily_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2, ensure_ascii=False)
    
    # Rapport mythologique
    with open(out / "mythological_report.txt", "w", encoding="utf-8") as f:
        f.write(mythological_report(sim))
    
    logger.info(f"📦 Données exportées dans {out}/")


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.0] CLI EXHAUSTIVE
# ═══════════════════════════════════════════════════════════════════════════════
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="archeoepidemic_chimera",
        description="🧬🌌 ARCHEOEPIDEMIC CHIMERA v2.0 — Simulateur d'épidémies narratives",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # --- Paramètres généraux ---
    gen = p.add_argument_group("Général")
    gen.add_argument("--seed", type=int, default=2075, help="Graine aléatoire")
    gen.add_argument("--steps", type=int, default=60, help="Nombre de pas de temps")
    gen.add_argument("--verbose", action="store_true", help="Affichage pas-à-pas")
    gen.add_argument("--log-file", type=str, default=None, help="Fichier de log (niveau DEBUG)")
    gen.add_argument("--log-level", type=str, default="INFO",
                     choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                     help="Niveau de log console")
    gen.add_argument("--export-dir", type=str, default=None,
                     help="Répertoire d'export des données JSON")
    gen.add_argument("--export-network", type=str, default=None,
                     help="Chemin PNG du réseau narratif")
    
    # --- Population ---
    pop = p.add_argument_group("Population")
    pop.add_argument("--pop-total", type=int, default=180, help="Nombre total d'agents")
    pop.add_argument("--nb-zones", type=int, default=6, help="Nombre de zones narratives")
    pop.add_argument("--initial-believers", type=int, default=3, help="Croyants initiaux")
    
    # --- Souche racine ---
    root = p.add_argument_group("Souche racine")
    root.add_argument("--root-theme", type=str, default="rituel",
                      choices=THEMES, help="Thème du mantra racine")
    root.add_argument("--r0-base", type=float, default=2.4, help="R0 de base (contagion)")
    root.add_argument("--latency-period", type=float, default=3.0,
                      help="Période de latence (internalisation)")
    
    # --- Dynamiques ---
    dyn = p.add_argument_group("Dynamiques narratives")
    dyn.add_argument("--disenchant-rate", type=float, default=0.04,
                     help="Taux de désenchantement")
    dyn.add_argument("--oblivion-rate", type=float, default=0.003,
                     help="Taux d'oubli (burnout)")
    dyn.add_argument("--mutation-prob", type=float, default=0.02,
                     help="Probabilité de mutation par pas")
    dyn.add_argument("--dogma-rate", type=float, default=0.01,
                     help="Intensité dogmatique de base")
    
    # --- [NOUVEAU] Événements aléatoires ---
    evt = p.add_argument_group("Événements aléatoires (v2.0)")
    evt.add_argument("--random-event-prob", type=float, default=0.03,
                     help="Probabilité d'événement aléatoire par pas")
    evt.add_argument("--myth-generation-period", type=int, default=20,
                     help="Période de génération des mythes")
    evt.add_argument("--max-myths", type=int, default=3,
                     help="Nombre maximum de mythes fondateurs")
    
    return p


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    
    # Configuration des logs
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    
    logger.info("🌌🧬 Démarrage d'ArcheoEpidemic Chimera v2.0 — Normandie Fractale, 2075")
    logger.info("Fusion : Glyphosophia (mantras/glyphes) × Corrupted Blood (épidémie agent-based)")
    logger.info("Ajouts v2.0 : événements aléatoires, reliques, mythes, oracle, CLI exhaustive")
    logger.debug(f"Arguments : {vars(args)}")
    
    params = {
        "seed": args.seed,
        "pop_total": args.pop_total,
        "nb_zones": args.nb_zones,
        "initial_believers": args.initial_believers,
        "root_theme": args.root_theme,
        "r0_base": args.r0_base,
        "disenchant_rate": args.disenchant_rate,
        "oblivion_rate": args.oblivion_rate,
        "mutation_prob": args.mutation_prob,
        "dogma_rate": args.dogma_rate,
        "latency_period": args.latency_period,
        "random_event_prob": args.random_event_prob,
        "myth_generation_period": args.myth_generation_period,
        "max_myths": args.max_myths,
    }
    
    sim = run_cultural_epidemic_simulation(params, steps=args.steps, verbose=args.verbose)
    
    print()
    print(mythological_report(sim))
    
    # Export des données
    if args.export_dir:
        export_simulation_data(sim, args.export_dir)
    
    # Export du réseau
    if args.export_network and HAS_MPL and HAS_NX:
        fig = draw_cultural_network(sim)
        if fig:
            fig.savefig(args.export_network, dpi=130, facecolor=fig.get_facecolor())
            logger.info(f"🖼  Réseau narratif exporté : {args.export_network}")
    elif args.export_network:
        logger.warning("matplotlib/networkx indisponibles — visualisation ignorée")


if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════════════════
# Fallback minimal si networkx est absent
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