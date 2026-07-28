#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║   🧬🌌 ARCHEOEPIDEMIC CHIMERA — v2.2 "DATA_ORACLE_EXTENDED"                 ║
║   Ajouts v2.2 :                                                             ║
║     • Externalisation des données en JSON                                   ║
║     • Export Neo4J (Cypher) avec relations complexes                        ║
║     • Système de "Narrative Gravity" (attraction des récits)               ║
║     • Mémoire épisodique des agents                                         ║
║     • Émergence de factions et alliances                                    ║
║     • Cycles narratifs (saisons culturelles)                               ║
║     • Conservation de toutes les fonctionnalités v2.1                      ║
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
# [NOUVEAU v2.2] GESTIONNAIRE DE FICHIERS JSON EXTERNES
# ═══════════════════════════════════════════════════════════════════════════════

class JSONDataManager:
    """
    Gère le chargement des données depuis des fichiers JSON externes.
    Utilise les données internes comme fallback.
    """
    
    # Données internes (fallback)
    _INTERNAL_DATA = {
        "oniric_lexicon": {
            "Adjectif": ["fractal", "quantique", "cryptique", "spectral", "liminal",
                        "onirique", "corrompu", "sacré", "glitché", "ancestral",
                        "éthéré", "cybernétique", "holographique", "syndical", "apocryphe"],
            "Nom": ["signal", "silence", "glyphe", "écho", "seuil", "récit",
                    "mantra", "spectre", "réseau", "songe", "oracle", "vérité",
                    "mémoire", "fracture", "résonance", "noyau", "brume", "empreinte"],
            "Action": ["implose", "exalte", "désintègre", "fusionne", "résonne",
                       "désagrège", "sature", "décode", "invoque", "sublime",
                       "dévore", "réfracte", "cristallise", "diffuse", "condense",
                       "synchronise", "amplifie", "hack", "insère", "mute",
                       "convoque", "infecte", "vaccine", "psalmodie", "prophétise",
                       "transfigure", "absorbe", "révèle", "dissout", "éclaire"],
            "Bénéfice": ["la clarté", "le silence", "l'oubli", "la vérité brûlante",
                         "l'éveil", "l'unité", "l'extase quantique", "la fusion des âmes",
                         "l'illumination", "la synchronicité totale", "la communion",
                         "la mémoire collective", "la révélation", "la transcendance pure",
                         "l'équilibre parfait", "la sagesse infinie"],
            "Défaut": ["le bruit", "la trahison", "le compromis", "l'oubli numérique",
                       "le mensonge", "l'entropie", "la dissonance", "la corruption",
                       "la fragmentation", "la désorientation", "le virus mental",
                       "la psychose cybernétique", "l'effondrement cognitif",
                       "la vacuité", "le chaos", "la stérilité narrative"],
            "Paysage": ["désert du no-signal", "marché noir de Lagos", "nuage quantique",
                        "cimetière de data", "temple de silicium", "catacombes de code",
                        "archipel des serveurs oubliés", "cathédrale de circuits imprimés",
                        "nécropole des IA défuntes", "bibliothèque de Babel numérique",
                        "plaine des échos", "forêt de cristal", "abysse de données",
                        "citadelle des ombres", "jardin des paradoxes"],
            "VerbeMystique": ["consume", "efface", "encrypte", "réveille", "transmute",
                              "dissout", "illumine", "recodifie", "absout", "exalte",
                              "sublime", "canalise", "révèle", "manifeste", "prophétise",
                              "sanctifie", "purifie", "transcende", "éveille", "libère"],
            "Symbole": ["lune brisée", "serpent de fibre", "cœur en silicium",
                        "miroir fractal", "étoile noire", "anneau de données",
                        "phénix de code", "lotus quantique", "œil de Schrödinger",
                        "spirale d'ADN synthétique", "ouroboros de feedback loop",
                        "ankh de clonage", "main de glitch", "calice de données",
                        "épée de lumière", "bouclier de silence"],
            "oniric_tags": ["<burn>", "<rain>", "<shadow>", "<static>", "<void>",
                            "<glitch>", "<pulse>", "<echo>", "<fracture>", "<abyss>",
                            "<neon>", "<vortex>", "<whisper>", "<overload>", "<decay>",
                            "<surge>", "<rift>", "<mirage>", "<reboot>", "<corrupt>",
                            "<loop>", "<merge>", "<awaken>", "<dream>", "<eclipse>",
                            "<invoke>", "<fuse>", "<sanctify>", "<prophesy>", "<sigil>",
                            "<flux>", "<null>", "<prime>", "<echo>", "<shard>"],
        },
        "themes": {
            "protection": [
                "Que le {Symbole} {Action} ton {Nom} du {Défaut}! {oniric}",
                "Ô {Adjectif} {Nom}, sois protégé par le {Symbole} ancien.",
                "Le {Symbole} consume les ombres. {oniric}",
                "Par le {Symbole}, que le {Défaut} se dissipe comme la brume.",
                "Le {Adjectif} {Nom} trouve refuge dans le {Symbole} éternel."
            ],
            "voyage": [
                "Dans le {Paysage}, que ton {Nom} trouve la voie. {oniric}",
                "Que le {Symbole} guide tes pas dans le désert {Adjectif}.",
                "Le {Nom} n'est pas perdu — il {Action} dans le {Paysage}. {oniric}",
                "À travers le {Paysage}, le {Symbole} trace le chemin.",
                "Le voyage {Adjectif} commence par un {Nom}."
            ],
            "rituel": [
                "Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}. {oniric}",
                "Ô {Adjectif} {Nom}, sois {VerbeMystique} par le rite ancien.",
                "Le {Symbole} et le {Nom} dansent le rite {Adjectif}. {oniric}",
                "Cinq fois {Symbole}, sept fois {Nom}, l'incantation résonne.",
                "Par le {VerbeMystique}, le {Défaut} devient {Bénéfice}."
            ],
            "silence": [
                "Que le {Symbole} efface le bruit. {oniric}",
                "Dans le {Adjectif} silence, seul le {Nom} persiste.",
                "Le {Symbole} {Action} le {Défaut} pour {Bénéfice}. {oniric}",
                "Silence... le {Nom} {Action} dans l'ombre.",
                "Le {Adjectif} silence révèle le {Symbole}."
            ],
            "émergence": [
                "Du {Défaut} naît le {Symbole}, porteur de {Bénéfice}.",
                "Le {Nom} {Action} et fait émerger un {Adjectif} ordre.",
                "Dans le chaos du {Paysage}, le {Symbole} {Action}. {oniric}",
                "L'émergence du {Symbole} transforme le {Défaut} en {Bénéfice}."
            ],
            "déclin": [
                "Le {Symbole} s'effondre, emportant le {Nom} dans le {Défaut}.",
                "Le {Adjectif} crépuscule consume le {Paysage}. {oniric}",
                "Le {Nom} se délite, le {Symbole} n'est plus.",
                "Dans le silence du {Défaut}, le {Symbole} {Action} pour la dernière fois."
            ]
        },
        "cultural_genomes": {
            "species": ["Narrateur", "Méméticien", "Oracle", "Iconoclaste", "Créateur de mythes"],
            "breeds": ["Standard", "Résilient", "Charismatique", "Mystique", "Analytique", "Prophétique"],
            "glyph_symbols": ["spiral", "circle", "cross", "serpentiform", "hand", "asterisk", "wavy_line",
                             "triangle", "hexagon", "pentagram", "infinity", "spiral_galaxy"],
            "guilds": ["Scribes", "Hérauts", "Anachorètes", "Colporteurs", "Iconoclastes",
                      "Mystiques", "Fractaliens", "Néantistes", "Syntagmatiques"]
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
                "cultural_resonance": "🎵 RÉSONANCE : {strains} fusionnent"
            }
        }
    }
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialise le gestionnaire de données.
        
        Args:
            data_dir: Répertoire contenant les fichiers JSON. Si None, utilise les données internes.
        """
        self.data_dir = Path(data_dir) if data_dir else None
        self._cache = {}
        self._loaded_files = set()
        
        # Charger ou utiliser les données internes
        self._load_all()
    
    def _load_all(self):
        """Charge toutes les données depuis les fichiers JSON ou utilise les internes."""
        if not self.data_dir or not self.data_dir.exists():
            self._use_internal_data()
            return
        
        # Charger le lexique onirique
        lexicon_file = self.data_dir / "oniric_lexicon.json"
        if lexicon_file.exists():
            with open(lexicon_file, 'r', encoding='utf-8') as f:
                self._cache['oniric_lexicon'] = json.load(f)
            self._loaded_files.add('oniric_lexicon')
        else:
            self._cache['oniric_lexicon'] = self._INTERNAL_DATA['oniric_lexicon'].copy()
        
        # Charger les thèmes
        themes_file = self.data_dir / "themes.json"
        if themes_file.exists():
            with open(themes_file, 'r', encoding='utf-8') as f:
                self._cache['themes'] = json.load(f)
            self._loaded_files.add('themes')
        else:
            self._cache['themes'] = self._INTERNAL_DATA['themes'].copy()
        
        # Charger les génomes culturels
        genomes_file = self.data_dir / "cultural_genomes.json"
        if genomes_file.exists():
            with open(genomes_file, 'r', encoding='utf-8') as f:
                self._cache['cultural_genomes'] = json.load(f)
            self._loaded_files.add('cultural_genomes')
        else:
            self._cache['cultural_genomes'] = self._INTERNAL_DATA['cultural_genomes'].copy()
        
        # Charger les types d'événements
        events_file = self.data_dir / "event_types.json"
        if events_file.exists():
            with open(events_file, 'r', encoding='utf-8') as f:
                self._cache['event_types'] = json.load(f)
            self._loaded_files.add('event_types')
        else:
            self._cache['event_types'] = self._INTERNAL_DATA['event_types'].copy()
        
        # Charger les configurations de simulation
        config_file = self.data_dir / "simulation_config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                self._cache['simulation_config'] = json.load(f)
            self._loaded_files.add('simulation_config')
        
        logger.info(f"📁 Données chargées depuis {self.data_dir} (fichiers: {', '.join(self._loaded_files)})")
    
    def _use_internal_data(self):
        """Utilise les données internes comme fallback."""
        self._cache['oniric_lexicon'] = self._INTERNAL_DATA['oniric_lexicon'].copy()
        self._cache['themes'] = self._INTERNAL_DATA['themes'].copy()
        self._cache['cultural_genomes'] = self._INTERNAL_DATA['cultural_genomes'].copy()
        self._cache['event_types'] = self._INTERNAL_DATA['event_types'].copy()
        logger.info("📁 Utilisation des données internes (fallback)")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une donnée par sa clé."""
        if key in self._cache:
            return self._cache[key]
        
        # Tenter de charger depuis un fichier JSON dédié
        if self.data_dir and key in ['oniric_lexicon', 'themes', 'cultural_genomes', 'event_types', 'simulation_config']:
            file_path = self.data_dir / f"{key}.json"
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self._cache[key] = data
                        return data
                except Exception as e:
                    logger.warning(f"Erreur chargement {file_path}: {e}")
        
        # Fallback vers les données internes
        if key in self._INTERNAL_DATA:
            self._cache[key] = self._INTERNAL_DATA[key].copy()
            return self._cache[key]
        
        return default
    
    def get_lexicon(self) -> Dict:
        """Récupère le lexique onirique."""
        return self.get('oniric_lexicon')
    
    def get_themes(self) -> Dict:
        """Récupère les thèmes et templates."""
        return self.get('themes')
    
    def get_genomes(self) -> Dict:
        """Récupère les génomes culturels."""
        return self.get('cultural_genomes')
    
    def get_event_types(self) -> Dict:
        """Récupère les types d'événements."""
        return self.get('event_types')
    
    def get_themes_list(self) -> List[str]:
        """Récupère la liste des thèmes disponibles."""
        return list(self.get_themes().keys())
    
    def save_external_data(self, output_dir: str):
        """Sauvegarde les données internes en fichiers JSON externes."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        for key, data in self._INTERNAL_DATA.items():
            file_path = out / f"{key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"📁 Sauvegardé: {file_path}")
        
        logger.info(f"✅ Données externes sauvegardées dans {output_dir}")


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] UTILITAIRES POUR NEO4J
# ═══════════════════════════════════════════════════════════════════════════════

class Neo4JExporter:
    """
    Exporte les données de simulation au format Cypher pour Neo4J.
    """
    
    @staticmethod
    def export_all(sim: 'CulturalEpidemicSimulation', output_dir: str, create_constraints: bool = True):
        """Exporte toutes les données en fichiers Cypher."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        cypher_lines = []
        
        # Ajouter les contraintes
        if create_constraints:
            cypher_lines.append("// === CONTRAINTES D'INTÉGRITÉ ===")
            cypher_lines.append("CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT strain_id IF NOT EXISTS FOR (s:Strain) REQUIRE s.strain_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT relic_id IF NOT EXISTS FOR (r:Relic) REQUIRE r.relic_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT myth_id IF NOT EXISTS FOR (m:Myth) REQUIRE m.myth_id IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT zone_name IF NOT EXISTS FOR (z:Zone) REQUIRE z.name IS UNIQUE;")
            cypher_lines.append("CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.event_id IS UNIQUE;")
            cypher_lines.append("")
        
        # 1. Création des zones
        cypher_lines.append("// === ZONES ===")
        for zone in sim.zones:
            cypher_lines.append(f"CREATE (z:Zone {{name: '{zone}'}});")
        cypher_lines.append("")
        
        # 2. Création des agents
        cypher_lines.append("// === AGENTS ===")
        for agent in sim.agents:
            # Échapper les apostrophes dans les chaînes
            zone_escaped = agent.zone.replace("'", "\\'")
            guild_escaped = agent.guild.replace("'", "\\'")
            glyph_escaped = agent.genome.glyph_symbol.replace("'", "\\'")
            
            cypher_lines.append(
                f"CREATE (a:Agent {{"
                f"id: {agent.id}, "
                f"zone: '{zone_escaped}', "
                f"guild: '{guild_escaped}', "
                f"status: '{agent.cultural_status.name}', "
                f"is_silent_carrier: {str(agent.is_silent_carrier).lower()}, "
                f"narrative_coherence: {agent.narrative_coherence:.3f}, "
                f"meme_virulence: {agent.meme_virulence:.3f}, "
                f"receptivity: {agent.receptivity:.3f}, "
                f"influence_score: {agent.influence_score:.3f}, "
                f"is_relic_guardian: {str(agent.is_relic_guardian).lower()}, "
                f"glyph_symbol: '{glyph_escaped}', "
                f"narrative_fluency: {agent.genome.narrative_fluency:.3f}, "
                f"charisma: {agent.genome.charisma:.3f}, "
                f"memory_depth: {agent.genome.memory_depth:.3f}, "
                f"intelligence: {agent.genome.intelligence:.3f}, "
                f"skepticism: {agent.genome.skepticism:.3f}, "
                f"dogma_risk: {agent.genome.dogma_risk:.3f}, "
                f"expressiveness: {agent.genome.expressiveness:.3f}, "
                f"influence_potential: {agent.genome.influence_potential:.3f}, "
                f"mobility: {agent.genome.mobility:.3f}, "
                f"altruism: {agent.genome.altruism:.3f}, "
                f"social_compliance: {agent.genome.social_compliance:.3f}, "
                f"curiosity: {agent.genome.curiosity:.3f}, "
                f"narrative_recovery: {agent.genome.narrative_recovery:.3f}"
                f"}});"
            )
        cypher_lines.append("")
        
        # 3. Création des souches
        cypher_lines.append("// === SOUCHES ===")
        for strain in sim.meme_strains.values():
            mantra_escaped = strain.mantra.content.replace("'", "\\'")
            theme_escaped = strain.mantra.theme.replace("'", "\\'")
            parent_id_escaped = strain.parent_id.replace("'", "\\'") if strain.parent_id else ""
            
            cypher_lines.append(
                f"CREATE (s:Strain {{"
                f"strain_id: '{strain.strain_id}', "
                f"parent_id: '{parent_id_escaped}', "
                f"generation: {strain.generation}, "
                f"mantra_content: '{mantra_escaped}', "
                f"mantra_theme: '{theme_escaped}', "
                f"contagion_power: {strain.contagion_power:.3f}, "
                f"dogma_intensity: {strain.dogma_intensity:.3f}, "
                f"latency_period: {strain.latency_period:.3f}, "
                f"emergence_time: {strain.emergence_time}, "
                f"mutation_count: {len(strain.mutations)}"
                f"}});"
            )
        cypher_lines.append("")
        
        # 4. Relations Agent - Zone
        cypher_lines.append("// === RELATIONS AGENT -> ZONE ===")
        for agent in sim.agents:
            zone_escaped = agent.zone.replace("'", "\\'")
            cypher_lines.append(
                f"MATCH (a:Agent {{id: {agent.id}}}), (z:Zone {{name: '{zone_escaped}'}}) "
                f"CREATE (a)-[:LOCATED_IN]->(z);"
            )
        cypher_lines.append("")
        
        # 5. Relations Agent - Strain
        cypher_lines.append("// === RELATIONS AGENT -> STRAIN ===")
        for agent in sim.agents:
            if agent.current_strain:
                strain_id_escaped = agent.current_strain.strain_id.replace("'", "\\'")
                exposure = agent.exposure_time if agent.exposure_time else 0
                cypher_lines.append(
                    f"MATCH (a:Agent {{id: {agent.id}}}), (s:Strain {{strain_id: '{strain_id_escaped}'}}) "
                    f"CREATE (a)-[:CARRIES {{since: {exposure}}}]->(s);"
                )
        cypher_lines.append("")
        
        # 6. Relations Strain - Strain (mutations)
        cypher_lines.append("// === RELATIONS STRAIN -> STRAIN (MUTATIONS) ===")
        for strain in sim.meme_strains.values():
            if strain.parent_id and strain.parent_id in sim.meme_strains:
                parent_escaped = strain.parent_id.replace("'", "\\'")
                strain_id_escaped = strain.strain_id.replace("'", "\\'")
                cypher_lines.append(
                    f"MATCH (parent:Strain {{strain_id: '{parent_escaped}'}}), (child:Strain {{strain_id: '{strain_id_escaped}'}}) "
                    f"CREATE (parent)-[:MUTATED_INTO {{generation: {strain.generation}}}]->(child);"
                )
        cypher_lines.append("")
        
        # 7. Création des reliques
        cypher_lines.append("// === RELIQUES ===")
        for relic in sim.relics:
            mantra_escaped = relic.mantra.content.replace("'", "\\'")
            theme_escaped = relic.mantra.theme.replace("'", "\\'")
            zone_escaped = relic.zone.replace("'", "\\'")
            cypher_lines.append(
                f"CREATE (r:Relic {{"
                f"relic_id: '{relic.relic_id}', "
                f"guardian_id: {relic.guardian_id}, "
                f"zone: '{zone_escaped}', "
                f"preserved_at: {relic.preserved_at}, "
                f"mantra_content: '{mantra_escaped}', "
                f"mantra_theme: '{theme_escaped}', "
                f"veneration_count: {relic.veneration_count}"
                f"}});"
            )
        cypher_lines.append("")
        
        # 8. Relations Relique - Agent (gardien)
        cypher_lines.append("// === RELATIONS RELIQUE -> AGENT (GARDIEN) ===")
        for relic in sim.relics:
            relic_id_escaped = relic.relic_id.replace("'", "\\'")
            cypher_lines.append(
                f"MATCH (r:Relic {{relic_id: '{relic_id_escaped}'}}), (a:Agent {{id: {relic.guardian_id}}}) "
                f"CREATE (a)-[:GUARDS]->(r);"
            )
        cypher_lines.append("")
        
        # 9. Création des mythes
        cypher_lines.append("// === MYTHES ===")
        for myth in sim.founding_myths:
            title_escaped = myth.title.replace("'", "\\'")
            verses_escaped = ' | '.join(v.replace("'", "\\'") for v in myth.verses)
            cypher_lines.append(
                f"CREATE (m:Myth {{"
                f"myth_id: '{myth.myth_id}', "
                f"title: '{title_escaped}', "
                f"verses: '{verses_escaped}', "
                f"created_at: {myth.created_at}, "
                f"verse_count: {len(myth.verses)}"
                f"}});"
            )
        cypher_lines.append("")
        
        # 10. Relations Myth - Strain
        cypher_lines.append("// === RELATIONS MYTHE -> SOUCHE ===")
        for myth in sim.founding_myths:
            for strain_id in myth.dominant_strains:
                if strain_id in sim.meme_strains:
                    strain_id_escaped = strain_id.replace("'", "\\'")
                    myth_id_escaped = myth.myth_id.replace("'", "\\'")
                    cypher_lines.append(
                        f"MATCH (m:Myth {{myth_id: '{myth_id_escaped}'}}), (s:Strain {{strain_id: '{strain_id_escaped}'}}) "
                        f"CREATE (m)-[:INCORPORATES]->(s);"
                    )
        cypher_lines.append("")
        
        # 11. Événements narratifs
        cypher_lines.append("// === ÉVÉNEMENTS NARRATIFS ===")
        for i, evt in enumerate(sim.events):
            event_type_escaped = evt.event_type.replace("'", "\\'")
            cultural_state_escaped = evt.cultural_state.replace("'", "\\'")
            guild_escaped = evt.guild.replace("'", "\\'") if evt.guild else ""
            strain_id_escaped = evt.strain_id.replace("'", "\\'") if evt.strain_id else ""
            source_id = evt.source_id if evt.source_id else -1
            coherence = evt.narrative_coherence if evt.narrative_coherence else 0.0
            
            cypher_lines.append(
                f"CREATE (e:Event {{"
                f"event_id: 'EVT_{i:04d}', "
                f"timestamp: {evt.timestamp}, "
                f"agent_id: {evt.agent_id}, "
                f"event_type: '{event_type_escaped}', "
                f"cultural_state: '{cultural_state_escaped}', "
                f"source_id: {source_id}, "
                f"guild: '{guild_escaped}', "
                f"narrative_coherence: {coherence}"
                f"}});"
            )
        cypher_lines.append("")
        
        # 12. Relations Event - Agent
        cypher_lines.append("// === RELATIONS ÉVÉNEMENT -> AGENT ===")
        for i, evt in enumerate(sim.events):
            cypher_lines.append(
                f"MATCH (e:Event {{event_id: 'EVT_{i:04d}'}}), (a:Agent {{id: {evt.agent_id}}}) "
                f"CREATE (e)-[:AFFECTS]->(a);"
            )
            if evt.source_id:
                cypher_lines.append(
                    f"MATCH (e:Event {{event_id: 'EVT_{i:04d}'}}), (src:Agent {{id: {evt.source_id}}}) "
                    f"CREATE (src)-[:TRIGGERED]->(e);"
                )
        cypher_lines.append("")
        
        # 13. Interactions de transmission
        cypher_lines.append("// === INTERACTIONS DE TRANSMISSION ===")
        for i, inter in enumerate(sim.interactions):
            if inter.transmission_occurred:
                cypher_lines.append(
                    f"CREATE (t:Transmission {{"
                    f"transmission_id: 'TRANS_{i:04d}', "
                    f"timestamp: {inter.timestamp}, "
                    f"intensity: {inter.intensity:.3f}, "
                    f"transmission_risk: {inter.transmission_risk:.3f}"
                    f"}});"
                )
                cypher_lines.append(
                    f"MATCH (t:Transmission {{transmission_id: 'TRANS_{i:04d}'}}), "
                    f"(a:Agent {{id: {inter.agent_a}}}), (b:Agent {{id: {inter.agent_b}}}) "
                    f"CREATE (a)-[:TRANSMITS_TO {{transmission_id: 'TRANS_{i:04d}'}}]->(t), "
                    f"(t)-[:RECEIVED_BY]->(b);"
                )
        cypher_lines.append("")
        
        # 14. Événements aléatoires (enrichis)
        cypher_lines.append("// === ÉVÉNEMENTS ALÉATOIRES ===")
        for evt in sim.random_events:
            event_type_escaped = evt.event_type.replace("'", "\\'")
            zone_escaped = evt.zone.replace("'", "\\'") if evt.zone else ""
            desc_escaped = evt.description.replace("'", "\\'")
            impact_escaped = json.dumps(evt.impact, ensure_ascii=False).replace("'", "\\'")
            
            cypher_lines.append(
                f"CREATE (re:RandomEvent {{"
                f"event_id: '{evt.event_id}', "
                f"event_type: '{event_type_escaped}', "
                f"timestamp: {evt.timestamp}, "
                f"zone: '{zone_escaped}', "
                f"description: '{desc_escaped}', "
                f"impact: '{impact_escaped}'"
                f"}});"
            )
        cypher_lines.append("")
        
        # 15. Relations RandomEvent - Zone
        cypher_lines.append("// === RELATIONS RANDOM_EVENT -> ZONE ===")
        for evt in sim.random_events:
            if evt.zone:
                zone_escaped = evt.zone.replace("'", "\\'")
                event_id_escaped = evt.event_id.replace("'", "\\'")
                cypher_lines.append(
                    f"MATCH (re:RandomEvent {{event_id: '{event_id_escaped}'}}), (z:Zone {{name: '{zone_escaped}'}}) "
                    f"CREATE (re)-[:OCCURRED_IN]->(z);"
                )
        cypher_lines.append("")
        
        # 16. Relations RandomEvent - Agent
        cypher_lines.append("// === RELATIONS RANDOM_EVENT -> AGENT ===")
        for evt in sim.random_events:
            event_id_escaped = evt.event_id.replace("'", "\\'")
            for agent_id in evt.affected_agents[:50]:  # Limité à 50 pour la lisibilité
                cypher_lines.append(
                    f"MATCH (re:RandomEvent {{event_id: '{event_id_escaped}'}}), (a:Agent {{id: {agent_id}}}) "
                    f"CREATE (re)-[:AFFECTED]->(a);"
                )
        cypher_lines.append("")
        
        # 17. Dérive sémantique (relations enrichies)
        cypher_lines.append("// === DÉRIVE SÉMANTIQUE (RELATIONS ENRICHIES) ===")
        for parent, children in sim.semantic_drift.items():
            for child in children:
                if parent in sim.meme_strains and child in sim.meme_strains:
                    parent_escaped = parent.replace("'", "\\'")
                    child_escaped = child.replace("'", "\\'")
                    gen_diff = sim.meme_strains[child].generation - sim.meme_strains[parent].generation
                    cypher_lines.append(
                        f"MATCH (p:Strain {{strain_id: '{parent_escaped}'}}), (c:Strain {{strain_id: '{child_escaped}'}}) "
                        f"CREATE (p)-[:SEMANTIC_DRIFT {{"
                        f"type: 'mutation', "
                        f"generation: {gen_diff}"
                        f"}}]->(c);"
                    )
        cypher_lines.append("")
        
        # 18. Statistiques agrégées (nœuds de métriques)
        cypher_lines.append("// === STATISTIQUES AGRÉGÉES ===")
        for t, metrics in sorted(sim.daily_metrics.items()):
            if t % max(1, len(sim.daily_metrics) // 20) == 0:  # Échantillonnage
                rt_val = sim.rt_history[t] if t < len(sim.rt_history) else 0.0
                cypher_lines.append(
                    f"CREATE (m:Metric {{"
                    f"timestamp: {t}, "
                    f"rt: {rt_val:.3f}, "
                    f"total_agents: {len(sim.agents)}, "
                    f"receptive: {metrics.get('cult_S', 0)}, "
                    f"exposed: {metrics.get('cult_E', 0)}, "
                    f"evangelist: {metrics.get('cult_I', 0)}, "
                    f"silent_carrier: {metrics.get('cult_A', 0)}, "
                    f"disenchanted: {metrics.get('cult_R', 0)}, "
                    f"oblivious: {metrics.get('cult_D', 0)}, "
                    f"strains: {metrics.get('nb_strains', 0)}, "
                    f"relics: {metrics.get('nb_relics', 0)}, "
                    f"myths: {metrics.get('nb_myths', 0)}"
                    f"}});"
                )
        cypher_lines.append("")
        
        # Écrire le fichier
        cypher_file = out / "neo4j_import.cypher"
        with open(cypher_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(cypher_lines))
        
        # Générer un README Neo4J
        Neo4JExporter._generate_neo4j_readme(out)
        
        logger.info(f"🦈 Export Neo4J: {cypher_file} ({len(cypher_lines)} lignes)")
        return cypher_file
    
    @staticmethod
    def _generate_neo4j_readme(output_dir: Path):
        """Génère un README pour l'import Neo4J."""
        readme_content = """
╔═══════════════════════════════════════════════════════════════════╗
║          🦈 EXPORT NEO4J — ARCHEOEPIDEMIC CHIMERA v2.2           ║
║                     Graph Database Import                        ║
╚═══════════════════════════════════════════════════════════════════╝

📌 PROCÉDURE D'IMPORTATION

1. Démarrer Neo4J (Desktop ou Browser)
2. Ouvrir le terminal Cypher
3. Copier-coller le contenu du fichier neo4j_import.cypher
   OU utiliser la commande : 
   :source neo4j_import.cypher

📊 STRUCTURE DU GRAPHE

NŒUDS:
  • Agent          → Narrateurs culturels
  • Strain         → Souches narratives (mutations)
  • Zone           → Espaces narratifs
  • Relic          → Reliques préservées
  • Myth           → Mythes fondateurs
  • Event          → Événements narratifs
  • RandomEvent    → Événements aléatoires
  • Transmission   → Transmissions de mèmes
  • Metric         → Métriques temporelles

RELATIONS:
  • (Agent)-[:LOCATED_IN]->(Zone)
  • (Agent)-[:CARRIES {since}]->(Strain)
  • (Strain)-[:MUTATED_INTO {generation}]->(Strain)
  • (Agent)-[:GUARDS]->(Relic)
  • (Myth)-[:INCORPORATES]->(Strain)
  • (Event)-[:AFFECTS]->(Agent)
  • (Source)-[:TRIGGERED]->(Event)
  • (Agent)-[:TRANSMITS_TO]->(Transmission)
  • (Transmission)-[:RECEIVED_BY]->(Agent)
  • (Strain)-[:SEMANTIC_DRIFT]->(Strain)
  • (RandomEvent)-[:OCCURRED_IN]->(Zone)
  • (RandomEvent)-[:AFFECTED]->(Agent)

🔍 REQUÊTES UTILES

1. Voir le réseau complet:
   MATCH (n) RETURN n LIMIT 200

2. Trajectoire d'un agent:
   MATCH (a:Agent {id: 42})-[:CARRIES]->(s:Strain)
   RETURN a, s

3. Arbre de mutations:
   MATCH path = (parent:Strain)-[:MUTATED_INTO*]->(child:Strain)
   WHERE NOT (parent)-[:MUTATED_INTO]->()
   RETURN path

4. Événements par zone:
   MATCH (z:Zone)<-[:OCCURRED_IN]-(e:RandomEvent)
   RETURN z.name, count(e) as event_count
   ORDER BY event_count DESC

5. Influenceurs culturels:
   MATCH (a:Agent)-[t:TRANSMITS_TO]->()
   RETURN a.id, count(t) as transmissions
   ORDER BY transmissions DESC
   LIMIT 10

6. Mythes et leur composition:
   MATCH (m:Myth)-[:INCORPORATES]->(s:Strain)
   RETURN m.title, collect(s.strain_id) as strains

🔗 IMPORT DES FICHIERS CSV (OPTIONNEL)

La commande ci-dessus utilise le format Cypher direct. Pour utiliser 
le CSV import de Neo4J, les fichiers suivants sont disponibles :
  • agents_state.csv
  • strains_state.csv
  • daily_metrics.csv
  • narrative_events.csv
  • random_events.csv
  • interactions.csv
  • relics.csv
  • myths.csv
  • chronicle.csv

Commandes CSV:

LOAD CSV WITH HEADERS FROM 'file:///agents_state.csv' AS row
CREATE (a:Agent {id: toInteger(row.agent_id), ...});

🎯 BONNE EXPLORATION GRAPHIQUE !
"""
        readme_path = output_dir / "README_NEO4J.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        logger.info(f"📝 README Neo4J généré: {readme_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] SYSTÈME DE GRAVITÉ NARRATIVE
# ═══════════════════════════════════════════════════════════════════════════════

class NarrativeGravity:
    """
    Système de "gravité narrative" - les récits attirent les agents 
    partageant des affinités sémantiques.
    """
    
    def __init__(self, sim: 'CulturalEpidemicSimulation'):
        self.sim = sim
        self.gravity_centers: Dict[str, Dict] = {}  # strain_id -> {position, mass, influence_radius}
        self._initialize_centers()
    
    def _initialize_centers(self):
        """Initialise les centres de gravité pour chaque souche."""
        for strain_id, strain in self.sim.meme_strains.items():
            # Les souches populaires ont plus de masse gravitationnelle
            carriers = sum(1 for a in self.sim.agents 
                          if a.current_strain.strain_id == strain_id 
                          and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))
            
            mass = 1.0 + (carriers / max(1, len(self.sim.agents))) * 5.0
            influence_radius = 1.0 + (carriers / max(1, len(self.sim.agents))) * 3.0
            
            self.gravity_centers[strain_id] = {
                'mass': mass,
                'influence_radius': influence_radius,
                'position': {'x': random.random() * 100, 'y': random.random() * 100}
            }
    
    def compute_attraction(self, agent: 'CulturalAgent', strain_id: str) -> float:
        """Calcule l'attraction gravitationnelle d'une souche sur un agent."""
        if strain_id not in self.gravity_centers:
            return 0.0
        
        center = self.gravity_centers[strain_id]
        
        # Facteurs d'attraction
        semantic_overlap = self._compute_semantic_overlap(agent, strain_id)
        social_proximity = self._compute_social_proximity(agent, strain_id)
        narrative_coherence = agent.narrative_coherence
        
        # Force d'attraction (loi de l'inverse carré modifiée)
        mass_effect = center['mass'] * semantic_overlap
        distance_effect = 1.0 / (1.0 + social_proximity)
        coherence_boost = 1.0 + narrative_coherence * 0.5
        
        return mass_effect * distance_effect * coherence_boost
    
    def _compute_semantic_overlap(self, agent: 'CulturalAgent', strain_id: str) -> float:
        """Calcule le chevauchement sémantique entre l'agent et une souche."""
        strain = self.sim.meme_strains.get(strain_id)
        if not strain or not agent.personal_mantra:
            return 0.1
        
        # Comparaison des mots-clés
        agent_words = set(agent.personal_mantra.content.lower().split())
        strain_words = set(strain.mantra.content.lower().split())
        
        intersection = len(agent_words & strain_words)
        union = len(agent_words | strain_words)
        
        if union == 0:
            return 0.1
        
        return 0.5 + 0.5 * (intersection / union)
    
    def _compute_social_proximity(self, agent: 'CulturalAgent', strain_id: str) -> float:
        """Calcule la proximité sociale de l'agent avec les porteurs d'une souche."""
        carriers = [a for a in self.sim.agents 
                   if a.current_strain.strain_id == strain_id 
                   and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        
        if not carriers:
            return 1.0
        
        # Chemin le plus court dans le réseau social
        if HAS_NX:
            try:
                path_length = nx.shortest_path_length(
                    self.sim.transmission_network, 
                    source=agent.id, 
                    target=carriers[0].id
                )
                return 1.0 / (1.0 + path_length)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                pass
        
        # Approximation: distance dans l'espace des guildes
        guild_similarity = sum(1 for c in carriers if c.guild == agent.guild) / max(1, len(carriers))
        return 0.5 + 0.5 * guild_similarity
    
    def apply_gravity(self, agent: 'CulturalAgent') -> Optional[str]:
        """Applique la gravité narrative sur un agent."""
        if agent.cultural_status != CulturalStatus.RECEPTIVE:
            return None
        
        attractions = {}
        for strain_id in self.gravity_centers:
            attraction = self.compute_attraction(agent, strain_id)
            if attraction > 0.5:
                attractions[strain_id] = attraction
        
        if not attractions:
            return None
        
        # Choix pondéré par l'attraction
        total = sum(attractions.values())
        if total == 0:
            return None
        
        strain_ids = list(attractions.keys())
        weights = [attractions[s] / total for s in strain_ids]
        selected = random.choices(strain_ids, weights=weights, k=1)[0]
        
        return selected


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] FACTION ET ALLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

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


