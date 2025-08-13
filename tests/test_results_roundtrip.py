import json
from freecad.StructureTools.core.results import build_results_bundle, results_to_json
from freecad.StructureTools.Pynite_main.FEModel3D import FEModel3D

def model():
    m = FEModel3D()
    m.add_node('0',0,0,0)
    m.add_node('1',1,0,0)
    m.add_material('MAT',200e9,80e9,0.3,7850)
    m.add_section('SEC',0.01,1e-6,1e-6,2e-6)
    m.add_member('M','0','1','MAT','SEC')
    m.def_support('0', True, True, True, True, True, True)
    m.add_member_dist_load('M','Fy',-1,-1)
    m.analyze()
    return m

def test_results_bundle_roundtrip_equivalence():
    m = model()
    b = build_results_bundle(m, num_moment=5, num_shear=5, num_axial=3, num_torque=3, num_deflection=5)
    js = b.to_json()
    data = json.loads(js)
    # ensure member names present in both metadata and results blocks
    member_names_meta = {mm['name'] for mm in data['members']}
    member_names_results = set(data['results']['members'].keys())
    assert member_names_meta == member_names_results
    # Re-serialize legacy path and ensure schema_version stable
    legacy_json = results_to_json(m, b)
    assert json.loads(legacy_json)['schema_version'] == '1.0'
