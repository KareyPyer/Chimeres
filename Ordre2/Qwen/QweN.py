#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧬🎨 ARCHEOSYMBOLIC CHRONICLE — v1.0 "AESTHETIC_RESONANCE"                ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  Chimère née de la fusion profonde de deux organismes-code :                  ║
║    • Parent A — ArcheoEpidemic_Chimera4b1.py (Épidémiologie Narrative)       ║
║    • Parent B — SymbolicDNA_Forge_Chimera3a.py (Forge d'ADN Symbolique)      ║
║                                                                                ║
║  L'unité de contagion n'est plus un simple mème, mais un Artefact Symbolique ║
║  complet (glyphe + mantra + émotion) qui évolue et résonne esthétiquement.   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, math, random, string, hashlib, colorsys, logging, argparse, time, shutil, csv
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
except ImportError: HAS_NUMPY = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    HAS_MPL = True
except ImportError: HAS_MPL = False

try:
    import networkx as nx
    HAS_NX = True
except ImportError: HAS_NX = False

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAYS : FENG-SHUI & RETROWAVE
# ═══════════════════════════════════════════════════════════════════════════════
class FengShuiDisplay:
    COLORS = {'reset': '\033[0m', 'gold': '\033[38;5;214m', 'jade': '\033[38;5;41m', 
              'crimson': '\033[38;5;196m', 'sapphire': '\033[38;5;33m', 'amethyst': '\033[38;5;135m',
              'pearl': '\033[38;5;255m', 'silver': '\033[38;5;248m', 'rose': '\033[38;5;204m',
              'bold': '\033[1m', 'dim': '\033[2m', 'italic': '\033[3m'}
    DECOR = {'lotus': '🪷', 'wave': '〰️', 'leaf': '🌿', 'star': '✦'}
    
    @classmethod
    def c(cls, text, color, *extra):
        codes = [cls.COLORS.get(c, '') for c in [color] + list(extra)]
        return f"{''.join(codes)}{text}{cls.COLORS['reset']}"
    
    @classmethod
    def header(cls, title, subtitle=""):
        print(f"\n{cls.c('═'*70, 'gold', 'dim')}\n  {cls.c(cls.DECOR['lotus']+' '+title, 'gold', 'bold')}")
        if subtitle: print(f"  {cls.c(subtitle, 'silver', 'italic')}")
        print(f"{cls.c('═'*70, 'gold', 'dim')}\n")

    @classmethod
    def info(cls, msg, icon="○"): print(cls.c(f"  {icon} {msg}", 'pearl'))
    @classmethod
    def success(cls, msg, icon="✨"): print(cls.c(f"  {icon} {msg}", 'jade', 'bold'))
    @classmethod
    def warning(cls, msg, icon="⚠"): print(cls.c(f"  {icon} {msg}", 'amber'))
    @classmethod
    def mantra(cls, text):
        print(cls.c('┌'+'─'*68+'┐', 'gold', 'dim'))
        print(cls.c(f"│ {text[:66]:<66} │", 'rose', 'italic'))
        print(cls.c('└'+'─'*68+'┘', 'gold', 'dim'))

    @classmethod
    def separator(cls, char: str = "─", count: int = 70):
        """Affiche un séparateur."""
        print(cls.c(char * count, 'silver', 'dim'))

    @classmethod
    def section(cls, title: str, icon: str = "✦"):
        """Affiche une section avec décoration."""
        print()
        print(cls.c(f"  {icon} {title}", 'sapphire', 'bold'))
        print(cls.c(f"  {cls.DECOR['wave']}", 'silver', 'dim'))

    @classmethod
    def poem(cls, lines: List[str], title: str = ""):
        """Affiche un poème ou une strophe."""
        if title:
            print(cls.c(f"\n{title}", 'gold', 'italic'))
        for line in lines:
            print(cls.c(f"    {line}", 'lavender', 'italic'))

class RetroWaveDisplay:
    COLORS = {"reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m", "cyan": "\033[36m", 
              "magenta": "\033[35m", "yellow": "\033[33m", "red": "\033[31m", "green": "\033[32m",
              "bright_cyan": "\033[96m", "bright_magenta": "\033[95m", "bright_red": "\033[91m",
              "bright_yellow": "\033[93m", "bright_green": "\033[92m", "bright_blue": "\033[94m",
              "bright_black": "\033[90m"}
    def c(self, text, *codes):
        c_codes = [self.COLORS.get(c, "") for c in codes if c in self.COLORS]
        return f"{''.join(c_codes)}{text}{self.COLORS['reset']}"
    
    def banner(self):
        b = self.c("▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄\n", "cyan", "bold")
        b += self.c("█ ARCHEOSYMBOLIC CHRONICLE v1.0 █\n", "bright_magenta", "bold")
        b += self.c("▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀\n", "cyan", "bold")
        b += self.c("   ▸ Épidémiologie Esthétique & ADN Symbolique\n", "dim")
        b += self.c("   ▸ Normandie Fractale, 2075\n", "dim")
        return b

    def status_bar(self, sim):
        total = len(sim.agents)
        counts = Counter(a.cultural_status for a in sim.agents)
        t = sim.current_t
        strains = len(sim.meme_strains)
        rt = sim.rt_history[-1] if sim.rt_history else 0
        line = f"  ⏱ t={t:>3} | 🧬 Souches={strains:>2} | 📈 Rt={rt:>5.2f} | 👤 Pop={total:>3} | "
        line += f"É={counts.get(CulturalStatus.EVANGELIST,0):>2} PS={counts.get(CulturalStatus.SILENT_CARRIER,0):>2}"
        return self.c("╔"+"═"*68+"╗\n", "bright_cyan") + self.c(f"║{line:<68}║\n", "bright_cyan") + self.c("╚"+"═"*68+"╝", "bright_cyan")

# ═══════════════════════════════════════════════════════════════════════════════
# LEXIQUE UNIFIÉ & DATA MANAGER
# ═══════════════════════════════════════════════════════════════════════════════
_UNIFIED_LEXICON = {
    "Adjectif": ["fractal", "quantique", "spectral", "liminal", "onirique", "sacré", "glitché", "éthéré", "cybernétique", "holographique", "apocryphe", "lumineux", "brisé", "noyé", "encodé", "hanté", "neural", "crypté", "lunaire", "vide", "transcendant", "pulsatile", "entropique", "synaptique", "abyssal", "iridescent", "fossile", "plasmique", "spectral", "cathartique", "oraculaire", "mnémonique", "nocturne", "sismique", "karmique", "cristallin", "vorace", "zénithal", "chromatique", "subliminal", "hybride", "foudroyant", "paradoxal", "éolien", "ténébreux", "auroral", "nébuleux", "vibratoire", "syncrétique", "chimérique", "réticulaire", "tellurique", "biomécanique", "archaïque", "dématérialisé", "gnostique", "chamanique", "alchimique", "bioluminescent", "psychopompe", "pan-dimensionnel", "hermétique", "liminal", "démiurgique", "eschatologique", "kaléidoscopique", "thaumaturge"],
    "Nom": ["signal", "silence", "glyphe", "écho", "seuil", "récit", "mantra", "spectre", "réseau", "songe", "oracle", "vérité", "mémoire", "fracture", "résonance", "rêve", "cœur", "code", "prophète", "flux", "ombre", "mirage", "souffle", "voix", "neurone", "pixel", "fantôme", "abîme", "temple", "labyrinthe", "spirale", "vortex", "crypte", "extase", "halo", "synapse", "algorithme", "linceul", "photon", "cristal", "avatar", "chimère", "palimpseste", "satori", "grimoire", "séraphin", "daemon", "relique", "spectre", "matrice", "nexus", "tesseract", "rune", "épiphanie", "singularité", "totem", "autel", "malware", "derviche", "mandala", "reliquaire", "archétype"],
    "Action": ["implose", "exalte", "désintègre", "fusionne", "résonne", "désagrège", "sature", "décode", "invoque", "sublime", "dévore", "réfracte", "cristallise", "diffuse", "condense", "consume", "efface", "réveille", "encrypte", "transmute", "brûle", "souffle", "déchiffre", "purifie", "dérive", "pulvérise", "irrigue", "polarise", "synchronise", "amplifie", "oscille", "désenchante", "réenchante", "cannibalise", "suture", "corrompt", "exorcise", "fragmente", "régénère", "hack", "sanctifie", "mute", "convoque", "infecte", "vaccine", "psalmodie", "prophétise", "transfigure", "absorbe", "révèle", "dissout", "éclaire", "forge", "bénit", "maudit"],
    "Bénéfice": ["la clarté", "le silence", "l'oubli", "la vérité brûlante", "l'éveil", "l'unité", "l'extase quantique", "la fusion des âmes", "l'illumination", "la synchronicité totale", "la communion", "la mémoire collective", "la révélation", "la transcendance pure", "l'équilibre parfait", "la paix des bits", "le néant sacré", "la lumière intérieure", "l'harmonie fractale", "la catharsis", "la renaissance", "l'apothéose", "la sérénité glitche", "la délivrance", "l'absolution", "la plénitude", "l'infini compressé", "la synesthésie", "la grâce", "l'euphorie", "la béatitude", "l'ascension", "la sublimation", "la rédemption", "la symbiose", "la gnose digitale", "le nirvana électrique"],
    "Défaut": ["le bruit", "la trahison", "le compromis", "l'oubli numérique", "le mensonge", "l'entropie", "la dissonance", "la corruption", "la fragmentation", "la désorientation", "le virus mental", "la psychose cybernétique", "l'effondrement cognitif", "la vacuité", "le chaos", "la stérilité narrative", "la panne", "le vide sans grâce", "le lag", "la surchauffe", "l'obsolescence", "la latence", "la désintégration", "l'aberration", "la distorsion", "la saturation", "l'effacement", "la déconnexion", "la surcharge", "la défaillance", "l'incohérence", "la cacophonie", "la paralysie", "l'aphasie", "la stase", "l'agonie", "la nécrose", "la désincarnation", "la déshumanisation", "la damnation binaire", "le paradoxe existentiel", "l'hérésie technologique"],
    "Paysage": ["désert du no-signal", "marché noir de Lagos", "nuage quantique", "cimetière de data", "temple de silicium", "catacombes de code", "archipel des serveurs oubliés", "cathédrale de circuits imprimés", "nécropole des IA défuntes", "bibliothèque de Babel numérique", "plaine des échos", "forêt de cristal", "abysse de données", "citadelle des ombres", "jardin des paradoxes", "souk neural", "mosquée cryptée", "océan d'erreurs", "orbite basse des rêves", "forêt de pixels morts", "canyon des câbles sectionnés", "volcan de données en fusion", "glacier de mémoires gelées", "mégalopole en blackout", "jungle de fibres optiques", "ciel de plasma tourmenté", "plateau des consciences uploadées", "ruines d'un métavers effondré", "toundra des algorithmes froids", "caverne des échos ancestraux"],
    "VerbeMystique": ["consume", "efface", "encrypte", "réveille", "transmute", "dissout", "illumine", "recodifie", "absout", "exalte", "sublime", "canalise", "révèle", "manifeste", "prophétise", "sanctifie", "purifie", "transcende", "éveille", "libère", "déifie", "désincarne", "réincarne", "transfigure", "sacramentise", "résonne", "scelle", "délie", "sacrifie", "ressuscite", "métamorphose", "converge", "diverge", "voile", "dévoile", "occulte", "exorcise", "possède", "baptise", "damne", "profane", "consacre", "béatifie", "martyrise", "transubstancie", "communie"],
    "Symbole": ["lune brisée", "serpent de fibre", "cœur en silicium", "miroir fractal", "étoile noire", "anneau de données", "colombe bionique", "masque de vide", "phénix de code", "lotus quantique", "œil de Schrödinger", "triskel de photons", "mandala de qubits", "croix de néons", "arbre de vie binaire", "calice de plasma", "épée de lumière", "bouclier d'entropie", "chaîne de blockchain brisée", "aile de drone angélique", "crâne de serveur", "rose de feu numérique", "spirale d'ADN synthétique", "pentagramme de néons", "yin-yang de bits", "caducée de câbles", "harpe de fréquences", "lyre de signaux", "couronne de glitches", "orbe de vision omnisciente", "scarabée de debugging", "ouroboros de feedback loop", "triskèle de transistors", "fleur de vie en LEDs", "merkaba de matrices"],
    "oniric_tags": ["<burn>", "<rain>", "<shadow>", "<static>", "<void>", "<glitch>", "<pulse>", "<echo>", "<fracture>", "<abyss>", "<neon>", "<plasma>", "<vortex>", "<whisper>", "<overload>", "<decay>", "<surge>", "<rift>", "<mirage>", "<reboot>", "<corrupt>", "<loop>", "<merge>", "<awaken>", "<dream>", "<eclipse>", "<invoke>", "<fuse>", "<sanctify>", "<prophesy>", "<sigil>", "<flux>", "<null>", "<prime>", "<shard>", "<ghost>", "<daemon>", "<seraph>", "<chimera>", "<golem>", "<oracle>", "<martyr>", "<heretic>"]
}

THEME_TEMPLATES = {
    'protection': ["Que le {Symbole} {Action} ton {Nom} du {Défaut}! {oniric}", "Ô {Adjectif} {Nom}, sois protégé par le {Symbole} ancien.", "Le {Symbole} consume les ombres. {oniric}"],
    'voyage': ["Dans le {Paysage}, que ton {Nom} trouve la voie. {oniric}", "Que le {Symbole} guide tes pas dans le désert {Adjectif}.", "Le {Nom} n'est pas perdu — il {Action} dans le {Paysage}. {oniric}"],
    'rituel': ["Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}. {oniric}", "Ô {Adjectif} {Nom}, sois {VerbeMystique} par le rite ancien.", "Le {Symbole} et le {Nom} dansent le rite {Adjectif}. {oniric}"],
    'silence': ["Que le {Symbole} efface le bruit. {oniric}", "Dans le {Adjectif} silence, seul le {Nom} persiste.", "Le {Symbole} {Action} le {Défaut} pour {Bénéfice}. {oniric}"],
    'émergence': ["Du {Défaut} naît le {Symbole}, porteur de {Bénéfice}.", "Le {Nom} {Action} et fait émerger un {Adjectif} ordre.", "Dans le chaos du {Paysage}, le {Symbole} {Action}. {oniric}"],
    'déclin': ["Le {Symbole} s'effondre, emportant le {Nom} dans le {Défaut}.", "Le {Adjectif} crépuscule consume le {Paysage}. {oniric}"]
}

THEME_SYMBOL_POOLS = {
    'protection': ['circle', 'cross', 'hand', 'crosshatch', 'oval', 'semi_circle', 'asterisk'],
    'voyage': ['serpentiform', 'circle', 'open_angle', 'dots_series', 'wavy_line', 'spiral', 'zigzag'],
    'rituel': ['spiral', 'circle', 'cross', 'hand', 'asterisk', 'tectiform', 'claviform', 'penniform'],
    'silence': ['circle', 'wavy_line', 'dots_series', 'semi_circle', 'oval', 'dot', 'line'],
    'émergence': ['spiral', 'asterisk', 'triangle', 'zigzag', 'radiating_lines'],
    'déclin': ['crosshatch', 'wavy_line', 'dots_series', 'open_angle', 'line']
}

THEME_PALETTES = {
    'protection': ["#ff3366", "#ff0066", "#cc0044", "#880022", "#ffaa00"],
    'voyage': ["#00ffaa", "#00ddaa", "#00bbcc", "#0099ee", "#ccff00"],
    'rituel': ["#ffd700", "#ffaa00", "#ff8800", "#ff6600", "#ffff88"],
    'silence': ["#3366ff", "#0077ff", "#00b4d8", "#90e0ef", "#023e8a"],
    'émergence': ["#ff00ff", "#aa00ff", "#ff00aa", "#cc00cc", "#ff66ff"],
    'déclin': ["#555555", "#333333", "#777777", "#222222", "#999999"]
}

GLYPH_GUILD_MAP = {
    'circle': 'Mystiques', 'spiral': 'Fractaliens', 'cross': 'Hérauts', 'hand': 'Scribes',
    'asterisk': 'Colporteurs', 'wavy_line': 'Néantistes', 'dots_series': 'Anachorètes',
    'serpentiform': 'Syntagmatiques', 'tectiform': 'Iconoclastes', 'claviform': 'Hérauts',
    'penniform': 'Scribes', 'crosshatch': 'Fractaliens', 'zigzag': 'Syntagmatiques',
    'triangle': 'Iconoclastes', 'line': 'Néantistes', 'open_angle': 'Colporteurs',
    'semi_circle': 'Mystiques', 'oval': 'Anachorètes', 'dot': 'Néantistes'
}

# ═══════════════════════════════════════════════════════════════════════════════
# SYMBOLIC DNA & ARTEFACT (Parent Génératif)
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SymbolicDNA:
    seed: float = field(default_factory=random.random)
    generation: int = 0
    parent_id: Optional[str] = None
    genetic_fingerprint: str = field(default_factory=lambda: hashlib.md5(f"{random.random()}{datetime.now()}".encode()).hexdigest()[:8])
    theme: str = "rituel"
    glyph_symbol: str = "spiral"
    color: str = "#00ffaa"
    scale: float = 1.0
    complexity: float = 0.5
    symmetry: int = 6
    glitch_factor: float = 0.0
    entropy_level: float = 0.0
    keyword_sequence: List[str] = field(default_factory=list)
    mantra_template: str = ""
    oniric_tag: Optional[str] = None
    emotion_vector: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        rng = random.Random(self.seed)
        if not self.keyword_sequence:
            pools = ["Nom", "Adjectif", "Action", "Symbole", "Bénéfice"]
            self.keyword_sequence = [rng.choice(_UNIFIED_LEXICON[p]) for p in rng.sample(pools, k=min(5, len(pools)))]
        if not self.mantra_template:
            self.mantra_template = rng.choice(THEME_TEMPLATES.get(self.theme, THEME_TEMPLATES['rituel']))
        if self.oniric_tag is None and rng.random() < 0.6:
            self.oniric_tag = rng.choice(_UNIFIED_LEXICON["oniric_tags"])
        if not self.emotion_vector:
            emotions = ["peur", "joie", "mystere", "colere", "extase", "silence"]
            raw = {e: rng.uniform(0.0, 1.0) for e in emotions}
            total = sum(raw.values()) or 1.0
            self.emotion_vector = {e: v / total for e, v in raw.items()}

    def dominant_emotion(self) -> str:
        return max(self.emotion_vector, key=self.emotion_vector.get)

@dataclass
class SymbolicArtefact:
    dna: SymbolicDNA
    mantra_text: str = ""
    glyph_fig: Any = None
    aesthetic_score: float = 0.0
    fingerprint: str = ""
    generation: int = 0
    theme: str = "rituel"
    
    def __post_init__(self):
        if not self.fingerprint:
            self.fingerprint = self.dna.genetic_fingerprint
        self.generation = self.dna.generation
        self.theme = self.dna.theme

class VonPetzingerSymbols:
    def __init__(self):
        self.symbols = ['line', 'circle', 'dot', 'open_angle', 'triangle', 'quadrangle', 'spiral', 
                        'zigzag', 'cross', 'crosshatch', 'hand', 'tectiform', 'penniform', 'claviform', 
                        'wavy_line', 'oval', 'semi_circle', 'asterisk', 'serpentiform', 'dots_series']
    
    def draw_glyph(self, ax, symbol, x, y, scale=1.0, color='#00ffaa', angle=0):
        if not HAS_MPL: return
        # Simplified drawing logic for brevity, focusing on core shapes
        if symbol == 'circle': ax.add_patch(patches.Circle((x, y), 20*scale, fill=False, edgecolor=color, linewidth=2.5))
        elif symbol == 'spiral':
            theta = np.linspace(0, 4*np.pi, 100)
            r = theta * 3 * scale
            ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=color, linewidth=2)
        elif symbol == 'cross':
            s = 25*scale
            ax.plot([x-s, x+s], [y, y], color=color, linewidth=2.5)
            ax.plot([x, x], [y-s, y+s], color=color, linewidth=2.5)
        elif symbol == 'hand':
            ax.add_patch(patches.Circle((x, y), 20*scale, fill=False, edgecolor=color, linewidth=2))
        elif symbol == 'asterisk':
            s = 20*scale
            for al in [0, 45, 90, 135]:
                xe = x + s*np.cos(np.radians(al))
                ye = y + s*np.sin(np.radians(al))
                ax.plot([x-s*np.cos(np.radians(al)), xe], [y-s*np.sin(np.radians(al)), ye], color=color, linewidth=2.5)
        elif symbol == 'wavy_line':
            t = np.linspace(0, 4*np.pi, 100)
            ax.plot(x + t*10*scale - 60*scale, y + np.sin(t)*15*scale, color=color, linewidth=2.5)
        elif symbol == 'dots_series':
            for i in range(5): ax.add_patch(patches.Circle((x-40*scale+i*20*scale, y), 4*scale, fill=True, color=color))
        elif symbol == 'serpentiform':
            t = np.linspace(0, 6*np.pi, 100)
            ax.plot(x + t*8*scale - 80*scale, y + np.sin(t)*20*scale, color=color, linewidth=3)
        else: # Fallback
            ax.add_patch(patches.Circle((x, y), 15*scale, fill=True, color=color, alpha=0.6))