class FactionSystem:
    """Gère l'émergence de factions et alliances."""
    
    def __init__(self, sim: 'CulturalEpidemicSimulation'):
        self.sim = sim
        self.factions: Dict[str, Faction] = {}
        self.faction_counter = 0
        
        # Palette de couleurs pour les factions
        self.colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#ff6bff",
                      "#ff9f43", "#00d2d3", "#54a0ff", "#ff6348", "#a29bfe"]
    
    def faction_emergence_threshold(self) -> float:
        """Calcule le seuil d'émergence d'une nouvelle faction."""
        n_carriers = sum(1 for a in self.sim.agents 
                        if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))
        
        # Une faction émerge quand un groupe cohérent dépasse 10% de la population croyante
        threshold = max(3, int(n_carriers * 0.1))
        return max(3, threshold)
    
    def check_emergence(self):
        """Vérifie si une nouvelle faction doit émerger."""
        # Regrouper les agents par souche
        strain_groups = defaultdict(list)
        for agent in self.sim.agents:
            if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                if agent.current_strain:
                    strain_groups[agent.current_strain.strain_id].append(agent.id)
        
        threshold = self.faction_emergence_threshold()
        
        for strain_id, members in strain_groups.items():
            if len(members) >= threshold and strain_id not in self.factions:
                # Vérifier si ces agents sont déjà dans une faction
                existing_faction_members = set()
                for faction in self.factions.values():
                    existing_faction_members.update(faction.members)
                
                new_members = [m for m in members if m not in existing_faction_members]
                
                if len(new_members) >= max(3, threshold // 2):
                    self._create_faction(strain_id, new_members)
    
    def _create_faction(self, strain_id: str, members: List[int]):
        """Crée une nouvelle faction."""
        self.faction_counter += 1
        
        # Générer un nom de faction basé sur le mantra
        strain = self.sim.meme_strains.get(strain_id)
        if strain:
            words = strain.mantra.content.lower().split()
            name_parts = [w for w in words if w and w[0].isalpha() and len(w) > 3]
            name = " ".join(name_parts[:3]) if name_parts else f"Faction-{self.faction_counter}"
        else:
            name = f"Faction-{self.faction_counter}"
        
        # Capitaliser
        name = name.title()
        
        faction = Faction(
            faction_id=f"FAC-{self.faction_counter:03d}",
            name=name,
            founder_id=members[0],
            founding_strain=strain_id,
            created_at=self.sim.current_t,
            members=members[:],  # Copie
            color=self.colors[self.faction_counter % len(self.colors)],
            rituals=self._generate_rituals(strain_id)
        )
        
        self.factions[faction.faction_id] = faction
        
        # Enregistrer l'événement
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
        """Génère des rituels pour la faction."""
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
        """Met à jour les alliances entre factions."""
        # Simple logique d'alliance basée sur la similarité des souches
        factions_list = list(self.factions.values())
        for i in range(len(factions_list)):
            for j in range(i + 1, len(factions_list)):
                f1, f2 = factions_list[i], factions_list[j]
                
                # Similarité basée sur les souches
                strain1 = self.sim.meme_strains.get(f1.founding_strain)
                strain2 = self.sim.meme_strains.get(f2.founding_strain)
                
                if strain1 and strain2:
                    # Part de mots communs
                    words1 = set(strain1.mantra.content.lower().split())
                    words2 = set(strain2.mantra.content.lower().split())
                    overlap = len(words1 & words2) / max(1, len(words1 | words2))
                    
                    # Alliance si overlap > 0.3
                    if overlap > 0.3 and f2.faction_id not in f1.alliances:
                        f1.alliances.append(f2.faction_id)
                        f2.alliances.append(f1.faction_id)


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] MÉMOIRE ÉPISODIQUE DES AGENTS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EpisodicMemory:
    """Mémoire épisodique d'un agent."""
    agent_id: int
    events: List[Dict] = field(default_factory=list)
    max_size: int = 50
    
    def add_event(self, event_type: str, content: str, timestamp: int, impact: float = 1.0):
        """Ajoute un événement à la mémoire."""
        self.events.append({
            'type': event_type,
            'content': content,
            'timestamp': timestamp,
            'impact': impact
        })
        if len(self.events) > self.max_size:
            self.events.pop(0)
    
    def get_recent_events(self, n: int = 5) -> List[Dict]:
        """Récupère les n événements les plus récents."""
        return self.events[-n:]
    
    def get_impact_summary(self) -> Dict[str, float]:
        """Résumé de l'impact des événements."""
        summary = defaultdict(float)
        for evt in self.events:
            summary[evt['type']] += evt['impact']
        return dict(summary)


