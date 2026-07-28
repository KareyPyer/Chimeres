#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  FengShui_JSON_Editor.py                                                    ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  "L'Éditeur de l'Harmonie des Données"                                      ║
║                                                                                ║
║  Un éditeur JSON méditatif qui transforme la manipulation de données        ║
║  en une expérience artistique et mystique.                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import shutil
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re


# ═══════════════════════════════════════════════════════════════════════════════
# FENG-SHUI DISPLAY — Version étendue pour l'éditeur
# ═══════════════════════════════════════════════════════════════════════════════

class FengShuiDisplay:
    """Affichage harmonieux pour l'éditeur JSON."""

    # Palettes de couleurs inspirées des pierres précieuses
    COLORS = {
        'reset': '\033[0m',
        # Pierres précieuses
        'jade': '\033[38;5;41m',
        'ruby': '\033[38;5;196m',
        'sapphire': '\033[38;5;33m',
        'amethyst': '\033[38;5;135m',
        'citrine': '\033[38;5;214m',
        'pearl': '\033[38;5;255m',
        'obsidian': '\033[38;5;236m',
        'rose_quartz': '\033[38;5;204m',
        'turquoise': '\033[38;5;80m',
        'lapis': '\033[38;5;62m',
        # Éléments
        'gold': '\033[38;5;220m',
        'silver': '\033[38;5;248m',
        'bronze': '\033[38;5;179m',
        'copper': '\033[38;5;166m',
        # États
        'success': '\033[38;5;118m',
        'warning': '\033[38;5;214m',
        'error': '\033[38;5;196m',
        'info': '\033[38;5;39m',
        # Styles
        'bold': '\033[1m',
        'italic': '\033[3m',
        'dim': '\033[2m',
        'underline': '\033[4m',
        # Fond
        'bg_dark': '\033[48;5;234m',
        'bg_deep': '\033[48;5;236m',
    }

    # Symboles Feng-Shui
    SYMBOLS = {
        'lotus': '🪷',
        'bamboo': '🎋',
        'cherry': '🌸',
        'wave': '〰️',
        'star': '✦',
        'diamond': '◇',
        'heart': '♥',
        'moon': '🌙',
        'sun': '☀️',
        'leaf': '🌿',
        'sparkle': '✨',
        'koi': '🐠',
        'mandala': '🕉️',
        'yin_yang': '☯',
        'zen': '🧘',
        'crystal': '💎',
        'feather': '🪶',
        'shell': '🐚',
        'pebble': '🪨',
        'flower': '🌸',
    }

    @classmethod
    def _c(cls, text: str, *colors) -> str:
        """Colorize text with ANSI codes."""
        codes = [cls.COLORS.get(c, '') for c in colors]
        reset = cls.COLORS['reset']
        return f"{''.join(codes)}{text}{reset}"

    @classmethod
    def header(cls, title: str, subtitle: str = "", width: int = 72):
        """Affiche un en-tête majestueux."""
        print()
        border = cls._c('═' * width, 'gold', 'dim')
        print(border)
        print(cls._c(f"  {cls.SYMBOLS['mandala']} {title}", 'gold', 'bold'))
        if subtitle:
            print(cls._c(f"  {subtitle}", 'silver', 'italic'))
        print(border)
        print()

    @classmethod
    def section(cls, title: str, icon: str = None):
        """Affiche une section avec décoration."""
        icon = icon or cls.SYMBOLS['wave']
        print()
        print(cls._c(f"  {icon} {title}", 'sapphire', 'bold'))
        print(cls._c(f"  {cls.SYMBOLS['wave']}", 'silver', 'dim'))

    @classmethod
    def info(cls, message: str, icon: str = "○"):
        print(cls._c(f"  {icon} {message}", 'pearl'))

    @classmethod
    def success(cls, message: str, icon: str = "✨"):
        print(cls._c(f"  {icon} {message}", 'success', 'bold'))

    @classmethod
    def warning(cls, message: str, icon: str = "⚠"):
        print(cls._c(f"  {icon} {message}", 'warning'))

    @classmethod
    def error(cls, message: str, icon: str = "✖"):
        print(cls._c(f"  {icon} {message}", 'error', 'bold'))

    @classmethod
    def tree(cls, items: List[Tuple[str, Any, Optional[str]]], title: str = "", indent: int = 0):
        """Affiche une arborescence élégante."""
        if title:
            print(cls._c("  " * indent + title, 'sapphire', 'bold'))
        for i, (label, value, color) in enumerate(items):
            prefix = cls._c('├──' if i < len(items) - 1 else '└──', 'silver', 'dim')
            label_colored = cls._c(label, color or 'pearl')
            value_str = cls._c(str(value), 'silver') if value is not None else ''
            print(f"{'  ' * indent}  {prefix} {label_colored}: {value_str}")

    @classmethod
    def json_tree(cls, data: Dict, title: str = "", indent: int = 0, max_depth: int = 3):
        """Affiche une structure JSON sous forme d'arbre."""
        if title:
            print(cls._c("  " * indent + title, 'sapphire', 'bold'))

        def _render(obj, level=1, prefix="", last=True):
            if level > max_depth:
                print(cls._c("  " * (indent + level) + prefix + "  ...", 'silver', 'dim'))
                return

            if isinstance(obj, dict):
                items = list(obj.items())
                for i, (key, value) in enumerate(items):
                    is_last = i == len(items) - 1
                    branch = "└──" if is_last else "├──"
                    if isinstance(value, (dict, list)):
                        key_color = 'gold' if key in ['theme', 'species', 'breed'] else 'citrine'
                        print(cls._c("  " * (indent + level) + prefix + branch + f" {key}", key_color, 'bold'))
                        _render(value, level + 1, "    " if is_last else "│   ")
                    elif isinstance(value, str) and len(value) > 60:
                        short = value[:57] + "..."
                        print(cls._c("  " * (indent + level) + prefix + branch + f" {key}: {short}", 'silver'))
                    else:
                        color = 'jade' if isinstance(value, (int, float)) else 'rose_quartz' if isinstance(value, str) else 'silver'
                        print(cls._c("  " * (indent + level) + prefix + branch + f" {key}: {value}", color))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    is_last = i == len(obj) - 1
                    branch = "└──" if is_last else "├──"
                    if isinstance(item, (dict, list)):
                        print(cls._c("  " * (indent + level) + prefix + branch + f" [{i}]", 'citrine', 'bold'))
                        _render(item, level + 1, "    " if is_last else "│   ")
                    else:
                        color = 'jade' if isinstance(item, (int, float)) else 'rose_quartz' if isinstance(item, str) else 'silver'
                        print(cls._c("  " * (indent + level) + prefix + branch + f" [{i}]: {item}", color))

        _render(data, 0)

    @classmethod
    def prompt(cls, message: str, default: str = "", options: List[str] = None) -> str:
        """Affiche une invite élégante avec suggestions."""
        print(cls._c(f"  {cls.SYMBOLS['zen']} {message}", 'sapphire'))
        if options:
            opts = " | ".join(f"[{o}]" for o in options)
            print(cls._c(f"  {cls.SYMBOLS['wave']} Options: {opts}", 'silver', 'dim'))
        if default:
            print(cls._c(f"  {cls.SYMBOLS['pebble']} Défaut: {default}", 'silver', 'dim'))
        print(cls._c("  └─> ", 'gold'), end='')
        return input().strip() or default

    @classmethod
    def separator(cls, char: str = "─", count: int = 72):
        print(cls._c(char * count, 'silver', 'dim'))

    @classmethod
    def poem(cls, lines: List[str], title: str = ""):
        """Affiche un poème ou une strophe."""
        if title:
            print(cls._c(f"\n  {title}", 'gold', 'italic'))
        for line in lines:
            print(cls._c(f"    {line}", 'lavender', 'italic'))

    @classmethod
    def mantra_box(cls, text: str, width: int = 70):
        """Affiche un texte encadré avec élégance."""
        lines = [text[i:i+width-6] for i in range(0, len(text), width-6)]
        print(cls._c('╭' + '─' * (width - 2) + '╮', 'gold', 'dim'))
        for line in lines:
            print(cls._c(f"│ {line.ljust(width - 4)} │", 'rose_quartz', 'italic'))
        print(cls._c('╰' + '─' * (width - 2) + '╯', 'gold', 'dim'))

    @classmethod
    def progress(cls, current: int, total: int, message: str = ""):
        """Affiche une barre de progression méditative."""
        bar_len = 30
        filled = int(bar_len * current / total)
        bar = '█' * filled + '░' * (bar_len - filled)
        color = 'success' if current / total > 0.7 else 'warning' if current / total > 0.3 else 'silver'
        print(cls._c(f"  [{bar}] {current}/{total}", color), end='')
        if message:
            print(cls._c(f" {message}", 'silver', 'italic'))
        else:
            print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSEUR DE DONNÉES JSON
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class JSONAnalysis:
    """Résultat de l'analyse d'un fichier JSON."""
    filename: str
    file_size: int
    keys_count: int
    total_items: int
    max_depth: int
    structure_type: str
    has_required_keys: bool
    missing_keys: List[str]
    data_quality_score: float
    issues: List[str]
    recommendations: List[str]

    def display(self):
        """Affiche l'analyse de manière élégante."""
        FengShuiDisplay.section("Analyse des données", "🔍")

        items = [
            ("Fichier", self.filename, "silver"),
            ("Taille", f"{self.file_size:,} octets", "silver"),
            ("Type", self.structure_type, "gold"),
            ("Profondeur max", self.max_depth, "citrine"),
            ("Clés totales", self.keys_count, "jade"),
            ("Éléments totaux", self.total_items, "sapphire"),
        ]
        FengShuiDisplay.tree(items)

        if self.has_required_keys:
            FengShuiDisplay.success("✅ Toutes les clés requises sont présentes")
        else:
            FengShuiDisplay.warning(f"⚠ Clés manquantes: {', '.join(self.missing_keys)}")

        FengShuiDisplay.info(f"📊 Score de qualité: {self.data_quality_score:.2%}")

        if self.issues:
            FengShuiDisplay.section("Points d'attention", "⚠")
            for issue in self.issues:
                FengShuiDisplay.warning(f"• {issue}")

        if self.recommendations:
            FengShuiDisplay.section("Recommandations", "💎")
            for rec in self.recommendations:
                FengShuiDisplay.info(f"• {rec}", "○")


