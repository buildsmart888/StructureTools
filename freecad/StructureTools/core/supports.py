from __future__ import annotations
from typing import Any
from .logger import get_logger

log = get_logger(__name__)

try:  # pragma: no cover - FreeCAD optional for tests
	import FreeCAD
except Exception:  # noqa: BLE001
	FreeCAD = None  # fallback stub


def _vertex_tuple(vertex, unitLength: str):
	if FreeCAD is None:
		return (
			round(float(vertex.Point.x), 2),
			round(float(vertex.Point.z), 2),
			round(float(vertex.Point.y), 2),
		)
	return (
		round(float(FreeCAD.Units.Quantity(vertex.Point.x, 'mm').getValueAs(unitLength)), 2),
		round(float(FreeCAD.Units.Quantity(vertex.Point.z, 'mm').getValueAs(unitLength)), 2),
		round(float(FreeCAD.Units.Quantity(vertex.Point.y, 'mm').getValueAs(unitLength)), 2),
	)


def apply_supports(model, supports, nodes_map, unitLength: str):
	count = 0
	for support in supports:
		token = support.ObjectBase[0][1][0]
		if 'Vertex' not in token:
			continue
		v_index = int(token.split('Vertex')[1]) - 1
		vertex = support.ObjectBase[0][0].Shape.Vertexes[v_index]
		target = _vertex_tuple(vertex, unitLength)
		for i, node in enumerate(nodes_map):
			if (round(node[0], 2), round(node[1], 2), round(node[2], 2)) == target:
				model.def_support(
					str(i),
					support.FixTranslationX,
					support.FixTranslationZ,
					support.FixTranslationY,
					support.FixRotationX,
					support.FixRotationZ,
					support.FixRotationY,
				)
				count += 1
				break
	log.debug("Applied %d supports", count)
	return model
