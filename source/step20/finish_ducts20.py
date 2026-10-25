from pathlib import Path
import cadquery as cq,json,math
O=Path(__file__).parent
names=json.loads((O/'ducts20_manifest.json').read_text())['part_names'];parts={n:cq.importers.importStep(str(O/f'Duct20_{n}.step')).val() for n in names}
ch=cq.importers.importStep(str(O/'6U_Chassis_Step_16.step')).val()
def vol(a,b):
 x=a.BoundingBox();y=b.BoundingBox()
 if any(getattr(x,k+'max')<=getattr(y,k+'min')+1e-6 or getattr(y,k+'max')<=getattr(x,k+'min')+1e-6 for k in 'xyz'):return 0
 return a.intersect(b).Volume()
issues=[]
for n,p in parts.items():
 assert p.isValid() and len(p.Solids())==1,n
 v=vol(p,ch)
 if v>.001:issues.append([n,'chassis',v])
for i,(n,p) in enumerate(parts.items()):
 for nn,q in list(parts.items())[i+1:]:
  v=vol(p,q)
  if v>.001:issues.append([n,nn,v])
for x,y,z in json.loads((O/'ducts20_manifest.json').read_text())['duct_screw_centers_xyz']:
 access=cq.Solid.makeCylinder(3.5,230,cq.Vector(x,y,z+.001))
 for n,p in parts.items():
  if n.endswith('_DUCT'):
   v=vol(p,access)
   if v>.001:issues.append(['external_driver_access',n,x,y,v])
 # 8 mm socket screw, 0.5 mm washer; head bearing53.6, tip45.6.
 bolt=cq.Solid.makeCylinder(1.5,8,cq.Vector(x,y,45.6)).fuse(cq.Solid.makeCylinder(2.75,3,cq.Vector(x,y,53.6)))
 washer=cq.Solid.makeCylinder(3.5,.5,cq.Vector(x,y,53.1)).cut(cq.Solid.makeCylinder(1.7,.5,cq.Vector(x,y,53.1)))
 for n,p in parts.items():
  v=vol(p,bolt.fuse(washer))
  if v>.001:issues.append(['external_hardware',n,x,y,v])
print('INTERFERENCES',issues,flush=True);assert not issues
for n,p in parts.items():
 q=p
 if n.endswith('_DUCT'):q=q.rotate((0,0,0),(1,0,0),-90)
 elif n=='FAN_BANK_CARRIER':q=q.rotate((0,0,0),(1,0,0),90)
 b=q.BoundingBox();q=q.translate((-b.xmin,-b.ymin,-b.zmin))
 cq.exporters.export(q,str(O/f'Duct20_{n}_Print.stl'),tolerance=.06,angularTolerance=.1)
# Optional 2mm shim is unchanged.
# Regenerate the existing 2 mm shim from its constant-section 10 mm riser.
# This removes the old external STL input; the hole layout is unchanged.
shim=parts['PAIR_A_FRONT_RISER_10'];b=shim.BoundingBox()
shim=shim.translate((-b.xmin,-b.ymin,-b.zmin))
shim=shim.intersect(cq.Solid.makeBox(26,30,2,cq.Vector(-1,-1,0))).clean()
cq.exporters.export(shim,str(O/'Duct20_Optional_2mm_Height_Shim_Print.stl'),tolerance=.06,angularTolerance=.1)
fans=cq.importers.importStep(str(O/'Duct18_Fan_Envelopes_Reference.step')).val()
a=cq.Assembly(name='Step20_Chassis_Context');a.add(ch,name='UNCHANGED_STEP16_CHASSIS',color=cq.Color(.56,.69,.78))
for n,p in parts.items():a.add(p,name=n,color=cq.Color(.9,.63,.22) if n.endswith('_DUCT') else cq.Color(.56,.69,.78))
a.add(fans,name='REFERENCE_FANS',color=cq.Color(.34,.38,.42));a.save(str(O/'6U_Chassis_Step20_Duct_Context.step'))
(O/'ducts20_geometry_checks.json').write_text(json.dumps({'part_count':len(parts),'all_single_valid_solids':True,'nominal_interferences':issues,'external_driver_and_hardware_clear':True,'chassis_changed':False},indent=2))
print('Step20 exported and checked',flush=True)
