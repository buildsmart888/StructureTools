# StructureTools Roadmap & Improvement Plan (Thai / EN)

อัปเดต: 2025-08-13  
สถานะ: Updated with progress (โปรดตรวจและเสนอแก้ไขได้)

Legend สถานะ / Status Legend:  
✅ = Done (เสร็จแล้ว)  | 🟡 = In Progress (กำลังทำ) | ⬜ = Pending (ยังไม่เริ่ม) | ⚠️ = Partial (บางส่วนเสร็จ)

---
 
## 1. เป้าหมายหลัก (High-Level Goals)

1. ทำให้ Workbench ติดตั้งง่าย (packaging / dependency ชัดเจน) และรองรับ FreeCAD รุ่นใหม่ได้ต่อเนื่อง
2. แยก "core analysis logic" ออกจาก FreeCAD GUI เพื่อให้เทสต์อัตโนมัติและ reuse headless ได้
3. เพิ่มความน่าเชื่อถือผ่าน Unit/Regression Tests (ตัวอย่างคาน / กรอบ / trellis) + ตรวจผลลัพธ์มาตรฐานทางกลศาสตร์
4. ปรับโครงสร้างโค้ดให้ดูแลง่าย (modularization, type hints, logging, lint)
5. รองรับ internationalization (i18n) workflow ที่ทำซ้ำง่ายบน Windows / Linux
6. เตรียมทางสำหรับ feature ขั้นสูง: load combinations, solver abstraction, caching, shell/plate, JSON export
7. สร้าง community contribution flow (docs, CONTRIBUTING, issue templates, CI ตรวจ)

---
## 2. Quick Wins (ทำก่อน – ผลกระทบสูง ใช้แรงต่ำ)

| ลำดับ | งาน | รายละเอียด | ผลกระทบ | Effort | Owner | สถานะ |
|-------|-----|------------|---------|--------|-------|--------|
| QW1 | แก้ dependencies ใน `pyproject.toml` | เปลี่ยนจากสตริงที่ครอบ list เป็น list จริง | Packaging | XS | | ✅ |
| QW2 | ใส่ `__version__` ใน `freecad/StructureTools/__init__.py` | ทำให้ dynamic version ทำงาน | Packaging | XS | | ✅ |
| QW3 | เพิ่ม `.gitignore` | กัน build/dist/egg-info | Clean | XS | | ✅ (ขั้นต่ำ) |
| QW4 | README: เพิ่ม Quick Start (ตัวอย่างคาน) | ลด learning friction | Docs | S | | ✅ |
| QW6 | สร้าง test ง่ายๆ (Simply supported beam) | ฐาน regression | QA | S | | ✅ |
| QW7 | สร้าง logger พื้นฐาน | Debug ง่าย | DX | XS | | ✅ (module สร้าง; integration รอ) |
| QW8 | Refactor: เก็บผลลัพธ์เป็น list (ไม่เป็น string join) | ลด parsing ภายหลัง | Data | S | | ✅ (GUI แปลงกลับชั่วคราว) |

---

## 3. แผน Phase ตามลำดับเวลา


### Phase 1: Foundation (สัปดาห์ 1–2)

สถานะรวม: ✅ (เสร็จ – logging integrated minimal, units context scaffold ok)

- Packaging fix (QW1–QW5) → ✅
- เพิ่ม test พื้นฐาน (UDL + point load cantilever + mapping & material integration) → ✅
- เพิ่ม tooling: ruff, mypy (strict core), pre-commit, coverage + CI → ✅
- Logging + โครงสร้าง config units → ✅ (baseline; further expansion in Phase 2)

### Phase 2: Quality & Extensibility (สัปดาห์ 3–5)

สถานะรวม: ✅ (core coverage>60%, JSON export v1 geometry+cases, templates+i18n script)

- Type hints ครอบคลุม core → ✅ (mypy strict core ผ่าน; vendor แยก stub)
- แยกผลลัพธ์เป็น object/model + ฟังก์ชัน `to_json()` → ✅ (v1: members + nodes + member meta + load_cases)
- เพิ่ม GitHub Actions: build / lint / test matrix (Python 3.10–3.12) → ✅
- Issue / PR templates + CONTRIBUTING.md → ✅ (templates + CONTRIBUTING พร้อมใช้งาน)
- i18n: สคริปต์ Python แทน `update_translation.sh` → ✅ (script พร้อม; integration docs รอ Phase 3)

### Phase 3: Feature Growth (สัปดาห์ 6–9)

