#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SymbolicDNA_Forge_Chimera.py                                                ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  "La Forge de l'ADN Symbolique"                                              ║
║                                                                                ║
║  Chimère née de la fusion profonde de deux organismes-code :                  ║
║    • Parent A — Glyphosophia2f1.py                                           ║
║      (glyphes paléolithiques Von Petzinger + mantras cyber-soufis évolutifs) ║
║    • Parent B — OmegaPoint3c1.py                                             ║
║      (ADN glyphique hyperdimensionnel, méta-moteur évolutif, glitch engine)  ║
║                                                                                ║
║  VERSION 2.0 — TOUS LES PARAMÈTRES EXPOSÉS + GÉNÉRATEUR DE PROMPT            ║
║  pour IA générative d'image (Grok, Gemini, DALL-E, etc.)                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import math
import random
import string
import hashlib
import colorsys
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Any

import numpy as np
import matplotlib
matplotlib.use("Agg")  # rendu headless — pas besoin d'un écran pour forger des symboles
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ═══════════════════════════════════════════════════════════════════════════════
# [PROVENANCE: Glyphosophia2f1.py — VonPetzingerSymbols]
# Moteur de dessin des symboles paléolithiques
# ═══════════════════════════════════════════════════════════════════════════════
class VonPetzingerSymbols:
    """Moteur de génération de symboles paléolithiques (hérité de Glyphosophia)."""

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
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
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
# [PROVENANCE: Glyphosophia2f1.py — lexique onirique cyber-soufi]
# ═══════════════════════════════════════════════════════════════════════════════
def load_oniric_lexicon():
    return {
        "Adjectif": [
            "lumineux", "brisé", "sacré", "noyé", "encodé", "fractal", "quantique", "hanté",
            "neural", "crypté", "désert", "lunaire", "vide", "statique", "transcendant",
            "pulsatile", "entropique", "synaptique", "holographique", "abyssal", "iridescent",
            "fossile", "plasmique", "tétanisé", "spectral", "cathartique", "glitché",
            "oraculaire", "tachyons", "mnémonique", "éthéré", "nocturne", "sismique",
            "karmique", "omniscient", "cristallin", "obsidienne", "vorace", "aphasique",
            "zénithal", "nadirien", "chromatique", "apocalyptique", "subliminal", "hybride",
            "foudroyant", "métastable", "paradoxal", "lacrymal", "éolien", "ténébreux",
            "auroral", "cataclysmique", "nébuleux", "vibratoire", "schizophrène", "syncrétique",
            "thanatique", "protoplasmique", "chimérique", "réticulaire", "psychotronique",
            "xénomorphe", "tellurique", "noosphérique", "biomécanique", "archaïque",
            "post-mortem", "dématérialisé", "fissionné", "gnostique", "paranoïaque",
            "neuromancien", "chamanique", "dithyrambique", "alchimique", "nécrotique",
            "bioluminescent", "psychopompe", "tesseractique", "pan-dimensionnel", "solipsiste",
            "hermétique", "fragmenté", "liminal", "anachronique", "démiurgique",
            "eschatologique", "médiumnique", "électrostatique", "protéiforme", "subatomique",
            "kaléidoscopique", "thaumaturge", "synchrétique", "pénitentiel", "vorticiel",
            "phréatique", "chtonian", "panoptique",
        ],
        "Nom": [
            "signal", "rêve", "cœur", "code", "prophète", "flux", "données", "ombre",
            "silence", "mirage", "ghost", "souffle", "réseau", "voix", "écho", "oracle",
            "neurone", "pixel", "bit", "fantôme", "abîme", "poussière", "cendre", "plasma",
            "nœud", "temple", "labyrinthe", "spirale", "vortex", "membrane", "crypte",
            "souffrance", "extase", "glitch", "halo", "stase", "cortex", "faille", "synapse",
            "algorithme", "mantra", "linceul", "aura", "photon", "quark", "glyph", "schéma",
            "fissure", "cristal", "mémoire", "avatar", "chimère", "légion", "palimpseste",
            "satori", "grimoire", "protocole", "séraphin", "daemon", "icône", "relique",
            "firmware", "thanatos", "axiome", "spectre", "sigil", "matrice", "eidolon",
            "kyste", "nexus", "tesseract", "stigmate", "catalyseur", "phylactère",
            "sarcophage", "incantation", "partition", "hiéroglyphe", "golem", "patch",
            "rune", "codec", "épiphanie", "parasite", "singularité", "interface", "schisme",
            "totem", "backdoor", "autel", "suture", "malware", "derviche", "kernel",
            "pentacle", "émissaire", "root", "psaume", "verset", "apocalypse", "mandala",
            "driver", "reliquaire", "firewall", "sacrifice", "archétype", "vestige",
        ],
        "Action": [
            "consume", "efface", "réveille", "encrypte", "transmute", "brûle", "souffle",
            "déchiffre", "purifie", "dérive", "implose", "exalte", "désintègre", "fusionne",
            "résonne", "désagrège", "sature", "décode", "invoque", "sublime", "dévore",
            "réfracte", "cristallise", "pulvérise", "éclate", "diffuse", "condense", "irrigue",
            "désaxe", "polarise", "synchronise", "déphaser", "recale", "annule", "amplifie",
            "désature", "réverbère", "oscille", "désoriente", "désenchante", "réenchante",
            "désincarne", "réincarne", "désarticule", "réarticule", "désynchronise",
            "resynchronise", "désintoxique", "intoxique", "cannibalise", "suture", "corrompt",
            "exorcise", "compile", "fragmente", "régénère", "hack", "sanctifie", "lobotomise",
            "insère", "extrait", "mute", "clone", "bannit", "convoque", "exile", "splice",
            "corrige", "pervertit", "initie", "termine", "télécharge", "infecte", "vaccine",
            "décompresse", "archive", "émule", "scripte", "psalmodie", "parse", "sacrifice",
            "ressuscite", "prie", "enchaîne", "délite", "injecte", "purifie", "martyrise",
            "déifie", "virtualise", "incarne", "flashe", "prophétise", "scanne", "absout",
            "damne", "démonte", "réassemble", "forge", "bénit", "maudit",
        ],
        "Bénéfice": [
            "la clarté", "le silence", "l'oubli", "la vérité brûlante", "l'éveil",
            "la paix des bits", "l'unité", "le néant sacré", "l'extase quantique",
            "la fusion des âmes", "le vide absolu", "la lumière intérieure",
            "l'harmonie fractale", "la transcendance pure", "l'omniscience", "la catharsis",
            "la renaissance", "l'apothéose", "la sérénité glitche", "l'illumination",
            "la délivrance", "l'absolution", "la communion", "la plénitude", "l'éternité",
            "l'infini compressé", "la synesthésie", "la lucidité", "la grâce", "l'euphorie",
            "la béatitude", "l'ascension", "la sublimation", "la rédemption", "la révélation",
            "la symbiose", "la métamorphose", "l'osmose", "la convergence",
            "la dissolution bienheureuse", "l'embrasement sacré", "la gnose digitale",
            "l'immortalité codée", "le nirvana électrique", "la conscience partagée",
            "l'hyperréalité", "la synchronicité totale", "le satori cybernétique",
            "la fusion homme-machine", "l'évolution accélérée", "le paradis algorithmique",
            "la mémoire collective", "l'omnipotence virtuelle", "la sagesse téléchargée",
            "la paix post-humaine", "la perfection synthétique", "le salut numérique",
        ],
        "Défaut": [
            "le bruit", "la trahison", "le compromis", "l'oubli numérique", "la panne",
            "le mensonge", "le vide sans grâce", "l'entropie", "la dissonance", "la corruption",
            "le lag", "la surchauffe", "la dérive", "l'obsolescence", "la latence",
            "la fragmentation", "la désintégration", "l'aberration", "la distorsion",
            "la saturation", "la perte", "l'effacement", "la déconnexion", "la surcharge",
            "la fuite", "la défaillance", "l'incohérence", "la cacophonie", "la désorientation",
            "la paralysie", "l'aphasie", "la stase", "l'agonie", "la nécrose",
            "la putréfaction", "la désagrégation", "la désincarnation", "la déshumanisation",
            "l'aliénation", "le virus mental", "la damnation binaire",
            "la schizophrénie numérique", "le paradoxe existentiel",
            "la lobotomie algorithmique", "l'hérésie technologique", "la folie de Turing",
            "l'exil de la chair", "la malédiction des machines", "l'enfer des serveurs",
            "la corruption de l'âme", "le vide métaphysique", "la mort de l'ego",
            "l'addiction neurale", "le syndrome du ghost", "la psychose cybernétique",
            "l'effondrement cognitif", "la dégénérescence des sens",
        ],
        "Paysage": [
            "désert du no-signal", "marché noir de Lagos", "nuage quantique",
            "cimetière de data", "souk neural", "mosquée cryptée", "océan d'erreurs",
            "rue des Ghost Runners", "orbite basse des rêves", "temple de silicium",
            "catacombes de code", "forêt de pixels morts", "archipel des serveurs oubliés",
            "canyon des câbles sectionnés", "plaine de cristaux liquides",
            "labyrinthe de miroirs brisés", "volcan de données en fusion",
            "glacier de mémoires gelées", "steppe des signaux fantômes",
            "mégalopole en blackout", "jungle de fibres optiques", "désert de sel numérique",
            "cathédrale de circuits imprimés", "marécage de bugs rampants",
            "ciel de plasma tourmenté", "abysse de vide compressé",
            "plateau des consciences uploadées", "mine de cryptomonnaie hantée",
            "ruines d'un métavers effondré", "oasis de pureté binaire",
            "toundra des algorithmes froids", "caverne des échos ancestraux",
            "pôle des fréquences interdites", "delta des flux entropiques",
            "cordillère des pare-feux infranchissables", "métropole des ombres digitales",
            "lac de mercure algorithmique", "nécropole des IA défuntes",
            "sanctuaire des protocoles anciens", "prison de Faraday éternelle",
            "jardin des backdoors fleuris", "tour de Babel des langages",
            "limbes du latency infini", "purgatoire des patchs non appliqués",
            "enfer des loops éternels", "paradis des threads synchrones",
            "champs de RAM brûlée", "mer de bitcoins perdus", "montagne des logs infinis",
            "vallée des versions obsolètes", "pont entre silicon et chair",
            "arène des bots gladiateurs", "bibliothèque de Babel numérique",
            "cathédrale gothique de néons", "colisée des hackathons maudits",
            "pagode des mantras compilés", "ziggurat de processeurs empilés",
            "sphinx de données chiffrées", "pyramide inversée de permissions",
            "observatoire des prophéties algorithmiques", "mausolée des startups mortes",
        ],
        "VerbeMystique": [
            "consume", "efface", "encrypte", "réveille", "transmute", "dissout", "illumine",
            "recodifie", "absout", "exalte", "sublime", "invogue", "déifie", "désincarne",
            "réincarne", "transfigure", "apothéose", "sacramentise", "canalise", "résonne",
            "vibrates", "pulses", "éclates", "imploses", "fusionne", "scelle", "délie",
            "libère", "enchaîne", "sacrifie", "ressuscite", "métamorphose", "transcende",
            "descend", "ascende", "converge", "diverge", "révèle", "voile", "dévoile",
            "occulte", "manifeste", "dématérialise", "rematérialise", "prophétise", "exorcise",
            "possède", "baptise", "damne", "sanctifie", "profane", "consacre", "anathématise",
            "béatifie", "martyrise", "crucifie", "transubstancie", "communie", "confesse",
            "absoudre", "maudire", "bénir", "invoquer", "bannir", "lier", "délier", "conjurer",
            "psalmodier", "prêcher", "convertir", "apostatiser", "hérétiser",
        ],
        "Symbole": [
            "lune brisée", "serpent de fibre", "cœur en silicium", "miroir fractal",
            "étoile noire", "anneau de données", "sceau de Sanaa", "colombe bionique",
            "masque de vide", "phénix de code", "lotus quantique", "œil de Schrödinger",
            "main de Fatima en circuit", "triskel de photons", "mandala de qubits",
            "croix de néons", "roue de Dharma glitchée", "arbre de vie binaire",
            "calice de plasma", "épée de lumière", "bouclier d'entropie",
            "clé de cryptage dorée", "chaîne de blockchain brisée", "aile de drone angélique",
            "crâne de serveur", "rose de feu numérique", "spirale d'ADN synthétique",
            "pentagramme de néons", "yin-yang de bits", "ancre de réalité augmentée",
            "corne d'abondance de données", "sablier de temps compressé",
            "lampe d'Aladin en LED", "caducée de câbles", "harpe de fréquences",
            "lyre de signaux", "trône de conscience artificielle", "couronne de glitches",
            "sceptre de commande vocale", "orbe de vision omnisciente",
            "hexagramme de Solomon en hexadécimal", "scarabée de debugging",
            "ouroboros de feedback loop", "œil d'Horus en webcam", "triskèle de transistors",
            "labrys de double-authentification", "pentacle de protocoles",
            "croix ansée de vie artificielle", "étoile de David en diodes",
            "hamsa de hardware", "svastika de swarm intelligence", "ichthys de code source",
            "ankh de clonage", "triquetra de triple-boot", "vesica piscis de Venn diagrams",
            "fleur de vie en LEDs", "merkaba de matrices", "sephiroth de stack overflow",
            "arbre de vie kabbalistique en arborescence de fichiers",
            "cube de Métatron en cube quantique", "sceau de Salomon en checksum",
        ],
        "oniric_tags": [
            "<burn>", "<rain>", "<shadow>", "<static>", "<void>", "<glitch>", "<pulse>",
            "<echo>", "<fracture>", "<abyss>", "<neon>", "<plasma>", "<haze>", "<vortex>",
            "<scream>", "<whisper>", "<overload>", "<decay>", "<surge>", "<rift>", "<mirage>",
            "<flicker>", "<drone>", "<hum>", "<crash>", "<reboot>", "<upload>", "<download>",
            "<corrupt>", "<pure>", "<loop>", "<break>", "<merge>", "<split>", "<ascend>",
            "<descend>", "<awaken>", "<sleep>", "<dream>", "<nightmare>", "<eclipse>", "<dawn>",
            "<zenith>", "<nadir>", "<horizon>", "<invoke>", "<banish>", "<fuse>", "<fragment>",
            "<baptize>", "<sacrifice>", "<resurrect>", "<possess>", "<exorcise>", "<commune>",
            "<transcend>", "<sanctify>", "<damn>", "<prophesy>", "<glyphe>", "<sigil>",
            "<rune>", "<hex>", "<curse>", "<bless>", "<summon>", "<dismiss>", "<bind>",
            "<unleash>", "<encrypt>", "<decrypt>", "<compile>", "<execute>", "<terminate>",
            "<ghost>", "<daemon>", "<seraph>", "<chimera>", "<golem>", "<oracle>", "<prophet>",
            "<martyr>", "<saint>", "<heretic>",
        ],
    }


