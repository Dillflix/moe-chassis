"""Step22: low front retaining bar, existing chassis and duct prints unchanged.

As-built datum supplied by user: front/intake faces of duct fans are 10mm
behind the front floor-insert centerline. CAD +X is left, +Y is front, +Z up.
"""
from pathlib import Path
import cadquery as cq
import json, math, hashlib, struct
import numpy as np

ROOT=Path(__file__).parent
OUT=ROOT/'duct_bar22'; OUT.mkdir(exist_ok=True)
SRC=ROOT/'assembly_sources/project'
FLOOR=19.05
FAN_X=(252.,372.); FAN_Z=(79.05,199.05)
ANCHOR_X=(260.,400.); ANCHOR_Y=520.
FAN_FRONT=510.; FAN_THICK=25.
BAR_THICK=6.; BAR_HIGH=24.; RAIL_THICK=2.

def box(x,y,z,a,b,c):
    return cq.Solid.makeBox(a,b,c,cq.Vector(x,y,z))
def cyl(r,h,p,axis=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(*p),cq.Vector(*axis))
def overlap(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if any(getattr(aa,k+'max')<=getattr(bb,k+'min')+1e-7 or
           getattr(bb,k+'max')<=getattr(aa,k+'min')+1e-7 for k in 'xyz'):
        return 0.
    return a.intersect(b).Volume()

# Open-top 120mm scallops keep the tall obstruction out of both lower inlets.
# Retain a 2mm sole across the fan-frame bottom edge. This sole is below the
# nominal 115mm fan/duct airway, which starts 2.5mm above the floor.
bar=box(192,FAN_FRONT,FLOOR,240,BAR_THICK,BAR_HIGH)
scallops=[]
for x in FAN_X:
    c=cyl(60,8,(x,FAN_FRONT-1,FAN_Z[0]),(0,1,0))
    scallops.append(c)
    bar=bar.cut(c)
bar=bar.fuse(box(192,FAN_FRONT,FLOOR,240,BAR_THICK,RAIL_THICK))

# Two forward-facing feet. 4mm thickness retains the existing carrier's M3x8
# floor screw + 0.5mm washer stack. Rounded toes avoid snagging cables/hands.
for x in ANCHOR_X:
    foot=box(x-9,514,FLOOR,18,13,4)
    foot=foot.fuse(box(x-7,527,FLOOR,14,2,4),
                   cyl(2,4,(x-7,527,FLOOR)),cyl(2,4,(x+7,527,FLOOR)))
    bar=bar.fuse(foot)
    bar=bar.cut(cyl(1.7,6,(x,ANCHOR_Y,FLOOR-1)))

# Four lower fan-corner holes: M3 on the existing 105mm square pattern.
# 45deg diamond clearance preserves a >=3.4mm inscribed opening and removes
# the small horizontal-hole roofs for underside-down printing.
corner_x=[x+dx for x in FAN_X for dx in (-52.5,52.5)]
fan_hole_z=FAN_Z[0]-52.5
d=3.4/math.sqrt(2)
for x in corner_x:
    pts=[cq.Vector(x+dx,509,fan_hole_z+dz) for dx,dz in [(0,-d),(d,0),(0,d),(-d,0)]]
    tool=cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts+[pts[0]]),[],cq.Vector(0,8,0))
    bar=bar.cut(tool)
# Relieve the small front-face cusp beside the right-hand floor screw so a
# 10mm-diameter driver envelope clears vertically with1mm radial allowance.
for x in ANCHOR_X:
    bar=bar.cut(cyl(6,35,(x,520,FLOOR+7.5)))
bar=bar.clean()
assert bar.isValid() and len(bar.Solids())==1

