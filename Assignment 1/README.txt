

## Part 1: 2D Isocontour Extraction
## enter isovalue within (-1438,630)

 for Windows:
    python contour_extract.py --isovalue <value>

for Linux/macOS:
    python3 contour_extract.py --isovalue <value>

Output: isocontour.vtp (open in ParaView)

---

## Part 2: 3D Volume Rendering

for Windows:
    python volume_render.py --phongshading <yes/no>

 for Linux/macOS:
    python3 volume_render.py <yes/no>

<yes> to enable Phong shading, <no> to disable it.
