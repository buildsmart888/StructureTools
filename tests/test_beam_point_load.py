from freecad.StructureTools.core.engine import analyze_cantilever_point_load


def test_cantilever_point_load_moment_close():
	L = 4.0
	P = 5.0  # kN
	E = 210000.0
	A = 0.02
	Iy = 9.0e-5
	Iz = 9.0e-5
	J = 1.2e-5
	result = analyze_cantilever_point_load(L, P, E, Iy, Iz, A, J)
	# theoretical fixed-end moment P*L
	assert abs(result.max_moment_model - result.max_moment_theoretical) / result.max_moment_theoretical < 0.05
