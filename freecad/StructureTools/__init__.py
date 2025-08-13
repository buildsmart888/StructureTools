"""StructureTools FreeCAD Workbench package.

Minimal init so dynamic version extraction during build succeeds even if
FreeCAD modules aren't present.
"""

try:  # pragma: no cover
	from .version import __version__  # noqa: F401
except Exception:  # pragma: no cover
	__version__ = "0.0.0+unknown"

__all__ = ["__version__"]
