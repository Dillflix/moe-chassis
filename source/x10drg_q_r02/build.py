"""Three separately ducted fans and segmented, clamped fit prototypes.

Unmeasured hardware envelopes are inherited by reference from R01, never edited.
This does not generate a complete enclosure or final GPU/fan mounting interfaces.
"""
from pathlib import Path
import json
import math
import sys
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont
from x10drg_q_r01.build import (box, bounds, overlap, section, duct_shell, fan_frame,
    mesh_report, render_cad, make_layout as base_layout, validate_config as base_validate,
    BLUE, GOLD, DARK, GREEN, PURPLE, RED)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "source/step20"))
from software_render_views import render as render_detail


def validate_config(c):
    base_validate(c)
    r = c["r02"]
    def finite_tree(value):
        if isinstance(value,dict):return all(finite_tree(v) for v in value.values())
        if isinstance(value,list):return all(finite_tree(v) for v in value)
        return not isinstance(value,(float,int)) or isinstance(value,bool) or math.isfinite(value)
    if not finite_tree(c):raise ValueError("All numeric configuration values must be finite")
    if c["printer"]["model"] != "Bambu Lab P1S" or c["board"]["mounting_holes"] is not None:
        raise ValueError("R02 is the P1S prototype with unmeasured board mounts")
    for k in ("spigot_wall", "spigot_length", "spigot_entry_taper", "radial_clearance", "collar_clearance", "collar_wall",
              "collar_length", "collar_split_gap", "ear_thickness", "bolt_clearance_diameter", "bolt_length"):
        if r[k] <= 0:
            raise ValueError(f"Invalid positive R02 dimension: {k}")
    if min(r["route_middle_width"],r["route_middle_height"]) - 2*(c["ducts"]["wall"] + r["radial_clearance"] + r["spigot_wall"]) <= 0:
        raise ValueError("Spigot has no remaining airway")
    if r["spigot_length"] >= r["collar_length"]/2:
        raise ValueError("Collar must extend beyond the spigot")
    if sorted(r["fan_routes"]) != ["4", "6", "8"]:
        raise ValueError("Exactly one dedicated fan per passive GPU is required")
    if any(len(r[k])!=3 for k in ("route_middle_centers_x","route_middle_bottom_z")):
        raise ValueError("All three passive routes need middle-section datums")
    if any(v<=0 for v in c["printer"]["bed_xyz"]) or c["printer"]["brim_mm"]<0:
        raise ValueError("Printer envelope must be positive and brim nonnegative")
    if r["bolt_length"]<2*r["ear_thickness"]+r["collar_split_gap"]+3+1:
        raise ValueError("Clamp bolt needs bearing stack,3mm nut and1mm minimum protrusion")
    if not 3<r["bolt_clearance_diameter"]<5.5:
        raise ValueError("M3 clearance hole must clear3mm shaft and retain5.5mm head")


def variable_shell(outer, inner):
    return cq.Solid.makeLoft([section(*s) for s in outer], ruled=True).cut(
        cq.Solid.makeLoft([section(*s) for s in inner], ruled=True)).clean()


def inset(s, amount):
    y,x0,x1,z0,z1=s
    return (y,x0+amount,x1-amount,z0+amount,z1-amount)


