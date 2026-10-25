# Marginal cost per incremental t Ni-eq: sorting at shaft bottom vs new deep shaft vs selective mining
crf=0.1455; Ni=15500; pay=0.75; down=0.25; c_mine=60; f=0.65; s=3.0
H=2.0e6
for name,V in (('Talnakh avg',484),('cuprous',723),('massive',1269)):
  for tn,(r,L) in (('Selebi 15%/2%',(0.152,0.02)),('stringer 44%/4%',(0.44,0.04))):
    rr=r*f; LL=L*f
    dNi=H*V*pay*((1-LL)/(1-rr)-1)/Ni                      # t Ni-eq/yr gained
    dcost=H*rr/(1-rr)*c_mine + H/(1-rr)*f*s - H*rr/(1-rr)*6 + 25e6*crf + dNi*Ni*down
    # new shaft giving the same dNi: hoist extra ore at the same grade; capex $400-600 per t/yr (2 km, ASSUMED, ~10 yr build)
    dore=dNi*Ni/(V*pay)
    shaft=[dore*(c_mine+3+12+2+40)+dore*cx*crf+dNi*Ni*down for cx in (400,600)]
    print(f"{name:12s} {tn:16s} +{dNi:6.0f} t Ni-eq/yr: sorting ${dcost/dNi:5.0f}/t vs new shaft ${shaft[0]/dNi:5.0f}-{shaft[1]/dNi:5.0f}/t  ratio {shaft[0]/dcost:.2f}-{shaft[1]/dcost:.2f}")