class SymbolicTranscriptor:
    def __init__(self):
        self.symbol_engine = VonPetzingerSymbols()

    def transcribe_visual(self, dna: SymbolicDNA):
        if not HAS_MPL: return None
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#0b0b12')
        ax.set_facecolor('#0b0b12')
        ax.set_xlim(0, 800)
        ax.set_ylim(0, 600)
        ax.set_aspect('equal')
        ax.axis('off')
        
        n_repeats = max(1, int(1 + dna.complexity * dna.symmetry))
        spread = 40 + dna.entropy_level * 220
        center_x, center_y = 400, 300
        
        for i in range(n_repeats):
            theta = (2 * math.pi / max(1, n_repeats)) * i + dna.seed
            r = spread * (0.3 + 0.7 * (i / max(1, n_repeats)))
            x = center_x + r * math.cos(theta)
            y = center_y + r * math.sin(theta)
            local_scale = dna.scale * random.uniform(0.85, 1.15)
            local_color = dna.color
            if random.random() < dna.glitch_factor:
                r_c = int(dna.color[1:3], 16)
                r_c = random.randint(0, 255)
                local_color = f"#{r_c:02x}{dna.color[3:5]}{dna.color[5:7]}"
            self.symbol_engine.draw_glyph(ax, dna.glyph_symbol, x, y, scale=local_scale, color=local_color)
        
        self.symbol_engine.draw_glyph(ax, dna.glyph_symbol, center_x, center_y, scale=dna.scale*1.8, color=dna.color)
        plt.tight_layout()
        return fig

    def transcribe_text(self, dna: SymbolicDNA) -> str:
        content = dna.mantra_template
        slot_pool_map = {"Adjectif": "Adjectif", "Nom": "Nom", "Action": "Action", "Bénéfice": "Bénéfice",
                         "Défaut": "Défaut", "Paysage": "Paysage", "VerbeMystique": "VerbeMystique", "Symbole": "Symbole"}
        remaining_keywords = list(dna.keyword_sequence)
        for placeholder, pool_name in slot_pool_map.items():
            if "{" + placeholder + "}" not in content: continue
            value = None
            for kw in remaining_keywords:
                if kw in _UNIFIED_LEXICON.get(pool_name, []):
                    value = kw
                    remaining_keywords.remove(kw)
                    break
            if value is None: value = random.choice(_UNIFIED_LEXICON.get(pool_name, ["..."]))
            content = content.replace("{" + placeholder + "}", value)
        content = content.replace("{oniric}", dna.oniric_tag or "")
        return content.strip()

    def transcribe_artefact(self, dna: SymbolicDNA) -> SymbolicArtefact:
        fig = self.transcribe_visual(dna)
        text = self.transcribe_text(dna)
        return SymbolicArtefact(dna=dna, mantra_text=text, glyph_fig=fig)