report={
 'revision':26,'step':22,'part_count':1,'changes_existing_prints':False,
 'user_datum':'duct-fan intake/front faces 10mm rearward of front floor-insert centers',
 'coordinate_frame':'+X chassis left; +Y front; +Z up',
 'floor_z_mm':FLOOR,'front_floor_inserts_xyz':[[x,520,FLOOR] for x in ANCHOR_X],
 'floor_insert_pitch_mm':140,'fan_contact_face_y_mm':FAN_FRONT,
 'retaining_face_to_insert_center_mm':ANCHOR_Y-FAN_FRONT,
 'bar_thickness_mm':BAR_THICK,'height_above_floor_mm':BAR_HIGH,
 'scallop_diameter_mm':120,'bottom_sole_thickness_mm':RAIL_THICK,
 'feet_thickness_mm':4,'fan_corner_holes_xz':[[x,fan_hole_z] for x in corner_x],
 'fan_holes':'45deg diamond, 3.4mm inscribed diameter; no new tapped holes',
 'fan_centers_xz':[[x,z] for x in FAN_X for z in FAN_Z],
 'nominal_fan_bank_top_z_mm':259.05,'existing_lid_bottom_z_mm':260.35,
 'floor_hardware':'2 M3x8 socket cap screws + 2 washers (0.5mm, OD<=7)',
 'bar_fan_hardware_single_25mm_stage':'4 M3x45 through bolts, 8 washers, 4 M3 nuts; includes unchanged 6mm duct seats',
 'other_fan_hardware_single_25mm_stage':'12 M3x40 through bolts, 24 washers, 12 M3 nuts if removing the former 20mm carrier',
 'front_fan_rear_y_mm':554.2,'fan_face_gap_mm':44.2,
 'nominal_front_fan_reference_gap_note':'44.2mm (1.74in) in existing CAD; user estimates about1.5in. The clarified10mm anchor datum controls.',
 'duct_context_translation_y_mm':5.,
 'duct_context_note':'One25mm fan stage; translated5mm forward to meet the as-built fan-front datum. Not a change to existing duct geometry; actual GPU seating controls.',
 'physical_fit_verified':False,
}
issues=[]
chpath=SRC/'References/6U_Chassis_Step_16.step'
ch=cq.importers.importStep(str(chpath)).val()
report['unchanged_chassis_sha256']=hashlib.sha256(chpath.read_bytes()).hexdigest()
report['chassis_overlap_mm3']=overlap(bar,ch)
if report['chassis_overlap_mm3']>.001:issues.append('bar/chassis')

ducts=[]
for pair in 'AB':
    p=cq.importers.importStep(str(SRC/f'Parts/Duct20_PAIR_{pair}_DUCT.step')).val().translate((0,5,0))
    ducts.append(p)
    if overlap(bar,p)>.001:issues.append('bar/duct '+pair)

fans=[]
for x in FAN_X:
    for z in FAN_Z:
        f=box(x-60,FAN_FRONT-FAN_THICK,z-60,120,FAN_THICK,120)
        f=f.cut(cyl(57.5,FAN_THICK,(x,FAN_FRONT-FAN_THICK,z),(0,1,0)))
        for dx in (-52.5,52.5):
            for dz in (-52.5,52.5):
                f=f.cut(cyl(1.7,FAN_THICK,(x+dx,FAN_FRONT-FAN_THICK,z+dz),(0,1,0)))
        fans.append(f)
        if overlap(bar,f)>.001:issues.append('bar/fan frame')

hardware=[]; floor_screws=[]; checks=[]
for x in ANCHOR_X:
    washer=cyl(3.5,.5,(x,520,FLOOR+4)).cut(cyl(1.6,.5,(x,520,FLOOR+4)))
    screw=cyl(1.5,8,(x,520,FLOOR+4.5-8)).fuse(cyl(2.75,3,(x,520,FLOOR+4.5)))
    hardware.extend([washer,screw]);floor_screws.extend([washer,screw])
    driver=cyl(5,280,(x,520,FLOOR+7.5))
    for n,p in [('chassis',ch),('bar',bar)]+[('fan',p) for p in fans]+[('duct',p) for p in ducts]:
        for label,h in [('washer',washer),('screw',screw),('vertical driver',driver)]:
            v=overlap(h,p)
            if v>.001:issues.append([n,label,x,v])
    # Verify the reference chassis actually contains the reused floor pocket.
    v=overlap(cyl(1.99,5.0,(x,520,FLOOR-5.0)),ch)
    if v>.001:issues.append(['missing floor pocket',x,v])
    checks.append({'x':x,'insert_engagement_mm':3.5,'blind_pocket_bottom_clearance_mm':1.7,
                   'vertical_driver_clear_diameter_mm':10})

# Through-bolts go in from the front, through bar/fan/duct, with nuts and
# washers at the already-accessible duct corner recesses. Attach on bench.
fan_hw=[]
for x in corner_x:
    z=fan_hole_z
    frontwasher=cyl(3.5,.5,(x,516,z),(0,1,0)).cut(cyl(1.6,.5,(x,516,z),(0,1,0)))
    screw=cyl(1.5,45,(x,471.5,z),(0,1,0)).fuse(cyl(2.75,3,(x,516.5,z),(0,1,0)))
    rearwasher=cyl(3.5,.5,(x,478.5,z),(0,1,0)).cut(cyl(1.6,.5,(x,478.5,z),(0,1,0)))
    rad=5.5/math.sqrt(3)
    pts=[cq.Vector(x+rad*math.cos(k*math.pi/3),476.1,z+rad*math.sin(k*math.pi/3)) for k in range(6)]
    nut=cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts+[pts[0]]),[],cq.Vector(0,2.4,0)).cut(cyl(1.5,2.4,(x,476.1,z),(0,1,0)))
    for h in [frontwasher,screw,rearwasher,nut]:
        for n,p in [('chassis',ch),('bar',bar)]+[('fan',p) for p in fans]+[('duct',p) for p in ducts]:
            v=overlap(h,p)
            if v>.001:issues.append(['fan hardware',x,n,v])
    hardware.extend([frontwasher,screw,rearwasher,nut]);fan_hw.extend([frontwasher,screw,rearwasher,nut])

