"""Result extraction utilities for FEModel3D members.

Separable from FreeCAD GUI so we can unit test formatting logic later.
"""
from __future__ import annotations
from typing import Dict, Any, List, TypedDict, Iterable
from dataclasses import dataclass
from .units import UnitContext
import json
from .logger import get_logger

log = get_logger(__name__)


class MemberResult(TypedDict, total=False):
    stations: List[float]
    My: Dict[str, Any]
    Mz: Dict[str, Any]
    Fy: Dict[str, Any]
    Fz: Dict[str, Any]
    T: Dict[str, Any]
    axial: Dict[str, Any]
    deflection: Dict[str, Any]


@dataclass(slots=True)
class ResultsBundle:
    """Structured, typed container for member results (numeric lists).

    This is a progressive replacement for the legacy dictionary of comma-separated
    strings used by the FreeCAD GUI properties. Keep both until migration done.
    """
    members: Dict[str, MemberResult]
    units: UnitContext
    node_coords: Dict[str, List[float]] | None = None  # optional until fully integrated
    member_meta: Dict[str, Dict[str, Any]] | None = None
    _load_cases: List[str] | None = None  # internal storage for JSON emission

    def to_json(self) -> str:
        payload: Dict[str, Any] = {
            "schema_version": "1.0",
            "units": self.units.as_dict(),
            "results": {"members": self.members},
        }
        # Optional geometry/meta
        if self.node_coords:
            payload["nodes"] = [
                {"id": name, "x": xyz[0], "y": xyz[1], "z": xyz[2]} for name, xyz in self.node_coords.items()
            ]
        if self.member_meta:
            payload["members"] = [
                {"name": m, **meta} for m, meta in self.member_meta.items()
            ]
        # Load cases (derived from model later via helper)
        lc = getattr(self, "_load_cases", None)
        if lc:
            payload["load_cases"] = lc
        return json.dumps(payload, ensure_ascii=False)


def collect_member_results(model, *, num_moment: int, num_shear: int, num_axial: int, num_torque: int, num_deflection: int) -> Dict[str, Any]:
    # Each list holds per-member arrays (list[member] -> list[float])
    momentz: List[List[float]] = [] ; momenty: List[List[float]] = []
    mimMomenty = [] ; mimMomentz = [] ; maxMomenty = [] ; maxMomentz = []
    axial: List[List[float]] = [] ; torque: List[List[float]] = [] ; minTorque = [] ; maxTorque = []
    sheary: List[List[float]] = [] ; shearz: List[List[float]] = [] ; minSheary = [] ; maxSheary = [] ; minShearz = [] ; maxShearz = []
    deflectiony: List[List[float]] = [] ; minDeflectiony = [] ; maxDeflectiony = []
    deflectionz: List[List[float]] = [] ; minDeflectionz = [] ; maxDeflectionz = []
    for name, member in model.members.items():
        momenty.append(list(member.moment_array('My', num_moment)[1]))
        momentz.append(list(member.moment_array('Mz', num_moment)[1]))
        sheary.append(list(member.shear_array('Fy', num_shear)[1]))
        shearz.append(list(member.shear_array('Fz', num_shear)[1]))
        axial.append(list(member.axial_array(num_axial)[1]))
        torque.append(list(member.torque_array(num_torque)[1]))
        deflectiony.append(list(member.deflection_array('dy', num_deflection)[1]))
        deflectionz.append(list(member.deflection_array('dz', num_deflection)[1]))
        mimMomenty.append(member.min_moment('My')) ; mimMomentz.append(member.min_moment('Mz'))
        maxMomenty.append(member.max_moment('My')) ; maxMomentz.append(member.max_moment('Mz'))
        minSheary.append(member.min_shear('Fy')) ; minShearz.append(member.min_shear('Fz'))
        maxSheary.append(member.max_shear('Fy')) ; maxShearz.append(member.max_shear('Fz'))
        minTorque.append(member.min_torque()) ; maxTorque.append(member.max_torque())
        minDeflectiony.append(member.min_deflection('dy')) ; minDeflectionz.append(member.min_deflection('dz'))
        maxDeflectiony.append(member.max_deflection('dy')) ; maxDeflectionz.append(member.max_deflection('dz'))
    return dict(
        momentz=momentz, momenty=momenty,
        mimMomenty=mimMomenty, mimMomentz=mimMomentz,
        maxMomenty=maxMomenty, maxMomentz=maxMomentz,
        axial=axial, torque=torque, minTorque=minTorque, maxTorque=maxTorque,
        sheary=sheary, shearz=shearz,
        minSheary=minSheary, maxSheary=maxSheary, minShearz=minShearz, maxShearz=maxShearz,
        deflectiony=deflectiony, deflectionz=deflectionz,
        minDeflectiony=minDeflectiony, minDeflectionz=minDeflectionz,
        maxDeflectiony=maxDeflectiony, maxDeflectionz=maxDeflectionz,
    )


