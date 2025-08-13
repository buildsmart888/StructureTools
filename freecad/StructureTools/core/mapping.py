from __future__ import annotations
from typing import List, Dict, Any, Sequence
from .logger import get_logger

log = get_logger(__name__)


def _vertex_to_xyz(vertex) -> Sequence[float]:
	if hasattr(vertex, 'Point'):
		p = vertex.Point
		return [float(p.x), float(p.y), float(p.z)]
	if isinstance(vertex, (list, tuple)) and len(vertex) == 3:
		return list(map(float, vertex))
	raise TypeError("Unsupported vertex type for mapping")


def map_nodes(elements, round_decimals: int = 2, swap_yz: bool = True, merge_tol: float | None = None) -> List[List[float]]:
	"""Map FreeCAD element vertices to unique node coordinate lists.

	Parameters
	----------
	elements : iterable
	round_decimals : int
		Rounding applied before uniqueness test.
	swap_yz : bool
		Swap Y/Z to preserve legacy axis mapping.
	merge_tol : float | None
		If provided, merge nodes whose euclidean distance < merge_tol after rounding.
	"""
	if merge_tol is None:
		# Use one rounding quantum as merge tolerance to collapse near-identical points
		merge_tol = 1.0 * 10 ** (-round_decimals)
	nodes: List[List[float]] = []
	for element in elements:
		for edge in element.Shape.Edges:
			for vertex in edge.Vertexes:
				x, y, z = _vertex_to_xyz(vertex)
				if swap_yz:
					cand = [round(x, round_decimals), round(z, round_decimals), round(y, round_decimals)]
				else:
					cand = [round(x, round_decimals), round(y, round_decimals), round(z, round_decimals)]
				# merge check
				found = False
				for existing in nodes:
					dx = existing[0]-cand[0]; dy = existing[1]-cand[1]; dz = existing[2]-cand[2]
					if (dx*dx + dy*dy + dz*dz) ** 0.5 < merge_tol:
						found = True
						break
				if not found:
					nodes.append(cand)
	log.debug("Mapped %d unique nodes (tol=%s)", len(nodes), merge_tol)
	return nodes


def map_members(elements, nodes: List[List[float]], round_decimals: int = 2, swap_yz: bool = True) -> Dict[str, Dict[str, Any]]:
	members: Dict[str, Dict[str, Any]] = {}
	for element in elements:
		for i, edge in enumerate(element.Shape.Edges):
			idxs = []
			for vertex in edge.Vertexes:
				x, y, z = _vertex_to_xyz(vertex)
				if swap_yz:
					node = [round(x, round_decimals), round(z, round_decimals), round(y, round_decimals)]
				else:
					node = [round(x, round_decimals), round(y, round_decimals), round(z, round_decimals)]
				index = nodes.index(node)
				idxs.append(index)
			n1, n2 = idxs
			if nodes[n1][1] > nodes[n2][1]:
				n1, n2 = n2, n1
			members[f"{element.Name}_{i}"] = {
				'nodes': [str(n1), str(n2)],
				'material': element.MaterialMember.Name,
				'section': element.SectionMember.Name,
				'trussMember': getattr(element, 'TrussMember', False),
			}
	log.debug("Mapped %d members", len(members))
	return members
