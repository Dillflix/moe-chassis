import numpy as np
from PIL import Image

def render(items,path,pos,focal,scale,size=(1050,850)):
 ss=1.5
 w,h=[int(v*ss) for v in size]
 rgb=np.zeros((h,w,3),dtype=np.uint8);rgb[:]=[246,248,250]
 zb=np.full((h,w),-1e9,dtype=np.float64)
 view=np.array([1. if pos[0]>focal[0] else -1.,1. if pos[1]>focal[1] else -1.,1.]);view/=np.linalg.norm(view)
 right=np.cross([0,0,1],view);right/=np.linalg.norm(right)
 up=np.cross(view,right)
 basis=np.array([right,up,view]).T
 focal=np.array(focal)
 factor=h/(2*scale)
 light=np.array([.2,-.4,1.]);light/=np.linalg.norm(light)
 edge_lists=[]
 for shape,color,alpha in items:
  vv,tt=shape.tessellate(.08,.08)
  world=np.array([[v.x,v.y,v.z] for v in vv])
  pts=(world-focal)@basis
  pts[:,0]=pts[:,0]*factor+w/2;pts[:,1]=h/2-pts[:,1]*factor
  for t in tt:
   pp=pts[list(t)]; a,b,c=pp
   xmin=max(0,int(np.floor(pp[:,0].min())));xmax=min(w-1,int(np.ceil(pp[:,0].max())))
   ymin=max(0,int(np.floor(pp[:,1].min())));ymax=min(h-1,int(np.ceil(pp[:,1].max())))
   if xmin>xmax or ymin>ymax:continue
   den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
   if abs(den)<1e-8:continue
   xs=np.arange(xmin,xmax+1)[None,:]+.5;ys=np.arange(ymin,ymax+1)[:,None]+.5
   v0=((b[1]-c[1])*(xs-c[0])+(c[0]-b[0])*(ys-c[1]))/den
   v1=((c[1]-a[1])*(xs-c[0])+(a[0]-c[0])*(ys-c[1]))/den
   v2=1-v0-v1
   dep=v0*a[2]+v1*b[2]+v2*c[2]
   target=zb[ymin:ymax+1,xmin:xmax+1]
   mask=(v0>=-1e-8)&(v1>=-1e-8)&(v2>=-1e-8)&(dep>=target-1e-7)
   if not np.any(mask):continue
   ww=world[list(t)]
   normal=np.cross(ww[1]-ww[0],ww[2]-ww[0])
   ln=np.linalg.norm(normal)
   normal=normal/ln if ln else normal
   shade=.70+.30*abs(float(normal@light))
   clr=np.array(color)*shade*255
   target[mask]=dep[mask]
   rgb[ymin:ymax+1,xmin:xmax+1][mask]=np.clip(clr,0,255).astype('uint8')
  for edge in shape.Edges():
   try:
    vv,_=edge.sample(80 if edge.geomType()!='LINE' else 2)
    edge_lists.append(np.array([[v.x,v.y,v.z] for v in vv]))
   except Exception:pass
 # visible CAD edges with a depth test
 for edge in edge_lists:
  pp=(edge-focal)@basis
  pp[:,0]=pp[:,0]*factor+w/2;pp[:,1]=h/2-pp[:,1]*factor
  for a,b in zip(pp[:-1],pp[1:]):
   n=max(2,int(np.linalg.norm(b[:2]-a[:2])*1.5))
   q=a[None,:]+(b-a)[None,:]*np.linspace(0,1,n)[:,None]
   xx=np.round(q[:,0]).astype(int);yy=np.round(q[:,1]).astype(int)
   good=(xx>=0)&(xx<w)&(yy>=0)&(yy<h)
   xx=xx[good];yy=yy[good];zz=q[:,2][good]
   visible=zz>=zb[yy,xx]-.55/factor
   rgb[yy[visible],xx[visible]]=[54,76,93]
 Image.fromarray(rgb).resize(size,Image.Resampling.LANCZOS).save(path)
