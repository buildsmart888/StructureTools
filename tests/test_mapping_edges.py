from types import SimpleNamespace
from freecad.StructureTools.core.mapping import map_nodes, map_members

class V:
    def __init__(self, x, y, z):
        self.Point = SimpleNamespace(x=x, y=y, z=z)

class E:
    def __init__(self, v1, v2):
        self.Vertexes = [v1, v2]

class S:
    def __init__(self, edges):
        self.Edges = edges

class DummyMaterial:
    def __init__(self, name):
        self.Name = name

class DummySection:
    def __init__(self, name):
        self.Name = name

class Elem:
    def __init__(self, name, p1, p2, mat='M', sec='S', truss=False):
        self.Name = name
        self.Shape = S([E(V(*p1), V(*p2))])
        self.MaterialMember = DummyMaterial(mat)
        self.SectionMember = DummySection(sec)
        self.TrussMember = truss

def test_duplicate_nodes_not_duplicated():
    # Two elements share middle node (1,0,0)
    elems = [
        Elem('L1', (0,0,0), (1,0,0)),
        Elem('L2', (1,0,0), (2,0,0)),
    ]
    nodes = map_nodes(elems)
    assert len(nodes) == 3  # shared node counted once
    members = map_members(elems, nodes)
    assert set(members.keys()) == {'L1_0','L2_0'}

def test_swap_yz_flag_changes_coordinates():
    elem = Elem('L', (0,1,2), (3,4,5))
    nodes_default = map_nodes([elem])  # swap_yz True default
    nodes_no_swap = map_nodes([elem], swap_yz=False)
    # First node comparison
    assert nodes_default[0] != nodes_no_swap[0]
    # Without swap should preserve y,z order
    assert nodes_no_swap[0] == [0,1,2]
    # With swap should have z in position 1 and y in position 2
    assert nodes_default[0] == [0,2,1]