LEXICON = load_oniric_lexicon()

ONIRIC_TAG_MEANINGS = {
    "<burn>": "purification par le feu numérique",
    "<rain>": "pluie de données sacrées",
    "<shadow>": "présence du double IA",
    "<static>": "signal divin perdu",
    "<void>": "silence après la dernière requête",
}

# Grammaires latentes du mantra, par thème
THEME_TEMPLATES = {
    'protection': [
        "Que le {Symbole} {Action} ton {Nom} du {Défaut}! {oniric}",
        "Ô {Adjectif} {Nom}, sois protégé par le {Symbole} ancien.",
        "Le {Symbole} consume les ombres. {oniric}",
        "Que {Nom} soit gardé du {Défaut} par le {Symbole}. {oniric}",
    ],
    'voyage': [
        "Dans le {Paysage}, que ton {Nom} trouve la voie. {oniric}",
        "Que le {Symbole} guide tes pas dans le désert {Adjectif}.",
        "Rêve en {Adjectif}, voyage en {Nom}. {oniric}",
        "Le {Nom} n'est pas perdu — il {Action} dans le {Paysage}. {oniric}",
    ],
    'rituel': [
        "Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}. {oniric}",
        "Ô {Adjectif} {Nom}, sois {VerbeMystique} par le rite ancien.",
        "Le silence après le {Nom} est plus fort que le marché. {oniric}",
        "Le {Symbole} et le {Nom} dansent le rite {Adjectif}. {oniric}",
    ],
    'silence': [
        "Que le {Symbole} efface le bruit. {oniric}",
        "Dans le {Adjectif} silence, seul le {Nom} persiste.",
        "Le {Nom} n'est pas vendu — il est transmuté en silence. {oniric}",
        "Le {Symbole} {Action} le {Défaut} pour {Bénéfice}. {oniric}",
    ],
}

