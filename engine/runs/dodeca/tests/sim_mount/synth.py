"""Synthetic hollow dodecahedron with known holes, wall thickness and knobs (manifold3d CSG).

Used to validate geom_scan.py (validate_geom.py) and to build idealised Jublains / Newhall models.
"""
import numpy as np
import manifold3d as m3
import trimesh
from common import canonical_vertices, canonical_face_normals, R_IN, R_CIRC


def _rot_z_to(n):
    """3x3 rotation taking +z to unit vector n."""
    z = np.array([0, 0, 1.0])
    v = np.cross(z, n); s = np.linalg.norm(v); cth = z @ n
    if s < 1e-12:
        return np.eye(3) if cth > 0 else np.diag([1, -1, -1.0])
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K * ((1 - cth) / s ** 2)


def build(edge=22.6, wall=1.2, holes=None, ovals=None, knob_r=2.9, knob_out=2.2, seg=96,
          oval_angle_deg=0.0, max_edge=1.4):
    """holes: 12 diameters (mm) in canonical_face_normals() order; ovals: {face: (major, minor)}.
    Knob = sphere of radius knob_r centred knob_out mm beyond the outer vertex along its radius."""
    cv = canonical_vertices(); cn = canonical_face_normals()
    s_out = edge / (2 / ((1 + 5 ** 0.5) / 2))       # canonical edge is 2/phi
    outer = m3.Manifold.hull_points((cv * s_out).tolist())
    r_in_out = R_IN * edge
    s_in = s_out * (r_in_out - wall) / r_in_out
    inner = m3.Manifold.hull_points((cv * s_in).tolist())
    shell = outer - inner
    ovals = ovals or {}
    L = 6 * wall + 2.0          # short cutter: must not reach the opposite face
    for f, n in enumerate(cn):
        if f in ovals:
            a, b = ovals[f]
            cyl = m3.Manifold.cylinder(L, 0.5, 0.5, seg, True).scale([a, b, 1.0]).rotate([0, 0, oval_angle_deg])
        else:
            d = holes[f]
            cyl = m3.Manifold.cylinder(L, d / 2, d / 2, seg, True)
        Rm = _rot_z_to(n)
        T = np.c_[Rm, n * r_in_out]          # centre the cutter on the face plane
        cyl = cyl.transform(T.tolist())
        shell = shell - cyl
    vdir = cv / np.linalg.norm(cv, axis=1, keepdims=True)
    r_v = R_CIRC * edge
    knobs = [m3.Manifold.sphere(knob_r, 48).translate((vd * (r_v + knob_out)).tolist()) for vd in vdir]
    # neck so the knob is joined to the shell
    necks = []
    for vd in vdir:
        cyl = m3.Manifold.cylinder(knob_out + 1.5, knob_r * 0.6, knob_r * 0.6, 24, False)
        Rm = _rot_z_to(vd)
        T = np.c_[Rm, vd * (r_v - 1.5)]
        necks.append(cyl.transform(T.tolist()))
    solid = m3.Manifold.batch_boolean([shell] + knobs + necks, m3.OpType.Add)
    mesh = solid.to_mesh()
    V = np.asarray(mesh.vert_properties)[:, :3]
    F = np.asarray(mesh.tri_verts)
    tm = trimesh.Trimesh(V, F, process=True)
    if max_edge:
        v2, f2 = trimesh.remesh.subdivide_to_size(tm.vertices, tm.faces, max_edge=max_edge, max_iter=20)
        tm = trimesh.Trimesh(v2, f2, process=True)
    return tm


def perturb(mesh, noise=0.0, seed=0, rotate=True, shift=(3.0, -2.0, 25.0)):
    from scipy.spatial.transform import Rotation as Rot
    rng = np.random.default_rng(seed)
    V = mesh.vertices.copy()
    R = Rot.random(random_state=seed).as_matrix() if rotate else np.eye(3)
    V = V @ R.T + np.asarray(shift)
    if noise > 0:
        m2 = trimesh.Trimesh(V, mesh.faces, process=False)
        V = V + m2.vertex_normals * rng.normal(0, noise, len(V))[:, None]
    return trimesh.Trimesh(V, mesh.faces.copy(), process=False), R
