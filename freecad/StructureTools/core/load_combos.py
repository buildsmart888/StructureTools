"""Load combination helper layer wrapping PyNite LoadCombo.

Provides a simple API for adding and listing combinations without exposing
PyNite internals to the GUI layer directly.
"""
from __future__ import annotations
from typing import Dict, Iterable
from ..Pynite_main.LoadCombo import LoadCombo
from .logger import get_logger

log = get_logger(__name__)


def add_load_combo(model, name: str, factors: Dict[str, float], tags: Iterable[str] | None = None) -> None:
    if name in model.load_combos:  # type: ignore[attr-defined]
        raise ValueError(f"Load combo '{name}' already exists")
    combo = LoadCombo(name, list(tags) if tags else None, dict(factors))
    model.load_combos[name] = combo  # type: ignore[attr-defined]
    log.debug("Added load combo %s: %s", name, factors)


def list_load_combos(model) -> Dict[str, Dict[str, float]]:
    return {n: c.factors for n, c in model.load_combos.items()}  # type: ignore[attr-defined]

__all__ = ["add_load_combo", "list_load_combos"]
