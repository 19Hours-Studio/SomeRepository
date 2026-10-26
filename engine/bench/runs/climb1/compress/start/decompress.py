import sys,time
from math import log,exp,erf
E=0
T=1<<24
class K:
 def __init__(s,d=None):
  s.g=(1<<48)-1
  if d is None:s.l=s.c=0;s.n=1;s.o=bytearray()
  else:s.d=d;s.p=7;s.v=int.from_bytes(d[1:7],'big')
 def sh(s):
  l=s.l
  if l<255<<40 or l>>48:
   c=l>>48;t=s.c
   while 1:
    s.o.append(t+c&255);t=255;s.n-=1
    if not s.n:break
   s.c=l>>40&255
  s.n+=1;s.l=(l&(1<<40)-1)<<8
 def e(s,c,f,t):
  r=s.g//t;s.l+=r*c;s.g=r*f
  while s.g<1<<40:s.g<<=8;s.sh()
 def fin(s):
  for _ in range(7):s.sh()
  return bytes(s.o)
 def gf(s,t):
  s.r=s.g//t;return min(s.v//s.r,t-1)
 def u(s,c,f):
  s.v-=c*s.r;s.g=s.r*f
  while s.g<1<<40:s.g<<=8;s.v=s.v<<8|(s.d[s.p] if s.p<len(s.d) else 0);s.p+=1
def cf(r,i):
 t=sum(r)
 if E:C.e(sum(r[:i]),r[i],t);return i
 v=C.gf(t);c=i=0
 while c+r[i]<=v:c+=r[i];i+=1
 C.u(c,r[i]);return i
def raw(v,n):
 while n>0:
  k=min(n,16);n-=k
  if E:C.e(v>>n&(1<<k)-1,1,1<<k)
  else:x=C.gf(1<<k);C.u(x,1);v=(v or 0)|x<<n
 return v
class B:
 def __init__(s):s.a=s.b=.4
 def __call__(s,b):
  p=min(max(int(4096*s.b/(s.a+s.b)),1),4095)
  b=cf([p,4096-p],0 if b else 1)==0
  if b:s.b+=1
  else:s.a+=1
  if s.a+s.b>4096:s.a/=2;s.b/=2
  return b
X=object()
class F:
 def __init__(s,n=8):s.s=[X];s.c=[1];s.x={};s.i=n
 def __call__(s,v):
  i=cf(s.c,s.x.get(v,0) if E else 0)
  if i:s.c[i]+=s.i
  return s.s[i]
 def add(s,v):s.x[v]=len(s.s);s.s.append(v);s.c.append(s.i);s.c[0]+=1
D={}
def M(k,f=F):
 if k not in D:D[k]=f()
 return D[k]
def sym(k,v,l=None,n=8):
 m=M(k,lambda:F(n));r=m(v)
 if r is X:r=(l or st)(v);m.add(r)
 return r
def fl(k,b):return M(k,B)(b)
def num(k,v):
 b=sym(('n',k),v.bit_length() if E else None,lambda x:raw(x,7))
 if b<2:return b
 z=1;n=b-1;t=min(n,3)
 for j in range(t):z=z*2+fl(('b',k,b,z),v>>n-1-j&1 if E else None)
 n-=t
 return z<<n|raw(v&(1<<n)-1 if E else None,n) if n else z
def cdf(k,v,G,h):
 S=T-h-2;cu=lambda x:int(G(x-.5)*S)+x;p=cu(h+1)
 if E:
  if v>h:C.e(p,T-p,T);return num(k,v-h-1)+h+1
  a=cu(v);C.e(a,cu(v+1)-a,T);return v
 t=C.gf(T)
 if t>=p:C.u(p,T-p);return num(k,None)+h+1
 a=0
 while a<h:
  m=a+h+1>>1
  if cu(m)<=t:a=m
  else:h=m-1
 m=cu(a);C.u(m,cu(a+1)-m);return a
class LN:
 def __init__(s):s.n=2;s.s=6;s.q=20
 def __call__(s,k,v):
  n=s.n;m=s.s/n;d=max((s.q/n-m*m)**.5,.03)*2**.5
  v=cdf(k,v,lambda x:x>0 and .5*(1+erf((log(x)-m)/d)),8191)
  l=log(max(v,.5));s.n+=1;s.s+=l;s.q+=l*l;return v
def st(s):
 n=num('sl',len(s) if E else None);o=''
 for i in range(n):o+=sym(('c',o[-2:]),s[i] if E else None,lambda x:sym('c0',x,lambda y:chr(raw(ord(y) if E else None,8))),4)
 return o
def wd(s):
 n=num('wn',s.count(' ')+1 if E else None);p='';o=[]
 for x in s.split(' ') if E else[None]*n:p=sym(('w',p),x,lambda y:sym('w0',y),4);o.append(p)
 return' '.join(o)
