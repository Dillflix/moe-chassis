from pathlib import Path
import json,struct,numpy as np
O=Path(__file__).parent
names=json.loads((O/'ducts20_manifest.json').read_text())['part_names']
files=[O/f'Duct20_{n}_Print.stl' for n in names]+[O/'Duct20_Optional_2mm_Height_Shim_Print.stl']
report=[]
for p in files:
 raw=p.read_bytes();n=struct.unpack_from('<I',raw,80)[0]
 dt=np.dtype([('normal','<f4',3),('v','<f4',(3,3)),('attr','<u2')])
 v=np.frombuffer(raw,dtype=dt,count=n,offset=84)['v'];vertices,inv=np.unique(np.round(v.reshape(-1,3),5),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 e=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);e=e[e[:,0]!=e[:,1]]
 _,idx,cnt=np.unique(np.sort(e,axis=1),axis=0,return_inverse=True,return_counts=True);w=np.bincount(idx,weights=np.where(e[:,0]<e[:,1],1,-1))
 dims=np.ptp(v.reshape(-1,3),axis=0)
 r={'file':p.name,'triangles':n,'closed':bool(np.all(cnt==2)),'consistent_winding':bool(np.all(w==0)),'print_bounds_mm':dims.tolist()};report.append(r)
 assert r['closed'] and r['consistent_winding'],r
(O/'ducts20_mesh_checks.json').write_text(json.dumps(report,indent=2));print('18 closed, consistently wound meshes verified')
