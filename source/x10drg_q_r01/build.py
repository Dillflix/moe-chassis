"""Parametric layout envelopes and three concept ducts, deliberately without mount holes.

This is a collision/packaging study. Valid CAD is not physical fit, cooling, print
readiness, an electrical design, or a verified 3D model of the owned hardware.
"""
from pathlib import Path
import json
import math
import struct
import cadquery as cq
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

BLUE = (.42, .61, .73)
GOLD = (.92, .65, .23)
DARK = (.28, .35, .40)
GREEN = (.25, .53, .43)
PURPLE = (.61, .43, .71)
RED = (.78, .34, .30)


def box(x, y, z, dx, dy, dz):
    return cq.Solid.makeBox(dx, dy, dz, cq.Vector(x, y, z))


def bounds(shape):
    # Ignore cached triangulation: OCC's conservative default bounding box can
    # grow after tessellating a loft, even though its actual geometry is unchanged.
    b = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped, b, False, False)
    x0, y0, z0, x1, y1, z1 = b.Get()
    return {k: round(v, 5) for k, v in zip(
        ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax", "xlen", "ylen", "zlen"),
        (x0, x1, y0, y1, z0, z1, x1-x0, y1-y0, z1-z0))}


def overlap(a, b):
    aa, bb = a.BoundingBox(), b.BoundingBox()
    if any(min(getattr(aa, k + "max"), getattr(bb, k + "max")) -
           max(getattr(aa, k + "min"), getattr(bb, k + "min")) <= 1e-6 for k in "xyz"):
        return 0.0
    return a.intersect(b).Volume()


def section(y, x0, x1, z0, z1):
    return cq.Wire.makePolygon([cq.Vector(x, y, z) for x, z in
                               ((x0, z0), (x1, z0), (x1, z1), (x0, z1), (x0, z0))])


def duct_shell(sections, wall):
    outer = cq.Solid.makeLoft([section(*s) for s in sections], ruled=True)
    inner = cq.Solid.makeLoft([section(y, x0 + wall, x1 - wall, z0 + wall, z1 - wall)
                              for y, x0, x1, z0, z1 in sections], ruled=True)
    return outer.cut(inner).clean()


def fan_frame(x, y, z, size, depth):
    return box(x - size / 2, y, z - size / 2, size, depth, size).cut(
        cq.Solid.makeCylinder(size / 2 - 2.5, depth, cq.Vector(x, y, z), cq.Vector(0, 1, 0)))


def validate_config(c):
    if c["units"] != "mm" or c["production_ready"] is not False:
        raise ValueError("R01 must remain an explicitly non-production millimetre layout")
    if c["board"]["mounting_holes"] is not None or c["psus"]["screw_holes"] is not None:
        raise ValueError("R01 has no verified hole datums; use a reviewed later revision for mounting holes")
    if c["gpus"]["slots"] != [8, 6, 4, 2] or c["gpus"]["cpu_owners"] != [2, 2, 1, 1]:
        raise ValueError("Unexpected X10DRG-Q GPU topology")
    if c["gpus"]["cooling"] != ["passive", "passive", "passive", "blower"]:
        raise ValueError("R01 reserves the outermost slot 2 for the blower card")
    if c["gpus"]["nvlink"]["pairs"] != [[8, 6], [4, 2]]:
        raise ValueError("Each NVLink pair must stay on one CPU")
    if not math.isclose(c["gpus"]["card_pitch"], 2 * c["gpus"]["slot_pitch"], abs_tol=1e-6):
        raise ValueError("GPU pair spacing must be exactly two nominal slot pitches")
    if c["psus"]["count"] != 2 or len(c["psus"]["bottom_z"]) != 2:
        raise ValueError("This study reserves two PSUs")
    for key in ("width", "height", "wall", "floor"):
        if c["chassis"][key] <= 0:
            raise ValueError(f"Invalid chassis {key}")
    if c["psus"]["body_depth_x"] <= 0 or c["psus"]["cable_clearance_x"] < 0:
        raise ValueError("Invalid PSU depth or cable reservation")
    if c["ducts"]["wall"] <= 0 or not c["required_measurements"]:
        raise ValueError("Duct walls and measurement gates are required")
    if c["board"]["width"] < max(c["board"]["dimension_evidence"]["product_page_mm"][0],
                                  c["board"]["dimension_evidence"]["manual_alternate_width_mm"]):
        raise ValueError("Concept envelope must accommodate both published board widths")


