from pathlib import Path
import cadquery as cq,numpy as np,json,math
O=Path(__file__).parent
# Fan-side-down build direction is -Y. Downward normals have +Y component.
reports={}
for n in ['PAIR_A_DUCT','PAIR_B_DUCT']:
 p=cq.importers.importStep(str(O/f'Duct20_{n}.step')).val()
 report=[]
 for f in p.Faces():
  verts,tris=f.tessellate(.08,.08);v=np.array([x.toTuple() for x in verts]);t=np.array(tris)
  if not len(t):continue
  u=v[t];ns=np.cross(u[:,1]-u[:,0],u[:,2]-u[:,0]);lens=np.linalg.norm(ns,axis=1);nz=np.divide(ns[:,1],lens,out=np.zeros_like(lens),where=lens>1e-10)
  mask=(nz>math.sin(math.radians(45))+1e-5)&(np.mean(u[:,:,1],axis=1)<479.999)
  area=float((lens[mask]/2).sum())
  if area>.01:
   b=f.BoundingBox();report.append({'area':round(area,3),'normal':f.normalAt().toTuple(),'bb':[round(a,3) for a in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)]})
 reports[n]=report
print(json.dumps({'criterion':'Duct surfaces >45 degrees from -Y build direction; fan bed face excluded','flagged_faces':reports,'passed':all(not x for x in reports.values())},indent=2))