def collar_parts(cx, z0, r):
    """Split friction collar; two M3 bolts, no fictitious positive axial capture."""
    width,height=r["route_middle_width"],r["route_middle_height"]
    y=r["joint_y"]-r["collar_length"]/2
    gap,wall=r["collar_clearance"],r["collar_wall"]
    x0,x1=cx-width/2-gap,cx+width/2+gap
    low,high=z0-gap,z0+height+gap
    ring=box(x0-wall,y,low-wall,width+2*(gap+wall),r["collar_length"],height+2*(gap+wall)).cut(
        box(x0,y-1,low,x1-x0,r["collar_length"]+2,high-low))
    mid=z0+height/2
    halves={}
    holes=[cx-width/2-gap-wall-5,cx+width/2+gap+wall+5]
    for tag,sgn in (("LOWER",-1),("UPPER",1)):
        za,zb=(low-wall,mid-r["collar_split_gap"]/2) if sgn<0 else (mid+r["collar_split_gap"]/2,high+wall)
        shape=ring.intersect(box(x0-wall-20,y-1,za,width+2*(gap+wall)+40,r["collar_length"]+2,zb-za))
        ez=mid-r["collar_split_gap"]/2-r["ear_thickness"] if sgn<0 else mid+r["collar_split_gap"]/2
        for hx in holes:
            # Ear overlaps the side-wall shell by .5 mm, ensuring one valid solid.
            ear=box(hx-5.5,r["joint_y"]-6,ez,11,12,r["ear_thickness"])
            hole=cq.Solid.makeCylinder(r["bolt_clearance_diameter"]/2,r["ear_thickness"]+2,
                                      cq.Vector(hx,r["joint_y"],ez-1))
            shape=shape.fuse(ear).cut(hole)
        halves[tag]=shape.clean()
    fasteners={}
    top=mid+r["collar_split_gap"]/2+r["ear_thickness"]
    bottom=mid-r["collar_split_gap"]/2-r["ear_thickness"]
    for i,hx in enumerate(holes,1):
        bolt=cq.Solid.makeCylinder(1.5,r["bolt_length"],cq.Vector(hx,r["joint_y"],top-r["bolt_length"]))
        bolt=bolt.fuse(cq.Solid.makeCylinder(2.75,3,cq.Vector(hx,r["joint_y"],top))).clean()
        nut=cq.Solid.makeCylinder(3.2,3,cq.Vector(hx,r["joint_y"],bottom-3)).cut(
            cq.Solid.makeCylinder(1.7,3,cq.Vector(hx,r["joint_y"],bottom-3)))
        fasteners[f"BOLT{i}_M3X{r['bolt_length']}_ENVELOPE"]=bolt
        fasteners[f"NUT{i}_M3_ENVELOPE"]=nut
    return halves,fasteners,{"radial_clearance_mm":gap,"split_gap_mm":r["collar_split_gap"],
        "bolts":f"2 x M3x{r['bolt_length']} provisional; actual head/nut dimensions and engagement require fit check",
        "bearing_stack_mm":2*r["ear_thickness"]+r["collar_split_gap"],
        "retention":"FRICTION ONLY; axial pull test required; not a structural support"}