H='https://shop.example.com'
P={'i':'/api/v2/items/%s','r':'/api/v2/items/%s/reviews?page=%s','c':'/api/v2/users/%s/cart','g':'/static/img/%s.png','j':'/static/js/app.%s.js','s':'/search?q=%s'}
def mp(c,a):
 if c[0]=='=':return c[1:]
 return P[c]%(('+'.join(a),) if c=='s' else tuple(a))
def fm(r):
 ms,ip,mc,a,pr,s,z,la,rf,ua=r;t=time.gmtime(ms//1000)
 return'%04d-%02d-%02dT%02d:%02d:%02d.%03dZ %d.%d.%d.%d "%s %s %s" %s %d %dms "%s" "%s"'%(*t[:6],ms%1000,*ip,mc[0],mp(mc[1],a),pr,s,z,la,rf,ua)
class O:pass
def it(S,h,v):
 I=S.gi;g=S.gc;e=1+len(I);k=16/(S.gt+e)
 w=[e*k]+[h.get(j,0)+g[j]*k for j in I];c=(T-len(w))/sum(w)
 if E:v=int(v)
 i=cf([int(x*c)+1 for x in w],I.index(v)+1 if E and v in g else 0)
 if i:v=I[i-1]
 else:v=num('gi',v);I.append(v);g[v]=0
 g[v]+=1;S.gt+=1;h[v]=h.get(v,0)+1;return str(v)
def nip(ip):return(sym('o1',ip[0] if E else None,lambda x:raw(x,8)),)+tuple(raw(ip[j] if E else None,8)for j in(1,2,3))
def line(S,f):
 ms,ip,mc,a,pr,s,z,la,rf,ua=f or[None]*10
 d=ms-S.t if E else None
 n=fl('tn',d<0 if E else None)
 m=(S.t-S.t0)/(S.nl-1) if S.nl>10 else 250
 x=cdf('dt',abs(d) if E else None,lambda x:x>0 and 1-exp(-x/m),1<<14)
 ms=S.t=S.t+(-x if n else x)
 if not S.nl:S.t0=ms
 S.nl+=1
 if S.pi and fl('r0',ip==S.pi if E else None):ip=S.pi
 else:ip=sym('ip',ip,nip,1)
 q=S.ips.get(ip);nw=q is None
 if nw:q=S.ips[ip]=O();q.ua=q.pa=q.us=None;q.it={}
 S.pi=ip
 if nw or not fl('U',ua==q.ua if E else None):q.ua=sym('ua',ua,wd)
 ua=q.ua
 mc=sym('mc',mc,lambda x:(st(x[0] if E else None),st(x[1] if E else None)))
 c=mc[1]
 if c=='i':a=(it(S,q.it,a[0] if E else None),)
 elif c=='r':a=(it(S,q.it,a[0] if E else None),str(num('pg',int(a[1]) if E else None)))
 elif c=='c':
  u=int(a[0]) if E else None
  if not fl(('us',q.us is None),u==q.us if E else None):q.us=num('u',u)
  a=(str(q.us),)
 elif c=='s':
  n=sym('sn',len(a) if E else None,lambda x:num('sn',x))
  a=[sym('sw',a[j] if E else None) for j in range(n)]
 elif c in('g','j'):a=(sym(('nm',c),a[0] if E else None),)
 else:a=()
 pr=sym('pr',pr)
 s=sym(('st',mc),s)
 pa=mp(c,a)
 k=('c',a[0],s) if c=='c' else(pa,s)
 p=S.sz.get(k)
 if p is None and s!='200':p=S.sz.get(s)
 h=0
 if c=='s' and s=='200':
  b=800+37*(len(pa)-10)
  if fl('sr',0<=z-b<16 if E else None):z=b+sym('sd',z-b if E else None,lambda x:raw(x,4));h=1
 if not h and p is not None:
  h=fl(('sh',c,s),z==p if E else None)
  if h:z=p
 if not h:z=num(('sz',c),z)
 S.sz[k]=z
 if s!='200':S.sz[s]=z
 k='5' if s=='500' else'g' if c in('g','j') else c
 la=M(('la',k),LN)(('la',k),la)
 p=H+q.pa if q.pa else None
 r=sym(('rf',nw),(0 if rf=='-' else 1 if rf==p else 2) if E else None,lambda x:num('rf',x))
 rf='-' if r==0 else p if r==1 else sym('ro',rf)
 q.pa=pa
 return ms,ip,mc,a,pr,s,z,la,rf,ua
def run(L=None):
 S=O();S.ips={};S.t=S.nl=0;S.pi=None;S.sz={};S.gi=[];S.gc={};S.gt=0
 n=num('L',len(L) if E else None);o=[]
 for i in range(n):
  f=parse(L[i]) if E else None
  o.append(fm(line(S,f)) if fl('ok',f is not None if E else None) else st(L[i] if E else None))
 return o
if __name__=='__main__':C=K(sys.stdin.buffer.read());sys.stdout.buffer.write('\n'.join(run()).encode('latin-1'))