def mesh_report(path):
    """Inspect the saved binary STL, including actual artifact bounds and bed contact."""
    data = Path(path).read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + count * 50 or not count:
        raise ValueError(f"Invalid binary STL: {path}")
    dtype = np.dtype([("normal", "<f4", 3), ("v", "<f4", (3, 3)), ("attribute", "<u2")])
    vertices = np.frombuffer(data, dtype=dtype, count=count, offset=84)["v"].astype(float)
    unique, indices = np.unique(np.round(vertices.reshape(-1, 3), 5), axis=0, return_inverse=True)
    faces = indices.reshape(-1, 3)
    edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    _, inverse, counts = np.unique(np.sort(edges, axis=1), axis=0,
                                   return_inverse=True, return_counts=True)
    winding = np.bincount(inverse, weights=np.where(edges[:, 0] < edges[:, 1], 1, -1))
    volume = float(np.einsum("ij,ij->i", vertices[:, 0],
                            np.cross(vertices[:, 1], vertices[:, 2])).sum() / 6)
    mins, maxs = vertices.min((0, 1)), vertices.max((0, 1))
    sizes = maxs-mins
    artifact_bounds = {k: round(float(v), 5) for k, v in zip(
        ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax", "xlen", "ylen", "zlen"),
        (mins[0], maxs[0], mins[1], maxs[1], mins[2], maxs[2], *sizes))}
    return {"source": "saved_binary_stl", "vertices": len(unique), "triangles": count,
            "watertight_edges": bool(np.all(counts == 2)),
            "consistent_winding": bool(np.all(winding == 0)),
            "positive_signed_volume": volume > 0, "on_bed": abs(float(mins[2])) < .001,
            "nonnegative_coordinates": bool(np.all(mins >= -.001)),
            "bounds_mm": artifact_bounds, "volume_mm3": round(volume, 3)}


