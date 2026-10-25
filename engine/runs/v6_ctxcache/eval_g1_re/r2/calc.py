from scipy.optimize import brentq
# IDEA1
for e in [0.05,0.1,0.2,0.3,0.5,1]:
    base=(1-e)+e*6.11; new=(1-e)+e*1.022
    for ka in [1.0,1.1]:
        g=base/new*ka
        bill=1/(0.9/g+0.1)
        print('I1 edit share',e,'ka',ka,'input gain',round(g,2),'bill gain',round(1/(0.9/g+0.1),2))
print('I1 need input gain',0.9/(1/2.4-0.1), 'input price frac',(1/2.4-0.1)/0.9)
# IDEA2
f=0.685
c=lambda r:r*.1+(1-r)*1.25
for z,r in [(1.05,.4),(1.2,.546),(1.5,.768)]:
    print('I2',z,r,'bill gain',1/(f*c(r)+1-f))
print('req r',(1.25-((1/1.5-(1-f))/f))/1.15)
# IDEA 5 variants: match 1.52,1.43,1.35,1.22
def ratio(m,mode):
    sh=0.01
    if mode=='A': #0.242 of prefill
        b=.45+.55*.242; ex=.45+.55*(.83+.031); base=.45+.55*.83; s=.55*sh
    if mode=='B': # 0.242,0.83 are whole-bill
        b=.242; ex=.83+.031*.55; base=.83; s=sh*.55
    return base/((1-m)*b+m*ex+s)
for m in [.1,.2,.3,.5]: print('I5',m,round(ratio(m,'A'),3),round(ratio(m,'B'),3))
for mode in 'AB':
    print(mode,'m for 1.5x',brentq(lambda m:ratio(m,mode)-1.5,0,.9) if ratio(0,mode)>1.5 else None, 'm=0 ratio',ratio(0,mode))
    print(mode,'m for 1.2x',brentq(lambda m:ratio(m,mode)-1.2,0,.99))
# IDEA 3 : blended 0.45+.55*.15, fallback = canonical baseline
for h in [.15,.31,.5]:
    B=.45+.55*(1-h); bl=.45+.55*.15+.0055
    need=(B/1.5)
    a=(B-need)/(B-bl) if B>bl else None
    print('I3 h',h,'B',round(B,3),'blend',round(bl,3),'max ratio',round(B/bl,2),'accept needed',round(a,3))
# Idea 4
print('I4 breakeven', .1/(1.25-.1), .1/1.25)
