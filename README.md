# StructureTools - alpha

![CI status](https://github.com/maykowsm/StructureTools/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/buildsmart888/StructureTools/branch/main/graph/badge.svg)
![PyPI](https://img.shields.io/pypi/v/freecad.StructureTools.svg)
[![Contributing](https://img.shields.io/badge/guide-contributing-blue)](CONTRIBUTING.md)

![Workbench preview](https://github.com/maykowsm/StructureTools/blob/main/freecad/StructureTools/resources/ui/img/img-1.png)

This is a workbench for FreeCAD that implements a set of tools for modeling and analyzing structural stresses, similar to analysis software such as SAP2000, Cype3D, SkyCiv, EdiLus, among many others.

The goal is to provide engineers and engineering students with a powerful and easy-to-use open source tool. Fully integrated with the existing tools in FreeCAD.

**Note:** The tools developed are limited to modeling, calculation and analysis of stresses in structural elements. The focus is not on developing tools for dimensioning these elements. The dimensioning will be handled by another workbench that I am developing in parallel to this one.

## screenshots

![Screenshot galpao](https://github.com/maykowsm/StructureTools/blob/main/freecad/StructureTools/resources/screenshots/galpao.png)
![Screenshot lajes](https://github.com/maykowsm/StructureTools/blob/main/freecad/StructureTools/resources/screenshots/lajes.png)
![Screenshot viga2D](https://github.com/maykowsm/StructureTools/blob/main/freecad/StructureTools/resources/screenshots/viga2D.png)
![Screenshot vigas3D](https://github.com/maykowsm/StructureTools/blob/main/freecad/StructureTools/resources/screenshots/vigas3D.png)
![Screenshot portico3D](https://github.com/maykowsm/StructureTools/blob/main/freecad/StructureTools/resources/screenshots/portico3D.png)

freecad/StructureTools/resources/screenshots/galpao.png

## Installing

At the moment, the StructureTools workbench can only be installed manually. I am working on getting the workbench into the FreeCAD repository.

To manually install the workbench, follow these steps:

1. Click on the “Code” button and then on Download ZIP.

2. Unzip the ZIP file to your computer.

3. Rename the extracted folder to “StructureTools.”

4. Copy the renamed folder to the Mod folder inside your FreeCAD default installation folder.

For more details on manual installation, watch the video: [YouTube walkthrough](https://www.youtube.com/watch?v=HeYGVXhw31A)

## Quick Start (Simple Cantilever Example)

Python (headless) analytical helper for a cantilever with a point load at the free end using the internal core engine:

```python
from freecad.StructureTools.core.engine import analyze_cantilever_point_load
from freecad.StructureTools.core.results import build_results_bundle, results_to_json
from freecad.StructureTools.Pynite_main.FEModel3D import FEModel3D

# Build a minimal PyNite model manually (example only)
model = FEModel3D()
model.add_node('0', 0, 0, 0)
model.add_node('1', 2.0, 0, 0)  # 2 m cantilever
model.add_material('MAT', 210e9, 80e9, 0.3, 7850)
model.add_section('SEC', 0.02, 2e-6, 2e-6, 4e-6)
model.add_member('B','0','1','MAT','SEC')
model.def_support('0', True, True, True, True, True, True)
model.add_member_dist_load('B','Fy', -1.5, -1.5)  # -1.5 kN/m uniform down
model.analyze()

bundle = build_results_bundle(model, num_moment=11, num_shear=11, num_axial=3, num_torque=3, num_deflection=11)
print(results_to_json(model, bundle))
```

Use the Calc tool inside FreeCAD GUI for interactive modeling; this quick start shows the emerging programmatic API.


## Tools

The StructureTools workbench is still under development and is constantly changing with the addition of new tools, improvements and bug fixes, I will try to keep this list updated whenever possible.

**Define Member** - modeling of bar elements, the graphical modeling of a bar element can be done using the Draft tool through the line tool and later converting it into a member of the structure. With the definition of the member of the structure done, it is possible to assign to this member several parameters such as Section, Material, and whether it is a truss member.

**Support** - modeling of the supports of the structure capable of fixing the individual rotation and translation of the X, Y and Z axes.

**Section** - defines the section of the members of the structure, capable of capturing the geometric parameters of the area of ​​any face.

**Material** - Defines the physical properties of the material of the structural elements.

**Distributed Load** - defines an external linear load distributed on a member of the structure, capable of modeling uniformly distributed loads, triangular and trapezoidal loads, definition in the global axis.

**Nodal Load** – defines an external force acting on a node of the structure, defined on the global axis.

**Calc Structure** – a tool that creates a calculation object with all the results of the efforts of the structural elements, bending moment, shear, axial force, torque and displacements. It is possible to change the units of the results, number of points calculated for each element, automatic calculation of own weight.

**Diagram** – generates the effort diagrams based on the Calc object. With this tool, it is possible to graphically view the diagram of the efforts of the same on the axis of the element itself. The tool has parameters for scale, color, text size, all to facilitate the visualization and interpretation of the results. It is possible to draw the diagram of individual elements or of the entire structure.

You can see more about the tools in these videos:

* StructureTools - Alpha Version - Workbench Tools and Workflow: [video](https://www.youtube.com/watch?v=AicdjiOc61k)
* StructureTools - Alpha Version - Calculation of forces of simply supported beams: [video](https://www.youtube.com/watch?v=Ig0SyqJao0Q)

## Core Architecture Overview

| Module | Purpose | Key Public Functions / Objects |
|--------|---------|--------------------------------|
| `core/engine.py` | Small analytical helpers & FE model setup for simple beams (testable) | `analyze_cantilever_uniform_load`, `analyze_cantilever_point_load`, `SimpleBeamResult` |
| `core/mapping.py` | Extract unique nodes & member definitions from FreeCAD elements | `map_nodes`, `map_members` |
| `core/materials.py` | Register materials and sections (with rotation handling) | `set_materials_and_sections` |
| `core/loads.py` | Apply distributed & nodal loads (axis remap logic) | `apply_loads` |
| `core/supports.py` | Apply supports by matching vertices to node map | `apply_supports` |
| `core/results.py` | Aggregate member result arrays & extrema; structured export | `collect_member_results`, `build_results_bundle`, `results_to_json` |

Note: PyPI badge will show "missing" until the first release is published.


## Development

You can follow the development of the project here: <https://github.com/users/maykowsm/projects/1/views/1>
I'm trying to write proper documentation for the FreeCAD Wiki, if you want to help me, you'll be welcome.

### Local development quick start

Clone the repo and install dev extras (creates venv if you prefer):

```bash
pip install -e .[dev]
```

Run tests:

```bash
pytest -q
```

Run lint & type checks:

```bash
ruff check .
mypy .
```

Pre-commit hooks are configured; enable with:

```bash
pre-commit install
```

This project is incrementally extracting solver-agnostic logic into `freecad/StructureTools/core` for better testability.

### Coverage Reporting

CI uploads coverage to Codecov. For private forks or if uploads fail, add a repository secret named `CODECOV_TOKEN` (see Codecov project settings) and the workflow will use it automatically. Public repos on Codecov may work without a token, but Codecov Action v4 recommends providing one.

See also: [Contributing guide](CONTRIBUTING.md).

You can also follow the discussion about StructureTools on the FreeCAD forum: <https://forum.freecad.org/viewtopic.php?t=94995>

Please consider supporting the project so I can dedicate more time to it: [Patreon](https://patreon.com/StructureTools), [ApoiaSe](https://apoia.se/structuretools)

## Dependencies

['numpy', 'scipy']

## Maintainer

Maykow Menezes

[linkedin](https://www.linkedin.com/in/engmaykowmenezes/)

[X old twitter](https://x.com/StructureTools)

Telegram: @Eng_Maykow_Menezes

Contact: <eng.maykowmenezes@gmail.com>
