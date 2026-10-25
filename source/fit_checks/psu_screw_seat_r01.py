"""Small #6-32 PSU screw-seat fit samples; these are not PSU mounting plates."""
from pathlib import Path
import json
import struct
import sys

import cadquery as cq
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def seat_sample(land_mm):
    """Keep a 5 mm wall, with a local recess on its outside/head side."""
    width, wall, through_diameter, recess_diameter = 30.0, 5.0, 4.0, 9.0
    if not 0 < land_mm <= wall:
        raise ValueError("Screw-bearing land must be between zero and wall thickness")
    solid = cq.Solid.makeBox(width, width, wall)
    solid = solid.cut(cq.Solid.makeCylinder(through_diameter / 2, wall,
                                          cq.Vector(width / 2, width / 2, 0)))
    if land_mm < wall:
        solid = solid.cut(cq.Solid.makeCylinder(recess_diameter / 2, wall - land_mm,
                                              cq.Vector(width / 2, width / 2, land_mm)))
    return solid.clean()


def inspect_mesh(path):
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + count * 50 or not count:
        raise ValueError(f"Invalid binary STL: {path}")
    dtype = np.dtype([("normal", "<f4", 3), ("v", "<f4", (3, 3)), ("attribute", "<u2")])
    vertices = np.frombuffer(data, dtype=dtype, count=count, offset=84)["v"].astype(float)
    _, indices = np.unique(np.round(vertices.reshape(-1, 3), 5), axis=0, return_inverse=True)
    faces = indices.reshape(-1, 3)
    edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    _, inverse, counts = np.unique(np.sort(edges, axis=1), axis=0,
                                   return_inverse=True, return_counts=True)
    winding = np.bincount(inverse, weights=np.where(edges[:, 0] < edges[:, 1], 1, -1))
    volume = float(np.einsum("ij,ij->i", vertices[:, 0],
                            np.cross(vertices[:, 1], vertices[:, 2])).sum() / 6)
    report = {"triangles": count, "closed": bool(np.all(counts == 2)),
              "consistent_winding": bool(np.all(winding == 0)),
              "positive_volume": volume > 0, "volume_mm3": volume,
              "on_bed": abs(float(vertices[:, :, 2].min())) < .001,
              "bounds_mm": (vertices.max((0, 1)) - vertices.min((0, 1))).tolist()}
    if not all(report[k] for k in ("closed", "consistent_winding", "positive_volume", "on_bed")):
        raise ValueError(f"Mesh integrity failed: {report}")
    return report


def build(output):
    output = Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Output must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    samples, reports = [], {}
    for index, land in enumerate((2.0, 5.0)):
        name = f"psu-seat-r01-{int(land)}mm"
        solid = seat_sample(land)
        if not solid.isValid() or len(solid.Solids()) != 1:
            raise ValueError(f"Invalid sample solid: {name}")
        cq.exporters.export(solid, str(output / f"{name}.step"))
        mesh_path = output / f"{name}.stl"
        cq.exporters.export(solid, str(mesh_path), tolerance=.025, angularTolerance=.08)
        mesh_report = inspect_mesh(mesh_path)
        if abs(mesh_report["volume_mm3"] / solid.Volume() - 1) > .001:
            raise ValueError(f"Mesh volume differs from solid: {name}")
        reports[name] = {"valid_single_solid": True, "land_mm": land,
                         "wall_mm": 5, "through_hole_mm": 4,
                         "head_recess_mm": 9 if land < 5 else None,
                         "solid_volume_mm3": solid.Volume(), "mesh": mesh_report}
        samples.append((solid.translate((index * 42, 0, 0)),
                        (.94, .66, .22) if land == 2 else (.53, .67, .77), 1))
    sys.path.insert(0, str(ROOT / "source/step20"))
    from software_render_views import render
    render(samples, output / "samples-cad.png", (-100, 100, 120), (36, 15, 2.5),
           35, size=(1000, 580))
    from PIL import Image, ImageDraw, ImageFont
    image = Image.open(output / "samples-cad.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 21)
    draw.text((22, 16), "PSU SCREW-SEAT SAMPLES / R01 / actual CAD", fill="#203747", font=font)
    draw.text((22, 508), "Gold: 2 mm recessed land. Blue: original 5 mm wall comparison.", fill="#203747", font=font)
    draw.text((22, 542), "30 x 30 x 5 mm each. Fit coupons only; physical fit remains unverified.", fill="#203747", font=font)
    image.save(output / "samples-cad.png")
    report = {"revision": "R01", "status": "fit_samples_not_mounting_hardware",
              "units": "mm", "physical_fit_verified": False,
              "source_issue": "https://github.com/PraxisOG/moe-chassis/issues/2",
              "note": "4 mm clearance hole and 9 mm recess are prototype choices. Confirm actual screw head, engagement and manufacturer penetration limit. These samples do not validate a load-bearing PSU mount.",
              "parts": reports}
    (output / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Created two checked fit samples in {output}")
