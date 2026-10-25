"""Step20 / Rev24: rigid fan-side-down ducts with trimmed interfaces and external fasteners."""
from pathlib import Path
import cadquery as cq, json, math
O=Path(__file__).parent;B=19.05
PC=[283.795,365.075];FC=[252.,372.];ST=[350.,400.]
SC=[[280.,268.],[374.,370.]]
def box(x,y,z,a,b,c):return cq.Solid.makeBox(a,b,c,cq.Vector(x,y,z))
def cyl(r,h,p,axis=(0,0,1)):return cq.Solid.makeCylinder(r,h,cq.Vector(*p),cq.Vector(*axis))
def wire(poly,y):return cq.Wire.makePolygon([cq.Vector(x,y,z) for x,z in poly]+[cq.Vector(poly[0][0],y,poly[0][1])])
def loft(polys,ys):return cq.Solid.makeLoft([wire(p,y) for p,y in zip(polys,ys)],ruled=True)
def hex_z(x,y,z,h):
 r=5.7/math.sqrt(3);w=cq.Wire.makePolygon([cq.Vector(x+r*math.cos(k*math.pi/3),y+r*math.sin(k*math.pi/3),z) for k in range(7)])
 return cq.Solid.extrudeLinear(w,[],cq.Vector(0,0,h))
def slot(x,y,z,axis,L,r,h):
 if axis=='y':return cyl(r,h,(x,y-L/2,z)).fuse(cyl(r,h,(x,y+L/2,z)),box(x-r,y-L/2,z,2*r,L,h))
 return cyl(r,h,(x-L/2,y,z)).fuse(cyl(r,h,(x+L/2,y,z)),box(x-L/2,y-r,z,L,2*r,h))
def pocket(x,y,top):return cyl(2,5.2,(x,y,top-5.2)).fuse(cq.Solid.makeCone(2,2.25,.3,cq.Vector(x,y,top-.3)))
def rect(x0,x1,z0,z1):return [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]
parts={};cavities=[];tubes=[];ifaces=[];screw_centers=[]
def gapcenter(i,y):
 t=(y-304)/141
 return (1-t)*(322.435+81.28*i-31.82)+t*(FC[i]-1)
# Low supports: same four floor anchors, no upright protrusions into the flow.
for i,cx in enumerate(PC):
 name='AB'[i];anchor=[260,400][i];x0,x1=[(246,310),(342,412)][i]
 base=box(x0,325,B,x1-x0,130,8)
 for y in (350.,430.):base=base.cut(slot(anchor,y,B-1,'y',20,1.7,10)).cut(slot(anchor,y,B+2,'y',20,4.1,7))
 for j,y in enumerate(ST):
  cx=SC[i][j]
  for yy in (y-7,y+7):
   base=base.cut(slot(cx,yy,B-1,'x',20,1.7,10))
   base=base.cut(box(x0-1,yy-2.85,B+1.2,x1-x0+2,5.7,2.6))
 parts[f'PAIR_{name}_BASE']=base.clean()
 for j,y in enumerate(ST):
  cx=SC[i][j]
  prefix=f'PAIR_{name}_{"REAR" if j==0 else "FRONT"}'
  carriage=box(cx-12,y-14,27.05,24,28,6)
  for yy in (y-7,y+7):carriage=carriage.cut(cyl(1.7,8,(cx,yy,26.05))).cut(cyl(4.1,4.6,(cx,yy,29.45)))
  for x in (cx-8,cx+8):carriage=carriage.cut(pocket(x,y,33.05))
  parts[prefix+'_SLIDER']=carriage.clean()
  saddle=box(cx-20,y-14,43.05,40,28,6)
  for x in (cx-8,cx+8):saddle=saddle.cut(cyl(1.7,8,(x,y,42.05))).cut(cyl(4.1,4.6,(x,y,45.45)))
  saddle=saddle.cut(pocket(gapcenter(i,y+8),y+8,49.05))
  for yy in (y-7,y+7):saddle=saddle.cut(cyl(2,8,(cx,yy,42.05)))
  parts[prefix+'_SADDLE']=saddle.clean()
  shim=box(cx-12,y-14,33.05,24,28,10)
  for x in (cx-8,cx+8):shim=shim.cut(cyl(1.8,12,(x,y,32.05)))
  for yy in (y-7,y+7):shim=shim.cut(cyl(2,12,(cx,yy,32.05)))
  parts[prefix+'_RISER_10']=shim.clean()
