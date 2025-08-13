from freecad.StructureTools.core.results import build_results_bundle, ResultsBundle
from freecad.StructureTools.Pynite_main.FEModel3D import FEModel3D


def simple_model():
    m = FEModel3D()
    m.add_node('0',0,0,0)
    m.add_node('1',1,0,0)
    # FEModel3D.add_material(name, E, G, nu, rho)
    m.add_material('MAT', 200e9, 80e9, 0.3, 7850)
    # add_section(name, A, Iy, Iz, J)
    m.add_section('SEC', 0.01, 1e-6, 1e-6, 2e-6)
    m.add_member('M1','0','1','MAT','SEC')
    # minimal load/support to allow analysis
    m.def_support('0', True, True, True, True, True, True)
    m.add_member_dist_load('M1','Fy',-1,-1)
    m.analyze()
    return m


def test_build_results_bundle_basic():
    model = simple_model()
    bundle = build_results_bundle(model, num_moment=3, num_shear=3, num_axial=2, num_torque=2, num_deflection=3)
    assert isinstance(bundle, ResultsBundle)
    assert 'M1' in bundle.members
    mr = bundle.members['M1']
    assert 'My' in mr and 'values' in mr['My']
    assert len(mr['My']['values']) >= 2
    # JSON roundtrip
    js = bundle.to_json()
    assert 'schema_version' in js
    import json
    data = json.loads(js)
    assert 'nodes' in data and 'members' in data
    assert 'load_cases' in data
