from freecad.StructureTools.Pynite_main.FEModel3D import FEModel3D
from freecad.StructureTools.core.load_combos import add_load_combo, list_load_combos

def test_add_and_list_load_combos():
    m = FEModel3D()
    # base model gets no combos until analysis runs
    assert list_load_combos(m) == {}
    add_load_combo(m, 'S1', {'DL':1.0, 'LL':0.5}, tags=['service'])
    combos = list_load_combos(m)
    assert 'S1' in combos and combos['S1']['DL'] == 1.0
    # duplicate should raise
    try:
        add_load_combo(m, 'S1', {'DL':1.0}, tags=None)
        assert False, 'Expected ValueError'
    except ValueError:
        pass