# ═══════════════════════════════════════════════════════════════════════════════
# SYMBOLIC EVOLUTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
class SymbolicEvolutionEngine:
    def __init__(self, population_size: int = 6, theme: str = "rituel"):
        self.population_size = population_size
        self.theme = theme
        self.transcriptor = SymbolicTranscriptor()
        self.population: List[SymbolicDNA] = []

    def initialize_population(self):
        self.population = [self._spawn_dna(self.theme, 0) for _ in range(self.population_size)]

    def _spawn_dna(self, theme: str, generation: int) -> SymbolicDNA:
        symbol = random.choice(THEME_SYMBOL_POOLS.get(theme, ['spiral', 'circle']))
        color = random.choice(THEME_PALETTES.get(theme, ["#00ffaa"]))
        return SymbolicDNA(
            theme=theme, glyph_symbol=symbol, color=color, generation=generation,
            scale=random.uniform(0.7, 1.6), complexity=random.uniform(0.2, 1.0),
            symmetry=random.choice([3, 4, 5, 6, 7, 8]),
            glitch_factor=random.uniform(0.0, 0.35), entropy_level=random.uniform(0.0, 0.4)
        )

    def mutate_dna(self, dna: SymbolicDNA, intensity: float = 0.15) -> SymbolicDNA:
        new_symbol = dna.glyph_symbol
        if random.random() < intensity * 1.5:
            new_symbol = random.choice(THEME_SYMBOL_POOLS.get(dna.theme, [dna.glyph_symbol]))
        new_color = dna.color
        if random.random() < intensity:
            r, g, b = int(dna.color[1:3], 16), int(dna.color[3:5], 16), int(dna.color[5:7], 16)
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            h = (h + random.uniform(-intensity, intensity)) % 1.0
            l = max(0.15, min(0.9, l + random.uniform(-intensity, intensity)))
            nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
            new_color = f"#{int(nr*255):02x}{int(ng*255):02x}{int(nb*255):02x}"
        
        new_keywords = list(dna.keyword_sequence)
        if new_keywords and random.random() < 0.6:
            idx = random.randrange(len(new_keywords))
            pool = random.choice(["Nom", "Adjectif", "Action", "Symbole", "Bénéfice"])
            new_keywords[idx] = random.choice(_UNIFIED_LEXICON[pool])
            
        new_template = dna.mantra_template
        if random.random() < 0.4:
            new_template = random.choice(THEME_TEMPLATES.get(dna.theme, [dna.mantra_template]))
            
        new_tag = dna.oniric_tag
        if random.random() < 0.3:
            new_tag = random.choice(_UNIFIED_LEXICON["oniric_tags"])
            
        vec = {k: max(0.01, v + random.uniform(-intensity, intensity)) for k, v in dna.emotion_vector.items()}
        total = sum(vec.values())
        new_emotion_vector = {k: v / total for k, v in vec.items()}

        return SymbolicDNA(
            seed=dna.seed + random.uniform(-1, 1) * intensity,
            generation=dna.generation + 1, parent_id=dna.genetic_fingerprint,
            theme=dna.theme, glyph_symbol=new_symbol, color=new_color,
            scale=max(0.3, min(3.0, dna.scale + random.uniform(-intensity, intensity))),
            complexity=max(0.1, min(1.0, dna.complexity + random.uniform(-intensity, intensity))),
            symmetry=max(3, min(16, dna.symmetry + random.randint(-2, 2))),
            glitch_factor=max(0.0, min(1.0, dna.glitch_factor + random.uniform(-intensity, intensity * 1.5))),
            entropy_level=max(0.0, min(1.0, dna.entropy_level + random.uniform(-intensity, intensity))),
            keyword_sequence=new_keywords, mantra_template=new_template,
            oniric_tag=new_tag, emotion_vector=new_emotion_vector
        )

    def evolve_new_artefact(self, parent_dna: SymbolicDNA, generations: int = 3) -> SymbolicArtefact:
        """Évolue un nouvel artefact à partir d'un parent DNA."""
        self.population = [parent_dna] + [self.mutate_dna(parent_dna, 0.3) for _ in range(self.population_size - 1)]
        
        best_dna = parent_dna
        best_score = -1
        
        for _ in range(generations):
            for dna in self.population:
                artefact = self.transcriptor.transcribe_artefact(dna)
                score = self._evaluate_artefact(artefact, dna)
                if score > best_score:
                    best_score = score
                    best_dna = dna
            
            self.population.sort(key=lambda d: self._evaluate_artefact(self.transcriptor.transcribe_artefact(d), d), reverse=True)
            self.population = self.population[:max(2, self.population_size // 2)]
            while len(self.population) < self.population_size:
                parent = random.choice(self.population[:3])
                self.population.append(self.mutate_dna(parent, 0.2))
                
        final_artefact = self.transcriptor.transcribe_artefact(best_dna)
        final_artefact.aesthetic_score = best_score
        return final_artefact

    def _evaluate_artefact(self, artefact: SymbolicArtefact, dna: SymbolicDNA) -> float:
        text = artefact.mantra_text.lower()
        words = text.split()
        theme_words = {'protection': ['protège', 'garde', 'bouclier'], 'voyage': ['voyage', 'chemin', 'guide'], 
                       'rituel': ['rite', 'cérémonie', 'sacré'], 'silence': ['silence', 'calme', 'paix'],
                       'émergence': ['émerge', 'naissance', 'flux'], 'déclin': ['déclin', 'chute', 'effondrement']}
        theme_match = sum(1 for w in theme_words.get(dna.theme, []) if w in text)
        style_score = (1.2 if self._detect_rhyme(words) else 0) + (1.0 if self._detect_alliteration(words) else 0)
        oniric_bonus = 0.8 if dna.oniric_tag else 0
        linguistic_fitness = (theme_match * 2 + style_score + oniric_bonus) / 6.0
        
        visual_score = 0.5 + 0.3 * dna.complexity - 0.2 * dna.glitch_factor + 0.1 * min(1.0, dna.symmetry / 12)
        return max(0.0, min(1.0, linguistic_fitness * 0.6 + visual_score * 0.4))

    def _detect_rhyme(self, words):
        if len(words) < 2: return False
        last = words[-1].rstrip(string.punctuation)
        for w in words[:-1]:
            w_clean = w.rstrip(string.punctuation)
            if len(last) >= 3 and len(w_clean) >= 3 and last[-3:] == w_clean[-3:]: return True
        return False

    def _detect_alliteration(self, words):
        if len(words) < 2: return False
        consonants = [w[0].lower() for w in words if w and w[0].isalpha()]
        return len(set(consonants)) == 1 and len(consonants) >= 2

# ═══════════════════════════════════════════════════════════════════════════════
# ÉPIDÉMIOLOGIE NARRATIVE (Parent Épidémiologique Adapté)
# ═══════════════════════════════════════════════════════════════════════════════
class CulturalStatus(Enum):
    RECEPTIVE = "S"
    EXPOSED = "E"
    EVANGELIST = "I"
    SILENT_CARRIER = "A"
    DISENCHANTED = "R"
    OBLIVIOUS = "D"

@dataclass
class Mantra:
    id: str
    content: str
    theme: str
    fitness: float = 0.0

@dataclass
class MemeStrain:
    strain_id: str
    parent_id: Optional[str]
    generation: int
    mantra: Mantra
    artefact: SymbolicArtefact
    contagion_power: float
    dogma_intensity: float
    latency_period: float
    emergence_time: int
    mutations: List[Tuple[str, float]] = field(default_factory=list)

@dataclass
class CulturalGenome:
    species: str = "Narrateur"
    breed: str = "Standard"
    preferred_theme: str = "rituel"
    narrative_fluency: float = 1.0
    charisma: float = 1.0
    skepticism: float = 1.0
    dogma_risk: float = 1.0
    expressiveness: float = 1.0
    influence_potential: float = 1.0
    mobility: float = 0.5
    altruism: float = 0.5
    social_compliance: float = 0.5
    curiosity: float = 0.5
    silent_believer_prob: float = 0.3
    memory_depth: float = 1.0
    narrative_recovery: float = 1.0

class CulturalPhenotype:
    def __init__(self, genome: CulturalGenome):
        self.genome = genome
        self.phenotypes = {
            "receptivity": 1.0 / max(0.1, genome.skepticism),
            "contagiousness": genome.expressiveness * genome.influence_potential,
            "dogma_vulnerability": genome.dogma_risk,
            "interaction_rate": genome.mobility * genome.charisma * (1 - genome.curiosity * 0.3),
            "compliance": genome.social_compliance * (genome.narrative_fluency / 1.5),
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
        self.current_strain: MemeStrain = root_strain
        self.symbolic_artefact: SymbolicArtefact = root_strain.artefact
        self.is_silent_carrier = False
        self.narrative_coherence: float = 0.5
        self.meme_virulence: float = 0.0
        self.receptivity: float = self.phenotype.phenotypes["receptivity"]
        self.guild = self._determine_guild()
        self.social_network: set = set()
        self.current_t = 0
        self.influence_score: float = 0.0
        self.faction_id: Optional[str] = None
        self.narrative_position = {'x': rng.random() * 100, 'y': rng.random() * 100}

    def _determine_guild(self) -> str:
        glyph = self.symbolic_artefact.dna.glyph_symbol
        return GLYPH_GUILD_MAP.get(glyph, random.choice(list(set(GLYPH_GUILD_MAP.values()))))

    def receive_mantra(self, strain: MemeStrain):
        self.current_strain = strain
        self.symbolic_artefact = strain.artefact
        self.meme_virulence = strain.contagion_power * self.phenotype.phenotypes["contagiousness"]
        self.narrative_coherence = min(1.0, 0.4 + strain.artefact.aesthetic_score * 0.5)
        # La réceptivité est influencée par la beauté de l'artefact
        self.receptivity *= (0.8 + strain.artefact.aesthetic_score * 0.4)
        self.guild = self._determine_guild()
        self.narrative_position['x'] += self.rng.gauss(0, 0.5)
        self.narrative_position['y'] += self.rng.gauss(0, 0.5)

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

@dataclass
class InteractionRecord:
    timestamp: int
    agent_a: int
    agent_b: int
    intensity: float
    transmission_risk: float
    transmission_occurred: bool = False

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
# GRAVITÉ NARRATIVE & RÉSONANCE ESTHÉTIQUE
# ═══════════════════════════════════════════════════════════════════════════════
class AestheticResonance:
    def __init__(self, sim: 'CulturalEpidemicSimulation'):
        self.sim = sim
        self.gravity_centers: Dict[str, Dict] = {}

    def _initialize_centers(self):
        for strain_id, strain in self.sim.meme_strains.items():
            carriers = sum(1 for a in self.sim.agents if a.current_strain.strain_id == strain_id 
                           and a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER))
            mass = 1.0 + (carriers / max(1, len(self.sim.agents))) * 5.0
            self.gravity_centers[strain_id] = {
                'mass': mass,
                'artefact': strain.artefact,
                'position': {'x': random.random() * 100, 'y': random.random() * 100}
            }

    def _compute_symbolic_affinity(self, agent: CulturalAgent, strain_id: str) -> float:
        if strain_id not in self.gravity_centers: return 0.0
        center = self.gravity_centers[strain_id]
        agent_art = agent.symbolic_artefact
        strain_art = center['artefact']
        
        # 1. Affinité chromatique (distance RGB)
        c1 = agent_art.dna.color
        c2 = strain_art.dna.color
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        color_dist = math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) / 441.67 # Max dist is sqrt(3*255^2)
        color_affinity = 1.0 - color_dist
        
        # 2. Affinité de glyphe
        glyph_affinity = 1.0 if agent_art.dna.glyph_symbol == strain_art.dna.glyph_symbol else 0.2
        
        # 3. Résonance émotionnelle (cosine similarity)
        vec1 = agent_art.dna.emotion_vector
        vec2 = strain_art.dna.emotion_vector
        dot_prod = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in set(vec1) | set(vec2))
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
        emotion_affinity = dot_prod / (mag1 * mag2) if mag1 * mag2 > 0 else 0
        
        # 4. Affinité esthétique (fitness)
        fitness_affinity = (agent_art.aesthetic_score + strain_art.aesthetic_score) / 2
        
        # Pondération
        return (color_affinity * 0.3 + glyph_affinity * 0.3 + emotion_affinity * 0.2 + fitness_affinity * 0.2)

    def apply_resonance(self, agent: CulturalAgent) -> Optional[str]:
        if agent.cultural_status != CulturalStatus.RECEPTIVE: return None
        attractions = {}
        for strain_id in self.gravity_centers:
            affinity = self._compute_symbolic_affinity(agent, strain_id)
            mass = self.gravity_centers[strain_id]['mass']
            attraction = affinity * mass
            if attraction > 0.5:
                attractions[strain_id] = attraction
        
        if not attractions: return None
        total = sum(attractions.values())
        if total == 0: return None
        strain_ids = list(attractions.keys())
        weights = [attractions[s] / total for s in strain_ids]
        return random.choices(strain_ids, weights=weights, k=1)[0]