# ═══════════════════════════════════════════════════════════════════════════════
# ÉDITEUR JSON FENG-SHUI
# ═══════════════════════════════════════════════════════════════════════════════

class FengShuiJSONEditor:
    """Éditeur JSON méditatif et harmonieux."""

    # Structure requise pour chaque type de fichier
    REQUIRED_STRUCTURES = {
        "oniric_lexicon": {
            "keys": ["Adjectif", "Nom", "Action", "Bénéfice", "Défaut", "Paysage", "VerbeMystique", "Symbole", "oniric_tags"],
            "description": "Lexique onirique pour la génération de mantras"
        },
        "theme_templates": {
            "keys": ["protection", "voyage", "rituel", "silence"],
            "description": "Gabarits de mantras par thème"
        },
        "theme_symbol_pools": {
            "keys": ["protection", "voyage", "rituel", "silence"],
            "description": "Pools de symboles par thème"
        },
        "theme_palettes": {
            "keys": ["protection", "voyage", "rituel", "silence"],
            "description": "Palettes chromatiques par thème"
        },
        "oniric_tag_meanings": {
            "keys": None,  # Structure libre
            "description": "Significations des tags oniriques"
        }
    }

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        self.current_file: Optional[str] = None
        self.current_data: Optional[Dict] = None
        self.file_type: Optional[str] = None
        self.backup_dir = os.path.join(base_dir, ".backups")

        # Créer les répertoires
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    # ──────────────────────────────────────────────────────────────────────────────
    # DISCOVERY — Découverte des fichiers disponibles
    # ──────────────────────────────────────────────────────────────────────────────

    def discover_files(self) -> Dict[str, List[str]]:
        """Découvre les fichiers JSON disponibles."""
        files = {}

        # Fichiers dans le dossier data
        if os.path.exists(self.data_dir):
            for f in os.listdir(self.data_dir):
                if f.endswith('.json'):
                    files[f] = os.path.join(self.data_dir, f)

        # Fichiers dans le répertoire courant
        for f in os.listdir(self.base_dir):
            if f.endswith('.json') and f not in files:
                files[f] = os.path.join(self.base_dir, f)

        return files

    def detect_file_type(self, data: Dict) -> str:
        """Détecte le type de fichier à partir de sa structure."""
        for type_name, structure in self.REQUIRED_STRUCTURES.items():
            if structure["keys"] is None:
                continue
            if all(k in data for k in structure["keys"]):
                return type_name
        return "unknown"

    # ──────────────────────────────────────────────────────────────────────────────
    # LOAD — Chargement méditatif
    # ──────────────────────────────────────────────────────────────────────────────

    def load(self, filepath: str) -> bool:
        """Charge un fichier JSON avec cérémonie."""
        FengShuiDisplay.info(f"📖 Chargement de {os.path.basename(filepath)}...", "🪷")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.current_data = json.load(f)

            self.current_file = filepath
            self.file_type = self.detect_file_type(self.current_data)

            # Analyse rapide
            keys = len(self.current_data)
            items = sum(len(v) if isinstance(v, (list, dict)) else 1 for v in self.current_data.values())

            FengShuiDisplay.success(f"✅ {os.path.basename(filepath)} chargé")
            FengShuiDisplay.info(f"   📊 {keys} clés, {items:,} éléments", "○")
            FengShuiDisplay.info(f"   🏷️  Type détecté: {self.file_type}", "○")

            return True

        except json.JSONDecodeError as e:
            FengShuiDisplay.error(f"Erreur de syntaxe JSON: {e}")
            return False
        except Exception as e:
            FengShuiDisplay.error(f"Erreur de chargement: {e}")
            return False

    # ──────────────────────────────────────────────────────────────────────────────
    # ANALYSE — Méditation sur la structure
    # ──────────────────────────────────────────────────────────────────────────────

    def analyze(self) -> JSONAnalysis:
        """Analyse en profondeur les données chargées."""
        if self.current_data is None:
            FengShuiDisplay.error("Aucune donnée chargée")
            return None

        def _count_items(obj) -> int:
            if isinstance(obj, dict):
                return sum(_count_items(v) for v in obj.values())
            elif isinstance(obj, list):
                return len(obj) + sum(_count_items(v) for v in obj)
            return 1

        def _max_depth(obj, depth=0) -> int:
            if isinstance(obj, dict):
                return max([depth] + [_max_depth(v, depth+1) for v in obj.values()])
            elif isinstance(obj, list):
                return max([depth] + [_max_depth(v, depth+1) for v in obj])
            return depth

        # Vérification des clés requises
        required = self.REQUIRED_STRUCTURES.get(self.file_type, {}).get("keys")
        missing_keys = []
        if required:
            missing_keys = [k for k in required if k not in self.current_data]

        # Détection d'issues
        issues = []
        recommendations = []

        # Vérifier les listes vides
        for key, value in self.current_data.items():
            if isinstance(value, list) and not value:
                issues.append(f"Liste vide: '{key}'")
                recommendations.append(f"Ajouter des éléments à '{key}'")

        # Vérifier la longueur des listes
        for key, value in self.current_data.items():
            if isinstance(value, list) and len(value) < 5:
                issues.append(f"Liste courte: '{key}' ({len(value)} éléments)")

        # Recommandations générales
        if self.file_type == "unknown":
            recommendations.append("Structure non reconnue — vérifier le format")

        if missing_keys:
            recommendations.append(f"Ajouter les clés manquantes: {', '.join(missing_keys)}")

        # Score de qualité
        quality_score = 1.0
        if missing_keys:
            quality_score -= len(missing_keys) * 0.1
        if issues:
            quality_score -= len(issues) * 0.05
        quality_score = max(0.0, min(1.0, quality_score))

        return JSONAnalysis(
            filename=os.path.basename(self.current_file),
            file_size=os.path.getsize(self.current_file) if self.current_file else 0,
            keys_count=len(self.current_data),
            total_items=_count_items(self.current_data),
            max_depth=_max_depth(self.current_data),
            structure_type=self.file_type,
            has_required_keys=len(missing_keys) == 0,
            missing_keys=missing_keys,
            data_quality_score=quality_score,
            issues=issues[:5],
            recommendations=recommendations[:5]
        )

    # ──────────────────────────────────────────────────────────────────────────────
    # ÉDITION — Art de la modification
    # ──────────────────────────────────────────────────────────────────────────────

    def edit_value(self, path: List[str], new_value: Any) -> bool:
        """Édite une valeur à un chemin donné."""
        if self.current_data is None:
            return False

        data = self.current_data
        for key in path[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]

        old_value = data.get(path[-1])
        data[path[-1]] = new_value

        FengShuiDisplay.success(f"✏️ {'.'.join(path)} mis à jour")
        if old_value is not None:
            FengShuiDisplay.info(f"   Ancien: {old_value}", "○")
        FengShuiDisplay.info(f"   Nouveau: {new_value}", "○")
        return True

    def add_item(self, path: List[str], key: str, value: Any) -> bool:
        """Ajoute un élément dans une liste ou un dictionnaire."""
        if self.current_data is None:
            return False

        data = self.current_data
        for k in path:
            if k not in data:
                data[k] = {}
            data = data[k]

        if isinstance(data, list):
            data.append(value)
            FengShuiDisplay.success(f"➕ Ajouté à {'.'.join(path)}")
        elif isinstance(data, dict):
            data[key] = value
            FengShuiDisplay.success(f"➕ Ajouté {key} à {'.'.join(path)}")
        else:
            FengShuiDisplay.error("Le chemin ne pointe pas vers un conteneur")
            return False
        return True

    def delete_item(self, path: List[str]) -> bool:
        """Supprime un élément."""
        if self.current_data is None:
            return False

        data = self.current_data
        for key in path[:-1]:
            if key not in data:
                FengShuiDisplay.error(f"Chemin invalide: {'.'.join(path)}")
                return False
            data = data[key]

        if isinstance(data, list):
            try:
                idx = int(path[-1])
                del data[idx]
                FengShuiDisplay.success(f"🗑️ Supprimé index {idx} de {'.'.join(path[:-1])}")
            except (ValueError, IndexError):
                FengShuiDisplay.error(f"Index invalide: {path[-1]}")
                return False
        elif isinstance(data, dict):
            if path[-1] in data:
                del data[path[-1]]
                FengShuiDisplay.success(f"🗑️ Supprimé {path[-1]} de {'.'.join(path[:-1])}")
            else:
                FengShuiDisplay.error(f"Clé introuvable: {path[-1]}")
                return False
        else:
            FengShuiDisplay.error("Le chemin ne pointe pas vers un conteneur")
            return False
        return True

    # ──────────────────────────────────────────────────────────────────────────────
    # SAUVEGARDE — Rituel de persistance
    # ──────────────────────────────────────────────────────────────────────────────

    def save(self, filepath: str = None) -> bool:
        """Sauvegarde les données avec un rituel de validation."""
        if self.current_data is None:
            FengShuiDisplay.error("Aucune donnée à sauvegarder")
            return False

        target = filepath or self.current_file
        if not target:
            FengShuiDisplay.error("Aucun chemin de sauvegarde spécifié")
            return False

        # Backup
        if os.path.exists(target):
            backup_name = f"{os.path.basename(target)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(target, backup_path)
            FengShuiDisplay.info(f"📦 Backup: {backup_name}", "○")

        # Validation
        try:
            json_str = json.dumps(self.current_data, ensure_ascii=False, indent=2)
            json.loads(json_str)  # Validation
        except Exception as e:
            FengShuiDisplay.error(f"Données invalides: {e}")
            return False

        # Sauvegarde
        try:
            with open(target, 'w', encoding='utf-8') as f:
                f.write(json_str)

            FengShuiDisplay.success(f"💾 Sauvegardé: {os.path.basename(target)}")
            FengShuiDisplay.info(f"   📊 {len(json_str):,} caractères", "○")
            return True

        except Exception as e:
            FengShuiDisplay.error(f"Erreur de sauvegarde: {e}")
            return False

    # ──────────────────────────────────────────────────────────────────────────────
    # EXPORTATION — Beauté partagée
    # ──────────────────────────────────────────────────────────────────────────────

    def export(self, format: str = "human") -> bool:
        """Exporte les données dans différents formats."""
        if self.current_data is None:
            return False

        base = os.path.splitext(self.current_file)[0]

        if format == "human":
            # Format lisible avec métadonnées
            out_path = f"{base}_human.json"
            data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "source": os.path.basename(self.current_file),
                    "type": self.file_type,
                    "total_keys": len(self.current_data),
                },
                "data": self.current_data
            }
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            FengShuiDisplay.success(f"📤 Exporté: {out_path}")

        elif format == "minimal":
            # Format compact
            out_path = f"{base}_minimal.json"
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_data, f, ensure_ascii=False, separators=(',', ':'))
            FengShuiDisplay.success(f"📤 Exporté (compact): {out_path}")

        else:
            FengShuiDisplay.error(f"Format inconnu: {format}")
            return False

        return True


