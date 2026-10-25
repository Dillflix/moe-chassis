"""Step21 / Rev25: four-piece low-profile lid, existing Step16 chassis unchanged."""
from pathlib import Path
import cadquery as cq, json, hashlib, math
R=Path(__file__).parent; O=R/'lid_step21';O.mkdir(exist_ok=True)
S=R/'assembly_sources/project'
W,L,Z=444.5,584.2,260.35
T,RIB=4.0,1.0
MX,MY=W/2,L/2
GAP=.30
ASSEMBLY_ORDER=['REAR_RIGHT','REAR_LEFT','FRONT_RIGHT','FRONT_LEFT']
HOLES={
 'REAR_RIGHT':[(7.5,65),(7.5,185)],
 'REAR_LEFT':[(437,65),(437,185)],
 'FRONT_RIGHT':[(7.5,320),(7.5,530)],
 'FRONT_LEFT':[(437,320),(437,530)]}
def box(x,y,z,a,b,c):return cq.Solid.makeBox(a,b,c,cq.Vector(x,y,z))
def cyl(r,h,x,y,z):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def bounds(n,z):
 # Inclined mating seams overlap 4mm in plan, with 0.3mm XY clearance.
 # Right/rear sections underlap left/front sections; all undersides stay at Z.
 sx=MX+(T-z);sy=MY+(T-z)
 xa,xb=(0,sx-GAP/2) if 'RIGHT' in n else (sx+GAP/2,W)
 ya,yb=(0,sy-GAP/2) if n.startswith('REAR') else (sy+GAP/2,L)
 return xa,xb,ya,yb
def wire(n,z):
 xa,xb,ya,yb=bounds(n,z)
 return cq.Wire.makePolygon([cq.Vector(x,y,Z+z) for x,y in [(xa,ya),(xb,ya),(xb,yb),(xa,yb),(xa,ya)]])
parts={};report={'revision':25,'step':21,'part_count':4,'chassis_changed':False,'checks':[]}
for n in ASSEMBLY_ORDER:
 p=cq.Solid.makeLoft([wire(n,0),wire(n,T)],ruled=True)
 xa,xb,ya,yb=bounds(n,T)
 ix0,ix1,iy0,iy1=xa+14,xb-14,ya+14,yb-14
 # All stiffening is above the skin, keeping fan/duct headroom unchanged.
 ribs=[box(ix0,iy0,Z+T,6,iy1-iy0,RIB),box(ix1-6,iy0,Z+T,6,iy1-iy0,RIB),
       box(ix0,iy0,Z+T,ix1-ix0,6,RIB),box(ix0,iy1-6,Z+T,ix1-ix0,6,RIB),
       box((ix0+ix1)/2-3,iy0,Z+T,6,iy1-iy0,RIB)]
 for frac in (1/3,2/3):ribs.append(box(ix0,iy0+(iy1-iy0)*frac-3,Z+T,ix1-ix0,6,RIB))
 p=p.fuse(*ribs).clean()
 for x,y in HOLES[n]:
  p=p.cut(cyl(1.7,8,x,y,Z-1)).cut(cyl(4.0,4,x,y,Z+1.2))
 # Recessed ID cannot increase the overall height.
 code=''.join(word[0] for word in n.split('_'))
 tx=(ix0+(ix0+ix1)/2)/2;ty=iy0+24
 stamp=cq.Workplane('XY').workplane(offset=Z+T-.35).center(tx,ty).text(code,9,.40,font='DejaVu Sans',kind='bold',combine=False).val()
 p=p.cut(stamp).clean()
 assert p.isValid() and len(p.Solids())==1,n
 parts[n]=p
 cq.exporters.export(p,str(O/f'Lid21_{n}.step'))
 b=p.BoundingBox();q=p.translate((-b.xmin,-b.ymin,-Z))
 cq.exporters.export(q,str(O/f'Lid21_{n}_Print.stl'),tolerance=.03,angularTolerance=.1)
 report['checks'].append({'part':n,'valid_single_solid':True,'print_bounds_mm':[b.xlen,b.ylen,b.zlen],'volume_mm3':p.Volume(),'floor_z':b.zmin,'max_z':b.zmax})

chpath=S/'References/6U_Chassis_Step_16.step';ch=cq.importers.importStep(str(chpath)).val()
chhash=hashlib.sha256(chpath.read_bytes()).hexdigest()
all_lid=cq.Compound.makeCompound(list(parts.values()))
issues=[]
def overlap(a,b):
 ba=a.BoundingBox();bb=b.BoundingBox()
 if any(getattr(ba,k+'max')<getattr(bb,k+'min')-1e-7 or getattr(bb,k+'max')<getattr(ba,k+'min')-1e-7 for k in 'xyz'):return 0.
 return a.intersect(b).Volume()