def build_results_bundle(model, *, num_moment: int, num_shear: int, num_axial: int, num_torque: int, num_deflection: int, units: UnitContext | None = None, include_geometry: bool = True, include_load_cases: bool = True) -> ResultsBundle:
    """Create a structured ResultsBundle with numeric arrays.

    Does not modify the legacy GUI-friendly string output; intended for future
    JSON export & programmatic consumption.
    """
    units = units or UnitContext()
    members: Dict[str, MemberResult] = {}
    member_meta: Dict[str, Dict[str, Any]] = {}
    for name, member in model.members.items():  # type: ignore[attr-defined]
        # PyNite arrays typically return (x, values)
        stations_momenty, values_momenty = member.moment_array('My', num_moment)
        stations_momentz, values_momentz = member.moment_array('Mz', num_moment)
        stations_sheary, values_sheary = member.shear_array('Fy', num_shear)
        stations_shearz, values_shearz = member.shear_array('Fz', num_shear)
        stations_axial, values_axial = member.axial_array(num_axial)
        stations_torque, values_torque = member.torque_array(num_torque)
        stations_defy, values_defy = member.deflection_array('dy', num_deflection)
        stations_defz, values_defz = member.deflection_array('dz', num_deflection)
        # Prefer moment station vector; fall back to axial if empty.
        stations_source = stations_momenty if len(stations_momenty) else stations_axial
        stations = [float(x) for x in stations_source]
        if not stations:
            log.debug("Member %s has no station data; skipping", name)
            continue
        members[name] = {
            "stations": stations,
            "My": {"values": list(values_momenty), "min": member.min_moment('My'), "max": member.max_moment('My')},
            "Mz": {"values": list(values_momentz), "min": member.min_moment('Mz'), "max": member.max_moment('Mz')},
            "Fy": {"values": list(values_sheary), "min": member.min_shear('Fy'), "max": member.max_shear('Fy')},
            "Fz": {"values": list(values_shearz), "min": member.min_shear('Fz'), "max": member.max_shear('Fz')},
            "T": {"values": list(values_torque), "min": member.min_torque(), "max": member.max_torque()},
            "axial": {"values": list(values_axial)},
            "deflection": {
                "dy": {"values": list(values_defy), "min": member.min_deflection('dy'), "max": member.max_deflection('dy')},
                "dz": {"values": list(values_defz), "min": member.min_deflection('dz'), "max": member.max_deflection('dz')},
            },
        }
        if include_geometry:
            try:
                member_meta[name] = {
                    "n1": member.i_node.name,
                    "n2": member.j_node.name,
                    "material": getattr(member, 'material_name', ''),
                    "section": getattr(member, 'section_name', ''),
                }
            except Exception:  # pragma: no cover - defensive
                pass
    node_coords = None
    if include_geometry:
        try:
            node_coords = {n: [float(nd.X), float(nd.Y), float(nd.Z)] for n, nd in model.nodes.items()}  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover
            node_coords = None
    bundle = ResultsBundle(members=members, units=units, node_coords=node_coords, member_meta=member_meta or None)
    if include_load_cases:
        try:
            cases = getattr(model, 'load_cases', [])  # property returns list
        except Exception:  # pragma: no cover
            cases = []
        bundle._load_cases = cases  # always set (may be empty)
    return bundle


def results_to_json(model, res: Dict[str, Any] | ResultsBundle, units: UnitContext | None = None) -> str:
    """Serialize results to JSON (draft schema 1.0).

    Accepts either a legacy dict (from collect_member_results) or a ResultsBundle.
    The legacy path only emits minimal moment_y data to remain backward compatible.
    """
    if isinstance(res, ResultsBundle):
        return res.to_json()
    units = units or UnitContext()
    payload: Dict[str, Any] = {"schema_version": "1.0", "units": units.as_dict(), "results": {"members": {}}}
    momenty = res.get("momenty", [])
    for idx, name in enumerate(model.members.keys()):  # type: ignore[attr-defined]
        # Support both list[str] (old) and list[list[float]] (new)
        raw = None
        if momenty:
            first = momenty[0]
            if isinstance(first, list):
                raw = momenty[idx] if idx < len(momenty) else []
            else:
                raw = momenty  # already a flat list of strings
        payload["results"]["members"][name] = {
            "My": {
                "values": raw or [],
                "min": res.get("mimMomenty", [None])[idx] if res.get("mimMomenty") else None,
                "max": res.get("maxMomenty", [None])[idx] if res.get("maxMomenty") else None,
            }
        }
    return json.dumps(payload, ensure_ascii=False)

__all__ = ["collect_member_results", "build_results_bundle", "ResultsBundle", "results_to_json"]
