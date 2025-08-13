"""i18n helper script to sync Qt .ts translation files.

Usage (PowerShell):
  python scripts/update_translations.py --ts-dir freecad/StructureTools/resources/translations --linguist-bin lupdate

This script abstracts platform differences. It searches for .ts files and runs lupdate
(optionally) to refresh source strings. If lupdate unavailable, it prints instructions.
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path


def run_lupdate(ts_dir: Path, linguist_bin: str) -> int:
    sources = ["freecad/StructureTools"]
    ts_files = list(ts_dir.glob("*.ts"))
    if not ts_files:
        print("No .ts files found in", ts_dir)
        return 0
    cmd = [linguist_bin, *sources, "-ts", *[str(f) for f in ts_files]]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ts-dir", default="freecad/StructureTools/resources/translations")
    parser.add_argument("--linguist-bin", default="lupdate", help="Path to lupdate executable")
    args = parser.parse_args()
    ts_dir = Path(args.ts_dir)
    if not ts_dir.exists():
        raise SystemExit(f"Translation directory not found: {ts_dir}")
    if shutil.which(args.linguist_bin) is None:
        print("lupdate not found. Install Qt Linguist or specify --linguist-bin path.")
        raise SystemExit(1)
    code = run_lupdate(ts_dir, args.linguist_bin)
    if code == 0:
        print("Translation sources updated successfully.")
    raise SystemExit(code)


if __name__ == "__main__":  # pragma: no cover
    main()
