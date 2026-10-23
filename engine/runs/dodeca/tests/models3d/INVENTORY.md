# 3D models of Roman dodecahedra (2026-10-23)

Model files are NOT committed (licences vary); `files/` is git-ignored. Sizes verified against museum data by
`../sim_mount/geom_scan.py` (mean face-to-face distance of the 6 opposite face planes).

## Measured (files on disk)
| object | museum / inv. | maker, method | source | licence | mesh | scale check |
|---|---|---|---|---|---|---|
| Kleiner Feldberg fort (Taunus) | Römerkastell Saalburg, FMb 2103 | Fraunhofer IGD CultLab3D | GLB https://alm-hessen.de/wp-content/uploads/53_Dodekaeder_100K-1.glb (page https://alm-hessen.de/mediathek/dodekaeder/) | not stated on the page | 95,348 faces, metres, closed hollow shell (genus 11) | 50.4 mm face to face vs museum "Höhe 5,1 cm" |
| unknown findspot | Hunt Museum, Limerick, HCM 157 | Hunt Museum photogrammetry | Sketchfab uid ed2916a7d53d4b80bc22e75fbf526979 (downloaded by the user, login needed); zip sha256 7cb349ac458562c91a8160a822ad228d4e266eb968f39a5985411013bce3eb5d, OBJ sha256 125988d9f60f3d1d8c8a8888f5df26a70fc49d55ee34cf28c99bff49973917b5 | CC-BY | 300,042 faces, mm, median edge 0.31 mm, closed hollow shell (genus 11); converted to `files/hunt_HCM157/HCM157_geom.ply` | 48.9 mm vs museum height 4.9 cm |

## Real objects on Sketchfab, view-only (not downloaded; geometry not extracted from the viewer)
- Corbridge, English Heritage — 1003b9ad0b244c57992266a8b8d8421c (250k faces)
- Musée d'Archéologie nationale MAN 65869, Rmn-GP — 50ab8e9a51844cb7bc66e8ad9ed8282c (4.5M faces, height 7.5 cm)
- Musée départemental Arles antique X-37086 — ccd1506a04ba49d1b4f65ae1787a26c9 (H 5.33 cm)
- Cardiff Castle, GGAT photogrammetry — b73ef0b56f154c54950f5891dbe4fc5a
- Carnuntum, noe-3d.at — 7dc7de27bb264ddaa373774c01a53432 (one knob missing)
- origin unknown, downloadable with login: deniel777 6e65be6ee1924efca5c2a2f99d128cbc (CC-BY, 1.27M faces) — not checked

Artistic re-creations (Blender, Maya, AI) found by the same API search are excluded. The full search across other
museum portals was stopped unfinished; asking the five museums above for their scan files is the cheapest way to
triple the measured sample.
