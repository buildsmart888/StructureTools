from importlib import import_module
from freecad.StructureTools.core.engine import analyze_cantilever_uniform_load


def test_package_version_exposed():
    mod = import_module('freecad.StructureTools')
    assert isinstance(mod.__version__, str) and mod.__version__


def test_cantilever_uniform_load_moment_close():
    L = 5.0
    w = 2.0
    E = 210000.0
    A = 0.02
    Iy = 8.0e-5
    Iz = 8.0e-5
    J = 1.0e-5
    result = analyze_cantilever_uniform_load(L, w, E, Iy, Iz, A, J)
    assert abs(result.max_moment_model - result.max_moment_theoretical) / result.max_moment_theoretical < 0.05
