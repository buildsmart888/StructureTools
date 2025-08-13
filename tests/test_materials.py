from types import SimpleNamespace
from freecad.StructureTools.core.materials import set_materials_and_sections


class DummyModel:
    def __init__(self):
        self.materials = []
        self.sections = []

    def add_material(self, name, E, G, nu, density):
        self.materials.append((name, E, G, nu, density))

    def add_section(self, name, A, Iy, Iz, J):
        self.sections.append((name, A, Iy, Iz, J))


def make_line(name: str, mat_name: str, sec_name: str):
    # When FreeCAD is absent, core.materials expects ModulusElasticity to be numeric
    material = SimpleNamespace(Name=mat_name, Density=25.0, ModulusElasticity=2.1e5, PoissonRatio=0.3)
    section = SimpleNamespace(Name=sec_name, MomentInertiaPolar=1.0, AreaSection=0.01, MomentInertiaY=1.2, MomentInertiaZ=1.5, ProductInertiaYZ=0.05)
    line = SimpleNamespace(Name=name, MaterialMember=material, SectionMember=section, RotationSection=0.0)
    return line


def test_set_materials_and_sections_deduplicates():
    model = DummyModel()
    lines = [make_line('L1', 'MAT', 'SEC'), make_line('L2', 'MAT', 'SEC')]
    set_materials_and_sections(model, lines, 'm', 'kN')
    assert len(model.materials) == 1
    assert len(model.sections) == 1