# ═══════════════════════════════════════════════════════════════════════════════
# SIMULATION PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════════
class CulturalEpidemicSimulation:
    def __init__(self, params: dict, genome_pool: Optional[List[CulturalGenome]] = None):
        self.params = params
        self.rng = random.Random(params.get("seed", 42))
        self.current_t = 0
        self.zones = ["Agora_Centrale", "Marché_Souterrain", "Forum_Diffus", "Sanctuaire_Reclus", "Carrefour_Nomade", "Archives_Oubliées"][:params.get("nb_zones", 6)]
        
        # Initialisation de la Forge Symbolique
        self.symbolic_engine = SymbolicEvolutionEngine(
            population_size=params.get("symbolic_pop", 6), 
            theme=params.get("root_theme", "rituel")
        )
        
        # Génération de la souche racine via évolution
        FengShuiDisplay.info(f"Forge de la souche racine (thème: {params.get('root_theme', 'rituel')})...", "🔨")
        self.symbolic_engine.initialize_population()
        root_dna = self.symbolic_engine._spawn_dna(params.get("root_theme", "rituel"), 0)
        root_artefact = self.symbolic_engine.evolve_new_artefact(root_dna, generations=params.get("symbolic_generations", 3))
        
        root_mantra = Mantra(id="M-001", content=root_artefact.mantra_text, theme=root_artefact.theme, fitness=root_artefact.aesthetic_score)
        self.root_strain = MemeStrain(
            strain_id="M-001", parent_id=None, generation=0, mutations=[],
            mantra=root_mantra, artefact=root_artefact,
            contagion_power=params.get("r0_base", 2.2) / 2.5,
            dogma_intensity=params.get("dogma_rate", 0.01) * 100,
            latency_period=params.get("latency_period", 3),
            emergence_time=0,
        )
        self.meme_strains: Dict[str, MemeStrain] = {"M-001": self.root_strain}
        self.strain_counter = 1
        self.meme_strains: Dict[str, MemeStrain] = {"M-001": self.root_strain}
        self.strain_counter = 1
        # ▼▼▼ AJOUTEZ CES 3 LIGNES ▼▼▼
        self.event_counter = 0
        self.relic_counter = 0
        self.myth_counter = 0
        # ▲▲▲ FIN DE L'AJOUT ▲▲▲
        # xTras
        self.relics: List = []
        self.founding_myths: List = []
        self.faction_system = None  # ou une version simplifiée si nécessaire        
        
        self.agents: List[CulturalAgent] = []
        self.events: List[NarrativeEvent] = []
        
        self.agents: List[CulturalAgent] = []
        self.events: List[NarrativeEvent] = []
        self.interactions: List[InteractionRecord] = []
        self.random_events: List[RandomEvent] = []
        self.chronicle: List[Dict] = []
        self.transmission_network = nx.DiGraph() if HAS_NX else None
        self.daily_metrics = defaultdict(lambda: defaultdict(int))
        self.rt_history: List[float] = []
        self.serial_intervals: List[int] = []
        
        self.aesthetic_resonance = AestheticResonance(self)
        self.aesthetic_resonance._initialize_centers()
        
        self._init_population(genome_pool)
        FengShuiDisplay.success(f"Simulation initialisée : {len(self.agents)} agents, souche racine: {root_artefact.dna.glyph_symbol}", "🌌")

    def _init_population(self, genome_pool: Optional[List[CulturalGenome]] = None):
        CulturalAgent._id_counter = 0
        pop_total = self.params.get("pop_total", 150)
        genomes = genome_pool or [CulturalGenome() for _ in range(pop_total)]
        genomes = (genomes * (pop_total // len(genomes) + 1))[:pop_total]
        
        for i, genome in enumerate(genomes):
            zone = self.rng.choice(self.zones)
            agent = CulturalAgent(zone, genome, self.rng, self.root_strain)
            if i < self.params.get("initial_believers", 3):
                self._expose_agent(agent, None, self.root_strain, force=True)
            self.agents.append(agent)
            
        # Réseau social
        n = len(self.agents)
        for i, agent in enumerate(self.agents):
            for j in range(1, 4):
                neighbor_idx = (i + j) % n
                if self.rng.random() > 0.3:
                    agent.social_network.add(self.agents[neighbor_idx].id)
                else:
                    agent.social_network.add(self.rng.choice(self.agents).id)

    def _expose_agent(self, agent: CulturalAgent, source: Optional[CulturalAgent], strain: MemeStrain, force: bool = False) -> bool:
        if agent.cultural_status != CulturalStatus.RECEPTIVE and not force: return False
        agent.cultural_status = CulturalStatus.EXPOSED
        agent.exposure_time = self.current_t
        agent.receive_mantra(strain)
        agent.evangelist_start = self.current_t + max(1, int(self.rng.gauss(strain.latency_period, 1)))
        agent.is_silent_carrier = self.rng.random() < agent.genome.silent_believer_prob
        
        self.events.append(NarrativeEvent(self.current_t, agent.id, "exposure", "E", 
                                          source.id if source else None, agent.guild, agent.narrative_coherence, strain.strain_id))
        if source and self.transmission_network:
            self.transmission_network.add_edge(source.id, agent.id, time=self.current_t, strain=strain.strain_id)
            source.influence_score += 1.0
        return True

    def _progress_narrative(self, agent: CulturalAgent):
        if agent.cultural_status == CulturalStatus.EXPOSED:
            if self.current_t >= agent.evangelist_start:
                agent.cultural_status = CulturalStatus.SILENT_CARRIER if agent.is_silent_carrier else CulturalStatus.EVANGELIST
        elif agent.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER):
            disenchant_prob = self.params.get("disenchant_rate", 0.05) * agent.phenotype.phenotypes["disenchant_boost"]
            if self.rng.random() < disenchant_prob:
                agent.cultural_status = CulturalStatus.DISENCHANTED
                self.events.append(NarrativeEvent(self.current_t, agent.id, "disenchantment", "R", guild=agent.guild, strain_id=agent.current_strain.strain_id))

    def transmit_meme(self, agent_a: CulturalAgent, agent_b: CulturalAgent) -> bool:
        if agent_a.cultural_status not in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER): return False
        if agent_b.cultural_status != CulturalStatus.RECEPTIVE: return False
        
        virulence = agent_a.meme_virulence * agent_a.phenotype.phenotypes["contagiousness"]
        if agent_a.cultural_status == CulturalStatus.SILENT_CARRIER: virulence *= 0.4
        p_transmission = min(0.95, 0.12 * virulence * agent_b.receptivity)
        occurred = self.rng.random() < p_transmission
        
        self.interactions.append(InteractionRecord(self.current_t, agent_a.id, agent_b.id, virulence, p_transmission, occurred))
        if occurred:
            self._expose_agent(agent_b, agent_a, agent_a.current_strain)
        return occurred

    def _run_interaction_round(self):
        carriers = [a for a in self.agents if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        for carrier in carriers:
            n_targets = max(1, int(carrier.phenotype.phenotypes["interaction_rate"] * 3))
            targets = self.rng.sample(list(carrier.social_network), k=min(n_targets, len(carrier.social_network))) if carrier.social_network else []
            for target_id in targets:
                target = next((a for a in self.agents if a.id == target_id), None)
                if target: self.transmit_meme(carrier, target)

    def mutate_meme(self):
        if self.rng.random() >= self.params.get("mutation_prob", 0.02): return
        carriers = [a for a in self.agents if a.cultural_status in (CulturalStatus.EVANGELIST, CulturalStatus.SILENT_CARRIER)]
        if not carriers: return
        
        agent = self.rng.choice(carriers)
        parent_strain = agent.current_strain
        parent_dna = parent_strain.artefact.dna
        
        # Évolution d'un nouvel artefact à partir du parent
        new_artefact = self.symbolic_engine.evolve_new_artefact(parent_dna, generations=self.params.get("symbolic_generations", 2))
        
        self.strain_counter += 1
        new_mantra = Mantra(id=f"MUT{self.strain_counter}", content=new_artefact.mantra_text, theme=new_artefact.theme, fitness=new_artefact.aesthetic_score)
        new_strain = MemeStrain(
            strain_id=f"MV-{self.strain_counter:03d}", parent_id=parent_strain.strain_id,
            generation=parent_strain.generation + 1, mutations=parent_strain.mutations + [("symbolic_evo", self.current_t)],
            mantra=new_mantra, artefact=new_artefact,
            contagion_power=parent_strain.contagion_power * (0.9 + new_artefact.aesthetic_score * 0.2),
            dogma_intensity=parent_strain.dogma_intensity * self.rng.lognormvariate(0, 0.08),
            latency_period=max(1.0, parent_strain.latency_period * self.rng.lognormvariate(0, 0.1)),
            emergence_time=self.current_t,
        )
        self.meme_strains[new_strain.strain_id] = new_strain
        agent.receive_mantra(new_strain)
        
        self.event_counter += 1
        evt = RandomEvent(f"EVT-{self.event_counter:03d}", "mutation", self.current_t, agent.zone,
                          f"🧬 MUTATION ESTHÉTIQUE : {parent_strain.strain_id} → {new_strain.strain_id} ({new_artefact.dna.glyph_symbol}, {new_artefact.dna.color})",
                          [agent.id], {"parent": parent_strain.strain_id, "child": new_strain.strain_id})
        self.random_events.append(evt)
        self.chronicle.append({"t": self.current_t, "type": "mutation", "strain": new_strain.strain_id})
        
        # Mise à jour des centres de gravité
        self.aesthetic_resonance._initialize_centers()

    def _apply_aesthetic_resonance(self):
        for agent in self.agents:
            if agent.cultural_status == CulturalStatus.RECEPTIVE:
                attracted_to = self.aesthetic_resonance.apply_resonance(agent)
                if attracted_to and attracted_to in self.meme_strains:
                    strain = self.meme_strains[attracted_to]
                    if self._expose_agent(agent, None, strain, force=True):
                        pass # Agent attiré par résonance esthétique

    def step(self) -> dict:
        self._run_interaction_round()
        self.mutate_meme()
        self._apply_aesthetic_resonance()
        
        for agent in self.agents:
            self._progress_narrative(agent)
            agent.current_t = self.current_t
            
        for status in CulturalStatus:
            self.daily_metrics[self.current_t][f"cult_{status.value}"] = sum(1 for a in self.agents if a.cultural_status == status)
        self.daily_metrics[self.current_t]["nb_strains"] = len(self.meme_strains)
        
        recent = [e for e in self.events if e.event_type == "exposure" and e.timestamp > self.current_t - 5]
        infectors = [e.source_id for e in recent if e.source_id]
        rt = sum(Counter(infectors).values()) / len(infectors) if infectors else 0.0
        self.rt_history.append(rt)
        
        self.current_t += 1
        return {"t": self.current_t, "rt": rt, "metrics": dict(self.daily_metrics[self.current_t - 1])}

    def run(self, steps: int):
        for _ in range(steps):
            yield self.step()

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS (CSV, Neo4J, JSON, Prompt)
# ═══════════════════════════════════════════════════════════════════════════════
class CSVExporter:
    @staticmethod
    def export_all(sim: CulturalEpidemicSimulation, output_dir: str):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        # Agents
        rows = []
        for a in sim.agents:
            rows.append({
                "agent_id": a.id, "zone": a.zone, "guild": a.guild, "status": a.cultural_status.name,
                "strain_id": a.current_strain.strain_id, "influence_score": a.influence_score,
                "glyph_symbol": a.symbolic_artefact.dna.glyph_symbol, "color": a.symbolic_artefact.dna.color,
                "complexity": a.symbolic_artefact.dna.complexity, "dominant_emotion": a.symbolic_artefact.dna.dominant_emotion(),
                "aesthetic_score": a.symbolic_artefact.aesthetic_score, "mantra": a.symbolic_artefact.mantra_text
            })
        if rows:
            with open(out / "agents_state.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
                
        # Souches
        rows = []
        for sid, s in sim.meme_strains.items():
            rows.append({
                "strain_id": s.strain_id, "parent_id": s.parent_id, "generation": s.generation,
                "glyph_symbol": s.artefact.dna.glyph_symbol, "color": s.artefact.dna.color,
                "contagion_power": s.contagion_power, "aesthetic_score": s.artefact.aesthetic_score,
                "mantra": s.mantra.content, "theme": s.mantra.theme
            })
        if rows:
            with open(out / "strains_state.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        FengShuiDisplay.success(f"CSV exportés dans {out}/", "📊")

class Neo4JExporter:
    @staticmethod
    def export_all(sim: CulturalEpidemicSimulation, output_dir: str):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        lines = []
        
        # Artefacts
        lines.append("// === ARTEFACTS SYMBOLIQUES ===")
        for sid, strain in sim.meme_strains.items():
            art = strain.artefact
            dna = art.dna
            lines.append(f"CREATE (a:Artefact {{strain_id: '{sid}', glyph: '{dna.glyph_symbol}', color: '{dna.color}', "
                         f"complexity: {dna.complexity:.2f}, emotion: '{dna.dominant_emotion()}', "
                         f"aesthetic_score: {art.aesthetic_score:.2f}, mantra: '{art.mantra_text.replace(chr(39), chr(32))}'}});")
        
        # Agents
        lines.append("\n// === AGENTS ===")
        for agent in sim.agents:
            lines.append(f"CREATE (ag:Agent {{id: {agent.id}, guild: '{agent.guild}', status: '{agent.cultural_status.name}'}});")
            lines.append(f"MATCH (ag:Agent {{id: {agent.id}}}), (a:Artefact {{strain_id: '{agent.current_strain.strain_id}'}}) CREATE (ag)-[:CARRIES]->(a);")
            
        with open(out / "neo4j_import.cypher", 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        FengShuiDisplay.success(f"Neo4J exporté dans {out}/", "🦈")

def generate_diffusion_prompt(sim: CulturalEpidemicSimulation, target: str = "grok") -> str:
    """Génère un prompt pour IA de diffusion basé sur l'état final de la simulation."""
    dominant_strains = sorted(sim.meme_strains.values(), key=lambda s: sum(1 for a in sim.agents if a.current_strain.strain_id == s.strain_id), reverse=True)[:3]
    
    visual_elements = []
    for strain in dominant_strains:
        art = strain.artefact
        visual_elements.append(f"a luminous {art.dna.glyph_symbol} symbol in {art.dna.color}")
        
    mood_map = {"peur": "dark, eerie", "joie": "bright, euphoric", "mystere": "mysterious, enigmatic", 
                "colere": "intense, fiery", "extase": "transcendent, glowing", "silence": "serene, meditative"}
    dominant_emotion = dominant_strains[0].artefact.dna.dominant_emotion() if dominant_strains else "mystere"
    mood = mood_map.get(dominant_emotion, "mystical")
    
    style_map = {
        "grok": "photorealistic, cinematic, 8k, detailed, mystical, symbolic, dramatic lighting",
        "gemini": "artistic, surreal, glowing, esoteric, highly detailed, painting, ethereal",
        "dalle": "digital art, fantasy, intricate, neon, cyberpunk, mystical, vibrant",
        "midjourney": "fantasy art, intricate, mystical, glowing, ethereal, detailed, majestic, --ar 16:9",
    }
    style = style_map.get(target.lower(), style_map["grok"])
    
    prompt = f"""Create a mystical, symbolic artwork representing a cultural epidemic.
VISUAL ELEMENTS:
- {', '.join(visual_elements)}.
- Background: dark, cosmic, with faint geometric patterns and neural networks.
- The symbols should feel like they are spreading and mutating.
HARMONIOUS FUSION:
- The overall mood is {mood}.
- The image should feel like an illuminated manuscript from a cyberpunk monastery.
- Style: {mood}, {style}.
- Resolution: 1024x1024, high detail.
"""
    return prompt.strip()

# ═══════════════════════════════════════════════════════════════════════════════
# CLI & MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(prog="archeosymbolic_chronicle", description="🧬🎨 ARCHEOSYMBOLIC CHRONICLE v1.0")
    parser.add_argument("--seed", type=int, default=2075, help="Graine aléatoire")
    parser.add_argument("--steps", type=int, default=40, help="Nombre de pas de temps")
    parser.add_argument("--pop-total", type=int, default=120, help="Nombre total d'agents")
    parser.add_argument("--nb-zones", type=int, default=6, help="Nombre de zones")
    parser.add_argument("--initial-believers", type=int, default=3, help="Croyants initiaux")
    parser.add_argument("--root-theme", type=str, default="rituel", choices=list(THEME_TEMPLATES.keys()), help="Thème du mantra racine")
    parser.add_argument("--r0-base", type=float, default=2.4, help="R0 de base")
    parser.add_argument("--mutation-prob", type=float, default=0.03, help="Probabilité de mutation par step")
    parser.add_argument("--disenchant-rate", type=float, default=0.04, help="Taux de désenchantement")
    
    # Paramètres de la Forge Symbolique
    parser.add_argument("--symbolic-pop", type=int, default=6, help="Population de la forge symbolique")
    parser.add_argument("--symbolic-generations", type=int, default=3, help="Générations d'évolution par mutation")
    
    # Exports
    parser.add_argument("--export-csv", type=str, default=None, help="Répertoire d'export CSV")
    parser.add_argument("--export-neo4j", type=str, default=None, help="Répertoire d'export Neo4J")
    parser.add_argument("--diffusion-prompt", action="store_true", help="Génère un prompt pour IA de diffusion à la fin")
    parser.add_argument("--diffusion-target", type=str, default="grok", choices=["grok", "gemini", "dalle", "midjourney"], help="Cible du prompt")
    parser.add_argument("--no-retro", action="store_true", help="Désactiver l'affichage rétro-wave")
    
    args = parser.parse_args()
    
    FengShuiDisplay.header("ARCHEOSYMBOLIC CHRONICLE v1.0", "Épidémiologie Esthétique & ADN Symbolique")
    
    params = {
        "seed": args.seed, "pop_total": args.pop_total, "nb_zones": args.nb_zones,
        "initial_believers": args.initial_believers, "root_theme": args.root_theme,
        "r0_base": args.r0_base, "mutation_prob": args.mutation_prob,
        "disenchant_rate": args.disenchant_rate, "symbolic_pop": args.symbolic_pop,
        "symbolic_generations": args.symbolic_generations, "latency_period": 3.0, "dogma_rate": 0.01
    }
    
    sim = CulturalEpidemicSimulation(params)
    display = RetroWaveDisplay()
    
    if not args.no_retro:
        print(display.banner())
        time.sleep(0.5)
    
    for i, snapshot in enumerate(sim.run(args.steps)):
        if not args.no_retro:
            print(f"\033[{display.banner().count(chr(10))+2}A", end="")
            print(display.status_bar(sim))
            time.sleep(0.05)
            
    FengShuiDisplay.separator("═", 70)
    FengShuiDisplay.section("Simulation achevée", "✨")
    
    # Exports
    if args.export_csv:
        CSVExporter.export_all(sim, args.export_csv)
    if args.export_neo4j:
        Neo4JExporter.export_all(sim, args.export_neo4j)
        
    # Génération du prompt de diffusion
    if args.diffusion_prompt:
        FengShuiDisplay.section("Génération du prompt pour diffusion", "🧠")
        prompt = generate_diffusion_prompt(sim, target=args.diffusion_target)
        prompt_path = Path(args.export_csv or "./output") / "diffusion_prompt.txt"
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        FengShuiDisplay.success(f"Prompt enregistré: {prompt_path}", "📜")
        FengShuiDisplay.mantra(prompt)
        
    FengShuiDisplay.poem([
        "Le code s'efface dans le silence,",
        "Le symbole danse dans la lumière,",
        "L'épidémie résonne dans l'éther,",
        "La chronique se repose en paix."
    ], title="🌸 Épilogue")

if __name__ == "__main__":
    main()