สถานะรวม: 🟡 (เริ่ม wrapper load combos)

- Load combinations (wrapper รอบ PyNite `LoadCombo` + UI mapping) → 🟡 (core.load_combos module + test)
- Caching (hash geometry + loads + material → skip analyze ถ้าไม่เปลี่ยน) → ⬜
- Export/Import รูปแบบ JSON โครงสร้าง + results → ⬜ (prototype partial for results only)
- Plate/Shell validation (benchmark พื้นสี่เหลี่ยม) → ⬜

### Phase 4: Advanced & Optimization (สัปดาห์ 10–14)

สถานะรวม: ⬜

- SolverAdapter (interface: add_node, add_member, analyze, get_member_results) → ⬜
- รองรับ solver อื่น (optional stub) → ⬜
- Performance profiling (cProfile + report) → ⬜
- Parallel post-processing (numpy vectorization diagrams) → ⬜
- Documentation site (mkdocs + API reference auto) → ⬜
 
---

## 4. สถาปัตยกรรมที่เสนอ (Refactor Architecture)

```text
freecad/StructureTools/
  core/
    engine.py          # FEModel orchestration
    mapping.py         # mapNodes/mapMembers + tolerance handling
    materials.py       # material/section registration
    loads.py           # load mapping functions
    supports.py        # support mapping
    results.py         # data classes + to_json
    units.py           # central unit conversions
    cache.py           # hashing + memoization
  gui/
    calc.py (เดิมย่อย) → เรียก core.engine
    dialogs/...        # future UI forms
  tests/
    test_beam_simple.py
    test_truss_basic.py
```

- DataClasses: `Node`, `Member`, `MaterialData`, `SectionData`, `LoadCase`, `ResultsBundle`
- Interface: `ISolverAdapter` (methods: `add_node`, `add_member`, `add_dist_load`, `add_point_load`, `analyze`, `member_results(name)`).

---

## 5. กลยุทธ์การทดสอบ (Testing Strategy)

| ประเภท | ตัวอย่าง | เกณฑ์ผ่าน | หมายเหตุ |
|--------|----------|-----------|----------|
| Unit | แปลงหน่วย mm→m | ค่าเทียบเท่า ±1e-9 | ไม่ round ก่อนเวลา |
| Unit | mapNodes tolerance | Node ซ้ำระยะ < 1e-6 m merge | ป้องกัน node float noise |
| Regression | Simply supported beam UDL | Mmax ≈ wL²/8 (≤2% error) | ตรวจ sign ถูกต้อง |
| Regression | Cantilever point load | δmax = PL³/(3EI) | ตรวจค่าที่ node ปลาย |
| Integration | Frame 2 ชั้น | ไม่ error + reaction sum balance loads | ตรวจสมดุล |
| JSON Export | roundtrip serialize/deserialize | data เทียบเท่า | hash identical |

เครื่องมือ: pytest + hypothesis (ภายหลังสำหรับ fuzz loads) (เริ่มจาก pytest พื้นฐานก่อน)

---

## 6. Packaging / Distribution

- เปลี่ยนชื่อ distribution: `freecad-structuretools` (PEP 503 friendly) | retain import path `freecad.StructureTools`
- Pin minimal versions: `numpy>=1.24`, `scipy>=1.10`
- `python_requires >= 3.10` (ใช้ match-case)
- ลบ `setup.py` (ถ้าไม่ต้องการ editable legacy)
- เพิ่ม `LICENSE` notice สำหรับโค้ดที่ vendored (PyNite) + พิจารณา external dependency แทนการคัดลอก

---

## 7. Internationalization (i18n)

- เพิ่มสคริปต์ Python: `scripts/update_translations.py`
- Workflow: extract → merge → push .ts → compile .qm → load runtime
- เพิ่มภาษา: pt-BR (จากผู้พัฒนา), th-TH (อาจภายหลัง)

---

## 8. Logging & Diagnostics

- โมดูล `logger.py` → `get_logger(__name__)`
- Levels: INFO (ขั้นตอนใหญ่), DEBUG (node mapping, loads), WARNING (fallback units), ERROR (solver fail)
- Optional: environment variable `STRUCTURETOOLS_LOG_LEVEL`

---

## 9. Risk Register (เบื้องต้น)

