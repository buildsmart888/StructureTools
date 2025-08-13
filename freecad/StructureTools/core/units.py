"""Centralized unit handling utilities (initial draft).

Establishes a UnitContext dataclass so future functions can receive a single
object instead of separate strings. Provides a minimal convert_quantity helper.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class UnitContext:
    length: str = "m"
    force: str = "kN"
    moment: str = "kN*m"

    def as_dict(self) -> dict[str, str]:  # simple helper for JSON export
        return {"length": self.length, "force": self.force, "moment": self.moment}


def convert_quantity(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value
    if from_unit == "mm" and to_unit == "m":
        return value / 1000.0
    if from_unit == "m" and to_unit == "mm":
        return value * 1000.0
    if from_unit == "N" and to_unit == "kN":
        return value / 1000.0
    if from_unit == "kN" and to_unit == "N":
        return value * 1000.0
    raise ValueError(f"Unsupported unit conversion {from_unit} -> {to_unit}")

__all__ = ["UnitContext", "convert_quantity"]
