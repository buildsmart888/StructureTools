import json
from freecad.StructureTools.core.results import build_results_bundle, results_to_json
from freecad.StructureTools.Pynite_main.FEModel3D import FEModel3D


def _model():
    m = FEModel3D()
    m.add_node('0',0,0,0)
    m.add_node('1',2,0,0)
    m.add_material('MAT', 210e9, 80e9, 0.3, 7850)
    m.add_section('SEC', 0.02, 2e-6, 2e-6, 4e-6)
    m.add_member('M','0','1','MAT','SEC')
    m.def_support('0', True, True, True, True, True, True)
    m.add_member_dist_load('M','Fy', -2, -2)
    m.analyze()
    return m


def test_results_bundle_json_roundtrip():
    model = _model()
    bundle = build_results_bundle(model, num_moment=5, num_shear=5, num_axial=3, num_torque=3, num_deflection=5)
    js = bundle.to_json()
    data = json.loads(js)
    assert data['schema_version'] == '1.0'
    assert 'results' in data and 'members' in data['results']
    assert 'nodes' in data and 'members' in data  # top-level geometry sections
    assert 'load_cases' in data
    assert 'M' in data['results']['members']
    assert 'My' in data['results']['members']['M']
    assert 'values' in data['results']['members']['M']['My']


def test_legacy_dict_json_export():
    model = _model()
    # legacy path: collect_member_results still returns nested list & min/max arrays
    from freecad.StructureTools.core.results import collect_member_results
    legacy = collect_member_results(model, num_moment=4, num_shear=4, num_axial=2, num_torque=2, num_deflection=4)
    js = results_to_json(model, legacy)
    data = json.loads(js)
    assert data['schema_version'] == '1.0'
    assert 'results' in data
    assert 'M' in data['results']['members']