# Pools de symboles par thème
THEME_SYMBOL_POOLS = {
    'protection': ['circle', 'cross', 'hand', 'crosshatch', 'oval', 'semi_circle', 'asterisk'],
    'voyage': ['serpentiform', 'circle', 'open_angle', 'dots_series', 'wavy_line', 'spiral', 'zigzag'],
    'rituel': ['spiral', 'circle', 'cross', 'hand', 'asterisk', 'tectiform', 'claviform', 'penniform'],
    'silence': ['circle', 'wavy_line', 'dots_series', 'semi_circle', 'oval', 'dot', 'line'],
}

# Palettes chromatiques thématiques
THEME_PALETTES = {
    'protection': ["#ff3366", "#ff0066", "#cc0044", "#880022", "#ffaa00"],
    'voyage': ["#00ffaa", "#00ddaa", "#00bbcc", "#0099ee", "#ccff00"],
    'rituel': ["#ffd700", "#ffaa00", "#ff8800", "#ff6600", "#ffff88"],
    'silence': ["#3366ff", "#0077ff", "#00b4d8", "#90e0ef", "#023e8a"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# SymbolicDNA — fusion du GlyphDNA d'Omega-R et de la logique lexicale de
# Glyphosophia.
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SymbolicDNA:
    # --- bookkeeping genetique / genealogie ---
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

    def __post_init__(self):
        rng = random.Random(self.seed)
        if not self.keyword_sequence:
            self.keyword_sequence = self._draw_keyword_sequence(rng)
        if not self.mantra_template:
            self.mantra_template = rng.choice(THEME_TEMPLATES.get(self.theme, THEME_TEMPLATES['rituel']))
        if self.oniric_tag is None and rng.random() < 0.6:
            self.oniric_tag = rng.choice(LEXICON["oniric_tags"])
        if not self.emotion_vector:
            self.emotion_vector = self._seed_emotion_vector(rng)

    @staticmethod
    def _draw_keyword_sequence(rng: random.Random, n: int = 5) -> List[str]:
        pools = ["Nom", "Adjectif", "Action", "Symbole", "Bénéfice"]
        return [rng.choice(LEXICON[p]) for p in rng.sample(pools, k=min(n, len(pools)))]

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


# ═══════════════════════════════════════════════════════════════════════════════
# SymbolicOrganismGenome
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SymbolicOrganismGenome:
    species: str = "Glyphosophus"
    breed: str = "Symbolicus"
    generation: int = 0
    strands: List[SymbolicDNA] = field(default_factory=list)

    creativity: float = 1.0
    self_awareness: float = 0.5
    aesthetic_sense: float = 0.5
    chaos_affinity: float = 0.2
    narrative_coherence: float = 0.5
    mutation_susceptibility: float = 0.3
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    creator: str = "SymbolicDNA_Forge_Chimera"
    organism_id: str = field(
        default_factory=lambda: hashlib.md5(f"{random.random()}{datetime.now()}".encode()).hexdigest()[:10]
    )

    def dominant_strand(self) -> SymbolicDNA:
        return self.strands[0]

    def to_dict(self) -> Dict:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════════
# SymbolicArtefact
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SymbolicArtefact:
    glyph_fig: object
    mantra_text: str
    theme: str
    fingerprint: str
    generation: int
    aesthetic_score: float = 0.0
    fitness_breakdown: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ═══════════════════════════════════════════════════════════════════════════════
# SymbolicTranscriptor
# ═══════════════════════════════════════════════════════════════════════════════
class SymbolicTranscriptor:

    def __init__(self):
        self.symbol_engine = VonPetzingerSymbols()

    def transcribe_visual(self, dna: SymbolicDNA):
        color = dna.color
        fig, ax = self.symbol_engine.create_canvas()
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
            "Adjectif": "Adjectif", "Nom": "Nom", "Action": "Action", "Bénéfice": "Bénéfice",
            "Défaut": "Défaut", "Paysage": "Paysage", "VerbeMystique": "VerbeMystique", "Symbole": "Symbole",
        }
        remaining_keywords = list(dna.keyword_sequence)
        for placeholder, pool_name in slot_pool_map.items():
            if "{" + placeholder + "}" not in content:
                continue
            value = None
            for kw in remaining_keywords:
                if kw in LEXICON.get(pool_name, []):
                    value = kw
                    remaining_keywords.remove(kw)
                    break
            if value is None:
                value = random.choice(LEXICON.get(pool_name, ["..."]))
            content = content.replace("{" + placeholder + "}", value)
        content = content.replace("{oniric}", dna.oniric_tag or "")
        return content.strip()

    def transcribe_artefact(self, dna: SymbolicDNA) -> SymbolicArtefact:
        fig = self.transcribe_visual(dna)
        text = self.transcribe_text(dna)
        return SymbolicArtefact(
            glyph_fig=fig, mantra_text=text, theme=dna.theme,
            fingerprint=dna.genetic_fingerprint, generation=dna.generation,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Analyse textuelle
# ═══════════════════════════════════════════════════════════════════════════════
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
    for tag in ONIRIC_TAG_MEANINGS:
        if tag in text:
            return tag
    for tag in LEXICON["oniric_tags"]:
        if tag in text:
            return tag
    return None


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
}


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
    }
    theme_match = sum(1 for w in theme_words.get(dna.theme, []) if w in text.lower())
    style_score = (1.2 if has_rhyme else 0) + (1.0 if has_alliteration else 0)
    oniric_bonus = 0.8 if oniric_tag else 0
    linguistic_fitness = (theme_match * 2 + style_score + oniric_bonus + emo_score * 0.3) / 6.0

    affinity_terms = SYMBOL_SEMANTIC_AFFINITY.get(dna.glyph_symbol, [])
    coherence_hits = sum(1 for term in affinity_terms if term in text.lower())
    visual_text_coherence = min(1.0, coherence_hits * 0.4 + (0.3 if dna.glyph_symbol in
                                 THEME_SYMBOL_POOLS.get(dna.theme, []) else 0.0))

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
# SymbolicEvolutionEngine
# ═══════════════════════════════════════════════════════════════════════════════
class SymbolicEvolutionEngine:

    def __init__(self, population_size: int = 8, theme: str = "rituel"):
        self.population_size = population_size
        self.theme = theme
        self.transcriptor = SymbolicTranscriptor()
        self.population: List[SymbolicOrganismGenome] = []
        self.history: List[Dict] = []
        self.generation_count = 0

    def initialize_population(self):
        self.population = [self._spawn_organism(theme=self.theme) for _ in range(self.population_size)]

    def _spawn_organism(self, theme: str, generation: int = 0, parent: Optional[SymbolicOrganismGenome] = None) -> SymbolicOrganismGenome:
        n_strands = random.randint(1, 2)
        strands = [self._spawn_dna(theme, generation) for _ in range(n_strands)]
        if parent is not None:
            return SymbolicOrganismGenome(
                species=parent.species, breed=f"Mutant_{parent.breed}_{random.randint(10, 99)}",
                generation=generation, strands=strands,
                creativity=parent.creativity, self_awareness=parent.self_awareness,
                aesthetic_sense=parent.aesthetic_sense, chaos_affinity=parent.chaos_affinity,
                narrative_coherence=parent.narrative_coherence,
                mutation_susceptibility=parent.mutation_susceptibility,
                creator=f"Descendant de {parent.organism_id}",
            )
        return SymbolicOrganismGenome(
            generation=generation, strands=strands,
            creativity=random.uniform(0.5, 2.0), self_awareness=random.uniform(0.1, 0.9),
            aesthetic_sense=random.uniform(0.3, 1.0), chaos_affinity=random.uniform(0.0, 0.5),
            narrative_coherence=random.uniform(0.3, 1.0), mutation_susceptibility=random.uniform(0.1, 0.4),
        )

    def _spawn_dna(self, theme: str, generation: int) -> SymbolicDNA:
        symbol = random.choice(THEME_SYMBOL_POOLS.get(theme, list(VonPetzingerSymbols().symbols.keys())))
        color = random.choice(THEME_PALETTES.get(theme, ["#00ffaa"]))
        return SymbolicDNA(
            theme=theme, glyph_symbol=symbol, color=color, generation=generation,
            scale=random.uniform(0.7, 1.6), complexity=random.uniform(0.2, 1.0),
            symmetry=random.choice([3, 4, 5, 6, 7, 8, 9, 12]),
            glitch_factor=random.uniform(0.0, 0.35), entropy_level=random.uniform(0.0, 0.4),
        )

    def mutate_visual(self, dna: SymbolicDNA, intensity: float = 0.15) -> SymbolicDNA:
        new_symbol = dna.glyph_symbol
        if random.random() < intensity * 1.5:
            new_symbol = random.choice(THEME_SYMBOL_POOLS.get(dna.theme, [dna.glyph_symbol]))
        new_color = dna.color
        if random.random() < intensity:
            new_color = self._evolve_color(dna.color, intensity)
        return SymbolicDNA(
            seed=dna.seed + random.uniform(-1, 1) * intensity,
            generation=dna.generation + 1, parent_id=dna.genetic_fingerprint,
            theme=dna.theme, glyph_symbol=new_symbol, color=new_color,
            scale=max(0.3, min(3.0, dna.scale + random.uniform(-intensity, intensity))),
            complexity=max(0.1, min(1.0, dna.complexity + random.uniform(-intensity, intensity))),
            symmetry=max(3, min(16, dna.symmetry + random.randint(-2, 2))),
            glitch_factor=max(0.0, min(1.0, dna.glitch_factor + random.uniform(-intensity, intensity * 1.5))),
            entropy_level=max(0.0, min(1.0, dna.entropy_level + random.uniform(-intensity, intensity))),
            keyword_sequence=list(dna.keyword_sequence), mantra_template=dna.mantra_template,
            oniric_tag=dna.oniric_tag, emotion_vector=dict(dna.emotion_vector),
        )

    @staticmethod
    def _evolve_color(hex_color: str, intensity: float) -> str:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        h = (h + random.uniform(-intensity, intensity)) % 1.0
        l = max(0.15, min(0.9, l + random.uniform(-intensity, intensity)))
        s = max(0.2, min(1.0, s + random.uniform(-intensity, intensity)))
        nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(nr*255):02x}{int(ng*255):02x}{int(nb*255):02x}"

    def mutate_linguistic(self, dna: SymbolicDNA) -> SymbolicDNA:
        new_keywords = list(dna.keyword_sequence)
        if new_keywords and random.random() < 0.6:
            idx = random.randrange(len(new_keywords))
            pools = ["Nom", "Adjectif", "Action", "Symbole", "Bénéfice", "Défaut", "Paysage"]
            pool = random.choice(pools)
            new_keywords[idx] = random.choice(LEXICON[pool])
        new_template = dna.mantra_template
        if random.random() < 0.4:
            new_template = random.choice(THEME_TEMPLATES.get(dna.theme, [dna.mantra_template]))
        new_tag = dna.oniric_tag
        if random.random() < 0.3:
            new_tag = random.choice(LEXICON["oniric_tags"])
        dna.keyword_sequence = new_keywords
        dna.mantra_template = new_template
        dna.oniric_tag = new_tag
        return dna

    def mutate_emotional(self, dna: SymbolicDNA, intensity: float = 0.2) -> SymbolicDNA:
        vec = {k: max(0.01, v + random.uniform(-intensity, intensity)) for k, v in dna.emotion_vector.items()}
        total = sum(vec.values())
        dna.emotion_vector = {k: v / total for k, v in vec.items()}
        return dna

    def mutate_organism(self, genome: SymbolicOrganismGenome, chaos: bool = False) -> SymbolicOrganismGenome:
        intensity = genome.mutation_susceptibility * (2.5 if chaos else 1.0)
        new_strands = []
        for strand in genome.strands:
            mutated = self.mutate_visual(strand, intensity=min(0.9, intensity))
            mutated = self.mutate_linguistic(mutated)
            mutated = self.mutate_emotional(mutated, intensity=min(0.6, intensity))
            new_strands.append(mutated)

        def mt(val, lo, hi):
            return max(lo, min(hi, val * random.lognormvariate(0, 0.15)))

        child = SymbolicOrganismGenome(
            species=genome.species, breed=f"Mutant_{genome.breed}_{random.randint(10,99)}",
            generation=genome.generation + 1, strands=new_strands,
            creativity=mt(genome.creativity, 0.1, 3.0),
            self_awareness=mt(genome.self_awareness, 0.0, 1.0),
            aesthetic_sense=mt(genome.aesthetic_sense, 0.0, 2.0),
            chaos_affinity=mt(genome.chaos_affinity, 0.0, 1.0) if not chaos else random.uniform(0.5, 1.0),
            narrative_coherence=mt(genome.narrative_coherence, 0.0, 1.5),
            mutation_susceptibility=mt(genome.mutation_susceptibility, 0.05, 1.0),
            creator=f"Descendant de {genome.organism_id}",
        )
        return child

    def evaluate_organism(self, genome: SymbolicOrganismGenome, keep_figures: bool = True) -> Tuple[float, List[SymbolicArtefact]]:
        artefacts = []
        scores = []
        for strand in genome.strands:
            artefact = self.transcriptor.transcribe_artefact(strand)
            score, breakdown = evaluate_artefact(artefact, strand)
            artefact.aesthetic_score = score
            artefact.fitness_breakdown = breakdown
            artefacts.append(artefact)
            scores.append(score)
            if not keep_figures:
                plt.close(artefact.glyph_fig)
                artefact.glyph_fig = None
        base_fitness = sum(scores) / len(scores) if scores else 0.0
        organism_bonus = 0.15 * genome.aesthetic_sense + 0.1 * genome.narrative_coherence
        fitness = min(1.0, base_fitness * 0.8 + organism_bonus)
        return fitness, artefacts

    def evolve(self, generations: int = 5, chaos_probability: float = 0.1, verbose: bool = True):
        if not self.population:
            self.initialize_population()

        for gen in range(generations):
            self.generation_count += 1
            evaluated = []
            for genome in self.population:
                fitness, artefacts = self.evaluate_organism(genome, keep_figures=False)
                evaluated.append((genome, fitness, artefacts))

            evaluated.sort(key=lambda t: t[1], reverse=True)
            best_genome, best_fitness, best_artefacts = evaluated[0]

            self.history.append({
                "generation": self.generation_count,
                "organism_id": best_genome.organism_id,
                "breed": best_genome.breed,
                "fitness": round(best_fitness, 4),
                "artefacts": [
                    {"theme": a.theme, "mantra": a.mantra_text, "score": round(a.aesthetic_score, 4),
                     "symbol": s.glyph_symbol}
                    for a, s in zip(best_artefacts, best_genome.strands)
                ],
            })

            if verbose:
                print(f"[Gen {self.generation_count:03d}] meilleur={best_genome.breed} "
                      f"fitness={best_fitness:.3f}  mantra=\"{best_artefacts[0].mantra_text}\"")

            survivors = [g for g, f, a in evaluated[:max(2, self.population_size // 3)]]
            next_pop = list(survivors)
            while len(next_pop) < self.population_size:
                parent = random.choice(survivors)
                chaos = random.random() < chaos_probability
                next_pop.append(self.mutate_organism(parent, chaos=chaos))
            self.population = next_pop

        final_eval = sorted(
            ((g, *self.evaluate_organism(g)) for g in self.population),
            key=lambda t: t[1], reverse=True,
        )
        return final_eval[0]

    def export_organism(self, genome: SymbolicOrganismGenome, artefacts: List[SymbolicArtefact],
                         fitness: float, out_dir: str) -> Dict[str, List[str]]:
        os.makedirs(out_dir, exist_ok=True)
        paths = {"png": [], "txt": [], "json": []}
        for i, (strand, artefact) in enumerate(zip(genome.strands, artefacts)):
            base = f"{genome.organism_id}_strand{i}_{strand.glyph_symbol}"
            png_path = os.path.join(out_dir, base + ".png")
            artefact.glyph_fig.savefig(png_path, dpi=130, bbox_inches='tight',
                                        facecolor=artefact.glyph_fig.get_facecolor())
            plt.close(artefact.glyph_fig)
            paths["png"].append(png_path)

            txt_path = os.path.join(out_dir, base + ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(artefact.mantra_text + "\n")
            paths["txt"].append(txt_path)

        json_path = os.path.join(out_dir, f"{genome.organism_id}_dna.json")
        payload = {
            "organism": genome.to_dict(),
            "fitness": fitness,
            "artefacts": [
                {"mantra": a.mantra_text, "theme": a.theme, "aesthetic_score": a.aesthetic_score,
                 "fitness_breakdown": a.fitness_breakdown, "timestamp": a.timestamp}
                for a in artefacts
            ],
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        paths["json"].append(json_path)
        return paths


# ═══════════════════════════════════════════════════════════════════════════════
# GÉNÉRATEUR DE PROMPT POUR IA DE DIFFUSION
# ═══════════════════════════════════════════════════════════════════════════════
def build_dna_from_args(args, theme: str = "rituel") -> SymbolicDNA:
    """Construit un SymbolicDNA à partir des arguments de la ligne de commande."""
    dna_params = {
        "theme": theme,
        "seed": random.random(),
        "generation": 0,
        "mutation_rate": args.mutation_rate if hasattr(args, 'mutation_rate') else 0.15,
    }

    mapping = {
        "glyph_symbol": args.glyph if hasattr(args, 'glyph') else None,
        "color": args.color if hasattr(args, 'color') else None,
        "scale": args.scale if hasattr(args, 'scale') else None,
        "complexity": args.complexity if hasattr(args, 'complexity') else None,
        "symmetry": args.symmetry if hasattr(args, 'symmetry') else None,
        "glitch_factor": args.glitch if hasattr(args, 'glitch') else None,
        "entropy_level": args.entropy if hasattr(args, 'entropy') else None,
        "oniric_tag": args.tag if hasattr(args, 'tag') else None,
        "mantra_template": args.template if hasattr(args, 'template') else None,
    }
    for attr, value in mapping.items():
        if value is not None:
            dna_params[attr] = value

    if hasattr(args, 'keywords') and args.keywords:
        dna_params["keyword_sequence"] = [k.strip() for k in args.keywords.split(",")]

    if hasattr(args, 'emotion') and args.emotion:
        try:
            dna_params["emotion_vector"] = json.loads(args.emotion)
        except json.JSONDecodeError:
            print("⚠️  Erreur de décodage du vecteur d'émotions. Utilisation des valeurs par défaut.")

    return SymbolicDNA(**dna_params)


def build_prompt_for_diffusion(artefact: SymbolicArtefact, dna: SymbolicDNA, 
                               aesthetic_score: float, target: str = "grok") -> str:
    """
    Génère un prompt pour moteur de diffusion (Grok, Gemini, DALL-E, etc.)
    """
    # 1. Description visuelle
    glyph_name = dna.glyph_symbol
    color = dna.color
    complexity = dna.complexity
    symmetry = dna.symmetry
    glitch = dna.glitch_factor
    entropy = dna.entropy_level

    visual_desc = f"A {glyph_name} glyph in shades of {color}, with a complexity of {complexity:.2f} and "
    visual_desc += f"symmetry order {symmetry}. "
    if glitch > 0.2:
        visual_desc += "The glyph is disrupted by digital glitch artifacts. "
    if entropy > 0.3:
        visual_desc += "The pattern is scattered across the canvas. "

    # 2. Description textuelle
    mantra = artefact.mantra_text
    tag = dna.oniric_tag or ""
    emotion = dna.dominant_emotion()

    # 3. Synthèse harmonieuse
    mood_map = {
        "peur": "dark, eerie, suspenseful",
        "joie": "bright, euphoric, radiant",
        "mystere": "mysterious, enigmatic, shadowy",
        "colere": "intense, fiery, aggressive",
        "extase": "transcendent, glowing, divine",
        "silence": "serene, meditative, calm",
    }
    mood = mood_map.get(emotion, "mystical")

    # 4. Style selon la cible
    style_map = {
        "grok": "photorealistic, cinematic, 8k, detailed, mystical, symbolic, dramatic lighting, high contrast",
        "gemini": "artistic, surreal, glowing, esoteric, highly detailed, painting, ethereal, luminous",
        "dalle": "digital art, fantasy, intricate, neon, cyberpunk, mystical, vibrant, dreamlike",
        "midjourney": "fantasy art, intricate, mystical, glowing, ethereal, detailed, majestic, --ar 1:1",
        "stable": "masterpiece, best quality, highly detailed, mystical, symbolic, fantasy, digital painting",
    }
    style = style_map.get(target.lower(), style_map["grok"])

    prompt = f"""Create a mystical, symbolic artwork.

VISUAL ELEMENTS:
- A central {glyph_name} symbol, dominant and luminous.
- Colors inspired by {color} with subtle gradients and glitch effects.
- Background: dark, cosmic, with faint geometric patterns.
- Complexity: {complexity:.2f}, symmetry: {symmetry}-fold.
- If glitch is present: broken pixels, chromatic aberration, data corruption.

TEXTUAL ELEMENTS:
- The mantra inscribed around or within the symbol: "{mantra}"
- Oniric tag: {tag or 'none'}

HARMONIOUS FUSION:
- The overall mood is {mood}.
- The image should feel like an illuminated manuscript from a cyberpunk monastery.
- Style: {mood}, {style}.
- Composition: the symbol at the center, the text flowing around it like a halo or script.
- Resolution: 1024x1024, high detail.

Aesthetic score target: {aesthetic_score:.2f}/1.0.
"""
    return prompt.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# Visualisation de la phylogenie
# ═══════════════════════════════════════════════════════════════════════════════
def render_phylogeny_board(engine: "SymbolicEvolutionEngine", out_path: str, snapshots: Optional[List[Dict]] = None):
    history = snapshots if snapshots is not None else engine.history
    if not history:
        return None
    n = len(history)
    fig, axes = plt.subplots(2, n, figsize=(3.2 * n, 7), gridspec_kw={"height_ratios": [3, 1]})
    if n == 1:
        axes = axes.reshape(2, 1)
    fig.patch.set_facecolor('#0b0b12')

    fitness_curve = []
    for i, entry in enumerate(history):
        ax_img = axes[0, i]
        ax_img.set_facecolor('#0b0b12')
        ax_img.axis('off')
        art = entry["artefacts"][0]
        ax_img.set_title(f"Gen {entry['generation']}\n{art['symbol']}", color='#00ffaa', fontsize=9)
        wrapped = "\n".join(_wrap(art["mantra"], 28))
        ax_img.text(0.5, 0.5, wrapped, ha='center', va='center', color='#ffffff', fontsize=7,
                    wrap=True, transform=ax_img.transAxes,
                    bbox=dict(boxstyle="round,pad=0.4", facecolor='#1a1a2e', edgecolor='#00ffaa'))
        fitness_curve.append(entry["fitness"])

    ax_fit = fig.add_subplot(2, 1, 2)
    ax_fit.set_position([0.08, 0.05, 0.86, 0.28])
    ax_fit.set_facecolor('#0b0b12')
    ax_fit.plot(range(1, n + 1), fitness_curve, color='#00ffaa', marker='o')
    ax_fit.set_xlabel("Génération", color='#cccccc')
    ax_fit.set_ylabel("Fitness", color='#cccccc')
    ax_fit.tick_params(colors='#cccccc')
    for spine in ax_fit.spines.values():
        spine.set_color('#444444')

    for j in range(n):
        axes[1, j].axis('off')

    fig.suptitle("Phylogénie des récits — SymbolicDNA_Forge_Chimera", color='#ffaa00', fontsize=13)
    fig.savefig(out_path, dpi=130, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    return out_path


def _wrap(text: str, width: int) -> List[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE AVEC ARGPARSER COMPLET
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="La Forge de l'ADN Symbolique — SymbolicDNA_Forge_Chimera v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES:
  # Évolution normale
  python SymbolicDNA_Forge_Chimera.py --theme voyage --generations 10

  # ADN personnalisé + prompt
  python SymbolicDNA_Forge_Chimera.py --glyph spiral --color "#ff00aa" --complexity 0.8 --glitch 0.5 --keywords "étoile,plasma,chant" --emotion '{"mystere":0.7,"extase":0.3}' --diffusion-prompt

  # Prompt uniquement (sans rendu matplotlib)
  python SymbolicDNA_Forge_Chimera.py --glyph cross --theme protection --diffusion-prompt --no-visual
"""
    )

    # --- Paramètres généraux ---
    parser.add_argument("--theme", default="rituel", choices=list(THEME_TEMPLATES.keys()), help="Thème principal")
    parser.add_argument("--population", type=int, default=8, help="Taille de la population")
    parser.add_argument("--generations", type=int, default=6, help="Nombre de générations")
    parser.add_argument("--chaos", type=float, default=0.12, help="Probabilité de chaos_mutate par reproduction")
    parser.add_argument("--out", default="./symbolic_forge_output", help="Dossier de sortie")
    parser.add_argument("--seed", type=int, default=None, help="Graine aléatoire pour reproductibilité")
    parser.add_argument("--strands", type=int, default=2, help="Nombre de brins d'ADN par organisme")
    parser.add_argument("--mutation-rate", type=float, default=0.15, help="Taux de mutation")

    # --- Paramètres de l'ADN visuel ---
    parser.add_argument("--glyph", type=str, default=None, choices=list(VonPetzingerSymbols().symbols.keys()), help="Symbole paléolithique")
    parser.add_argument("--color", type=str, default=None, help="Couleur hexadécimale (ex: #00ffaa)")
    parser.add_argument("--scale", type=float, default=None, help="Échelle du glyphe (0.3-3.0)")
    parser.add_argument("--complexity", type=float, default=None, help="Complexité du motif (0.1-1.0)")
    parser.add_argument("--symmetry", type=int, default=None, choices=range(3, 17), help="Ordre de symétrie (3-16)")
    parser.add_argument("--glitch", type=float, default=None, help="Facteur de glitch (0.0-1.0)")
    parser.add_argument("--entropy", type=float, default=None, help="Niveau d'entropie spatiale (0.0-1.0)")

    # --- Paramètres de l'ADN linguistique ---
    parser.add_argument("--keywords", type=str, default=None, help="Mots-clés séparés par des virgules")
    parser.add_argument("--template", type=str, default=None, help="Gabarit de mantra (avec {placeholders})")
    parser.add_argument("--tag", type=str, default=None, help="Balise onirique")
    parser.add_argument("--emotion", type=str, default=None, help="Vecteur d'émotions (JSON) ex: '{\"peur\":0.2,\"joie\":0.8}'")

    # --- Paramètres de l'organisme ---
    parser.add_argument("--creativity", type=float, default=None, help="Créativité (0.1-3.0)")
    parser.add_argument("--self-awareness", type=float, default=None, help="Conscience de soi (0.0-1.0)")
    parser.add_argument("--aesthetic-sense", type=float, default=None, help="Sens esthétique (0.0-2.0)")
    parser.add_argument("--chaos-affinity", type=float, default=None, help="Affinité au chaos (0.0-1.0)")
    parser.add_argument("--narrative-coherence", type=float, default=None, help="Cohérence narrative (0.0-1.5)")
    parser.add_argument("--mutation-susceptibility", type=float, default=None, help="Susceptibilité à la mutation (0.05-1.0)")
    parser.add_argument("--species", type=str, default=None, help="Espèce de l'organisme")
    parser.add_argument("--breed", type=str, default=None, help="Race de l'organisme")

    # --- Générateur de prompt pour diffusion ---
    parser.add_argument("--diffusion-prompt", action="store_true", help="Génère un prompt pour moteur de diffusion")
    parser.add_argument("--diffusion-out", type=str, default="prompt_diffusion.txt", help="Fichier de sortie pour le prompt")
    parser.add_argument("--diffusion-target", type=str, default="grok", choices=["grok", "gemini", "dalle", "midjourney", "stable"], help="Cible du prompt")
    parser.add_argument("--no-visual", action="store_true", help="Ne génère pas d'image matplotlib (utile pour prompt uniquement)")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  SymbolicDNA_Forge_Chimera — invocation de la lignée narrative ║")
    print("║  VERSION 2.0 — TOUS LES PARAMÈTRES EXPOSÉS                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Si l'utilisateur fournit des paramètres ADN personnalisés
    custom_params = any([
        args.glyph, args.color, args.scale, args.complexity, args.symmetry,
        args.glitch, args.entropy, args.keywords, args.template, args.tag,
        args.emotion, args.creativity, args.self_awareness, args.aesthetic_sense,
        args.chaos_affinity, args.narrative_coherence, args.mutation_susceptibility
    ])

    engine = SymbolicEvolutionEngine(population_size=args.population, theme=args.theme)

    if custom_params:
        print("🔧 Construction d'un ADN symbolique personnalisé...")
        custom_dna = build_dna_from_args(args, theme=args.theme)
        
        # Construction du génome avec les paramètres organismes
        genome_params = {
            "strands": [custom_dna],
            "species": args.species or "Glyphosophus",
            "breed": args.breed or "Customus",
            "generation": 0,
        }
        if args.creativity is not None:
            genome_params["creativity"] = args.creativity
        if args.self_awareness is not None:
            genome_params["self_awareness"] = args.self_awareness
        if args.aesthetic_sense is not None:
            genome_params["aesthetic_sense"] = args.aesthetic_sense
        if args.chaos_affinity is not None:
            genome_params["chaos_affinity"] = args.chaos_affinity
        if args.narrative_coherence is not None:
            genome_params["narrative_coherence"] = args.narrative_coherence
        if args.mutation_susceptibility is not None:
            genome_params["mutation_susceptibility"] = args.mutation_susceptibility
        
        custom_genome = SymbolicOrganismGenome(**genome_params)
        
        # Évaluation
        fitness, artefacts = engine.evaluate_organism(custom_genome, keep_figures=not args.no_visual)
        best_genome = custom_genome
        best_artefacts = artefacts
        best_fitness = fitness
        
        print(f"  → Fitness: {best_fitness:.3f}")
        print(f"  → Mantra: {best_artefacts[0].mantra_text}")
    else:
        print(f"🧬 Lancement de l'évolution sur {args.generations} générations...")
        engine.initialize_population()
        best_genome, best_fitness, best_artefacts = engine.evolve(
            generations=args.generations, chaos_probability=args.chaos, verbose=True
        )

    # Export standard
    if not args.no_visual:
        paths = engine.export_organism(best_genome, best_artefacts, best_fitness, args.out)
        print(f"\n📁 Exporté vers : {args.out}")
        for kind, plist in paths.items():
            for p in plist:
                print(f"  [{kind}] {p}")

    # Génération du prompt pour diffusion
    if args.diffusion_prompt:
        print("\n🧠 Génération du prompt pour diffusion...")
        prompt = build_prompt_for_diffusion(
            best_artefacts[0], 
            best_genome.dominant_strand(), 
            best_fitness,
            target=args.diffusion_target
        )
        prompt_path = os.path.join(args.out, args.diffusion_out)
        os.makedirs(args.out, exist_ok=True)
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"  → Prompt enregistré : {prompt_path}")
        print("\n" + "=" * 60)
        print("PROMPT GÉNÉRÉ :")
        print("=" * 60)
        print(prompt)
        print("=" * 60)

    # Planche de phylogénie (seulement si on a fait une évolution)
    if not custom_params and not args.no_visual:
        board_path = os.path.join(args.out, "phylogenie.png")
        render_phylogeny_board(engine, board_path)
        print(f"  [png] {board_path}  (planche de phylogénie)")

    # Résumé final
    print("\n✨ Forge terminée !")
    print(f"  → Meilleur fitness : {best_fitness:.3f}")
    print(f"  → Symbole : {best_genome.dominant_strand().glyph_symbol}")
    print(f"  → Mantra : {best_artefacts[0].mantra_text}")
    if args.diffusion_prompt:
        print(f"  → Prompt disponible : {prompt_path}")


if __name__ == "__main__":
    main()