source=cq.importers.importStep(str(O/'V620_Trimmed_Interface_Step19.step')).val()
outer0=[(0,0),(23,0),(23,44),(15,44),(15,89),(0,89),(0,75),(0,73)]
inner0=[(2,2),(21,2),(21,34),(13,42),(13,87),(8,87),(8,73),(2,73)]
def inletpoly(x0,x1,z0,z1):
 h=z1-z0
 return [(x1,z0),(x0,z0),(x0,z0+.4*h),(x0,z0+.6*h),(x0,z1),(x1,z1),(x1,z0+.8*h),(x1,z0+.6*h)]
def section(poly,out,y,inner=False):
 t=min(1.,(y-304)/141)
 pts=[((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(poly,out)]
 # Keep support-contact zones flat. Smooth rectangular inlet recovers floor clearance.
 low_linear=(1-t)*40+t*34.05
 floor=40+(53.05-40)*(y-304)/26 if y<330 else (53.05 if y<=424 else 53.05+(34.05-53.05)*min(1.,(y-424)/21))
 delta=floor-low_linear
 zlo=min(z for x,z in pts);zhi=max(z for x,z in pts)
 return [(x,z+delta*(zhi-z)/(zhi-zlo)) for x,z in pts]
for i,fc in enumerate(FC):
 xT=322.435+81.28*i
 iface=source.rotate((0,0,0),(0,0,1),180).translate((xT,281,40));ifaces.append(iface)
 shells=[]
 for k in range(2):
  ox=[(xT-x-40.64*k,z+40) for x,z in outer0]
  ix=[(xT-x-40.64*k,z+40) for x,z in inner0]
  x0=fc+(2 if k==0 else -49);x1=x0+45
  oo=inletpoly(x0,x1,34.05,244.05);ii=inletpoly(x0+2,x1-2,36.05,242.05)
  ys=[304,330,424,445]
  outer=loft([section(ox,oo,y) for y in ys],ys)
  inner=loft([section(ix,ii,y,True) for y in ys],ys)
  assert inner.cut(outer).Volume()<.01,('loft containment',i,k)
  shells.append(outer.cut(inner).clean());cavities.append(inner)
 # Join both channels via original mating flange and low external feet.
 duct=iface.fuse(*shells,tol=0.0001)
 print("join iface",i,duct.isValid(),len(duct.Solids()),flush=True)
 for j,y in enumerate(ST):
  # Foot spans the two passages without protruding into them.
  t=min(1.,(y-304)/141)
  xmin=(1-t)*(xT-40.64-23)+t*(fc-49);xmax=(1-t)*xT+t*(fc+47)
  vp=[cq.Vector(xmin,yy,zz) for yy,zz in [(y-14.1,53.1),(y+14.1,53.1),(y+10,49.05),(y-10,49.05)]]
  foot=cq.Solid.extrudeLinear(cq.Wire.makePolygon(vp+[vp[0]]),[],cq.Vector(xmax-xmin,0,0))
  duct=duct.fuse(foot)
  cx=SC[i][j]
  # One external screw in the open channel gap; no holes through either airway.
  x=gapcenter(i,y+8);yy=y+8
  # Diamond bore: vertical chassis axis is horizontal on the print bed.
  pts=[cq.Vector(x+dx,yy+dy,48) for dx,dy in [(0,-2.5),(2.5,0),(0,2.5),(-2.5,0)]]
  tool=cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts+[pts[0]]),[],cq.Vector(0,0,7))
  duct=duct.cut(tool);screw_centers.append([x,yy,53.1])
 # Thin external ties behind the boot collars keep paired mouths rigid.
 # Mouths connect through the original flange and the two external foot bridges.
 # Fan adapter will be fused into the same print below.
 # Integral fan face; central bed-contact strip supports the divider from layer one.
 adapter=box(fc-60,478,B,120,2,240)
 for zc in (79.05,199.05):adapter=adapter.cut(cyl(57.5,4,(fc,477,zc),(0,1,0)))
 adapter=adapter.fuse(box(fc-1,478,B,2,2,240))
 envelope=box(fc-60,478,B,120,2,240)
 for k in range(2):
  nx0=fc+(2 if k==0 else -49);nx1=nx0+45
  fx0=fc+(0 if k==0 else -60);fx1=fx0+60
  out=loft([rect(nx0,nx1,34.05,244.05),rect(fx0-(1 if k==0 else 0),fx1+(1 if k==1 else 0),B,B+240)],[445,478])
  inn=loft([rect(nx0+2,nx1-2,36.05,242.05),rect(fx0+1,fx1-1,B+2,B+238)],[445,478])
  adapter=adapter.fuse(out.cut(inn))
  envelope=envelope.fuse(out)
 for zc in (79.05,199.05):
  for x in (fc-52.5,fc+52.5):
   for z in (zc-52.5,zc+52.5):
    # Rounded external corner recess, sealed from the passage by a 2mm wall.
    # A tapered upstream end closes at45deg in fan-side-down printing.
    housing=cq.Solid.makeCone(.001,7,7.3,cq.Vector(x,444.7,z),cq.Vector(0,1,0)).fuse(cyl(7,26,(x,452,z),(0,1,0)))
    pockettool=cq.Solid.makeCone(.001,5,5.3,cq.Vector(x,446.7,z),cq.Vector(0,1,0)).fuse(cyl(5,22,(x,452,z),(0,1,0)))
    adapter=adapter.fuse(housing.intersect(envelope,tol=.0001),cyl(4,4,(x,474,z),(0,1,0)))
    adapter=adapter.cut(pockettool).cut(cyl(1.7,8,(x,473,z),(0,1,0)))
 print("pre adapter",i,duct.isValid(),len(duct.Solids()),adapter.isValid(),len(adapter.Solids()),flush=True)
 duct=duct.fuse(adapter,tol=.0001).clean()
 print("post adapter",i,duct.isValid(),len(duct.Solids()),flush=True)
 parts[f'PAIR_{"AB"[i]}_DUCT']=duct;tubes.append(duct)
