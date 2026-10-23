"""Shared helpers for the sim_mount tests (geometry of a regular dodecahedron, mesh loading).

All lengths in mm unless stated otherwise.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_DODECA = os.path.normpath(os.path.join(HERE, "..", ".."))
GLB = os.path.join(REPO_DODECA, "tests", "models3d", "files", "saalburg_FMb2103",
                   "53_Dodekaeder_100K-1.glb")
HUNT_PLY = os.path.join(REPO_DODECA, "tests", "models3d", "files", "hunt_HCM157", "HCM157_geom.ply")
# name -> (file, factor to mm, museum label)
SCANS = {
    "saalburg": (GLB, 1000.0, "Kleiner Feldberg / Saalburg FMb 2103 (Fraunhofer IGD), museum height 5.1 cm"),
    "hunt": (HUNT_PLY, 1.0, "Hunt Museum HCM 157, Limerick, museum height 4.9 cm"),
}
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)

PHI = (1 + 5 ** 0.5) / 2

# ---------------------------------------------------------------- regular dodecahedron
# Exact relations for edge length a (standard results, e.g. Wikipedia "Regular dodecahedron"):
#   inradius r_i = a/2 * phi^2 / sqrt(3 - phi) = 1.113516 a
#   circumradius R = a * sqrt(3)/2 * phi        = 1.401259 a
#   pentagon inradius  = a / (2 tan 36deg)      = 0.688191 a
#   pentagon circumradius = a / (2 sin 36deg)   = 0.850651 a
#   dihedral angle = arccos(-1/sqrt5)           = 116.565 deg
R_IN = 0.5 * PHI ** 2 / np.sqrt(3 - PHI)
R_CIRC = np.sqrt(3) / 2 * PHI
PENT_IN = 1 / (2 * np.tan(np.radians(36)))
PENT_CIRC = 1 / (2 * np.sin(np.radians(36)))


def canonical_vertices():
    """20 vertices of the regular dodecahedron with edge 2/phi (circumradius sqrt3)."""
    v = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                v.append((sx, sy, sz))
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            v.append((0, s1 / PHI, s2 * PHI))
            v.append((s1 / PHI, s2 * PHI, 0))
            v.append((s1 * PHI, 0, s2 / PHI))
    return np.array(v, float)


def canonical_face_normals():
    """12 unit face normals of the dodecahedron of canonical_vertices() (cyclic permutations
    of (0, phi, 1)); checked in _selftest(): each normal has exactly 5 vertices at maximal
    height."""
    n = []
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            n.append((0, s1 * PHI, s2))
            n.append((s2, 0, s1 * PHI))
            n.append((s1 * PHI, s2, 0))
    n = np.array(n, float)
    return n / np.linalg.norm(n, axis=1, keepdims=True)


def _selftest():
    v = canonical_vertices()
    n = canonical_face_normals()
    edge = 2 / PHI
    for f in n:
        h = v @ f
        assert np.sum(np.isclose(h, h.max())) == 5
        assert np.isclose(h.max(), R_IN * edge)
    assert np.allclose(np.linalg.norm(v, axis=1), R_CIRC * edge)
    return True


def face_vertex_incidence(normals, verts):
    """For each face normal the indices of its 5 vertices (largest dot products)."""
    vd = verts / np.linalg.norm(verts, axis=1, keepdims=True)
    out = []
    for n in normals:
        d = vd @ n
        out.append(list(np.argsort(-d)[:5]))
    return out


def opposite_index(normals):
    return [int(np.argmin(normals @ n)) for n in normals]


def load_scan_mm(name="saalburg"):
    """Load a scan as a single watertight trimesh in mm (largest component, texture seams merged)."""
    import trimesh
    path, f, _ = SCANS[name]
    s = trimesh.load(path, process=False)
    m = s.to_geometry() if hasattr(s, "to_geometry") else s
    m = trimesh.Trimesh(vertices=m.vertices * f, faces=m.faces.copy(), process=False)
    m.merge_vertices(merge_tex=True, merge_norm=True, digits_vertex=4)
    parts = sorted(m.split(only_watertight=False), key=lambda p: -len(p.faces))
    return parts[0]


def save_json(name, obj):
    path = os.path.join(RESULTS, name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    return path


def load_json(name):
    with open(os.path.join(RESULTS, name), encoding="utf-8") as f:
        return json.load(f)
