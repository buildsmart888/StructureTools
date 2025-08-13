from __future__ import annotations
from dataclasses import dataclass
from typing import List
from ..Pynite_main.FEModel3D import FEModel3D


@dataclass
class SimpleBeamResult:
	length: float
	w: float
	my_stations: List[float]
	my_values: List[float]
	max_moment_theoretical: float
	max_moment_model: float


def analyze_cantilever_uniform_load(length: float, w: float, E: float, Iy: float, Iz: float, A: float, J: float, n_points: int = 21) -> SimpleBeamResult:
	model = FEModel3D()
	model.add_node('N1', 0.0, 0.0, 0.0)
	model.add_node('N2', length, 0.0, 0.0)
	G = E / (2 * (1 + 0.3))
	model.add_material('MAT', E, G, 0.3, 1.0)
	model.add_section('SEC', A, Iy, Iz, J)
	model.add_member('M1', 'N1', 'N2', 'MAT', 'SEC')
	model.def_support('N1', True, True, True, True, True, True)
	model.add_member_dist_load('M1', 'FY', -w, -w)
	model.analyze()
	# PyNite member local axis orientation can cause bending to appear in either My or Mz
	stations_y, My = model.members['M1'].moment_array('My', n_points)
	stations_z, Mz = model.members['M1'].moment_array('Mz', n_points)
	if max(abs(v) for v in My) >= max(abs(v) for v in Mz):
		stations, Mvals = stations_y, My
	else:
		stations, Mvals = stations_z, Mz
	theoretical = w * length**2 / 2.0
	model_max = max(abs(v) for v in Mvals)
	return SimpleBeamResult(length, w, list(stations), list(Mvals), theoretical, model_max)


def analyze_cantilever_point_load(length: float, P: float, E: float, Iy: float, Iz: float, A: float, J: float, n_points: int = 21) -> SimpleBeamResult:
	model = FEModel3D()
	model.add_node('N1', 0.0, 0.0, 0.0)
	model.add_node('N2', length, 0.0, 0.0)
	G = E / (2 * (1 + 0.3))
	model.add_material('MAT', E, G, 0.3, 1.0)
	model.add_section('SEC', A, Iy, Iz, J)
	model.add_member('M1', 'N1', 'N2', 'MAT', 'SEC')
	model.def_support('N1', True, True, True, True, True, True)
	model.add_node_load('N2', 'FY', -P)
	model.analyze()
	stations_y, My = model.members['M1'].moment_array('My', n_points)
	stations_z, Mz = model.members['M1'].moment_array('Mz', n_points)
	if max(abs(v) for v in My) >= max(abs(v) for v in Mz):
		stations, Mvals = stations_y, My
	else:
		stations, Mvals = stations_z, Mz
	theoretical = P * length
	model_max = max(abs(v) for v in Mvals)
	return SimpleBeamResult(length, P, list(stations), list(Mvals), theoretical, model_max)
