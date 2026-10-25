from pathlib import Path
import json,struct,numpy as np
O=Path(__file__).parent/'lid_step21';report=[]
for p in sorted(O.glob('*_Print.stl')):
 raw=p.read_bytes();n=struct.unpack_from('<I',raw,80)[0]
 assert len(raw)==84+50*n
 dt=np.dtype([('normal','<f4',3),('v','<f4',(3,3)),('attr','<u2')])
 v=np.frombuffer(raw,dtype=dt,count=n,offset=84)['v'].astype(float)
 vertices,inv=np.unique(np.round(v.reshape(-1,3),5),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 edges=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);edges=edges[edges[:,0]!=edges[:,1]]
 _,idx,cnt=np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True,return_counts=True)
 winding=np.bincount(idx,weights=np.where(edges[:,0]<edges[:,1],1,-1))
 normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);area2=np.linalg.norm(normal,axis=1)
 normal=normal/np.where(area2>1e-12,area2,1)[:,None]
 not_bed=np.max(v[:,:,2],axis=1)>.001
 steep=(normal[:,2]<-2**-.5-1e-4)&not_bed&(area2>1e-6)
 r={'file':p.name,'triangles':n,'closed':bool(np.all(cnt==2)),'consistent_winding':bool(np.all(winding==0)),
    'print_bounds_mm':np.ptp(v.reshape(-1,3),axis=0).tolist(),'bottom_z_mm':float(v[:,:,2].min()),
    'downward_faces_steeper_than_45_degrees_excluding_bed':int(steep.sum()),
    'signed_mesh_volume_mm3':float(np.sum(np.einsum('ij,ij->i',v[:,0],np.cross(v[:,1],v[:,2])))/6)}
 assert r['closed'] and r['consistent_winding'] and not steep.any() and r['signed_mesh_volume_mm3']>0,r
 report.append(r)
(O/'Lid21_Mesh_Checks.json').write_text(json.dumps(report,indent=2))
print('4 closed, consistently wound meshes; 45-degree print screen passed.')