# Floor-fixed 20 mm interstage spacer; second fan stage is optional.
carrier=box(192,505,B,240,20,240)
for fc in FC:
 for zc in (79.05,199.05):
  carrier=carrier.cut(box(fc-58,504,zc-58,116,22,116))
  for x0 in (fc-60,fc+45):
   for z0 in (zc-60,zc+45):carrier=carrier.fuse(box(x0,505,z0,15,20,15))
  for x in (fc-52.5,fc+52.5):
   for z in (zc-52.5,zc+52.5):carrier=carrier.cut(cyl(1.7,22,(x,504,z),(0,1,0)))
for x in (260,400):carrier=carrier.fuse(box(x-9,511,B,18,14,4)).cut(cyl(1.7,6,(x,520,B-1)))
parts['FAN_BANK_CARRIER']=carrier.clean()
fans=[]
for y in (480,525):
 for fc in FC:
  for zc in (79.05,199.05):
   f=box(fc-60,y,zc-60,120,25,120).cut(cyl(57.5,25,(fc,y,zc),(0,1,0)))
   fans.append(f)
def export():
 for n,p in parts.items():
  print(n,len(p.Solids()),p.isValid(),round(p.Volume(),2),flush=True)
  assert p.isValid() and len(p.Solids())==1,n
  cq.exporters.export(p,str(O/f'Duct20_{n}.step'))
 # Whole review STEP and meshes; production split parts follow in a separate export stage.
 a=cq.Assembly(name='Step20_Duct_System')
 for n,p in parts.items():a.add(p,name=n,color=cq.Color(.9,.63,.22) if not n.startswith('TPU') else cq.Color(.2,.62,.58))
 a.save(str(O/'V620_Duct_System_Step20.step'))
 (O/'ducts20_manifest.json').write_text(json.dumps({'part_names':list(parts),'part_count':len(parts),'duct_screw_centers_xyz':screw_centers,'all_rigid':True,'nominal_riser_mm':10},indent=2))
 print('EXPORTED',len(parts),'parts',flush=True)
if __name__=='__main__':export()
