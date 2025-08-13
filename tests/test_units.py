from freecad.StructureTools.core.units import convert_quantity


def test_mm_to_m():
    assert convert_quantity(1000.0, 'mm', 'm') == 1.0


def test_m_to_mm():
    assert convert_quantity(1.2, 'm', 'mm') == 1200.0


def test_kN_N_roundtrip():
    assert convert_quantity(5.0, 'kN', 'N') == 5000.0
    assert convert_quantity(5000.0, 'N', 'kN') == 5.0
