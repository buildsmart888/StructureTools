"""Core headless analysis & helpers for StructureTools.

Exports mapping, engine helpers for easier imports in tests.
"""
from .engine import analyze_cantilever_uniform_load, analyze_cantilever_point_load  # noqa: F401
from .mapping import map_nodes, map_members  # noqa: F401
