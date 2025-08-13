from __future__ import annotations
from typing import Any, Sequence
from .logger import get_logger

log = get_logger(__name__)

try:  # FreeCAD is optional for pure unit tests; a stub can be injected.
    import FreeCAD
except Exception:  # pragma: no cover - fallback for test environment without FreeCAD
    FreeCAD = None


def _vertex_to_list(vertex: Any, unitLength: str) -> Sequence[float]:
    if FreeCAD is None:  # test stub path; vertex assumed to already have numeric x,y,z in desired units
        return [round(float(vertex.Point.x), 2), round(float(vertex.Point.z), 2), round(float(vertex.Point.y), 2)]
    return [
        round(float(FreeCAD.Units.Quantity(vertex.Point.x, 'mm').getValueAs(unitLength)), 2),
        round(float(FreeCAD.Units.Quantity(vertex.Point.z, 'mm').getValueAs(unitLength)), 2),
        round(float(FreeCAD.Units.Quantity(vertex.Point.y, 'mm').getValueAs(unitLength)), 2),
    ]


def apply_loads(model, loads, nodes_map, unitForce: str, unitLength: str):
    """Apply nodal and distributed loads to the FE model.

    Keeps original axis remapping logic used in the legacy calc implementation.
    Pure logic (string parsing + list search) so we can test with FreeCAD stubs.
    """
    count_nodal = 0
    count_dist = 0
    for load in loads:
        direction_token = getattr(load, 'GlobalDirection', None)
        match direction_token:
            case '+X':
                axis, direction = 'FX', 1
            case '-X':
                axis, direction = 'FX', -1
            case '+Y':
                axis, direction = 'FZ', 1
            case '-Y':
                axis, direction = 'FZ', -1
            case '+Z':
                axis, direction = 'FY', 1
            case '-Z':
                axis, direction = 'FY', -1
            case _:
                continue  # ignore unsupported direction

        token = load.ObjectBase[0][1][0]
        if 'Edge' in token:  # distributed load along member
            initial = float(load.InitialLoading.getValueAs(unitForce))
            final = float(load.FinalLoading.getValueAs(unitForce))
            subname = int(token.split('Edge')[1]) - 1
            name = f"{load.ObjectBase[0][0].Name}_{subname}"
            model.add_member_dist_load(name, axis, initial * direction, final * direction)
            count_dist += 1
        elif 'Vertex' in token:  # point (nodal) load
            num_vertex = int(token.split('Vertex')[1]) - 1
            vertex = load.ObjectBase[0][0].Shape.Vertexes[num_vertex]
            target = _vertex_to_list(vertex, unitLength)
            node = list(filter(lambda n: n == target, nodes_map))[0]
            index_node = nodes_map.index(node)
            model.add_node_load(str(index_node), axis, float(load.NodalLoading.getValueAs(unitForce)) * direction)
            count_nodal += 1
    log.debug("Applied loads: %d nodal, %d distributed", count_nodal, count_dist)
    return model
