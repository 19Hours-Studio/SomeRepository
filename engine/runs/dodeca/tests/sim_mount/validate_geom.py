"""Validation of geom_scan.measure() on synthetic hollow dodecahedra with known geometry.

Known truth: edge 22.6 mm, wall 1.2 mm, holes (incl. one oval opposite pair), knob sphere r=2.9.
Cases: exact mesh; random rotation+shift; plus 0.05 mm and 0.1 mm normal noise (scan-like).
Pass criteria: d_mic within 0.3 mm of the true (minor) diameter, wall within 0.15 mm,
opposite pairs correct, oval major/minor within 0.4 mm.
"""
import numpy as np
from synth import build, perturb
from geom_scan import measure
from common import canonical_face_normals, save_json

HOLES = [23.0, 16.5, 15.2, 19.6, 11.9, 15.9, 11.4, 13.9, 16.2, 24.6, 20.0, 16.4]


def run_case(noise, seed, rotate=True):
    cn = canonical_face_normals()
    opp = {i: int(np.argmin(cn @ n)) for i, n in enumerate(cn)}
    pole = 0
    ovals = {pole: (26.0, 21.5), opp[pole]: (25.5, 21.5)}
    m = build(holes=HOLES, ovals=ovals)
    mp, R = perturb(m, noise=noise, seed=seed, rotate=rotate)
    g = measure(mp, verbose=False)
    N = np.array(g["normals"])
    true_N = cn @ R.T
    rows = []
    for i, n in enumerate(N):
        k = int(np.argmax(true_N @ n))
        if k in ovals:
            true_min, true_maj = ovals[k][1], ovals[k][0]
        else:
            true_min = true_maj = HOLES[k]
        h = g["holes"][i]
        rows.append(dict(face_true=k, true_min=true_min, true_maj=true_maj, d_mic=h["d_mic"],
                         ell_major=h["ell_major"], ell_minor=h["ell_minor"], width_min=h["width_min"],
                         t_plane=g["wall_t_plane"][i], t_ray_med=g["wall_t_ray_p10_med_p90_n"][i][1],
                         t_ray_p10=g["wall_t_ray_p10_med_p90_n"][i][0],
                         opp_ok=int(np.argmax(true_N @ N[g["opposite"][i]])) == opp[k]))
    return rows, g


def main():
    allres = {}
    for noise, seed in [(0.0, 1), (0.05, 2), (0.1, 3)]:
        rows, g = run_case(noise, seed)
        e_mic = np.array([r["d_mic"] - r["true_min"] for r in rows])
        e_wmin = np.array([r["width_min"] - r["true_min"] for r in rows])
        e_maj = np.array([r["ell_major"] - r["true_maj"] for r in rows])
        e_min = np.array([r["ell_minor"] - r["true_min"] for r in rows])
        tpl = np.array([r["t_plane"] for r in rows]); tr = np.array([r["t_ray_med"] for r in rows])
        tp10 = np.array([r["t_ray_p10"] for r in rows])
        print(f"noise {noise} mm: d_mic err mean {e_mic.mean():+.3f} max|{np.abs(e_mic).max():.3f}| ;"
              f" width_min err max|{np.abs(e_wmin).max():.3f}| ; ellipse major err max|{np.abs(e_maj).max():.3f}|"
              f" minor max|{np.abs(e_min).max():.3f}| ; wall plane {tpl.mean():.3f}+-{tpl.std():.3f},"
              f" ray median {tr.mean():.3f}, ray p10 {tp10.mean():.3f} (true 1.200) ; opposite pairs ok: "
              f"{all(r['opp_ok'] for r in rows)} ; knob cap r {np.mean([k['cap_radius'] for k in g['knobs']]):.2f}"
              f" body r {np.mean([k['body_radius'] for k in g['knobs']]):.2f} (true 2.90) ; orient err {g['orientation_fit_err_deg'][0]:.2f} deg")
        allres[str(noise)] = rows
    save_json("validate_geom.json", allres)


if __name__ == "__main__":
    main()
