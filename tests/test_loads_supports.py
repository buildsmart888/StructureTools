from types import SimpleNamespace
from freecad.StructureTools.core.loads import apply_loads
from freecad.StructureTools.core.supports import apply_supports


class DummyVertex:
    def __init__(self, x, y, z):
        self.Point = SimpleNamespace(x=x, y=y, z=z)


class DummyEdge:
    def __init__(self, v1, v2):
        self.Vertexes = [v1, v2]


class DummyModel:
    def __init__(self):
        self.member_dist_loads = []
        self.node_loads = []
        self.supports = []

    def add_member_dist_load(self, name, axis, wi, wf):
        self.member_dist_loads.append((name, axis, wi, wf))

    def add_node_load(self, index, axis, value):
        self.node_loads.append((index, axis, value))

    def def_support(self, index, *flags):
        self.supports.append((index, flags))


def make_distributed_load(member_name: str, edge_index: int, global_dir: str, wi: float, wf: float):
    token = f"Edge{edge_index+1}"
    member = SimpleNamespace(Name=member_name)
    load = SimpleNamespace(
        GlobalDirection=global_dir,
        InitialLoading=SimpleNamespace(getValueAs=lambda unit: wi),
        FinalLoading=SimpleNamespace(getValueAs=lambda unit: wf),
        ObjectBase=[(member, [token])],
    )
    return load


def make_nodal_load(member_name: str, vertex_index: int, global_dir: str, value: float, v: DummyVertex):
    token = f"Vertex{vertex_index+1}"
    shape = SimpleNamespace(Vertexes=[v])
    obj = SimpleNamespace(Name=member_name, Shape=shape)
    load = SimpleNamespace(
        GlobalDirection=global_dir,
        NodalLoading=SimpleNamespace(getValueAs=lambda unit: value),
        ObjectBase=[(obj, [token])],
    )
    return load


def test_apply_loads_member_and_nodal():
    model = DummyModel()
    nodes_map = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ]
    dist = make_distributed_load('Line001', 0, '+Z', 2.0, 2.0)
    vertex = DummyVertex(1.0, 0.0, 0.0)
    nodal = make_nodal_load('Line001', 0, '-Z', 5.0, vertex)
    apply_loads(model, [dist, nodal], nodes_map, 'kN', 'm')
    assert model.member_dist_loads == [('Line001_0', 'FY', 2.0, 2.0)]
    assert model.node_loads == [('1', 'FY', -5.0)]


def test_apply_supports():
    model = DummyModel()
    nodes_map = [
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
    ]
    shape = SimpleNamespace(Vertexes=[DummyVertex(0.0, 0.0, 0.0)])
    support = SimpleNamespace(
        ObjectBase=[(SimpleNamespace(Shape=shape), ['Vertex1'])],
        FixTranslationX=True,
        FixTranslationZ=False,
        FixTranslationY=True,
        FixRotationX=False,
        FixRotationZ=True,
        FixRotationY=False,
    )
    apply_supports(model, [support], nodes_map, 'm')
    assert model.supports and model.supports[0][0] == '0'