def make_layout(c, depth):
    s, b, g, p, f, d = (c[k] for k in ("chassis", "board", "gpus", "psus", "fans", "ducts"))
    width, height, wall, floor = (s[k] for k in ("width", "height", "wall", "floor"))
    parts, colors, kinds = {}, {}, {}

    def add(name, shape, color, kind="hardware_envelope"):
        parts[name], colors[name], kinds[name] = shape, color, kind

    # A plain boundary shell, deliberately not the original printable quadrants.
    boundary = box(0, 0, 0, width, depth, floor)
    for shape in (box(0, 0, floor, wall, depth, height - floor),
                  box(width - wall, 0, floor, wall, depth, height - floor),
                  box(wall, 0, floor, width - 2 * wall, wall, height - floor),
                  box(wall, depth - wall, floor, width - 2 * wall, wall, height - floor)):
        boundary = boundary.fuse(shape)
    add("CHASSIS_BOUNDARY_REFERENCE_NO_JOINTS_OR_MOUNTS", boundary.clean(), BLUE, "boundary")
    pcb_z = floor + b["standoff_height"]
    pcb_top = pcb_z + b["thickness"]
    add("PCB_REFERENCE_NO_MOUNTING_HOLES", box(*b["origin_xy"], pcb_z, b["width"], b["depth"], b["thickness"]), GREEN)
    for i, (x, y) in enumerate(c["cpu_coolers"]["centers_xy"], 1):
        dx, dy, dz = c["cpu_coolers"]["envelope_xyz"]
        add(f"CPU{i}_COOLER_PROVISIONAL", box(x - dx / 2, y - dy / 2, pcb_top, dx, dy, dz), DARK)
    q = b["front_component_reservation"]
    add("PCH_FRONT_COMPONENT_PROVISIONAL", box(q["x"], q["y"], pcb_top, q["width"], q["depth"], q["height_above_pcb"]), PURPLE, "reservation")
    slot_planes = {}
    gpu_y_end = g["rear_y"] + g["body_length"]
    gpu_z_end = g["body_bottom_z"] + g["body_height"]
    for i, slot in enumerate(g["slots"]):
        x = g["first_slot_plane_x"] + i * g["card_pitch"]
        slot_planes[slot] = x
        add(f"GPU_SLOT{slot}_{g['cooling'][i].upper()}_PROVISIONAL",
            box(x - g["backplate_offset"], g["rear_y"], g["body_bottom_z"],
                g["body_width_reservation"], g["body_length"], g["body_height"]), GREEN if i < 3 else DARK)
    nv = g["nvlink"]
    for a, z in nv["pairs"]:
        x0, x1 = sorted((slot_planes[a], slot_planes[z]))
        add(f"NVLINK_{a}_{z}_UNMEASURED_RESERVATION",
            box(x0 - nv["extra_x"], nv["y_min"], gpu_z_end, x1 - x0 + 2 * nv["extra_x"],
                nv["y_max"] - nv["y_min"], nv["height_above_gpu"]), PURPLE, "reservation")
    air = g["blower_air_reservation"]
    air_x = slot_planes[2] - g["backplate_offset"] + g["body_width_reservation"]
    if air_x >= width - wall:
        raise ValueError("No side-intake reservation remains outside the blower GPU")
    add("BLOWER_SIDE_AIR_UNMEASURED_RESERVATION",
        box(air_x, air["y_min"], air["z_min"], width - wall - air_x,
            air["y_max"] - air["y_min"], air["z_max"] - air["z_min"]), PURPLE, "reservation")
    for i, z in enumerate(p["bottom_z"], 1):
        add(f"PSU{i}_BODY_PROVISIONAL", box(p["x"], p["y"], z, p["body_depth_x"], p["face_width_y"], p["height"]), DARK)
        if p["cable_clearance_x"]:
            add(f"PSU{i}_CABLE_RESERVATION", box(p["x"] + p["body_depth_x"], p["y"], z,
                p["cable_clearance_x"], p["face_width_y"], p["height"]), RED, "reservation")
    front_y = depth - f["front_rear_offset_from_depth"]
    fan_y = depth - f["duct_rear_offset_from_depth"]
    for x in f["front_centers_x"]:
        for z in f["centers_z"]:
            add(f"FRONT_FAN_{x}_{z}_FULL_KEEP_OUT", box(x-f["size"]/2, front_y, z-f["size"]/2, f["size"], f["thickness"], f["size"]), DARK, "fan_keepout")
    for x in f["duct_centers_x"]:
        for z in f["centers_z"]:
            add(f"DUCT_FAN_{x}_{z}_FULL_KEEP_OUT", box(x-f["size"]/2, fan_y, z-f["size"]/2, f["size"], f["thickness"], f["size"]), DARK, "fan_keepout")
    transition_y = fan_y - d["front_transition_length"]
    mouth_y = gpu_y_end + d["gpu_end_gap"]
    if not mouth_y < d["rise_end_y"] < transition_y < fan_y:
        raise ValueError("Duct sections must proceed monotonically toward the front fan bank")
    a, z = f["duct_centers_x"]
    # Two half-column passages serve slots 8/6; the complete second column serves
    # slot 4. The fourth GPU has no front duct and gets a side-air reservation.
    inlets = [(a - f["size"] / 2, a), (a, a + f["size"] / 2),
              (z - f["size"] / 2, z + f["size"] / 2)]
    for slot, (ix0, ix1) in zip(g["slots"][:3], inlets):
        x0 = slot_planes[slot] - g["backplate_offset"]
        x1 = x0 + g["body_width_reservation"]
        sections = [(mouth_y, x0, x1, d["outlet_bottom_z"], d["outlet_top_z"]),
                    (d["rise_end_y"], x0, x1, d["middle_bottom_z"], d["middle_top_z"]),
                    (transition_y, x0, x1, d["middle_bottom_z"], d["middle_top_z"]),
                    (fan_y, ix0, ix1, floor, floor + 2 * f["size"])]
        add(f"DUCT_SLOT{slot}_CONCEPT_NOT_FIT_VALIDATED", duct_shell(sections, d["wall"]), GOLD, "concept_duct")
    anchor_checks = [{"anchor_xy": [x, y], "covered_by_board":
        b["origin_xy"][0] <= x <= b["origin_xy"][0]+b["width"] and
        b["origin_xy"][1] <= y <= b["origin_xy"][1]+b["depth"]}
        for x, y in [(260, 350), (400, 350)]]
    return parts, colors, kinds, {"slot_planes_x": slot_planes, "pcb_bottom_z": pcb_z,
        "gpu_front_y": gpu_y_end, "duct_outlet_y": mouth_y, "duct_rise_end_y": d["rise_end_y"],
        "duct_transition_start_y": transition_y, "duct_fan_rear_y": fan_y,
        "duct_fan_intake_y": fan_y + f["thickness"], "front_fan_rear_y": front_y,
        "fan_bank_gap_y": front_y - fan_y - f["thickness"],
        "psu_front_y": p["y"] + p["face_width_y"],
        "pcb_front_y": b["origin_xy"][1] + b["depth"],
        "psu_to_pcb_gap_y": p["y"] - b["origin_xy"][1] - b["depth"],
        "baseline_y350_duct_anchor_checks": anchor_checks,
        "old_y350_duct_anchors_covered_by_board": all(a["covered_by_board"] for a in anchor_checks),
        "passive_duct_inlet_areas_mm2": {str(slot): (x1-x0)*2*f["size"]
            for slot, (x0, x1) in zip(g["slots"][:3], inlets)},
        "flow_distribution_status": "UNRESOLVED: inlet areas are 1:1:2. This routing study does not balance airflow; dedicated fans or a common plenum remain alternatives."}


