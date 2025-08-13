"""Minimal FreeCAD API stub used in unit tests.

Allows core modules (loads, supports, materials) to be imported/run without a real
FreeCAD installation. Only required attributes are implemented.
"""
class _UnitsQuantity:
    def __init__(self, value, unit=None):
        self._value = value

    def getValueAs(self, _target):  # simple passthrough
        return self._value


class _Units:
    Quantity = _UnitsQuantity


class FreeCADStub:
    Units = _Units()


FreeCAD = FreeCADStub()  # noqa: N816