# The 2mm sole stays below the 115mm reference airway. Feet and screws occupy
# a small zone in front of the lower inlets; measure rather than claim zero.
airway=[]
for x in FAN_X:
    flow=cyl(57.5,19,(x,510,79.05),(0,1,0))
    core_bar=bar.intersect(box(192,510,FLOOR,240,4,30))
    assert overlap(core_bar,flow)<.001
    airway.append({'fan_center_x':x,'bar_and_foot_overlap_volume_mm3':overlap(bar,flow),
                   'floor_screw_envelope_overlap_volume_mm3':sum(overlap(h,flow) for h in floor_screws)})
report['airway_notes']='No bar crosses either upper fan;120mm scallops and2mm sole clear nominal115mm bore at contact face. Two local forward feet/floor screws are near the lower inlet rim; not a full-flow simulation.'
report['airway_checks']=airway
report['floor_hardware_checks']=checks
report['interferences']=issues
assert not issues,issues

b=bar.BoundingBox()
report['valid_single_solid']=True
report['print_bounds_mm']=[b.xlen,b.ylen,b.zlen]
report['part_volume_mm3']=bar.Volume()
report['part_mass_g_at_1p27_g_per_cc']=bar.Volume()/1000*1.27
cq.exporters.export(bar,str(OUT/'MOE_Duct_Retaining_Bar_Step22.step'))
printpart=bar.translate((-b.xmin,-b.ymin,-FLOOR))
cq.exporters.export(printpart,str(OUT/'MOE_Duct_Retaining_Bar_Step22_Print.stl'),tolerance=.025,angularTolerance=.08)

# Mesh checks: watertight, positive, consistently wound, and support-free
# 45degree screen for the supplied underside-down orientation.
raw=(OUT/'MOE_Duct_Retaining_Bar_Step22_Print.stl').read_bytes()
n=struct.unpack_from('<I',raw,80)[0]
dt=np.dtype([('normal','<f4',3),('v','<f4',(3,3)),('attr','<u2')])
v=np.frombuffer(raw,dtype=dt,count=n,offset=84)['v'].astype(float)
vv,inv=np.unique(np.round(v.reshape(-1,3),5),axis=0,return_inverse=True);ff=inv.reshape(-1,3)
edges=np.concatenate([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);edges=edges[edges[:,0]!=edges[:,1]]
_,idx,count=np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True,return_counts=True)
winding=np.bincount(idx,weights=np.where(edges[:,0]<edges[:,1],1,-1))
nn=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);aa=np.linalg.norm(nn,axis=1)
nn=nn/np.where(aa>1e-12,aa,1)[:,None]
steep=(nn[:,2]<-2**-.5-1e-4)&(np.max(v[:,:,2],axis=1)>.001)&(aa>1e-6)
report['mesh']={'triangles':n,'watertight':bool(np.all(count==2)),
 'consistent_winding':bool(np.all(winding==0)),
 'unsupported_triangles_beyond_45deg':int(steep.sum()),
 'signed_volume_mm3':float(np.sum(np.einsum('ij,ij->i',v[:,0],np.cross(v[:,1],v[:,2])))/6)}
assert report['mesh']['watertight'] and report['mesh']['consistent_winding']
assert not steep.any() and report['mesh']['signed_volume_mm3']>0

assembly=cq.Assembly(name='Step22_Retaining_Bar_Context')
assembly.add(ch,name='UNCHANGED_CHASSIS',color=cq.Color(.53,.67,.77))
assembly.add(bar,name='NEW_RETAINING_BAR',color=cq.Color(.94,.66,.22))
for i,p in enumerate(ducts):assembly.add(p,name=f'EXISTING_DUCT_{i+1}_POSITION_REFERENCE',color=cq.Color(.53,.67,.77))
for i,p in enumerate(fans):assembly.add(p,name=f'FAN_FRAME_REFERENCE_{i+1}',color=cq.Color(.32,.38,.42))
assembly.add(cq.Compound.makeCompound(hardware),name='HARDWARE_REFERENCES',color=cq.Color(.70,.72,.74))
assembly.save(str(OUT/'MOE_Duct_Retaining_Bar_Step22_Context.step'))
(OUT/'Step22_Checks_And_Dimensions.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