def make_layout(c, depth):
    parts,colors,kinds,datums=base_layout(c,depth)
    for n in list(parts):
        if n.startswith("DUCT_FAN_") or kinds[n]=="concept_duct":
            del parts[n],colors[n],kinds[n]
    r,g,d,f=c["r02"],c["gpus"],c["ducts"],c["fans"]
    fan_y=depth-f["duct_rear_offset_from_depth"]
    transition=fan_y-d["front_transition_length"]
    mouth=g["rear_y"]+g["body_length"]+d["gpu_end_gap"]
    if not mouth<r["clearance_y"]<r["middle_start_y"]<r["joint_y"]-r["spigot_entry_taper"]<r["joint_y"]+r["spigot_length"]<transition:
        raise ValueError("Route and joint sections must remain ordered along +Y")
    joints={}
    def add(n,p,color=GOLD,kind="prototype"):
        parts[n],colors[n],kinds[n]=p,color,kind
    for i,slot in enumerate(g["slots"][:3]):
        cx=r["route_middle_centers_x"][i];z0=r["route_middle_bottom_z"][i]
        hw=r["route_middle_width"]/2;z1=z0+r["route_middle_height"]
        plane=g["first_slot_plane_x"]+i*g["card_pitch"]
        x0=plane-g["backplate_offset"]+r["mouth_side_inset"]
        x1=plane-g["backplate_offset"]+g["body_width_reservation"]-r["mouth_side_inset"]
        mid=(r["middle_start_y"],cx-hw,cx+hw,z0,z1)
        # Rise above the provisional PCH before changing lateral position.
        clear=(r["clearance_y"],x0,x1,r["clearance_bottom_z"],r["clearance_top_z"])
        outer=[(mouth,x0,x1,d["outlet_bottom_z"],d["outlet_top_z"]),clear,mid,
               (r["joint_y"]-r["spigot_entry_taper"],cx-hw,cx+hw,z0,z1)]
        inner=[inset(s,d["wall"]) for s in outer]
        reduction=d["wall"]+r["radial_clearance"]
        for y in (r["joint_y"],r["joint_y"]+r["spigot_length"]):
            s=(y,cx-hw+reduction,cx+hw-reduction,z0+reduction,z1-reduction)
            outer.append(s);inner.append(inset(s,r["spigot_wall"]))
        upstream=variable_shell(outer,inner)
        fx,fz=r["fan_routes"][str(slot)];half=f["size"]/2
        downstream=duct_shell([(r["joint_y"],cx-hw,cx+hw,z0,z1),
            (transition,cx-hw,cx+hw,z0,z1),(fan_y,fx-half,fx+half,fz-half,fz+half)],d["wall"])
        add(f"SLOT{slot}_GPU_HALF_PROTOTYPE",upstream)
        add(f"SLOT{slot}_FAN_HALF_PROTOTYPE",downstream)
        clamps,fasteners,report=collar_parts(cx,z0,r)
        for tag,p in clamps.items():add(f"SLOT{slot}_COLLAR_{tag}_PROTOTYPE",p)
        for tag,p in fasteners.items():add(f"SLOT{slot}_{tag}",p,DARK,"fastener_envelope")
        add(f"DEDICATED_FAN_SLOT{slot}_FULL_KEEP_OUT",box(fx-half,fan_y,fz-half,f["size"],f["thickness"],f["size"]),DARK,"fan_keepout")
        report.update({"spigot_length_mm":r["spigot_length"],"spigot_wall_mm":r["spigot_wall"],
            "spigot_radial_clearance_mm":r["radial_clearance"],
            "male_female_intersection_mm3":round(overlap(upstream,downstream),6),
            "male_outer_wh_mm":[r["route_middle_width"]-2*reduction,r["route_middle_height"]-2*reduction],
            "receiver_inner_wh_mm":[r["route_middle_width"]-2*d["wall"],r["route_middle_height"]-2*d["wall"]]})
        male_airway=[r["route_middle_width"]-2*(reduction+r["spigot_wall"]),r["route_middle_height"]-2*(reduction+r["spigot_wall"])]
        receiver_airway=report["receiver_inner_wh_mm"]
        report.update({"spigot_y_section_airway_wh_mm":male_airway,
            "spigot_y_section_airway_area_mm2":male_airway[0]*male_airway[1],
            "middle_y_section_airway_area_mm2":receiver_airway[0]*receiver_airway[1],
            "joint_area_reduction_fraction":1-(male_airway[0]*male_airway[1])/(receiver_airway[0]*receiver_airway[1]),
            "nominal_fan_face_area_mm2":f["size"]**2,
            "duct_fan_opening_area_mm2":(f["size"]-2*d["wall"])**2,
            "area_scope":"Areas are sections perpendicular to chassis Y, not a proven minimum flow-normal airway. Inclined passages, bends, contractions and real heatsinks require pressure/flow testing.",
            "route_rise_angle_degrees":math.degrees(math.atan2(abs(z0-r["clearance_bottom_z"]),r["middle_start_y"]-r["clearance_y"])),
            "airflow_direction":"Front fan -> FAN_HALF -> joint -> GPU_HALF -> GPU; pressure loss is untested"})
        joints[str(slot)]=report
    datums.update({"r02_joint_y":r["joint_y"],"dedicated_fan_count":3,
        "passive_duct_inlet_areas_mm2":{str(s):f["size"]**2 for s in g["slots"][:3]},
        "flow_distribution_status":"One equal-area fan face per passive GPU. Paths, bends and actual heatsinks differ: equal airflow is NOT established.",
        "joints":joints})
    return parts,colors,kinds,datums


def collision_report(parts,kinds):
    hardware=[(n,p) for n,p in parts.items() if kinds[n]!="boundary"]
    collisions=[]
    for i,(n,p) in enumerate(hardware):
        for m,q in hardware[i+1:]:
            v=overlap(p,q)
            if v>.01:collisions.append({"a":n,"b":m,"volume_mm3":round(v,4)})
    return collisions