| ความเสี่ยง | ผลกระทบ | โอกาส | แนวทางบรรเทา |
|------------|---------|-------|---------------|
| Rounding ทำ node merge ผิด | ผลวิเคราะห์คลาดเคลื่อน | Medium | ใช้ tolerance + เก็บ coords full precision |
| Drift PyNite version (vendored) | บั๊ก/patch ไม่เข้า | High | เปลี่ยนเป็น dependency pip + test lock |
| ไม่มี test ครอบคลุม diagram sign | ความเชื่อถือผลต่ำ | Medium | เพิ่ม regression sign tests |
| GUI coupling แน่น | test headless ยาก | High | แยก core engine |
| Multi-unit conversions ซ้ำซ้อน | performance + bug | Medium | central units.py |

---

## 10. Metrics (Definition of Done สำหรับแต่ละ Phase)

| Phase | Metric | Target |
|-------|--------|--------|
| 1 | Lint errors (ruff) | 0 blocking |
| 1 | Beam test | Pass deterministic |
| 2 | Coverage (core) | ≥60% lines |
| 2 | Mypy strict (core) | <5 errors |
| 3 | JSON schema version | v1 documented |
| 3 | Load combo test | 2 scenarios pass |
| 4 | Performance (frame benchmark) | ≤ baseline time +5% |

หมายเหตุ: ตัวเลข performance เปรียบเทียบกับ baseline ก่อน optimization

---

## 11. JSON Result Schema (Draft)

```jsonc
{
  "schema_version": "1.0",
  "units": {"length": "m", "force": "kN"},
  "nodes": [{"id": "0", "x": 0.0, "y": 0.0, "z": 0.0}, ...],
  "members": [{"name": "Beam_0", "n1": "0", "n2": "1", "section": "SEC1", "material": "MAT1"}],
  "load_cases": [{"name": "LC1", "type": "service", "description": "Self Weight"}],
  "results": {
     "members": {
       "Beam_0": {
         "stations": [0.0, 0.25, 0.5, 0.75, 1.0],
         "My": {"values": [...], "min": -12.3, "max": 15.6},
         "Mz": {"values": [...], "min": -5.1, "max": 5.1},
         "Fy": {"values": [...]},
         "Fz": {"values": [...]},
         "T":  {"values": [...]},
         "axial": {"values": [...], "min": -5.0, "max": 20.0},
         "deflection": {"dy": {...}, "dz": {...}}
       }
     }
  }
}
```

---

## 12. Guidelines สำหรับ Contributor (ย่อ)

1. Fork + branch: `feature/<short-name>`
2. รัน `poetry install` หรือ `pip install -e .[dev]` (ถ้าเพิ่ม extras) – (จะกำหนดตอนจัด tooling)
3. รัน `pytest` + `ruff check` + `mypy` ก่อน PR
4. ใส่ test case เมื่อมี logic ใหม่ / bug fix
5. อัปเดต CHANGELOG (จะเพิ่มภายหลัง)

---

## 13. Changelog Format (ที่จะเพิ่ม)

ใช้ Keep a Changelog + SemVer (เริ่มที่ 0.x จน API เสถียร). Categories: Added / Changed / Fixed / Removed / Performance / Docs.

---

## 14. งานถัดไปที่เสนอเริ่มทำจริง (Implementation Entry Points)

1. สร้าง `__init__.py` ใส่ `from .version import __version__`
2. ปรับ `pyproject.toml` dependencies + classifiers + python_requires>=3.10
3. เพิ่ม `.gitignore`
4. สร้างโครง `core/` + ย้าย mapping functions
5. สร้าง test แรก `tests/test_beam_simple.py`
6. ตั้งค่า ruff + pre-commit

---

## 15. หมายเหตุเพิ่มเติม

- ถ้าต้องการเผยแพร่ FreeCAD Addon Manager ต้องมี metadata ตามแนวทาง FreeCAD (ตรวจชื่อโฟลเดอร์/Manifest)
- ประสาน License PyNite (ตรวจ LICENSE ไฟล์ upstream) ถ้า embed ต้อง credit
- ควรเตรียม script สร้าง release: bump version → tag → build wheel → upload (twine)

---

## 16. สรุปสั้น

Roadmap นี้มุ่งให้ StructureTools มั่นคง (foundation), ขยายได้ (extensibility), ตรวจสอบได้ (testable), และพร้อมต่อยอด feature ทางวิศวกรรมขั้นสูง.

> โปรดแก้/เพิ่มประเด็นที่เห็นว่าสำคัญ แล้วแจ้งฉันเพื่ออัปเดตไฟล์นี้อีกครั้ง.