for i,(n,p) in enumerate(parts.items()):
 if overlap(p,ch)>.001:issues.append([n,'chassis',overlap(p,ch)])
 for nn,q in list(parts.items())[i+1:]:
  if overlap(p,q)>.001:issues.append([n,nn,overlap(p,q)])
 # Later panels can be lowered vertically after the earlier ones are installed.
 for dz in [.1,.5,1.,2.,3.,6.]:
  for nn in ASSEMBLY_ORDER[:i]:
   v=overlap(p.translate((0,0,dz)),parts[nn])
   if v>.001:issues.append(['drop_in_path',n,nn,dz,v])

refs={}
for f in (S/'Parts').glob('Duct20_*.step'):refs[f.stem]=cq.importers.importStep(str(f)).val()
refs['duct_fan_frames']=cq.importers.importStep(str(S/'References/Duct18_Fan_Envelopes_Reference.step')).val()
for x in [139.5,259.5,379.5]:
 for z in [79.05,199.05]:refs[f'front_fan_{x}_{z}']=box(x-60,554.2,z-60,120,25,120)
refs['upper_psu_envelope']=box(38.1,334.6082,164.35,125,150,86)
for n,p in refs.items():
 v=overlap(all_lid,p)
 if v>.001:issues.append(['lid_ref',n,v])

hardware=[];hardware_checks=[]
for n,coords in HOLES.items():
 for x,y in coords:
  washer=cyl(3.5,.5,x,y,Z+1.2).cut(cyl(1.6,.5,x,y,Z+1.2))
  under_head=Z+1.7
  screw=cyl(1.5,6,x,y,under_head-6).fuse(cyl(2.75,3,x,y,under_head))
  # Hex recess is visual only; hardware is a dimensional reference.
  socket=cq.Workplane('XY').workplane(offset=under_head+1.5).center(x,y).polygon(6,2.5/math.cos(math.pi/6)).extrude(1.6).val()
  screw=screw.cut(socket)
  for rn,shape in [('washer',washer),('screw',screw)]:
   for an,target in [('chassis',ch),('lid',all_lid)]:
    v=overlap(shape,target)
    if v>.001:issues.append(['hardware_intersection',n,x,y,rn,an,v])
  # Nut-driver/hex-bit access should not be blocked by ribs.
  driver=cyl(3,20,x,y,under_head+3.001)
  if overlap(driver,all_lid)>.001:issues.append(['driver_clearance',n,x,y])
  pocket=cyl(1.99,5,x,y,Z-5)
  if overlap(pocket,ch)>.001:issues.append(['mount_not_existing',n,x,y])
  hardware.extend([washer,screw])
  hardware_checks.append({'xy':[x,y],'counterbore_floor_z':Z+1.2,'screw_head_top_z':under_head+3,'screw_tip_z':under_head-6,'penetration_below_insert_top_mm':4.3,'blind_pocket_bottom_clearance_mm':.9})

report.update({'outer_width_mm':W,'outer_depth_mm':L,'skin_mm':T,'ribs_above_skin_mm':RIB,
 'total_max_height_mm':Z+T+RIB,'total_height_in':(Z+T+RIB)/25.4,'six_u_mm':266.7,'six_u_margin_mm':266.7-(Z+T+RIB),
 'screw_head_top_mm':Z+4.7,'mount_screws':'8 x M3x6 socket cap','washers':'8 x 0.5mm thick, OD <=7mm',
 'counterbore_diameter_mm':8,'counterbore_depth_mm':T-1.2,'clearance_hole_mm':3.4,'seam_xy_clearance_mm':GAP,
 'seam_slope_deg':45,'vertical_install_order':ASSEMBLY_ORDER,'hardware_checks':hardware_checks,
 'nominal_front_and_duct_fan_gap_mm':1.3,'chassis_sha256':chhash,'interferences':issues})
assert not issues,issues
assert report['total_max_height_mm']<266.7
assert all(max(x['print_bounds_mm'][:2])<350 for x in report['checks'])

a=cq.Assembly(name='Step21_Lid')
for n,p in parts.items():a.add(p,name=n,color=cq.Color(.91,.65,.26))
a.save(str(O/'MOE_Lid_Step21.step'))
context=cq.Assembly(name='Step21_Chassis_And_Lid');context.add(ch,name='UNCHANGED_STEP16_CHASSIS',color=cq.Color(.53,.67,.77))
for n,p in parts.items():context.add(p,name='LID_'+n,color=cq.Color(.91,.65,.26))
context.add(cq.Compound.makeCompound(hardware),name='M3x6_HARDWARE_REFERENCE',color=cq.Color(.38,.43,.47))
context.save(str(O/'MOE_Chassis_With_Lid_Step21.step'))
(O/'Lid21_Checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