def placement_report(size,printer):
    # Center actual body; the 5mm reservation is a conservative rectangular brim.
    dx,dy,dz=(size[k] for k in ("xlen","ylen","zlen"))
    brim=printer["brim_mm"];bed=printer["nominal_machine_xyz"]
    rect=[(bed[0]-dx)/2-brim,(bed[1]-dy)/2-brim,(bed[0]+dx)/2+brim,(bed[1]+dy)/2+brim]
    ex=printer["cutter_exclusion_xy"]
    intersects=rect[0]<ex[2] and rect[2]>ex[0] and rect[1]<ex[3] and rect[3]>ex[1]
    cap=all(v<=lim+.001 for v,lim in zip((dx,dy,dz),printer["bed_xyz"]))
    contained=rect[0]>=0 and rect[1]>=0 and rect[2]<=bed[0] and rect[3]<=bed[1] and dz<=printer["profile_print_height"]
    return {"fits_conservative_body_cap":cap,"body_cap_mm":printer["bed_xyz"],"brim_reserved_mm":brim,
        "plate_body_translation_xy_mm":[(bed[0]-dx)/2,(bed[1]-dy)/2],
        "body_plus_brim_rectangle_xy_mm":rect,"intersects_cutter_exclusion":intersects,
        "within_profile_volume":contained,"placement_pass":cap and contained and not intersects,
        "scope":"Bounding-envelope placement only; final slicer supports, toolpaths and purge/calibration zones remain unchecked"}


def title_image(path,title,subtitle):
    im=Image.open(path);draw=ImageDraw.Draw(im)
    font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    draw.rectangle((0,0,im.width,105),fill=(246,248,250))
    draw.text((24,18),title,font=ImageFont.truetype(font,23),fill="#173449")
    draw.text((24,57),subtitle,font=ImageFont.truetype(font,16),fill="#a03d32")
    im.save(path)


def export_prototype(p,n,out,printer):
    cq.exporters.export(p,str(out/"parts"/(n+".step")))
    q=p.rotate((0,0,0),(1,0,0),-90);b=bounds(q);q=q.translate((-b["xmin"],-b["ymin"],-b["zmin"]))
    mesh_path=out/"stl-fit-prototypes"/(n+".stl")
    cq.exporters.export(q,str(mesh_path),tolerance=.06,angularTolerance=.12)
    mesh=mesh_report(mesh_path);size=mesh["bounds_mm"]
    center=[(size[a+"min"]+size[a+"max"])/2 for a in "xyz"]
    render_detail([(q,GOLD,1)],out/"renders/parts"/(n+".png"),(-100,100,120),center,max(size[k] for k in ("xlen","ylen","zlen"))*.8,size=(900,700))
    title_image(out/"renders/parts"/(n+".png"),n,"R02 actual CAD | fit prototype | slicing/supports and physical fit unverified")
    return {"name":n,"step":"parts/"+n+".step","stl":"stl-fit-prototypes/"+n+".stl",
        "mesh":mesh,"placement":placement_report(size,printer),"physical_fit_verified":False}


def make_joint_coupon(c):
    """Crop the exact slot6 production-study joint; no independently redrawn mating shapes."""
    parts,colors,kinds,datums=make_layout(c,max(c["chassis"]["variants"].values()))
    selected={};selected_kinds={};r=c["r02"]
    for n,p in parts.items():
        if not n.startswith("SLOT6_"):continue
        name=n.replace("SLOT6_","COUPON_")
        if "GPU_HALF" in n:
            p=p.intersect(box(-1000,r["joint_y"]-20,-1000,2000,20+r["spigot_length"],2000)).clean()
        elif "FAN_HALF" in n:
            p=p.intersect(box(-1000,r["joint_y"],-1000,2000,25,2000)).clean()
        selected[name]=p;selected_kinds[name]=kinds[n]
    return selected,selected_kinds,datums["joints"]["6"]