def render_cad(items, path, width, depth, top=False):
    """Orthographic triangle z-buffer render derived entirely from BRep tessellation."""
    w, h = 1400, 1120
    image = np.full((h, w, 3), [246, 248, 250], dtype=np.uint8)
    zbuffer = np.full((h, w), -1e30, dtype=np.float64)
    view = np.array([0., 0., 1.]) if top else np.array([-1., 1., 1.2])
    view /= np.linalg.norm(view)
    right = np.array([1., 0., 0.]) if top else np.cross([0, 0, 1], view)
    right /= np.linalg.norm(right)
    up = np.cross(view, right)
    basis = np.array([right, up, view]).T
    focal = np.array([width / 2, depth / 2, 100.])
    scale = 1.30 if top else 1.23
    lines = []
    for shape, color in items:
        vv, tt = shape.tessellate(.2, .25)
        world = np.array([[v.x, v.y, v.z] for v in vv])
        pp = (world - focal) @ basis
        pp[:, 0] = pp[:, 0] * scale + w / 2
        pp[:, 1] = h / 2 - pp[:, 1] * scale
        for tri in tt:
            q = pp[list(tri)]
            a, b, c = q
            xmin, xmax = max(0, math.floor(q[:, 0].min())), min(w - 1, math.ceil(q[:, 0].max()))
            ymin, ymax = max(0, math.floor(q[:, 1].min())), min(h - 1, math.ceil(q[:, 1].max()))
            if xmin > xmax or ymin > ymax:
                continue
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(den) < 1e-9:
                continue
            xx, yy = np.arange(xmin, xmax + 1)[None, :] + .5, np.arange(ymin, ymax + 1)[:, None] + .5
            v0 = ((b[1] - c[1]) * (xx - c[0]) + (c[0] - b[0]) * (yy - c[1])) / den
            v1 = ((c[1] - a[1]) * (xx - c[0]) + (a[0] - c[0]) * (yy - c[1])) / den
            v2 = 1 - v0 - v1
            zz = v0 * a[2] + v1 * b[2] + v2 * c[2]
            region = zbuffer[ymin:ymax + 1, xmin:xmax + 1]
            mask = (v0 >= -1e-8) & (v1 >= -1e-8) & (v2 >= -1e-8) & (zz >= region - 1e-6)
            normal = np.cross(world[tri[1]] - world[tri[0]], world[tri[2]] - world[tri[0]])
            nlen = np.linalg.norm(normal)
            shade = .75 + .25 * abs(float(np.dot(normal / nlen, np.array([.2, -.4, 1.]) / np.linalg.norm([.2, -.4, 1.])))) if nlen else 1
            region[mask] = zz[mask]
            image[ymin:ymax + 1, xmin:xmax + 1][mask] = np.clip(np.array(color) * 255 * shade, 0, 255).astype(np.uint8)
        for edge in shape.Edges():
            points, _ = edge.sample(24 if edge.geomType() != "LINE" else 2)
            lines.append(np.array([[v.x, v.y, v.z] for v in points]))
    for line in lines:
        p = (line - focal) @ basis
        p[:, 0] = p[:, 0] * scale + w / 2
        p[:, 1] = h / 2 - p[:, 1] * scale
        for a, b in zip(p[:-1], p[1:]):
            q = np.linspace(a, b, max(2, int(np.linalg.norm(b[:2] - a[:2]) * 1.5)))
            x, y = np.round(q[:, 0]).astype(int), np.round(q[:, 1]).astype(int)
            valid = (x >= 0) & (x < w) & (y >= 0) & (y < h)
            x, y, z = x[valid], y[valid], q[valid, 2]
            mask = z >= zbuffer[y, x] - .5
            image[y[mask], x[mask]] = [55, 72, 85]
    im = Image.fromarray(image)
    draw = ImageDraw.Draw(im)
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    title = ImageFont.truetype(font, 26)
    small = ImageFont.truetype(font, 19)
    draw.text((30, 20), f"X10DRG-Q R01 | {'TOP' if top else 'CUTAWAY'} | {depth:.1f} mm depth", fill="#173449", font=title)
    draw.text((30, 60), "CONCEPT ONLY | provisional hardware envelopes | no mounting holes | no fit/thermal certification", fill="#a03d32", font=small)
    draw.text((30, 1030), "Gold: three new passive ducts   Green: PCB/passive GPUs   Dark: fans/PSUs/coolers/blower", fill="#173449", font=small)
    draw.text((30, 1063), "Red: PSU cable reservations   Purple: unmeasured NVLink / component / blower-air reservations", fill="#173449", font=small)
    draw.text((30, 1090), "Fan frames shown cut away for clarity; full rectangular fan volumes are collision checked.", fill="#173449", font=ImageFont.truetype(font, 16))
    im.save(path)


