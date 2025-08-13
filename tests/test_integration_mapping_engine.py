from types import SimpleNamespace
from freecad.StructureTools.core.mapping import map_nodes, map_members
from freecad.StructureTools.core.engine import analyze_cantilever_uniform_load


class V:  # simple vertex stub
    def __init__(self, x, y, z):
        self.Point = SimpleNamespace(x=x, y=y, z=z)


class Edge:
    def __init__(self, v1, v2):
        self.Vertexes = [v1, v2]


class Elem:
    def __init__(self, name, p1, p2):
        self.Name = name
        self.Shape = SimpleNamespace(Edges=[Edge(V(*p1), V(*p2))])
        self.MaterialMember = SimpleNamespace(Name='MAT')
        self.SectionMember = SimpleNamespace(Name='SEC')
        self.TrussMember = False


def test_mapping_then_engine_uniform_load():
    elems = [Elem('Line001', (0, 0, 0), (2, 0, 0))]
    nodes = map_nodes(elems)
    members = map_members(elems, nodes)
    assert len(nodes) == 2 and len(members) == 1
    result = analyze_cantilever_uniform_load(2.0, 1.0, 210000.0, 8e-5, 8e-5, 0.02, 1.0e-5)
    assert abs(result.max_moment_model - result.max_moment_theoretical) / result.max_moment_theoretical < 0.05