def build_coupon(c,out):
    out.mkdir(parents=True);(out/"parts").mkdir();(out/"stl-fit-prototypes").mkdir();(out/"renders/parts").mkdir(parents=True)
    parts,kinds,joint=make_joint_coupon(c)
    invalid=[n for n,p in parts.items() if not p.isValid() or len(p.Solids())!=1 or p.Volume()<=0]
    collisions=collision_report(parts,kinds)
    assembly=cq.Assembly(name="R02_IDENTICAL_JOINT_FIT_COUPON")
    prints=[]
    for n,p in parts.items():
        assembly.add(p,name=n,color=cq.Color(*(GOLD if kinds[n]=="prototype" else DARK)))
        if kinds[n]=="prototype":prints.append(export_prototype(p,n,out,c["printer"]))
    assembly.save(str(out/"layout.step"))
    r=c["r02"];center=[r["route_middle_centers_x"][1],r["joint_y"],r["route_middle_bottom_z"][1]+r["route_middle_height"]/2]
    render_detail([(p,GOLD if kinds[n]=="prototype" else DARK,1) for n,p in parts.items()],out/"renders/overview.png",(-100,100,120),center,85,size=(1000,760))
    title_image(out/"renders/overview.png","R02 JOINT COUPON | exact cropped interfaces",f"Print these four small parts first | {r['radial_clearance']}mm radial fit | M3x{r['bolt_length']} clamp | friction retention only")
    report={"revision":c["revision"],"type":"joint_fit_coupon","production_ready":False,
        "invalid_solids":invalid,"collisions":collisions,"joint":joint,"print_prototypes":prints,
        "all_meshes_pass":all(all(x["mesh"][k] for k in ("watertight_edges","consistent_winding","positive_signed_volume","on_bed","nonnegative_coordinates")) for x in prints),
        "all_placement_envelopes_pass":all(x["placement"]["placement_pass"] for x in prints),
        "physical_fit_verified":False,"acceptance":"Check slide fit, closure before ear contact, M3 head/nut access, cracking, axial pull retention and seal leakage. This does not validate full ducts or GPU fit."}
    (out/"checks.json").write_text(json.dumps(report,indent=2)+"\n")
    (out/"dimensions.json").write_text(json.dumps({"units":"mm","part_bounds":{n:bounds(p) for n,p in parts.items()},"joint":joint},indent=2)+"\n")
    return {"prototype_count":len(prints),"collision_count":len(collisions),"all_meshes_pass":report["all_meshes_pass"],"all_placement_envelopes_pass":report["all_placement_envelopes_pass"]}


def psu_profiles(c,parts,kinds):
    results=[];p=c["psus"]
    for body in c["r02"]["psu_body_depth_profiles"]:
        for cable in c["r02"]["psu_cable_profiles"]:
            candidates={n:s for n,s in parts.items() if not n.startswith("PSU")}
            ck={n:kinds[n] for n in candidates}
            for i,z in enumerate(p["bottom_z"],1):
                for tag,x,dx in (("BODY",p["x"],body),("CABLE_RESERVATION",p["x"]+body,cable)):
                    n=f"PSU{i}_{tag}";candidates[n]=box(x,p["y"],z,dx,p["face_width_y"],p["height"]);ck[n]="reservation"
            collisions=[x for x in collision_report(candidates,ck) if x["a"].startswith("PSU") or x["b"].startswith("PSU")]
            results.append({"body_depth_mm":body,"cable_zone_mm":cable,"psu_collisions":collisions,"psu_clearance_pass":not collisions})
    return results