def build_variant(c, label, depth, out):
    out.mkdir(parents=True)
    (out / "renders").mkdir()
    (out / "concept-only").mkdir()
    parts, colors, kinds, datums = make_layout(c, depth)
    invalid = [n for n, p in parts.items() if not p.isValid() or len(p.Solids()) != 1 or p.Volume() <= 0]
    collisions = []
    hardware = [(n, p) for n, p in parts.items() if kinds[n] != "boundary"]
    for i, (name, shape) in enumerate(hardware):
        for other, target in hardware[i + 1:]:
            volume = overlap(shape, target)
            if volume > .01:
                collisions.append({"a": name, "b": other, "volume_mm3": round(volume, 3)})
    s = c["chassis"]
    outside = []
    for name, p in hardware:
        b = p.BoundingBox()
        if (b.xmin < s["wall"] - .001 or b.xmax > s["width"] - s["wall"] + .001 or
            b.ymin < s["wall"] - .001 or b.ymax > depth - s["wall"] + .001 or
            b.zmin < s["floor"] - .001 or b.zmax > s["height"] + .001):
            outside.append(name)
    assembly = cq.Assembly(name=f"{c['revision']}_{label}")
    for name, p in parts.items():
        assembly.add(p, name=name, color=cq.Color(*colors[name]))
    assembly.save(str(out / "layout.step"))
    prints = []
    for name, p in parts.items():
        if kinds[name] != "concept_duct":
            continue
        q = p.rotate((0, 0, 0), (1, 0, 0), -90)
        b = bounds(q)
        q = q.translate((-b["xmin"], -b["ymin"], -b["zmin"]))
        filename = name + ".stl"
        mesh_path = out / "concept-only" / filename
        cq.exporters.export(q, str(mesh_path), tolerance=.06, angularTolerance=.12)
        mesh = mesh_report(mesh_path)
        measures = mesh["bounds_mm"]
        fits = all(measures[k] <= limit + .001 for k, limit in zip(("xlen", "ylen", "zlen"), c["printer"]["bed_xyz"]))
        prints.append({"file": f"concept-only/{filename}", "bounds_mm": measures,
            "fits_provisional_printer": fits, "requires_segmentation_or_larger_printer": not fits,
            "mesh": mesh, "production_ready": False})
    (out / "concept-only/README.txt").write_text(
        "CONCEPT GEOMETRY ONLY. These are packaging-study shells, not fitted RTX 8000 ducts.\n"
        "No fan screws, measured GPU interfaces or support mounts are included.\n"
        "No print-overhang/strength/thermal validation has been performed.\n"
        "Check checks.json for printer-envelope failures before using these files.\n")
    mesh_ok = all(all(x["mesh"][k] for k in ("watertight_edges", "consistent_winding", "positive_signed_volume", "on_bed", "nonnegative_coordinates")) for x in prints)
    checks = {"revision": c["revision"], "variant": label, "production_ready": False,
        "modeled_geometry_pass": not invalid and not outside and not collisions and mesh_ok,
        "invalid_solids": invalid, "outside_chassis": outside, "collisions": collisions,
        "concept_print_checks": prints, "physical_measurement_status": "BLOCKED: unmeasured interfaces",
        "thermal_status": "NOT TESTED", "print_overhang_status": "NOT CHECKED",
        "structural_status": "NOT TESTED; enclosure shell is an envelope, not a printable supported chassis",
        "rack_mount_status": "No ears/rails; shelf/support design outstanding",
        "fan_collision_model": "Full rectangular fan volumes, including rotor space, not only hollow frames",
        "flow_distribution_status": datums["flow_distribution_status"],
        "required_measurements": c["required_measurements"]}
    dimensions = {"units": "mm", "width": s["width"], "depth": depth,
        "body_height": s["height"], "height_with_lid_allowance": s["height"] + s["lid_allowance"],
        "datums": datums, "part_bounds": {n: bounds(p) for n, p in parts.items()},
        "board_mounting_holes": None, "configuration": c}
    (out / "checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    (out / "dimensions.json").write_text(json.dumps(dimensions, indent=2) + "\n")
    # Render a geometrically cut-down boundary for visibility; the exported STEP
    # retains the full plain shell and is still explicitly an envelope reference.
    cut = box(-1, -1, 0, s["width"] + 2, depth + 2, 30)
    render_items = [(parts[next(iter(parts))].intersect(cut), BLUE)]
    for n, p in hardware:
        if kinds[n] == "fan_keepout":
            b = p.BoundingBox()
            p = fan_frame((b.xmin+b.xmax)/2, b.ymin, (b.zmin+b.zmax)/2, b.xlen, b.ylen)
        render_items.append((p, colors[n]))
    render_cad(render_items, out / "renders/overview.png", s["width"], depth)
    render_cad(render_items, out / "renders/top.png", s["width"], depth, top=True)
    return {"depth_mm": depth, "modeled_geometry_pass": checks["modeled_geometry_pass"],
            "collision_count": len(collisions), "outside_count": len(outside),
            "concept_meshes_pass": mesh_ok, "all_concept_parts_fit_provisional_printer": all(x["fits_provisional_printer"] for x in prints),
            "production_ready": False, "files": f"{label}/"}


def build(config_path, output):
    config_path, output = Path(config_path).resolve(), Path(output).resolve()
    c = json.loads(config_path.read_text())
    validate_config(c)
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Refusing to overwrite a nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    (output / "config-used.json").write_text(json.dumps(c, indent=2) + "\n")
    variants = {}
    for name, depth in c["chassis"]["variants"].items():
        print(f"Building {name}: {depth} mm", flush=True)
        variants[name] = build_variant(c, name, depth, output / name)
        print(json.dumps({name: variants[name]}), flush=True)
    comparison = {"revision": c["revision"], "variants": variants, "production_ready": False,
        "interpretation": "A modeled clearance pass applies only to these provisional envelopes. It does not validate owned hardware, mounting, airflow, structural capacity or printability."}
    (output / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
    print(f"Layout study written to {output}", flush=True)
