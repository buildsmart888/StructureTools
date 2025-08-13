from __future__ import annotations
import math
from typing import Iterable

try:  # pragma: no cover - FreeCAD optional for tests
	import FreeCAD
except Exception:  # noqa: BLE001
	FreeCAD = None  # fallback


def set_materials_and_sections(model, lines, unitLength: str, unitForce: str):
	"""Register materials and sections on the FE model.

	Mirrors legacy logic from Calc.setMaterialAndSections, but isolated here so it can
	be invoked headlessly (with FreeCAD stubs) and unit-tested later.
	"""
	materials_added: list[str] = []
	sections_added: list[str] = []
	for line in lines:
		material = line.MaterialMember
		section = line.SectionMember

		if material.Name not in materials_added:
			# density: input stored (likely) in kg/m^3 equivalent via FreeCAD Units.
			if FreeCAD is not None:
				density_val = FreeCAD.Units.Quantity(material.Density).getValueAs('t/m^3') * 10  # t/m^3 -> kN/m^3
				density = float(FreeCAD.Units.Quantity(density_val, 'kN/m^3').getValueAs(f'{unitForce}/{unitLength}^3'))
				modulus = float(material.ModulusElasticity.getValueAs(f'{unitForce}/{unitLength}^2'))
			else:  # test stub path expects numeric fields
				density = float(material.Density)
				modulus = float(material.ModulusElasticity)
			poisson = float(material.PoissonRatio)
			shear_modulus = modulus / (2 * (1 + poisson))
			model.add_material(material.Name, modulus, shear_modulus, poisson, density)
			materials_added.append(material.Name)

		if section.Name not in sections_added:
			if FreeCAD is not None:
				ang = line.RotationSection.getValueAs('rad')
				J = float(FreeCAD.Units.Quantity(section.MomentInertiaPolar, 'mm^4').getValueAs(f'{unitLength}^4'))
				A = float(section.AreaSection.getValueAs(f'{unitLength}^2'))
				Iy = float(FreeCAD.Units.Quantity(section.MomentInertiaY, 'mm^4').getValueAs(f'{unitLength}^4'))
				Iz = float(FreeCAD.Units.Quantity(section.MomentInertiaZ, 'mm^4').getValueAs(f'{unitLength}^4'))
				Iyz = float(FreeCAD.Units.Quantity(section.ProductInertiaYZ, 'mm^4').getValueAs(f'{unitLength}^4'))
			else:  # test stub path expects numeric attributes
				ang = float(getattr(line, 'RotationSection', 0.0))
				J = float(section.MomentInertiaPolar)
				A = float(section.AreaSection)
				Iy = float(section.MomentInertiaY)
				Iz = float(section.MomentInertiaZ)
				Iyz = float(section.ProductInertiaYZ)
			RIy = ((Iz + Iy) / 2) - ((Iz - Iy) / 2) * math.cos(2 * ang) + Iyz * math.sin(2 * ang)
			RIz = ((Iz + Iy) / 2) + ((Iz - Iy) / 2) * math.cos(2 * ang) - Iyz * math.sin(2 * ang)
			model.add_section(section.Name, A, RIy, RIz, J)
			sections_added.append(section.Name)
	return model