def build_variant(c,label,depth,out):
    out.mkdir(parents=True);(out/"parts").mkdir();(out/"stl-fit-prototypes").mkdir();(out/"renders/parts").mkdir(parents=True)
    parts,colors,kinds,datums=make_layout(c,depth)
    invalid=[n for n,p in parts.items() if not p.isValid() or len(p.Solids())!=1 or p.Volume()<=0]
    collisions=collision_report(parts,kinds)
    ch=c["chassis"];outside=[]
    for n,p in parts.items():
        if kinds[n]=="boundary":continue
        b=bounds(p)
        if b["xmin"]<ch["wall"]-.001 or b["xmax"]>ch["width"]-ch["wall"]+.001 or b["ymin"]<ch["wall"]-.001 or b["ymax"]>depth-ch["wall"]+.001 or b["zmin"]<ch["floor"]-.001 or b["zmax"]>ch["height"]+.001:outside.append(n)
    assembly=cq.Assembly(name=c["revision"]+"_"+label)
    for n,p in parts.items():assembly.add(p,name=n,color=cq.Color(*colors[n]))
    assembly.save(str(out/"layout.step"))
    print_reports=[]
    for n,p in parts.items():
        if kinds[n]!="prototype":continue
        print_reports.append(export_prototype(p,n,out,c["printer"]))
    cut=box(-1,-1,0,ch["width"]+2,depth+2,30)
    items=[]
    for n,p in parts.items():
        if kinds[n]=="boundary":p=p.intersect(cut)
        if kinds[n]=="fan_keepout":
            b=bounds(p);p=fan_frame((b["xmin"]+b["xmax"])/2,b["ymin"],(b["zmin"]+b["zmax"])/2,b["xlen"],b["ylen"])
        items.append((p,colors[n]))
    for name,top in (("overview",False),("top",True)):
        path=out/"renders"/(name+".png");render_cad(items,path,ch["width"],depth,top)
        title_image(path,f"X10DRG-Q R02 | {label.upper()} | {depth:.1f} mm | 3 dedicated fans","FIT PROTOTYPES | unmeasured hardware datums | equal fan area does not establish equal airflow")
    meshes_ok=all(all(p["mesh"][k] for k in ("watertight_edges","consistent_winding","positive_signed_volume","on_bed","nonnegative_coordinates")) for p in print_reports)
    check={"revision":c["revision"],"variant":label,"production_ready":False,
        "modeled_geometry_pass":not invalid and not collisions and not outside and meshes_ok,
        "invalid_solids":invalid,"collisions":collisions,"outside_chassis":outside,
        "fan_collision_model":"Full rectangular fan keepouts including rotor volume; cutaway frames shown only in renders",
        "print_prototypes":print_reports,"all_meshes_pass":meshes_ok,
        "all_placement_envelopes_pass":all(p["placement"]["placement_pass"] for p in print_reports),
        "joints":datums["joints"],"flow_distribution_status":datums["flow_distribution_status"],
        "psu_profiles":psu_profiles(c,parts,kinds),
        "physical_fit_status":"UNVERIFIED; motherboard not ordered, PSUs and fans not selected",
        "lid_clearance_status":"Checked to260.35mm body ceiling. R01's5mm lid allowance is additive above it; ribs, screws and other lid intrusions remain unmodeled.",
        "thermal_status":"NOT TESTED","structural_status":"NOT TESTED; clamps are friction joints, not chassis supports",
        "print_support_status":"NOT SLICED: spigot transitions, clamp ears and overhangs need slicer review",
        "required_measurements":c["required_measurements"]}
    dims={"units":"mm","depth":depth,"datums":datums,"part_bounds":{n:bounds(p) for n,p in parts.items()},"configuration":c}
    (out/"checks.json").write_text(json.dumps(check,indent=2)+"\n")
    (out/"dimensions.json").write_text(json.dumps(dims,indent=2)+"\n")
    return {"modeled_geometry_pass":check["modeled_geometry_pass"],"collision_count":len(collisions),"outside_count":len(outside),"prototype_count":len(print_reports),"all_meshes_pass":meshes_ok,"all_placement_envelopes_pass":check["all_placement_envelopes_pass"],"production_ready":False}


def build(config_path,output):
    c=json.loads(Path(config_path).read_text());validate_config(c);output=Path(output).resolve()
    if output.exists() and any(output.iterdir()):raise SystemExit(f"Refusing nonempty output directory: {output}")
    output.mkdir(parents=True,exist_ok=True)
    (output/"config-used.json").write_text(json.dumps(c,indent=2)+"\n")
    variants={}
    for label,depth in c["chassis"]["variants"].items():
        print(f"Building {label}: {depth} mm",flush=True)
        variants[label]=build_variant(c,label,depth,output/label);print(json.dumps({label:variants[label]}),flush=True)
    coupon=build_coupon(c,output/"joint-coupon")
    (output/"comparison.json").write_text(json.dumps({"revision":c["revision"],"variants":variants,"joint_coupon":coupon,"production_ready":False},indent=2)+"\n")
