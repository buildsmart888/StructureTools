from types import SimpleNamespace
from freecad.StructureTools.core.mapping import map_nodes, map_members

class DummyVertex:
	def __init__(self, x, y, z):
		self.Point = SimpleNamespace(x=x, y=y, z=z)

class DummyEdge:
	def __init__(self, v1, v2):
		self.Vertexes = [v1, v2]

class DummyShape:
	def __init__(self, edges):
		self.Edges = edges

class DummyMaterial:
	def __init__(self, name):
		self.Name = name

class DummySection:
	def __init__(self, name):
		self.Name = name

class DummyElement:
	def __init__(self, name, p1, p2, mat_name='MAT', sec_name='SEC', truss=False):
		self.Name = name
		self.Shape = DummyShape([DummyEdge(DummyVertex(*p1), DummyVertex(*p2))])
		self.MaterialMember = DummyMaterial(mat_name)
		self.SectionMember = DummySection(sec_name)
		self.TrussMember = truss

def test_map_nodes_and_members_basic():
	elements = [
		DummyElement('Line001', (0, 0, 0), (1, 0, 0)),
		DummyElement('Line002', (1, 0, 0), (1, 1, 0)),
	]
	nodes = map_nodes(elements)
	assert len(nodes) == 3
	members = map_members(elements, nodes)
	assert len(members) == 2
	assert 'Line001_0' in members and 'Line002_0' in members
