# Quick checks for the exam answers (regular dodecahedron geometry).
import math
k_in = math.sqrt(250 + 110*math.sqrt(5))/20   # inradius / edge
k_face = 0.25*math.sqrt(5*(5+2*math.sqrt(5)))  # face area / edge^2
for d in (40, 45, 60, 80, 100):                # face-to-face height without knobs, mm
    a = d/(2*k_in); A = k_face*a*a
    # inscribed circle of the pentagon face (max hole) radius
    r_face = a/(2*math.tan(math.pi/5))
    print(f"d={d} mm edge={a:.1f} face={A:.0f} mm2 max hole dia={2*r_face:.1f} mm")
# Kleiner Feldberg-like: d~45, typical ringed holes 11-22 mm, unringed ~22 mm
a = 45/(2*k_in); A = k_face*a*a
for holes in ([11,13,14,15,16,17,18,19,21,22,22,22],):
    removed = sum(math.pi*(h/2)**2 for h in holes)
    print("fraction of face area removed by 12 holes:", round(removed/(12*A),2))
# Gellep: bone object 30 mm diameter vs production holes 23-24 mm
print("Gellep bone/hole ratio:", round(30/23.5,2), "-> bone cannot pass through; needs a tenon or ends at the hole")