# ═══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL — Interface utilisateur
# ═══════════════════════════════════════════════════════════════════════════════

class FengShuiJSONEditorUI:
    """Interface utilisateur de l'éditeur JSON Feng-Shui."""

    def __init__(self):
        self.editor = FengShuiJSONEditor()
        self.running = True

    def run(self):
        """Lance l'interface principale."""
        FengShuiDisplay.header(
            "Éditeur JSON Feng-Shui",
            "L'art de façonner les données avec grâce"
        )

        self._show_welcome()

        while self.running:
            self._show_menu()

    def _show_welcome(self):
        """Affiche un message d'accueil poétique."""
        FengShuiDisplay.poem([
            "Dans le jardin des données,",
            "Chaque fichier est un galet,",
            "Chaque clé est une graine,",
            "Chaque valeur est une fleur.",
            "",
            "Prenons soin de ce jardin,",
            "Avec patience et harmonie."
        ], title="🌸 Bienvenue")

        FengShuiDisplay.separator()

    def _show_menu(self):
        """Affiche le menu principal."""
        print()

        # État actuel
        if self.editor.current_file:
            status = f"📁 {os.path.basename(self.editor.current_file)}"
            status += f"  🏷️  {self.editor.file_type}"
            if self.editor.file_type != "unknown":
                status += " ✅"
        else:
            status = "📭 Aucun fichier chargé"

        FengShuiDisplay.info(f"État: {status}", "○")
        FengShuiDisplay.separator()

        # Menu
        options = [
            ("1", "📂 Charger un fichier", "load"),
            ("2", "👁️  Visualiser les données", "view"),
            ("3", "🔍 Analyser la structure", "analyze"),
            ("4", "✏️  Éditer une valeur", "edit"),
            ("5", "➕ Ajouter un élément", "add"),
            ("6", "🗑️  Supprimer un élément", "delete"),
            ("7", "💾 Sauvegarder", "save"),
            ("8", "📤 Exporter", "export"),
            ("9", "🆕 Créer un nouveau fichier", "new"),
            ("0", "🚪 Quitter", "quit"),
        ]

        print()
        FengShuiDisplay.info("Que souhaitez-vous faire ?", "🧘")
        for num, label, _ in options:
            print(FengShuiDisplay._c(f"  {num}. {label}", 'silver'))

        choice = input(FengShuiDisplay._c("\n  └─> ", 'gold')).strip()

        # Exécution
        for num, _, action in options:
            if choice == num:
                self._execute_action(action)
                return

        FengShuiDisplay.warning("Option invalide, veuillez réessayer.")

    def _execute_action(self, action: str):
        """Exécute une action du menu."""
        if action == "load":
            self._action_load()
        elif action == "view":
            self._action_view()
        elif action == "analyze":
            self._action_analyze()
        elif action == "edit":
            self._action_edit()
        elif action == "add":
            self._action_add()
        elif action == "delete":
            self._action_delete()
        elif action == "save":
            self._action_save()
        elif action == "export":
            self._action_export()
        elif action == "new":
            self._action_new()
        elif action == "quit":
            self._action_quit()

    # ──────────────────────────────────────────────────────────────────────────────
    # ACTIONS
    # ──────────────────────────────────────────────────────────────────────────────

    def _action_load(self):
        """Charge un fichier."""
        files = self.editor.discover_files()
        if not files:
            FengShuiDisplay.warning("Aucun fichier JSON trouvé.")
            return

        FengShuiDisplay.section("Fichiers disponibles", "📂")
        file_list = list(files.items())
        for i, (name, path) in enumerate(file_list, 1):
            size = os.path.getsize(path)
            print(FengShuiDisplay._c(f"  {i:2d}. {name}", 'silver'),
                  FengShuiDisplay._c(f"({size:,} octets)", 'dim'))

        print()
        choice = input(FengShuiDisplay._c("  └─> Choisissez un fichier (0 pour annuler): ", 'gold')).strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(file_list):
                name, path = file_list[idx]
                self.editor.load(path)
            else:
                FengShuiDisplay.warning("Numéro invalide.")
        except ValueError:
            FengShuiDisplay.warning("Entrez un nombre valide.")

    def _action_view(self):
        """Visualise les données chargées."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée chargée.")
            return

        FengShuiDisplay.section("Visualisation des données", "👁️")
        FengShuiDisplay.json_tree(self.editor.current_data, indent=0, max_depth=4)

        # Stats rapides
        total = sum(len(v) if isinstance(v, (list, dict)) else 1
                   for v in self.editor.current_data.values())
        FengShuiDisplay.info(f"📊 {len(self.editor.current_data)} clés, {total:,} éléments", "○")

    def _action_analyze(self):
        """Analyse les données chargées."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée chargée.")
            return

        analysis = self.editor.analyze()
        if analysis:
            analysis.display()

    def _action_edit(self):
        """Édite une valeur."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée chargée.")
            return

        FengShuiDisplay.section("Édition de valeur", "✏️")

        # Afficher les clés disponibles
        keys = list(self.editor.current_data.keys())
        for i, key in enumerate(keys, 1):
            value = self.editor.current_data[key]
            if isinstance(value, list):
                count = f"({len(value)} éléments)"
            elif isinstance(value, dict):
                count = f"({len(value)} sous-clés)"
            else:
                count = str(value)[:30]
            print(FengShuiDisplay._c(f"  {i:2d}. {key}", 'silver'),
                  FengShuiDisplay._c(f"{count}", 'dim'))

        print()
        choice = input(FengShuiDisplay._c("  └─> Choisissez une clé (0 pour annuler): ", 'gold')).strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                key = keys[idx]
                current = self.editor.current_data[key]

                # Nouvelle valeur
                print()
                FengShuiDisplay.info(f"Valeur actuelle: {current}", "○")
                new_val = input(FengShuiDisplay._c("  Nouvelle valeur (JSON): ", 'gold')).strip()

                if not new_val:
                    FengShuiDisplay.warning("Annulé.")
                    return

                try:
                    parsed = json.loads(new_val)
                    self.editor.edit_value([key], parsed)
                except json.JSONDecodeError:
                    # Essayer comme chaîne simple
                    self.editor.edit_value([key], new_val)
            else:
                FengShuiDisplay.warning("Numéro invalide.")
        except ValueError:
            FengShuiDisplay.warning("Entrez un nombre valide.")

    def _action_add(self):
        """Ajoute un élément."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée chargée.")
            return

        FengShuiDisplay.section("Ajout d'élément", "➕")

        print()
        FengShuiDisplay.info("📍 Ajouter à une liste ou un dictionnaire", "○")

        # Afficher les clés qui sont des conteneurs
        containers = []
        for key, value in self.editor.current_data.items():
            if isinstance(value, (list, dict)):
                containers.append(key)
                count = len(value) if isinstance(value, list) else len(value)
                print(FengShuiDisplay._c(f"  • {key}", 'silver'),
                      FengShuiDisplay._c(f"({count} éléments)", 'dim'))

        if not containers:
            FengShuiDisplay.warning("Aucun conteneur trouvé.")
            return

        print()
        target = input(FengShuiDisplay._c("  └─> Cible (clé): ", 'gold')).strip()

        if target not in self.editor.current_data:
            FengShuiDisplay.warning(f"Clé '{target}' introuvable.")
            return

        data = self.editor.current_data[target]

        if isinstance(data, list):
            print()
            FengShuiDisplay.info(f"Liste actuelle: {len(data)} éléments", "○")
            value = input(FengShuiDisplay._c("  Valeur à ajouter (JSON): ", 'gold')).strip()

            if not value:
                FengShuiDisplay.warning("Annulé.")
                return

            try:
                parsed = json.loads(value)
                self.editor.add_item([target], "", parsed)
            except json.JSONDecodeError:
                self.editor.add_item([target], "", value)

        elif isinstance(data, dict):
            print()
            key = input(FengShuiDisplay._c("  Nouvelle clé: ", 'gold')).strip()
            if not key:
                FengShuiDisplay.warning("Annulé.")
                return

            value = input(FengShuiDisplay._c("  Valeur (JSON): ", 'gold')).strip()
            if not value:
                FengShuiDisplay.warning("Annulé.")
                return

            try:
                parsed = json.loads(value)
                self.editor.add_item([target], key, parsed)
            except json.JSONDecodeError:
                self.editor.add_item([target], key, value)
        else:
            FengShuiDisplay.warning(f"'{target}' n'est pas un conteneur.")

    def _action_delete(self):
        """Supprime un élément."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée chargée.")
            return

        FengShuiDisplay.section("Suppression d'élément", "🗑️")

        # Afficher les clés disponibles
        keys = list(self.editor.current_data.keys())
        for i, key in enumerate(keys, 1):
            value = self.editor.current_data[key]
            if isinstance(value, list):
                info = f"liste ({len(value)})"
            elif isinstance(value, dict):
                info = f"dict ({len(value)})"
            else:
                info = str(value)[:20]
            print(FengShuiDisplay._c(f"  {i:2d}. {key}", 'silver'),
                  FengShuiDisplay._c(f"{info}", 'dim'))

        print()
        choice = input(FengShuiDisplay._c("  └─> Choisissez une clé (0 pour annuler): ", 'gold')).strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                key = keys[idx]
                confirm = input(FengShuiDisplay._c(f"  Confirmer la suppression de '{key}' (o/N): ", 'warning')).strip().lower()
                if confirm in ('o', 'oui', 'yes', 'y'):
                    self.editor.delete_item([key])
                else:
                    FengShuiDisplay.info("Suppression annulée.", "○")
            else:
                FengShuiDisplay.warning("Numéro invalide.")
        except ValueError:
            FengShuiDisplay.warning("Entrez un nombre valide.")

    def _action_save(self):
        """Sauvegarde les données."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée à sauvegarder.")
            return

        FengShuiDisplay.section("Sauvegarde", "💾")

        if self.editor.current_file:
            print(FengShuiDisplay._c(f"  📁 Fichier: {os.path.basename(self.editor.current_file)}", 'silver'))
            confirm = input(FengShuiDisplay._c("  Sauvegarder ? (o/N): ", 'gold')).strip().lower()
            if confirm in ('o', 'oui', 'yes', 'y'):
                self.editor.save()
            else:
                FengShuiDisplay.info("Sauvegarde annulée.", "○")
        else:
            new_file = input(FengShuiDisplay._c("  Nouveau nom de fichier: ", 'gold')).strip()
            if new_file:
                if not new_file.endswith('.json'):
                    new_file += '.json'
                self.editor.save(os.path.join(self.editor.data_dir, new_file))

    def _action_export(self):
        """Exporte les données."""
        if self.editor.current_data is None:
            FengShuiDisplay.warning("Aucune donnée à exporter.")
            return

        FengShuiDisplay.section("Exportation", "📤")
        print()
        FengShuiDisplay.info("  [1] Format lisible (avec métadonnées)", "○")
        FengShuiDisplay.info("  [2] Format compact", "○")
        print()

        choice = input(FengShuiDisplay._c("  └─> Choisissez un format (0 pour annuler): ", 'gold')).strip()

        if choice == "1":
            self.editor.export("human")
        elif choice == "2":
            self.editor.export("minimal")
        elif choice == "0":
            FengShuiDisplay.info("Exportation annulée.", "○")
        else:
            FengShuiDisplay.warning("Option invalide.")

    def _action_new(self):
        """Crée un nouveau fichier JSON."""
        FengShuiDisplay.section("Nouveau fichier", "🆕")

        types = [
            ("oniric_lexicon", "Lexique onirique"),
            ("theme_templates", "Templates de thèmes"),
            ("theme_symbol_pools", "Pools de symboles"),
            ("theme_palettes", "Palettes chromatiques"),
            ("oniric_tag_meanings", "Significations des tags"),
            ("custom", "Structure personnalisée"),
        ]

        for i, (t, desc) in enumerate(types, 1):
            print(FengShuiDisplay._c(f"  {i:2d}. {desc}", 'silver'),
                  FengShuiDisplay._c(f"({t})", 'dim'))

        print()
        choice = input(FengShuiDisplay._c("  └─> Choisissez un type (0 pour annuler): ", 'gold')).strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(types):
                type_name, _ = types[idx]

                if type_name == "custom":
                    data = {}
                else:
                    # Modèle initial
                    data = self._create_template(type_name)

                filename = input(FengShuiDisplay._c("  Nom du fichier (.json): ", 'gold')).strip()
                if not filename:
                    FengShuiDisplay.warning("Annulé.")
                    return
                if not filename.endswith('.json'):
                    filename += '.json'

                filepath = os.path.join(self.editor.data_dir, filename)
                self.editor.current_data = data
                self.editor.current_file = filepath
                self.editor.file_type = type_name
                self.editor.save(filepath)

                FengShuiDisplay.success(f"✅ Nouveau fichier créé: {filename}")

            else:
                FengShuiDisplay.warning("Numéro invalide.")
        except ValueError:
            FengShuiDisplay.warning("Entrez un nombre valide.")

    def _create_template(self, type_name: str) -> Dict:
        """Crée un modèle de données pour un type donné."""
        templates = {
            "oniric_lexicon": {
                "Adjectif": ["lumineux", "brisé", "sacré"],
                "Nom": ["signal", "rêve", "cœur"],
                "Action": ["consume", "efface", "réveille"],
                "Bénéfice": ["la clarté", "le silence"],
                "Défaut": ["le bruit", "la trahison"],
                "Paysage": ["désert du no-signal"],
                "VerbeMystique": ["consume", "efface", "illumine"],
                "Symbole": ["lune brisée", "serpent de fibre"],
                "oniric_tags": ["<burn>", "<rain>"]
            },
            "theme_templates": {
                "protection": ["Que le {Symbole} {Action} ton {Nom} du {Défaut}!"],
                "voyage": ["Dans le {Paysage}, que ton {Nom} trouve la voie."],
                "rituel": ["Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}."],
                "silence": ["Que le {Symbole} efface le bruit."]
            },
            "theme_symbol_pools": {
                "protection": ["circle", "cross", "hand"],
                "voyage": ["serpentiform", "circle", "wavy_line"],
                "rituel": ["spiral", "circle", "cross"],
                "silence": ["circle", "wavy_line", "dot"]
            },
            "theme_palettes": {
                "protection": ["#ff3366", "#ff0066", "#cc0044"],
                "voyage": ["#00ffaa", "#00ddaa", "#00bbcc"],
                "rituel": ["#ffd700", "#ffaa00", "#ff8800"],
                "silence": ["#3366ff", "#0077ff", "#00b4d8"]
            },
            "oniric_tag_meanings": {
                "<burn>": "purification par le feu numérique",
                "<rain>": "pluie de données sacrées"
            }
        }
        return templates.get(type_name, {})

    def _action_quit(self):
        """Quitte l'éditeur."""
        if self.editor.current_data and self.editor.current_file:
            FengShuiDisplay.info("Souhaitez-vous sauvegarder avant de quitter ?", "🧘")
            choice = input(FengShuiDisplay._c("  (o/N): ", 'gold')).strip().lower()
            if choice in ('o', 'oui', 'yes', 'y'):
                self.editor.save()

        FengShuiDisplay.poem([
            "Le jardin des données repose,",
            "Les galets sont alignés,",
            "Les fleurs de code s'épanouissent,",
            "Dans la paix du silence numérique."
        ], title="🌸 Au revoir")

        self.running = False


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée de l'éditeur Feng-Shui."""
    try:
        ui = FengShuiJSONEditorUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n")
        FengShuiDisplay.poem([
            "Le vent du silence souffle,",
            "Les données s'apaisent,",
            "L'éditeur se repose en paix."
        ], title="🌸 Interruption")
        sys.exit(0)
    except Exception as e:
        FengShuiDisplay.error(f"Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()