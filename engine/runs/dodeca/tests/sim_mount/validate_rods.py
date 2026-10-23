"""Validation of the see-through rod method (rods.py) on synthetic shells with known answers.

Known answers:
 * coaxial round holes d1, d2 -> largest straight round rod = min(d1, d2), square = min/sqrt2;
 * a single oval a x b paired with a circle d > b -> round rod = b; square in ellipse
   = 2AB/sqrt(A^2+B^2) with semi-axes A,B (if the circle does not limit it);
 * analytic check of largest_square() and mic() on a circle and an ellipse polygon.
"""
import numpy as np
from shapely.geometry import Point
from rods import see_through, mic, largest_square, ellipse
from synth import build
from common import canonical_face_normals, R_IN


def main():
    # analytic polygon checks
    circ = Point(0, 0).buffer(10.0, quad_segs=512)
    d, _ = mic(circ); s, _ = largest_square(circ)
    print("circle d=20: mic %.3f (20), square %.3f (%.3f)" % (d, s, 20 / np.sqrt(2)))
    E = ellipse(26.0, 21.5)
    A, B = 13.0, 10.75
    d, _ = mic(E); s, _ = largest_square(E)
    print("ellipse 26x21.5: mic %.3f (21.5), square %.3f (%.3f)" % (d, s, 2 * A * B / np.sqrt(A * A + B * B)))
    # synthetic shells
    cn = canonical_face_normals()
    opp = [int(np.argmin(cn @ n)) for n in cn]
    holes = [20.0] * 12
    holes[1], holes[opp[1]] = 17.0, 12.0       # unequal coaxial pair
    holes[2], holes[opp[2]] = 15.0, 15.0
    ovals = {0: (26.0, 21.5)}
    holes[opp[0]] = 24.0                        # oval against a 24 mm circle
    m = build(holes=holes, ovals=ovals, max_edge=None, seg=256)
    T = m.vertices[m.faces]
    for f, truth_round, truth_sq in [(1, 12.0, 12.0 / np.sqrt(2)), (2, 15.0, 15.0 / np.sqrt(2)),
                                     (0, 21.5, None)]:
        u = cn[f]
        g = see_through(T, u)
        d, c = mic(g); s, _ = largest_square(g)
        if truth_sq is None:
            # square limited by the ellipse or by the 24 mm circle, whichever is smaller
            truth_sq = min(2 * A * B / np.sqrt(A * A + B * B), 24.0 / np.sqrt(2))
        print("synthetic pair face %d/%d: round rod %.3f (true %.2f), square %.3f (true %.3f)" % (
            f, opp[f], d, truth_round, s, truth_sq))


if __name__ == "__main__":
    main()