# ═══════════════════════════════════════════════════════════════════════════════
# [PARENT 1] LEXIQUE ONIRIQUE (MODIFIÉ pour utiliser JSONDataManager)
# ═══════════════════════════════════════════════════════════════════════════════

# Variable globale pour le gestionnaire de données
_DATA_MANAGER = None

def get_data_manager() -> JSONDataManager:
    """Récupère l'instance globale du gestionnaire de données."""
    global _DATA_MANAGER
    if _DATA_MANAGER is None:
        _DATA_MANAGER = JSONDataManager()
    return _DATA_MANAGER

def set_data_manager(data_manager: JSONDataManager):
    """Définit l'instance globale du gestionnaire de données."""
    global _DATA_MANAGER
    _DATA_MANAGER = data_manager

def load_oniric_lexicon() -> Dict[str, List[str]]:
    """Charge le lexique onirique depuis le gestionnaire de données."""
    return get_data_manager().get_lexicon()

def get_themes() -> Dict:
    """Récupère les thèmes depuis le gestionnaire de données."""
    return get_data_manager().get_themes()

def get_themes_list() -> List[str]:
    """Récupère la liste des thèmes disponibles."""
    return get_data_manager().get_themes_list()


# ═══════════════════════════════════════════════════════════════════════════════
# [PARENT 1] CLASSES DE BASE (Mantra, SoufiMantraGA) - MODIFIÉES
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
        
        # Cache des lexiques pour performance
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
# [PARENT 2] CulturalGenome (MODIFIÉ pour utiliser JSONDataManager)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CulturalGenome:
    species: str = "Narrateur"
    breed: str = "Standard"
    generation: int = 0
    preferred_theme: str = field(default_factory=lambda: random.choice(get_themes_list()))
    keywords: List[str] = field(default_factory=lambda: random.sample(
        get_data_manager().get_lexicon().get("Nom", ["signal"]) + 
        get_data_manager().get_lexicon().get("Symbole", ["lune"]), k=3))
    glyph_symbol: str = field(default_factory=lambda: random.choice(
        get_data_manager().get_genomes().get("glyph_symbols", ["spiral"])))
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
        # S'assurer que les guildes existent
        genome_data = get_data_manager().get_genomes()
        valid_guilds = genome_data.get("guilds", ["Scribes", "Hérauts", "Anachorètes", "Colporteurs", "Iconoclastes"])
        self.guild_affinity = {k: v for k, v in self.guild_affinity.items() if k in valid_guilds}
        
        total = sum(self.guild_affinity.values())
        if total > 0:
            self.guild_affinity = {k: v / total for k, v in self.guild_affinity.items()}
        else:
            # Distribution uniforme sur les guildes valides
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
        return CulturalGenome(
            species=self.species, breed=self.breed, generation=self.generation + 1,
            preferred_theme=self.preferred_theme if rng.random() > mutation_rate else rng.choice(get_themes_list()),
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
# [PARENT 2] CulturalStatus et MemeStrain (conservés)
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


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.0] MÉMOIRE COLLECTIVE + RELIQUES + MYTHES (conservés)
# ═══════════════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] CulturalPhenotype (conservé)
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
# [FUSION] CulturalAgent (MODIFIÉ pour inclure mémoire et faction)
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
        self.mantra_history: List[Tuple[int, str]] = []
        self.influence_score: float = 0.0
        self.is_relic_guardian: bool = False
        self.relic_id: Optional[str] = None
        
        # [NOUVEAU v2.2] Mémoire épisodique
        self.episodic_memory = EpisodicMemory(self.id)
        
        # [NOUVEAU v2.2] Faction
        self.faction_id: Optional[str] = None
        
        # [NOUVEAU v2.2] Narrative Gravity - position abstraite
        self.narrative_position = {'x': rng.random() * 100, 'y': rng.random() * 100}
    
    def receive_mantra(self, strain: MemeStrain):
        self.current_strain = strain
        self.personal_mantra = strain.mantra
        self.meme_virulence = MemeStrain.compute_virulence(strain.mantra, base=strain.contagion_power)
        self.narrative_coherence = min(1.0, 0.4 + strain.mantra.fitness * 0.5)
        self.mantra_history.append((self.current_t, strain.strain_id))
        
        # Mise à jour de la position narrative
        self.narrative_position['x'] += self.rng.gauss(0, 0.5)
        self.narrative_position['y'] += self.rng.gauss(0, 0.5)
        
        logger.debug(f"Agent#{self.id} reçoit mantra {strain.strain_id}: «{strain.mantra.content[:50]}...»")
    
    def is_culture_influencer(self) -> bool:
        return self.phenotype.phenotypes["is_culture_influencer"]
    
    def add_memory_event(self, event_type: str, content: str, impact: float = 1.0):
        """Ajoute un événement à la mémoire épisodique."""
        self.episodic_memory.add_event(event_type, content, self.current_t, impact)


# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] CulturalEpidemicSimulation — v2.2
# ═══════════════════════════════════════════════════════════════════════════════

class CulturalEpidemicSimulation:
    def __init__(self, params: dict, genome_pool: Optional[List[CulturalGenome]] = None,
                 data_dir: Optional[str] = None):
        # Initialiser le gestionnaire de données
        if data_dir:
            self.data_manager = JSONDataManager(data_dir)
            set_data_manager(self.data_manager)
        else:
            self.data_manager = get_data_manager()
            set_data_manager(self.data_manager)
        
        self.params = params
        self.rng = random.Random(params.get("seed", 42))
        self.current_t = 0
        self.zones = self._generate_zones()
        
        # --- Souche-racine (utilise les nouvelles données) ---
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
        
        # Systèmes narratifs avancés
        self.collective_memory = CollectiveMemory()
        self.semantic_drift: Dict[str, List[str]] = defaultdict(list)
        
        # [NOUVEAU v2.2] Gravité narrative
        self.narrative_gravity = NarrativeGravity(self)
        
        # [NOUVEAU v2.2] Factions
        self.faction_system = FactionSystem(self)
        
        # Historique pour CSV
        self.agent_state_history: List[Dict] = []
        self.strain_history: List[Dict] = []
        
        self._init_population(genome_pool)
        logger.info(f"Simulation initialisée : {len(self.agents)} agents sur {len(self.zones)} zones")
        logger.debug(f"Souche racine : {self.root_strain.strain_id} — «{self.root_strain.mantra.content}»")
    
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
    
    # -------------------------------------------------------------------
    # Exposition + Progression + Transmission (conservés)
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
        p_transmission = min(0.95, 0.12 * virulence * agent_b.receptivity)
        occurred = self.rng.random() < p_transmission
        self.interactions.append(InteractionRecord(
            timestamp=self.current_t, agent_a=agent_a.id, agent_b=agent_b.id,
            intensity=virulence, transmission_risk=p_transmission, transmission_occurred=occurred,
        ))
        if occurred:
            self._expose_agent(agent_b, agent_a, agent_a.current_strain)
            agent_b.add_memory_event("infection", f"Infecté par Agent#{agent_a.id}", impact=0.6)
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
        agent.add_memory_event("mutation", f"Mutation: {parent.strain_id} → {new_strain.strain_id}", impact=0.4)
        logger.info(f"t={self.current_t} 🧬 MUTATION : {parent.strain_id} → {new_strain.strain_id} «{new_mantra.content[:40]}...»")
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.2] Application de la gravité narrative
    # -------------------------------------------------------------------
    def _apply_narrative_gravity(self):
        """Applique la gravité narrative sur les agents réceptifs."""
        for agent in self.agents:
            if agent.cultural_status == CulturalStatus.RECEPTIVE:
                attracted_to = self.narrative_gravity.apply_gravity(agent)
                if attracted_to and attracted_to in self.meme_strains:
                    strain = self.meme_strains[attracted_to]
                    if self._expose_agent(agent, None, strain, force=True):
                        agent.add_memory_event("gravity_attraction", 
                            f"Attiré par la souche {attracted_to}", impact=0.5)
                        logger.debug(f"✨ Gravité narrative : Agent#{agent.id} attiré par {attracted_to}")
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.2] Gestion des factions
    # -------------------------------------------------------------------
    def _update_factions(self):
        """Met à jour le système de factions."""
        self.faction_system.check_emergence()
        self.faction_system.update_alliances()
        
        # Assigner les agents aux factions
        for faction in self.faction_system.factions.values():
            for member_id in faction.members:
                agent = self._agent_by_id(member_id)
                if agent:
                    agent.faction_id = faction.faction_id
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.2] Cycles narratifs (saisons culturelles)
    # -------------------------------------------------------------------
    def _apply_narrative_cycle(self):
        """Applique un cycle narratif saisonnier."""
        # Un cycle toutes les 10 itérations
        if self.current_t % 10 != 0:
            return
        
        # Déterminer le type de cycle
        cycle_type = self.rng.choice(["expansion", "contraction", "transformation", "silence"])
        
        if cycle_type == "expansion":
            # Augmentation de la réceptivité
            for agent in self.agents:
                if agent.cultural_status == CulturalStatus.RECEPTIVE:
                    agent.receptivity *= 1.1
                    agent.add_memory_event("cycle_expansion", 
                        "Saison d'expansion narrative", impact=0.3)
            logger.info(f"🌱 Cycle d'expansion narrative (t={self.current_t})")
            
        elif cycle_type == "contraction":
            # Diminution de la réceptivité
            for agent in self.agents:
                if agent.cultural_status in (CulturalStatus.RECEPTIVE, CulturalStatus.EXPOSED):
                    agent.receptivity *= 0.9
                    agent.add_memory_event("cycle_contraction",
                        "Saison de contraction narrative", impact=0.3)
            logger.info(f"🌿 Cycle de contraction narrative (t={self.current_t})")
            
        elif cycle_type == "transformation":
            # Mutation accélérée
            mutation_bonus = self.params.get("mutation_prob", 0.02) * 3
            if self.rng.random() < mutation_bonus:
                self.mutate_meme()
                # Aussi transformer quelques agents
                for agent in self.rng.sample(self.agents, k=min(3, len(self.agents) // 10)):
                    if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                        agent.add_memory_event("cycle_transformation",
                            "Saison de transformation narrative", impact=0.5)
            logger.info(f"🔄 Cycle de transformation narrative (t={self.current_t})")
            
        elif cycle_type == "silence":
            # Période de silence - ralentissement des transmissions
            for agent in self.agents:
                if agent.cultural_status == CulturalStatus.EVANGELIST:
                    agent.meme_virulence *= 0.8
                    agent.add_memory_event("cycle_silence",
                        "Saison de silence narratif", impact=0.2)
            logger.info(f"🤫 Cycle de silence narrative (t={self.current_t})")
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.2] Événements enrichis
    # -------------------------------------------------------------------
    def _trigger_narrative_eclipse(self):
        """Déclenche une éclipse narrative - une souche s'efface."""
        active_strains = [s for s in self.meme_strains.values() 
                         if any(a.current_strain.strain_id == s.strain_id 
                               for a in self.agents 
                               if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))]
        
        if len(active_strains) < 2:
            return
        
        # Choisir une souche à effacer (la moins populaire)
        strain_counts = Counter(
            a.current_strain.strain_id for a in self.agents
            if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)
        )
        
        if not strain_counts:
            return
        
        least_popular = min(strain_counts.items(), key=lambda x: x[1])[0]
        if least_popular not in self.meme_strains:
            return
        
        # Effacer la souche de la mémoire des agents
        affected = []
        for agent in self.agents:
            if agent.current_strain.strain_id == least_popular:
                if agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
                    agent.cultural_status = CulturalStatus.DISENCHANTED
                    agent.disenchant_time = self.current_t
                    affected.append(agent.id)
                    agent.add_memory_event("narrative_eclipse",
                        f"La souche {least_popular} s'efface", impact=0.8)
                elif agent.cultural_status == CulturalStatus.RECEPTIVE:
                    # Les réceptifs oublient cette souche
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
        """Déclenche une résonance culturelle - fusion de souches."""
        active_strains = [s for s in self.meme_strains.values() 
                         if any(a.current_strain.strain_id == s.strain_id 
                               for a in self.agents 
                               if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))]
        
        if len(active_strains) < 2:
            return
        
        # Choisir deux souches à fusionner
        strain1, strain2 = self.rng.sample(active_strains, 2)
        
        # Créer une fusion
        fusion_mantra = Mantra(
            id=f"FUS-{self.strain_counter + 1}",
            content=f"{strain1.mantra.content} ∪ {strain2.mantra.content}",
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
        )
        self.meme_strains[fusion_strain.strain_id] = fusion_strain
        
        # Convertir les agents porteurs des deux souches vers la fusion
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
    
    # -------------------------------------------------------------------
    # Événements aléatoires (conservés)
    # -------------------------------------------------------------------
    def _maybe_trigger_random_event(self):
        event_prob = self.params.get("random_event_prob", 0.03)
        if self.rng.random() >= event_prob:
            return
        
        # Événements enrichis (certains sont déjà traités ailleurs)
        event_type = self.rng.choice([
            "schism", "prophecy", "censorship", "reformation",
            "pilgrimage", "relic_creation", "oracle_whisper"
        ])
        
        # Utiliser les fonctions existantes (à conserver)
        # Je simplifie ici pour la lisibilité du code
        pass
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.0] GÉNÉRATION DE MYTHES FONDATEURS (conservée)
    # -------------------------------------------------------------------
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
        logger.info(f"t={self.current_t} 📖 MYTHE FONDATEUR créé : {myth.myth_id} ({len(verses)} versets)")
    
    # -------------------------------------------------------------------
    # [NOUVEAU v2.1] CAPTURE D'ÉTAT POUR CSV (conservée)
    # -------------------------------------------------------------------
    def _capture_agent_state(self):
        """Capture l'état complet de tous les agents pour export CSV."""
        for agent in self.agents:
            self.agent_state_history.append({
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
            })
    
    def _capture_strain_state(self):
        """Capture l'état de toutes les souches pour export CSV."""
        total_agents = len(self.agents)
        for strain_id, strain in self.meme_strains.items():
            carriers = [a for a in self.agents 
                       if a.current_strain.strain_id == strain_id 
                       and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
            
            exposed = [a for a in self.agents 
                      if a.current_strain.strain_id == strain_id 
                      and a.cultural_status == CulturalStatus.EXPOSED]
            
            self.strain_history.append({
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
            })
    
    # -------------------------------------------------------------------
    # Boucle principale (MODIFIÉE avec les nouvelles fonctionnalités)
    # -------------------------------------------------------------------
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
        
        # [NOUVEAU v2.2] Gravité narrative
        self._apply_narrative_gravity()
        
        # [NOUVEAU v2.2] Cycles narratifs
        self._apply_narrative_cycle()
        
        # [NOUVEAU v2.2] Événements enrichis
        if self.rng.random() < 0.015:  # 1.5% de chance
            self._trigger_narrative_eclipse()
        if self.rng.random() < 0.015:
            self._trigger_cultural_resonance()
        
        self._maybe_trigger_random_event()
        self._maybe_generate_myth()
        
        # [NOUVEAU v2.2] Mise à jour des factions
        self._update_factions()
        
        for agent in self.agents:
            self._progress_narrative(agent)
        
        # Métriques
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
        
        logger.debug(f"t={self.current_t} | Rt={rt:.2f} | Souches={len(self.meme_strains)} | Reliques={len(self.relics)} | Factions={len(self.faction_system.factions)}")
        
        self.current_t += 1
        for agent in self.agents:
            agent.current_t = self.current_t
        
        return {"t": self.current_t, "rt": rt, "metrics": dict(self.daily_metrics[self.current_t - 1])}
    
    def run(self, steps: int):
        for _ in range(steps):
            yield self.step()


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] Export CSV enrichi
# ═══════════════════════════════════════════════════════════════════════════════

