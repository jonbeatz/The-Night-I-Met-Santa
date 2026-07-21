"""DEPRECATED pointer — use scripts/ps-export-layers-jpg.py or: npm run ps:export-layers

See .cursor/skills/Photoshop-Layer-Export/SKILL.md
"""
from pathlib import Path
import runpy
import sys

target = Path(__file__).resolve().parents[1] / "ps-export-layers-jpg.py"
sys.argv = [str(target), *sys.argv[1:]]
runpy.run_path(str(target), run_name="__main__")
