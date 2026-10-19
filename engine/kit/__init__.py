"""Verified calculators for screening/review of Arctic & permafrost resource ideas
(Yakutia, Magadan, Chukotka, Siberia).

    import sys; sys.path.insert(0, '/home/user/SomeRepository/engine')
    from kit import ice, thermal, geotech, hydro, naval, econ, stats, climate, data

Modules: thermal, ice, geotech, hydro, naval, econ, stats, climate, data. See CATALOG.md for the killer
classes and INVENTORY.md for where each model and value came from. Run tests: python3 engine/kit/test_kit.py
"""
from . import data, climate, thermal, ice, geotech, hydro, naval, econ, stats  # noqa: F401

__all__ = ["data", "climate", "thermal", "ice", "geotech", "hydro", "naval", "econ", "stats"]