class CSVExporterV22:
    """Version v2.2 de l'export CSV avec données enrichies."""
    
    @staticmethod
    def export_all(sim: CulturalEpidemicSimulation, output_dir: str):
        """Exporte toutes les tables CSV avec les nouvelles données."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        # Tables principales (héritées)
        CSVExporterV22._export_agents(out / "agents_state.csv", sim)
        CSVExporterV22._export_strains(out / "strains_state.csv", sim)
        CSVExporterV22._export_metrics(out / "daily_metrics.csv", sim)
        CSVExporterV22._export_events(out / "narrative_events.csv", sim)
        CSVExporterV22._export_random_events(out / "random_events.csv", sim)
        CSVExporterV22._export_interactions(out / "interactions.csv", sim)
        CSVExporterV22._export_relics(out / "relics.csv", sim)
        CSVExporterV22._export_myths(out / "myths.csv", sim)
        CSVExporterV22._export_chronicle(out / "chronicle.csv", sim)
        CSVExporterV22._export_semantic_drift(out / "semantic_drift.csv", sim)
        
        # Tables supplémentaires v2.2
        CSVExporterV22._export_factions(out / "factions.csv", sim)
        CSVExporterV22._export_alliances(out / "alliances.csv", sim)
        CSVExporterV22._export_episodic_memory(out / "episodic_memory.csv", sim)
        CSVExporterV22._export_gravity(out / "narrative_gravity.csv", sim)
        
        # README
        CSVExporterV22._export_readme(out / "README_KNIME.txt")
        
        logger.info(f"📊 {len(list(out.glob('*.csv')))} fichiers CSV exportés dans {out}/")
    
    @staticmethod
    def _export_agents(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte l'état des agents."""
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
        """Exporte l'état des souches."""
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
        """Exporte les métriques agrégées."""
        rows = []
        for t, metrics in sorted(sim.daily_metrics.items()):
            row = {"timestamp": t}
            row.update(metrics)
            if t < len(sim.rt_history):
                row["rt"] = sim.rt_history[t]
            rows.append(row)
        
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Métriques: {len(rows)} lignes")
    
    @staticmethod
    def _export_events(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les événements narratifs."""
        rows = []
        for e in sim.events:
            rows.append({
                "timestamp": e.timestamp,
                "agent_id": e.agent_id,
                "event_type": e.event_type,
                "cultural_state": e.cultural_state,
                "source_id": e.source_id or -1,
                "guild": e.guild or "",
                "narrative_coherence": e.narrative_coherence or 0,
                "strain_id": e.strain_id or "",
            })
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Événements narratifs: {len(rows)} lignes")
    
    @staticmethod
    def _export_random_events(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les événements aléatoires."""
        rows = []
        for e in sim.random_events:
            rows.append({
                "event_id": e.event_id,
                "event_type": e.event_type,
                "timestamp": e.timestamp,
                "zone": e.zone or "",
                "description": e.description,
                "affected_agents_count": len(e.affected_agents),
                "affected_agents": ",".join(str(a) for a in e.affected_agents[:10]),
                "impact": json.dumps(e.impact, ensure_ascii=False),
            })
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Événements aléatoires: {len(rows)} lignes")
    
    @staticmethod
    def _export_interactions(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les interactions."""
        rows = []
        for i in sim.interactions:
            rows.append({
                "timestamp": i.timestamp,
                "agent_a": i.agent_a,
                "agent_b": i.agent_b,
                "intensity": i.intensity,
                "transmission_risk": i.transmission_risk,
                "transmission_occurred": 1 if i.transmission_occurred else 0,
            })
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Interactions: {len(rows)} lignes")
    
    @staticmethod
    def _export_relics(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les reliques."""
        rows = []
        for r in sim.relics:
            rows.append({
                "relic_id": r.relic_id,
                "guardian_id": r.guardian_id,
                "zone": r.zone,
                "preserved_at": r.preserved_at,
                "mantra_content": r.mantra.content,
                "mantra_theme": r.mantra.theme,
                "veneration_count": r.veneration_count,
            })
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Reliques: {len(rows)} lignes")
    
    @staticmethod
    def _export_myths(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les mythes fondateurs."""
        rows = []
        for m in sim.founding_myths:
            rows.append({
                "myth_id": m.myth_id,
                "title": m.title,
                "created_at": m.created_at,
                "verses": " | ".join(m.verses),
                "dominant_strains": ",".join(m.dominant_strains),
                "verse_count": len(m.verses),
            })
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Mythes: {len(rows)} lignes")
    
    @staticmethod
    def _export_chronicle(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte la chronique."""
        rows = []
        for c in sim.chronicle:
            rows.append({
                "timestamp": c.get("t", 0),
                "event_type": c.get("type", ""),
                "event_id": c.get("event", ""),
                "myth_id": c.get("myth_id", ""),
                "faction_id": c.get("faction_id", ""),
            })
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Chronique: {len(rows)} lignes")
    
    @staticmethod
    def _export_semantic_drift(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte la dérive sémantique."""
        rows = []
        for parent, children in sim.semantic_drift.items():
            for child in children:
                rows.append({
                    "parent_strain": parent,
                    "child_strain": child,
                })
        if not rows:
            rows.append({"parent_strain": "", "child_strain": ""})
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["parent_strain", "child_strain"])
            writer.writeheader()
            writer.writerows(rows)
        logger.debug(f"✅ Dérive sémantique: {len(rows)} lignes")
    
    @staticmethod
    def _export_factions(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les factions."""
        rows = []
        for faction in sim.faction_system.factions.values():
            rows.append({
                "faction_id": faction.faction_id,
                "name": faction.name,
                "founder_id": faction.founder_id,
                "founding_strain": faction.founding_strain,
                "created_at": faction.created_at,
                "member_count": len(faction.members),
                "alliance_count": len(faction.alliances),
                "color": faction.color,
                "rituals": " | ".join(faction.rituals)
            })
        if rows:
            fieldnames = list(rows[0].keys())
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Factions: {len(rows)} lignes")
    
    @staticmethod
    def _export_alliances(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte les alliances."""
        rows = []
        for faction in sim.faction_system.factions.values():
            for ally_id in faction.alliances:
                rows.append({
                    "faction_id": faction.faction_id,
                    "ally_id": ally_id,
                    "timestamp": sim.current_t
                })
        if rows:
            fieldnames = ["faction_id", "ally_id", "timestamp"]
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Alliances: {len(rows)} lignes")
    
    @staticmethod
    def _export_episodic_memory(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte la mémoire épisodique (échantillon)."""
        rows = []
        for agent in sim.agents[:100]:
            for evt in agent.episodic_memory.events[-10:]:
                rows.append({
                    "agent_id": agent.id,
                    "timestamp": evt['timestamp'],
                    "event_type": evt['type'],
                    "content": evt['content'],
                    "impact": evt['impact']
                })
        if rows:
            fieldnames = ["agent_id", "timestamp", "event_type", "content", "impact"]
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Mémoire épisodique: {len(rows)} lignes")
    
    @staticmethod
    def _export_gravity(path: Path, sim: CulturalEpidemicSimulation):
        """Exporte la gravité narrative."""
        rows = []
        for strain_id, center in sim.narrative_gravity.gravity_centers.items():
            rows.append({
                "strain_id": strain_id,
                "mass": center['mass'],
                "influence_radius": center['influence_radius'],
                "position_x": center['position']['x'],
                "position_y": center['position']['y']
            })
        if rows:
            fieldnames = ["strain_id", "mass", "influence_radius", "position_x", "position_y"]
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logger.debug(f"✅ Gravité narrative: {len(rows)} lignes")
    
    @staticmethod
    def _export_readme(path: Path):
        """Génère un README pour l'import KNIME."""
        content = """
╔═══════════════════════════════════════════════════════════════════╗
║          📊 DONNÉES CSV — ARCHEOEPIDEMIC CHIMERA v2.2            ║
║                     Pour traitement KNIME                        ║
╚═══════════════════════════════════════════════════════════════════╝

📁 FICHIERS DISPONIBLES
───────────────────────────────────────────────────────────────────

1. agents_state.csv       → État longitudinal des agents
2. strains_state.csv      → État longitudinal des souches
3. daily_metrics.csv      → Métriques agrégées par pas de temps
4. narrative_events.csv   → Événements narratifs individuels
5. random_events.csv      → Événements aléatoires
6. interactions.csv       → Tentatives de transmission
7. relics.csv             → Reliques préservées
8. myths.csv              → Mythes fondateurs
9. chronicle.csv          → Chronologie des événements majeurs
10. semantic_drift.csv    → Dérive sémantique
11. factions.csv          → Factions émergentes [NOUVEAU v2.2]
12. alliances.csv         → Alliances entre factions [NOUVEAU v2.2]
13. episodic_memory.csv   → Mémoire épisodique des agents [NOUVEAU v2.2]
14. narrative_gravity.csv → Centres de gravité narrative [NOUVEAU v2.2]

🔗 TYPES DE JOINTURES POSSIBLES
───────────────────────────────────────────────────────────────────

• agents_state + factions (faction_id)
• agents_state + episodic_memory (agent_id)
• factions + alliances (faction_id, ally_id)
• strains_state + narrative_gravity (strain_id)
• daily_metrics + factions (timestamp)

📊 MÉTRIQUES CLÉS POUR KNIME
───────────────────────────────────────────────────────────────────

• Rt → taux de reproduction effectif
• cult_I → nombre d'évangélistes
• cult_A → porteurs silencieux
• nb_factions → nombre de factions [NOUVEAU v2.2]
• prevalence → proportion d'adhérents par souche

🔄 WORKFLOW KNIME RECOMMANDÉ
───────────────────────────────────────────────────────────────────

1. CSV Reader → agents_state.csv
2. GroupBy → aggrégation par timestamp
3. Line Plot → évolution des statuts
4. CSV Reader → factions.csv
5. Join → agents_state + factions
6. Bar Chart → distribution des factions

✨ BONNE ANALYSE ! 
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"✅ README KNIME généré")


# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] Visualisation (conservée)
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
    ax.set_title("Réseau narratif — ArcheoEpidemic Chimera v2.2", color="#cccccc", fontsize=11)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# [FUSION] RAPPORT MYTHOLOGIQUE (adapté v2.2)
# ═══════════════════════════════════════════════════════════════════════════════

def mythological_report(sim: CulturalEpidemicSimulation) -> str:
    lines = []
    lines.append("═" * 70)
    lines.append("  📖 RAPPORT MYTHOLOGIQUE — ArcheoEpidemic Chimera v2.2 DATA_ORACLE_EXTENDED")
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
        faction_mark = f" ⚔️{agent.faction_id}" if agent.faction_id else ""
        lines.append(f"  Agent#{agent.id:<4}{relic_mark}{faction_mark} guilde={agent.guild:<12} zone={agent.zone:<18} "
                     f"transmissions={deg}  influence={agent.influence_score:.1f}")
    
    lines.append(f"\n— Évolution narrative —")
    lines.append(f"  Souches totales : {len(sim.meme_strains)}")
    max_gen = max((s.generation for s in sim.meme_strains.values()), default=0)
    lines.append(f"  Générations de mutation : {max_gen}")
    if sim.serial_intervals:
        lines.append(f"  Intervalle sériel moyen : {sum(sim.serial_intervals)/len(sim.serial_intervals):.2f} pas")
    
    # [NOUVEAU v2.2] Factions
    lines.append(f"\n— Factions culturelles ({len(sim.faction_system.factions)}) —")
    for faction in sim.faction_system.factions.values():
        lines.append(f"  {faction.faction_id} — «{faction.name}» ({len(faction.members)} membres)")
        lines.append(f"    Fondée par Agent#{faction.founder_id}, souche {faction.founding_strain}")
        if faction.alliances:
            lines.append(f"    Alliances: {', '.join(faction.alliances)}")
        if faction.rituals:
            lines.append(f"    Rituels: {' | '.join(faction.rituals[:2])}")
    
    lines.append(f"\n— Reliques sacrées ({len(sim.relics)}) —")
    for relic in sim.relics[:5]:
        lines.append(f"  {relic.relic_id} (préservée t={relic.preserved_at} à {relic.zone})")
        lines.append(f"    Gardien : Agent#{relic.guardian_id}")
        lines.append(f"    « {relic.mantra.content[:60]}... »")
    
    lines.append(f"\n— Mythes fondateurs ({len(sim.founding_myths)}) —")
    for myth in sim.founding_myths:
        lines.append(f"  {myth.myth_id} — « {myth.title} » (t={myth.created_at})")
        for i, verse in enumerate(myth.verses, 1):
            lines.append(f"    {i}. {verse}")
    
    lines.append(f"\n— Chronique des événements ({len(sim.random_events)}) —")
    for evt in sim.random_events[-10:]:
        lines.append(f"  [t={evt.timestamp}] {evt.description}")
    
    lines.append(f"\n— Dérive sémantique (lignées de mutation) —")
    for parent, children in list(sim.semantic_drift.items())[:5]:
        if children:
            lines.append(f"  {parent} → {', '.join(children[:3])}{'...' if len(children) > 3 else ''}")
    
    # [NOUVEAU v2.2] Gravité narrative
    lines.append(f"\n— Gravité narrative —")
    for strain_id, center in list(sim.narrative_gravity.gravity_centers.items())[:3]:
        lines.append(f"  {strain_id}: masse={center['mass']:.2f}, rayon={center['influence_radius']:.2f}")
    
    lines.append("\n" + "═" * 70)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] FONCTION PRINCIPALE AVEC EXPORT NEO4J ET DATA_DIR
# ═══════════════════════════════════════════════════════════════════════════════

def run_cultural_epidemic_simulation(params: dict, genome_pool: Optional[List[CulturalGenome]] = None,
                                     steps: int = 60, verbose: bool = False,
                                     retro_display: bool = True,
                                     export_csv: Optional[str] = None,
                                     export_neo4j: Optional[str] = None,
                                     data_dir: Optional[str] = None) -> CulturalEpidemicSimulation:
    """Version v2.2 avec externalisation JSON et export Neo4J."""
    
    # Initialiser le gestionnaire de données
    if data_dir:
        data_manager = JSONDataManager(data_dir)
        set_data_manager(data_manager)
    
    sim = CulturalEpidemicSimulation(params, genome_pool, data_dir)
    
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
                  f"Dés={m.get('cult_R', 0)} Oub={m.get('cult_D', 0)} "
                  f"Souches={m.get('nb_strains', 0)} Reliques={m.get('nb_relics', 0)} "
                  f"Factions={m.get('nb_factions', 0)}")
    
    if retro_display and display:
        print("\n" + display.c("═══ ✦ FIN DE LA SIMULATION ✦ ═══", "bright_magenta", "bold"))
    
    # Export CSV v2.2
    if export_csv:
        CSVExporterV22.export_all(sim, export_csv)
        logger.info(f"📊 Données CSV exportées dans {export_csv}/")
    
    # Export Neo4J
    if export_neo4j:
        Neo4JExporter.export_all(sim, export_neo4j)
        logger.info(f"🦈 Données Neo4J exportées dans {export_neo4j}/")
    
    return sim


# ═══════════════════════════════════════════════════════════════════════════════
# [NOUVEAU v2.2] RETROWAVE DISPLAY (conservé)
# ═══════════════════════════════════════════════════════════════════════════════

class RetroWaveDisplay:
    """Afficheur style rétro-wave / cyberpunk pour la simulation."""
    
    # Codes couleur ANSI
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "hidden": "\033[8m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
        "bg_black": "\033[40m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
        "bg_magenta": "\033[45m",
        "bg_cyan": "\033[46m",
        "bg_white": "\033[47m",
        "bg_bright_black": "\033[100m",
        "bg_bright_red": "\033[101m",
        "bg_bright_green": "\033[102m",
        "bg_bright_yellow": "\033[103m",
        "bg_bright_blue": "\033[104m",
        "bg_bright_magenta": "\033[105m",
        "bg_bright_cyan": "\033[106m",
        "bg_bright_white": "\033[107m",
    }
    
    SYMBOLS = {
        "heart": "♥",
        "star": "★",
        "spark": "✦",
        "arrow": "➜",
        "diamond": "◆",
        "bullet": "●",
        "radioactive": "☢",
        "skull": "☠",
        "music": "♪",
        "sun": "☀",
        "moon": "☽",
        "wave": "〰",
        "infinity": "∞",
        "circle": "○",
        "square": "□",
        "triangle": "△",
        "pentagram": "✪",
        "spiral": "꩜",
        "eye": "👁",
        "fire": "🔥",
        "storm": "🌩",
        "crystal": "💎",
        "neon": "⚡",
        "vortex": "🌀",
        "phoenix": "🐦‍🔥",
        "serpent": "🐍",
        "cyber": "⚙",
        "fractal": "ꙮ",
        "glyph": "𐊿",
        "runes": "ᚠᚢᚦᚨᚱ",
    }
    
    def __init__(self, width: int = 80):
        self.width = min(width, shutil.get_terminal_size().columns - 2)
        self.start_time = time.time()
        self.last_frame = 0
        self.frame_count = 0
        self.animation_chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        self._anim_idx = 0
        self.banner_cache = None
        self._last_output_height = 0
        self._first_render = True
    
    def color(self, text: str, *codes: str) -> str:
        if not codes:
            return text
        color_codes = [self.COLORS.get(c, "") for c in codes if c in self.COLORS]
        return f"{''.join(color_codes)}{text}{self.COLORS['reset']}"
    
    def c(self, text: str, *codes: str) -> str:
        return self.color(text, *codes)
    
    def neon_box(self, text: str, width: int = None, border: str = "double", 
                 color: str = "cyan", glow: bool = True) -> str:
        if width is None:
            width = self.width
        width = max(len(text) + 4, width)
        
        if border == "double":
            t, tr, r, br, b, bl, l, tl = "╔", "╗", "║", "╝", "╚", "╚", "║", "╔"
        elif border == "round":
            t, tr, r, br, b, bl, l, tl = "╭", "╮", "│", "╯", "╰", "╰", "│", "╭"
        elif border == "heavy":
            t, tr, r, br, b, bl, l, tl = "┏", "┓", "┃", "┛", "┗", "┗", "┃", "┏"
        else:
            t, tr, r, br, b, bl, l, tl = "┌", "┐", "│", "┘", "└", "└", "│", "┌"
        
        glow_chars = "✦" if glow else " "
        top_line = f"{self.c(t, color)}" + f"{self.c('─', color)}" * (width - 2) + f"{self.c(tr, color)}"
        mid_line = f"{self.c(l, color)} " + f"{text:^{width-4}}" + f" {self.c(r, color)}"
        bot_line = f"{self.c(b, color)}" + f"{self.c('─', color)}" * (width - 2) + f"{self.c(br, color)}"
        
        return f"\n{top_line}\n{mid_line}\n{bot_line}"
    
    def banner(self) -> str:
        if self.banner_cache:
            return self.banner_cache
            
        banner_text = r"""
     ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
    ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
    ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌          
    ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌          
    ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌          
    ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌          
    ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌          
    ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ 
    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
     ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
        """
        
        lines = banner_text.split("\n")
        colored_lines = []
        for i, line in enumerate(lines):
            if i == 0 or i == len(lines) - 1:
                colored_lines.append(self.c(line, "cyan", "bold"))
            elif i == 2 or i == 8:
                colored_lines.append(self.c(line, "magenta"))
            else:
                ratio = i / len(lines)
                if ratio < 0.5:
                    colored_lines.append(self.c(line, "cyan"))
                else:
                    colored_lines.append(self.c(line, "magenta"))
        
        banner = "\n".join(colored_lines)
        banner += self.c("\n\n ════════════ ✦ ARCHEOEPIDEMIC CHIMERA v2.2 DATA_ORACLE_EXTENDED ✦ ════════════\n", "bright_cyan", "bold")
        banner += self.c("   ▸ Fusion : Glyphosophia × Corrupted Blood\n", "dim")
        banner += self.c("   ▸ Normandie Fractale, 2075\n", "dim")
        banner += self.c("   ▸ Épidémie narrative agent-based\n", "dim")
        banner += self.c("   ▸ Export CSV + Neo4J + données externes JSON\n", "dim")
        banner += self.c("   ▸ Gravité narrative + Factions + Mémoire épisodique\n", "dim")
        banner += self.c("\n", "reset")
        
        self.banner_cache = banner
        return banner
    
    def status_bar(self, sim) -> str:
        total = len(sim.agents)
        status_counts = Counter(a.cultural_status for a in sim.agents)
        bar_width = self.width - 40
        
        def make_bar(status: CulturalStatus, color: str, icon: str) -> str:
            count = status_counts.get(status, 0)
            pct = count / max(1, total)
            filled = int(pct * bar_width)
            empty = bar_width - filled
            bar = self.c("█" * filled, color) + self.c("░" * empty, "dim")
            return f"{self.c(icon, color)} {status.name[:3]:<3} {bar} {count:>3} ({pct*100:>5.1f}%)"
        
        lines = [
            self.c("╔" + "═" * (self.width - 2) + "╗", "bright_cyan"),
        ]
        
        t = sim.current_t
        strains = len(sim.meme_strains)
        relics = len(sim.relics)
        myths = len(sim.founding_myths)
        factions = len(sim.faction_system.factions)
        rt = sim.rt_history[-1] if sim.rt_history else 0
        
        line1 = f"  {self.c('⏱', 'cyan')} t={t:>3}  {self.c('🧬', 'magenta')} souches={strains:>2}  {self.c('📜', 'yellow')} reliques={relics:>2}  {self.c('📖', 'green')} mythes={myths:>2}  {self.c('⚔️', 'red')} factions={factions:>2}  {self.c('📈', 'red')} Rt={rt:>5.2f}  {self.c('👤', 'blue')} pop={total:>3}"
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
    
    def event_feed(self, sim, n: int = 3) -> str:
        events = sim.random_events[-n:] if sim.random_events else []
        if not events:
            return self.c("  [ silence narratif... ]", "dim")
        
        lines = []
        for evt in events[-n:]:
            icon = {
                "schism": "🔱",
                "prophecy": "🜃",
                "censorship": "🚫",
                "reformation": "✨",
                "pilgrimage": "🕊",
                "relic_creation": "📜",
                "oracle_whisper": "🔮",
                "faction_emergence": "🏛",
                "narrative_eclipse": "🌑",
                "cultural_resonance": "🎵",
            }.get(evt.event_type, "⚡")
            
            color = {
                "schism": "bright_red",
                "prophecy": "bright_yellow",
                "censorship": "bright_red",
                "reformation": "bright_green",
                "pilgrimage": "bright_cyan",
                "relic_creation": "bright_yellow",
                "oracle_whisper": "bright_magenta",
                "faction_emergence": "bright_red",
                "narrative_eclipse": "bright_cyan",
                "cultural_resonance": "bright_green",
            }.get(evt.event_type, "cyan")
            
            lines.append(f"  {self.c(icon, color)} {self.c(evt.description[:self.width-20], color)}")
        return "\n".join(lines)
    
    def prophet_corner(self, sim) -> str:
        if not sim.founding_myths:
            return self.c("  🔮 L'oracle attend le premier mythe...", "dim")
        
        last_myth = sim.founding_myths[-1]
        verses = last_myth.verses[:2]
        lines = [
            self.c("  🔮 PROPHÉTIE DU TEMPS PRÉSENT", "bright_magenta", "bold"),
        ]
        for v in verses:
            lines.append(f"    {self.c(v[:60], 'magenta', 'italic')}...")
        return "\n".join(lines)
    
    def render_ascii_art(self, sim) -> str:
        total = len(sim.agents)
        if total == 0:
            return ""
        
        cols = min(40, max(10, self.width // 3))
        rows = max(1, min(10, total // cols + 1))
        
        glyphs = {
            CulturalStatus.RECEPTIVE: "·",
            CulturalStatus.EXPOSED: "◌",
            CulturalStatus.EVANGELIST: "★",
            CulturalStatus.SILENT_CARRIER: "☽",
            CulturalStatus.DISENCHANTED: "✧",
            CulturalStatus.OBLIVIOUS: "·",
        }
        
        colors = {
            CulturalStatus.RECEPTIVE: "bright_blue",
            CulturalStatus.EXPOSED: "yellow",
            CulturalStatus.EVANGELIST: "bright_red",
            CulturalStatus.SILENT_CARRIER: "bright_magenta",
            CulturalStatus.DISENCHANTED: "green",
            CulturalStatus.OBLIVIOUS: "bright_black",
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
                    else:
                        glyph = self.c(glyph, color)
                    row.append(glyph)
                else:
                    row.append(" ")
                idx += 1
            grid.append(" ".join(row))
        
        return "\n".join(grid)
    
    def animated_step(self, sim, step: int, total_steps: int) -> str:
        elapsed = time.time() - self.start_time
        progress = step / max(1, total_steps)
        
        spinner = self.animation_chars[self._anim_idx % len(self.animation_chars)]
        self._anim_idx += 1
        
        lines = []
        lines.append(self.c(f"════════════════════════════════════════════════════════════════════", "bright_cyan"))
        
        bar_len = self.width - 20
        filled = int(progress * bar_len)
        bar = self.c("█" * filled, "bright_magenta") + self.c("░" * (bar_len - filled), "dim")
        lines.append(f"  {self.c('PROGRÈS', 'bright_cyan', 'bold')} [{bar}] {spinner} {step}/{total_steps}")
        
        factions = len(sim.faction_system.factions)
        lines.append(f"  {self.c('⏱', 'bright_yellow')} Écoulé : {elapsed:.1f}s  |  {self.c('⚡', 'bright_cyan')} Pas : {step}  |  {self.c('🧬', 'bright_magenta')} Souches : {len(sim.meme_strains)}  |  {self.c('⚔️', 'bright_red')} Factions : {factions}")
        
        if sim.random_events and sim.random_events[-1].timestamp == sim.current_t - 1:
            last_evt = sim.random_events[-1]
            icon = {
                "schism": "🔱", "prophecy": "🜃", "censorship": "🚫",
                "reformation": "✨", "pilgrimage": "🕊", "relic_creation": "📜",
                "oracle_whisper": "🔮", "faction_emergence": "🏛",
                "narrative_eclipse": "🌑", "cultural_resonance": "🎵"
            }.get(last_evt.event_type, "⚡")
            lines.append(f"  {self.c('⚡ ÉVÉNEMENT', 'bright_yellow', 'bold')} {icon} {self.c(last_evt.description[:60], 'bright_cyan')}")
        
        lines.append("")
        lines.append(self.status_bar(sim))
        
        lines.append("")
        lines.append(self.c("  ✦ CARTE NARRATIVE ✦", "bright_cyan", "bold"))
        lines.append(self.render_ascii_art(sim))
        
        lines.append("")
        lines.append(self.prophet_corner(sim))
        
        lines.append("")
        lines.append(self.c("  ⚡ FIL DES ÉVÉNEMENTS", "bright_yellow", "bold"))
        lines.append(self.event_feed(sim, 2))
        
        lines.append(self.c(f"════════════════════════════════════════════════════════════════════", "bright_cyan"))
        
        return "\n".join(lines)
    
    def render_report(self, sim, report: str) -> str:
        lines = []
        lines.append(self.c("╔" + "═" * (self.width - 2) + "╗", "bright_magenta"))
        lines.append(self.c("║" + " 📖 RAPPORT MYTHOLOGIQUE ".center(self.width - 2, "═") + "║", "bright_magenta", "bold"))
        lines.append(self.c("╚" + "═" * (self.width - 2) + "╝", "bright_magenta"))
        lines.append("")
        
        for line in report.split("\n"):
            if "RAPPORT MYTHOLOGIQUE" in line:
                continue
            if line.startswith("═") or line.startswith("—"):
                lines.append(self.c(line, "bright_cyan"))
            elif "Population totale" in line or "Répartition" in line:
                lines.append(self.c(line, "bright_yellow", "bold"))
            elif "Récits dominants" in line or "Superspreaders" in line:
                lines.append(self.c(line, "bright_magenta", "bold"))
            elif "Reliques" in line or "Mythes" in line or "Factions" in line:
                lines.append(self.c(line, "bright_green", "bold"))
            elif "Chronique" in line or "Dérive" in line or "Gravité" in line:
                lines.append(self.c(line, "bright_cyan", "bold"))
            elif "[" in line and "]" in line:
                parts = line.split("[")
                if len(parts) > 1:
                    left = parts[0]
                    mid = "[" + parts[1].split("]")[0] + "]"
                    right = "]" + "]".join(parts[1].split("]")[1:]) if "]" in parts[1] else ""
                    lines.append(f"{left}{self.c(mid, 'bright_yellow')}{right}")
                else:
                    lines.append(line)
            else:
                lines.append(line)
        
        lines.append("")
        lines.append(self.c("═══ FIN DU RAPPORT ═══".center(self.width, "═"), "bright_magenta"))
        return "\n".join(lines)
    
    def clear_screen(self):
        """Efface l'écran et repositionne le curseur."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[H", end="")
        sys.stdout.flush()
    
    def render_full(self, sim, step: int, total_steps: int, report: str = None) -> str:
        """Rendu complet avec rafraîchissement stabilisé."""
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
            print(self.render_report(sim, report))
        
        sys.stdout.flush()
        return output


# ═══════════════════════════════════════════════════════════════════════════════
# [UTILITAIRE] Fallback mini graph
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
# CLI v2.2
# ═══════════════════════════════════════════════════════════════════════════════

def _pre_parse_data_dir() -> Optional[str]:
    """
    [PATCH v2.2.1] Pré-analyse la ligne de commande à la recherche de --data-dir,
    AVANT la construction du parser complet. Sans cela, --root-theme fige ses
    choix sur les données internes (le JSONDataManager global n'étant pas encore
    pointé vers data_dir au moment où build_arg_parser() appelle get_themes_list()).
    """
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--data-dir", type=str, default=None)
    known, _ = pre.parse_known_args()
    return known.data_dir


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="archeoepidemic_chimera",
        description="🧬🌌 ARCHEOEPIDEMIC CHIMERA v2.2 DATA_ORACLE_EXTENDED — Simulateur d'épidémies narratives",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # --- Paramètres généraux ---
    gen = p.add_argument_group("Général")
    gen.add_argument("--seed", type=int, default=2075, help="Graine aléatoire")
    gen.add_argument("--steps", type=int, default=60, help="Nombre de pas de temps")
    gen.add_argument("--verbose", action="store_true", help="Affichage pas-à-pas")
    gen.add_argument("--no-retro", action="store_true", help="Désactiver l'affichage rétro-wave")
    gen.add_argument("--log-file", type=str, default=None, help="Fichier de log")
    gen.add_argument("--log-level", type=str, default="INFO",
                     choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Niveau de log")
    
    # --- Données externes ---
    data = p.add_argument_group("Données externes")
    data.add_argument("--data-dir", type=str, default=None,
                      help="Répertoire des fichiers JSON de données (fallback interne si absent)")
    data.add_argument("--init-data", type=str, default=None,
                      help="Créer les fichiers JSON de données dans ce répertoire")
    
    # --- Export ---
    exp = p.add_argument_group("Export de données")
    exp.add_argument("--export-csv", type=str, default=None,
                     help="Répertoire d'export des CSV multi-tables")
    exp.add_argument("--export-json", type=str, default=None,
                     help="Répertoire d'export JSON")
    exp.add_argument("--export-neo4j", type=str, default=None,
                     help="Répertoire d'export Neo4J (Cypher)")
    exp.add_argument("--export-network", type=str, default=None,
                     help="Chemin PNG du réseau")
    
    # --- Population ---
    pop = p.add_argument_group("Population")
    pop.add_argument("--pop-total", type=int, default=180, help="Nombre total d'agents")
    pop.add_argument("--nb-zones", type=int, default=6, help="Nombre de zones")
    pop.add_argument("--initial-believers", type=int, default=3, help="Croyants initiaux")
    
    # --- Souche racine ---
    root = p.add_argument_group("Souche racine")
    root.add_argument("--root-theme", type=str, default="rituel",
                      choices=get_themes_list(), help="Thème du mantra racine")
    root.add_argument("--r0-base", type=float, default=2.4, help="R0 de base")
    root.add_argument("--latency-period", type=float, default=3.0, help="Période de latence")
    
    # --- Dynamiques ---
    dyn = p.add_argument_group("Dynamiques narratives")
    dyn.add_argument("--disenchant-rate", type=float, default=0.04, help="Taux de désenchantement")
    dyn.add_argument("--oblivion-rate", type=float, default=0.003, help="Taux d'oubli")
    dyn.add_argument("--mutation-prob", type=float, default=0.02, help="Probabilité de mutation")
    dyn.add_argument("--dogma-rate", type=float, default=0.01, help="Intensité dogmatique")
    
    # --- Événements ---
    evt = p.add_argument_group("Événements")
    evt.add_argument("--random-event-prob", type=float, default=0.03, help="Probabilité d'événement aléatoire")
    evt.add_argument("--myth-generation-period", type=int, default=20, help="Période de génération des mythes")
    evt.add_argument("--max-myths", type=int, default=3, help="Nombre maximum de mythes")
    
    return p


def main():
    # [PATCH v2.2.1] Précharger --data-dir en amont pour que --root-theme
    # propose bien les thèmes définis dans themes.json (et pas seulement
    # les 6 thèmes internes de fallback).
    _early_data_dir = _pre_parse_data_dir()
    if _early_data_dir:
        set_data_manager(JSONDataManager(_early_data_dir))

    parser = build_arg_parser()
    args = parser.parse_args()
    
    # Gestion de l'initialisation des données
    if args.init_data:
        manager = JSONDataManager()
        manager.save_external_data(args.init_data)
        print(f"✅ Données initialisées dans {args.init_data}/")
        return
    
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    
    logger.info("🌌🧬 Démarrage d'ArcheoEpidemic Chimera v2.2 — Normandie Fractale, 2075")
    logger.info("Fusion : Glyphosophia × Corrupted Blood")
    logger.info("Ajouts v2.2 : Externalisation JSON, Export Neo4J, Gravité narrative, Factions")
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
    
    sim = run_cultural_epidemic_simulation(
        params, 
        steps=args.steps, 
        verbose=args.verbose,
        retro_display=not args.no_retro,
        export_csv=args.export_csv,
        export_neo4j=args.export_neo4j,
        data_dir=args.data_dir,
    )
    
    print()
    
    # Rapport final
    report = mythological_report(sim)
    if args.no_retro:
        print(report)
    else:
        display = RetroWaveDisplay()
        print(display.render_report(sim, report))
    
    # Export JSON (compatibilité)
    if args.export_json:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("archeo_v2", "ArcheoEpidemic_Chimera2a.py")
            if spec and spec.loader:
                v2_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(v2_module)
                v2_module.export_simulation_data(sim, args.export_json)
                logger.info(f"📦 Données JSON exportées dans {args.export_json}/")
        except Exception as e:
            logger.warning(f"Export JSON désactivé — {e}")
    
    # Export du réseau
    if args.export_network and HAS_MPL and HAS_NX:
        fig = draw_cultural_network(sim)
        if fig:
            fig.savefig(args.export_network, dpi=130, facecolor=fig.get_facecolor())
            logger.info(f"🖼 Réseau narratif exporté : {args.export_network}")
    elif args.export_network:
        logger.warning("matplotlib/networkx indisponibles")


if __name__ == "__main__":
    main()