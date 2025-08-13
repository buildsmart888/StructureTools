from freecad.StructureTools.core.mapping import map_nodes

class V:  # simple vertex stub
    def __init__(self,x,y,z):
        self.Point = type('P',(),{'x':x,'y':y,'z':z})()

class Edge:
    def __init__(self, verts):
        self.Vertexes = verts

class Shape:
    def __init__(self, edges):
        self.Edges = edges

class Element:
    def __init__(self, name, coords):
        self.Name = name
        verts = [V(*c) for c in coords]
        edge = Edge(verts)
        self.Shape = Shape([edge])
        self.MaterialMember = type('M',(),{'Name':'MAT'})()
        self.SectionMember = type('S',(),{'Name':'SEC'})()
        self.TrussMember = False

def test_map_nodes_merges_close_points():
    # two points almost identical after rounding
    e = Element('E',[ (0.0004,0,0), (0.00049,0,0) ])
    nodes = map_nodes([e], round_decimals=3, swap_yz=False)
    assert len(nodes) == 1
