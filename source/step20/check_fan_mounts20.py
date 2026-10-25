from pathlib import Path
import cadquery as cq,json
O=Path(__file__).parent
report=[];issues=[]
for i,fc in enumerate([252.,372.]):
 p=cq.importers.importStep(str(O/f'Duct20_PAIR_{"AB"[i]}_DUCT.step')).val()
 for zc in [79.05,199.05]:
  for sx in [-1,1]:
   for sz in [-1,1]:
    x=fc+sx*52.5;z=zc+sz*52.5
    # Hole axis +Y; socket head on GPU-facing side. Short hex key exits sideways.
    shaft=cq.Solid.makeCylinder(1.5,7,cq.Vector(x,473.5,z),cq.Vector(0,1,0))
    head=cq.Solid.makeCylinder(3.18,2.4,cq.Vector(x,471.1,z),cq.Vector(0,1,0))
    washer=cq.Solid.makeCylinder(3.5,.5,cq.Vector(x,473.5,z),cq.Vector(0,1,0)).cut(cq.Solid.makeCylinder(1.7,.5,cq.Vector(x,473.5,z),cq.Vector(0,1,0)))
    key=cq.Solid.makeCylinder(4,18,cq.Vector(x,455.5,z),cq.Vector(0,1,0)).fuse(cq.Solid.makeCylinder(2,15,cq.Vector(x,457.5,z),cq.Vector(sx,0,0)))
    v=p.intersect(shaft.fuse(head,washer,key)).Volume()
    seat=cq.Solid.makeCylinder(3.5,.2,cq.Vector(x,474.01,z),cq.Vector(0,1,0)).cut(cq.Solid.makeCylinder(1.71,.2,cq.Vector(x,474.01,z),cq.Vector(0,1,0)))
    missing=seat.cut(p).Volume()
    if v>.001 or missing>.001:issues.append([i,x,z,v,missing])
    report.append({'pair':'AB'[i],'center_xz':[x,z],'hardware_or_key_overlap_mm3':v,'missing_washer_seat_mm3':missing})
print('16 fan mount checks',issues);assert not issues
(O/'ducts20_fan_mount_checks.json').write_text(json.dumps({'hole_count':16,'hole_diameter_mm':3.4,'pattern_mm':105,'recess_radius_mm':5,'nut_washer_seat_y':474,'fan_face_y':480,'checks':report,'issues':issues},indent=2))
