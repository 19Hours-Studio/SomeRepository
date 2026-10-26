import sys,re,math,datetime as D
from itertools import accumulate as AC
from bisect import bisect_right as BR
M=(1<<64)-1
class C:
 def __init__(s,e,d=b''):
  s.e=e;s.lo=0;s.rg=M;s.o=bytearray();s.ca=0;s.cs=1;s.T={};s.d=d;s.p=9;s.cd=int.from_bytes(d[1:9],'big')
 def sh(s):
  if s.lo<255<<56 or s.lo>M:
   c=s.lo>>64;s.o.append(s.ca+c&255);s.o+=bytes([255+c&255])*(s.cs-1);s.cs=0;s.ca=s.lo>>56&255
  s.cs+=1;s.lo=s.lo<<8&M
 def fin(s):
  for _ in range(9):s.sh()
  return bytes(s.o)
 def go(s,t,cf,g):
  r=s.rg//t
  if s.e:c,f=cf;s.lo+=r*c;x=None
  else:c,f,x=g(min(s.cd//r,t-1));s.cd-=r*c
  s.rg=r*f
  while s.rg<1<<56:
   s.rg<<=8
   if s.e:s.sh()
   else:s.cd=(s.cd<<8|(s.d[s.p] if s.p<len(s.d) else 0))&M;s.p+=1
  return x
 def u(s,n,x):
  r=s.go(n,(x,1),lambda t:(t,1,t))
  return x if s.e else r
 def bit(s,k,b):
  k='b',k;p=s.T.get(k,2048)
  r=s.go(4096,(0,p) if b==0 else (p,4096-p),lambda t:(0,p,0) if t<p else (p,4096-p,1))
  if not s.e:b=r
  s.T[k]=p+(4096-p>>4) if b==0 else p-(p>>4)
  return b
 def pc(s,F,v,cap,k):
  t=1<<40;A=t-cap-1
  cu=lambda j:int(F(j)*A)+j
  def g(x):
   l,h=0,cap
   while l<h:
    m=l+h+1>>1
    if cu(m)<=x:l=m
    else:h=m-1
   a=cu(l)
   return a,(t if l==cap else cu(l+1))-a,l
  if s.e:a=cu(min(v,cap));s.go(t,(a,(t if v>=cap else cu(v+1))-a),0);r=v
  else:r=s.go(t,0,g)
  if r>=cap:r=s.num(k,None if v is None else v-cap)+cap
  return r
 def plog(s,k,v):
  k='l',k;n,a,b=s.T.get(k,(1,3.,10.));mu=a/n;sg=math.sqrt(max(b/n-mu*mu,.01))*2**.5
  v=s.pc(lambda x:.5+.5*math.erf((math.log(x)-mu)/sg) if x else 0.,v,4096,k)
  x=math.log(v+.5)
  if v<4096:s.T[k]=n+1,a+x,b+x*x
  return v
 def pexp(s,v):
  n,a=s.T.get('e',(1,100.));m=a/n
  v=s.pc(lambda x:1-math.exp(-x/m),v,1<<16,'e')
  if v<1<<16:s.T['e']=n+1,a+v
  return v
 def num(s,k,n):
  nb=s.ppm([(k,)],None if n is None else n.bit_length(),lambda x:s.u(64,x))
  if nb<2:return nb
  v=1
  for i in range(nb-2,-1,-1):v=v*2+s.bit((k,nb,i,v if nb-i<5 else 0),None if n is None else n>>i&1)
  return v
 def ppm(s,X,x,fb):
  T=s.T;ex=set();res=x;fd=0
  for k in X:
   t=T.get(k)
   if not t:continue
   it=[(a,n) for a,n in t.items() if a not in ex]
   if not it:continue
   es=len(it);tot=sum(n for _,n in it)+es
   if s.e:
    c=f=0
    for a,n in it:
     if a==x:f=n;break
     c+=n
    if f:s.go(tot,(c,f),0);fd=1;break
    s.go(tot,(tot-es,es),0)
   else:
    def g(y):
     c=0
     for a,n in it:
      if y<c+n:return c,n,a
      c+=n
     return c,es,ex
    r=s.go(tot,0,g)
    if r is not ex:res=r;fd=1;break
   ex.update(a for a,_ in it)
  if not fd:
   res=fb(x)
   if s.e:res=x
  for k in X:
   t=T.setdefault(k,{});t[res]=t.get(res,0)+1
   if t[res]>4000:
    for a in t:t[a]=t[a]+1>>1
  return res
 def lit(s,k,x):
  o=[];a=b='';i=0
  while 1:
   h=None
   if s.e:h=x[i] if i<len(x) else -1;i+=1
   h=s.ppm([('L',k,a,b),('L',k,b),('L',k)],h,s.ul)
   if h==-1:return ''.join(o)
   o.append(h);a,b=b,h
 def ul(s,c):
  if s.e:s.u(257,256 if c==-1 else ord(c));return c
  v=s.u(257,0)
  return -1 if v==256 else chr(v)
 def sym(s,X,x,k):return s.ppm(X,x,lambda v:s.lit(k,v))
 def f(s,k,x,n=2):return s.ppm([(k,)],x,lambda v:s.u(n,v))
PAT=re.compile(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z) (\S+) "(\S+) (\S+) (\S+)" (\d+) (\d+) (\d+)ms "([^"]*)" "([^"]*)"\Z')
EP=D.datetime(2000,1,1)
def fmt(t):return (EP+D.timedelta(milliseconds=t)).strftime('%Y-%m-%dT%H:%M:%S.')+'%03dZ'%(t%1000)
def pts(x):
 d=D.datetime.strptime(x[:19],'%Y-%m-%dT%H:%M:%S')-EP
 return d.days*86400000+d.seconds*1000+int(x[20:23])
def ipc(c,ip):
 p=None if ip is None else ip.split('.')
 if c.f('I',None if p is None else int(len(p)!=4 or any(not q.isdigit() or str(int(q))!=q or int(q)>255 for q in p))):return c.lit('I',ip)
 o=[]
 for i in range(4):
  v=None if p is None else int(p[i])
  o.append(c.ppm([('o',)],v,lambda v:c.u(256,v)) if i==0 else c.u(256,v))
 return '.'.join(map(str,o))
def rb(tp,nu,q):
 it=iter(nu)
 return re.sub(r'[#*]',lambda m:q if m.group()=='*' else str(next(it)),tp)
def uc(c,ip,me,url):
 mt=q=nu=None
 if c.e:
  m=re.search(r'q=([^&]*)',url);u2=url
  if m:q=m.group(1);u2=url[:m.start(1)]+'*'+url[m.end(1):]
  nu=[int(x) for x in re.findall(r'\d+',u2)];mt=me+' '+re.sub(r'\d+','#',u2)
  try:
   if rb(mt.split(' ',1)[1],nu,q)!=url:mt='!'
  except Exception:mt='!'
 mt=c.sym([('t',)],mt,'t')
 if mt=='!':return c.sym([('m',)],me,'m'),c.lit('u',url),mt,None
 me,tp=mt.split(' ',1);o=[];ps=tp.split('#')
 for j in range(len(ps)-1):
  k='#'.join(ps[:j+1]);X=[('n',k)]
  if len(c.T.get(X[0],()))!=1:X=[('n',k,ip)]+X
  o.append(c.ppm(X,None if nu is None else nu[j],lambda v:c.num(('N',k),v)))
 if '*' in tp:
  w=None if q is None else q.split('+')+[-1];r=[]
  while 1:
   x=None if w is None else w[len(r)]
   if c.f(('W',min(len(r),3)),None if x is None else int(x==-1)):break
   r.append(c.sym([('w',)],x,'w'))
  q='+'.join(r)
 return me,rb(tp,o,q),mt,q
def run(c,L=None):
 out=[];S={};ips=[];ix={};cn=[];pv=None;lt=0;i=0
 while 1:
  if c.e:
   ty=2
   if i<len(L):
    m=PAT.match(L[i]);ty=1
    if m:
     g=list(m.groups())
     if fmt(pts(g[0]))==g[0] and pts(g[0])>=lt and all(str(int(g[j]))==g[j] for j in(5,6,7)):ty=0
   i+=1
  else:ty=None;g=[None]*10
  ty=c.f('y',ty,3)
  if ty==2:return '\n'.join(out)
  if ty:out.append(c.lit('R',L and L[i-1]));continue
  ip=g[1]
  if not c.f('s',None if ip is None else int(ip==pv)):
   k=ix.get(ip,-1) if c.e else None
   if c.f('n',None if k is None else int(k<0)) if ips else 1:
    ip=ipc(c,ip);k=len(ips);ips.append(ip);ix[ip]=k;cn.append(0)
   else:
    pk=ix[pv];p0=cn[pk];cn[pk]=0
    if c.e:c.go(sum(cn),(sum(cn[:k]),cn[k]),0)
    else:A=list(AC(cn));k=c.go(A[-1],0,lambda t:(lambda j:(A[j]-cn[j],cn[j],j))(BR(A,t)))
    cn[pk]=p0;ip=ips[k]
   cn[k]+=2 if cn[k] else 1
  else:ip=pv
  pv=ip;new=ip not in S
  if new:S[ip]=[None,'']
  st=S[ip]
  t=lt=lt+c.pexp(None if g[0] is None else pts(g[0])-lt)
  me,url,cu,q=uc(c,ip,g[2],g[3])
  pr=c.sym([('p',)],g[4],'p')
  co=cu.rsplit('/',1)[0]
  if co.count('/')<2:co=cu
  sa=int(c.sym([('S',co),('S',)],g[5],'s'))
  z=None if g[6] is None else int(g[6])
  if q is None:z=c.ppm([('z',url,sa),('z',cu,sa),('z',sa)],z,lambda v:c.num(('Z',cu),v))
  else:
   o=37*len(q);v=None if z is None else z-o
   z=c.ppm([('q',sa)],v,lambda v:(lambda z:-(z+1>>1) if z&1 else z>>1)(c.num('Q',None if v is None else v*2 if v>=0 else -2*v-1)))+o
  la=c.plog((co,sa),None if g[7] is None else int(g[7]))
  rf=g[8];pu='https://shop.example.com'+st[1]
  rv=c.f(('r',new),None if rf is None else 0 if rf=='-' else 1 if rf==pu and not new else 2,3)
  rf='-' if rv==0 else pu if rv==1 else c.lit('f',rf)
  ua=g[9]
  if st[0] is None or c.f('a',None if ua is None else int(ua!=st[0])):ua=c.sym([('A',)],ua,'a')
  else:ua=st[0]
  st[0]=ua;st[1]=url
  if not c.e:out.append('%s %s "%s %s %s" %d %d %dms "%s" "%s"'%(fmt(t),ip,me,url,pr,sa,z,la,rf,ua))
if __name__=='__main__':sys.stdout.buffer.write(run(C(0,sys.stdin.buffer.read())).encode('latin-1'))
