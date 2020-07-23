pro abun

dir = '/home/terese/projects/Gjoll/plot/'

N3201 = dir + 'N3201_red.tab'
Carretta = dir + 'Carretta.tab'
Carretta_u = dir + 'Carretta_upper.tab'
Gjoll1 = dir + 'Gjoll1.tab'
Gjoll2 = dir + 'Gjoll2.tab'
Gjoll4 = dir + 'Gjoll4.tab'
Gjoll5 = dir + 'Gjoll5.tab'
Magurno = dir + 'Magurno18.tab'

readcol, Gjoll1, star1,Fe1,C1,Na1,Mg1,Al1,Si1,Ca1,Sc1,Ti1,Cr1,Mn1,Co1,Ni1,Cu1,Zn1,Sr1,Y1,Zr1,Ba1,La1,Ce1,Nd1,Eu1, format='a,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d'
readcol, Gjoll2, star2,Fe2,C2,Na2,Mg2,Al2,Si2,Ca2,Sc2,Ti2,Cr2,Mn2,Co2,Ni2,Cu2,Zn2,Sr2,Y2,Zr2,Ba2,La2,Ce2,Nd2,Eu2, format='a,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d'
readcol, Gjoll4, star4,Fe4,C4,Na4,Mg4,Al4,Si4,Ca4,Sc4,Ti4,Cr4,Mn4,Co4,Ni4,Cu4,Zn4,Sr4,Y4,Zr4,Ba4,La4,Ce4,Nd4,Eu4, format='a,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d'
readcol, Gjoll5, star5,Fe5,C5,Na5,Mg5,Al5,Si5,Ca5,Sc5,Ti5,Cr5,Mn5,Co5,Ni5,Cu5,Zn5,Sr5,Y5,Zr5,Ba5,La5,Ce5,Nd5,Eu5, format='a,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d'


readcol, N3201, NFe,NC,NN,NO,NNa,NMg,NAl,NSi,NK,NCa,NCe,format='d,d,d,d,d,d,d,d,d,d,d'
readcol, Carretta, star, CFe, CO, CNa, CMg,CAl,CSi,format='d,d,d,d,d,d,d'
readcol, Carretta_u, star, CuFe, CuO, CuNa,CuMg,CuAl,CuSi,format='d,d,d,d,d,d,d'
readcol, Magurno, Mstar, MFe, MMg, MCa, MTi,MSc, MCr,MNi,MZn, MY ,format='a,d,d,d,d,d,d,d,d,d'


alpha1=(Mg1+Si1+Ca1)/3 ;+Ti1
alpha2=(Mg2+Si2+Ca1)/3
alpha4=(Mg4+Si4+Ca1)/3
alpha5=(Mg4+Si4+Ca1)/3
Calpha=(CMg+CSi)/2
Nalpha=(NMg+NSi+NCa)/3



set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'AlMg.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Mg1,Al1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-1,1],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-1.5,1.5],ythick=4.9,ycharsize=1.2,ytitle='[Al/Fe]',xtitle='[Mg/Fe]',/nodata
loadct,0
plotsym, 0, 0.7, /fil
oplot,NMg,NAl,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 5, 0.7, /fil
oplot,CuMg,CuAl,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 8, 0.7, /fil
oplot,CMg,CAl,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 5, 0.7, /fill
oplot,Mg1,Al1,psym=8,symsize=2.5,thick=3.6
plotsym, 3, 0.7, /fill
oplot,Mg2,Al2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Mg4,Al4,psym=8,symsize=2.5,thick=3.6, color=100
oplot,Mg5,Al5,psym=8,symsize=2.5,thick=3.6, color=200


device,/close
set_plot,'X'

set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'AlSi.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Si1,Al1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-0.5,1],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-1.5,1.5],ythick=4.9,ycharsize=1.2,ytitle='[Al/Fe]',xtitle='[Si/Fe]',/nodata
loadct,0
plotsym, 0, 0.7, /fil
oplot,NSi,NAl,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 5, 0.7, /fil
oplot,CuSi,CuAl,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 8, 0.7, /fil
oplot,CSi,CAl,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 5, 0.7, /fill
oplot,Si1,Al1,psym=8,symsize=2.5,thick=3.6
plotsym, 3, 0.7, /fill
oplot,Si2,Al2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Si4,Al4,psym=8,symsize=2.5,thick=3.6, color=100
oplot,Si5,Al5,psym=8,symsize=2.5,thick=3.6, color=200


device,/close
set_plot,'X'

set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'MgSi.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Si1,Mg1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-0.5,1],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,1.0],ythick=4.9,ycharsize=1.2,ytitle='[Mg/Fe]',xtitle='[Si/Fe]',/nodata
loadct,0
plotsym, 0, 0.7, /fil
oplot,NSi,NMg,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 8, 0.7, /fil
oplot,CSi,CMg,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Si1,Mg1,psym=8,symsize=2.5,thick=3.6
oplot,Si2,Mg2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Si4,Mg4,psym=8,symsize=2.5,thick=3.6, color=100
oplot,Si5,Mg5,psym=8,symsize=2.5,thick=3.6, color=200

device,/close
set_plot,'X'


set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'AlNa.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Na1,Al1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-0.5,1],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-1.2,1.0],ythick=4.9,ycharsize=1.2,ytitle='[Al/Fe]',xtitle='[Na/Fe]',/nodata
loadct,0
plotsym, 5, 0.7, /fil
oplot,CuNa,CuAl,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 8, 0.7, /fil
oplot,CNa,CAl,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 5, 0.7, /fill
oplot,Na1,Al1,psym=8,symsize=2.5,thick=3.6
plotsym, 3, 0.7, /fill
oplot,Na2,Al2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Na4,Al4,psym=8,symsize=2.5,thick=3.6, color=100
oplot,Na5,Al5,psym=8,symsize=2.5,thick=3.6, color=200


device,/close
set_plot,'X'


set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'alpha.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,alpha1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.5],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,1.0],ythick=4.9,ycharsize=1.2,ytitle='[alpha/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 0, 0.7, /fil
oplot,NFe,Nalpha,psym=8,symsize=1.5,thick=1.0, color=200
plotsym, 8, 0.7, /fil
oplot,CFe,Calpha,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,alpha1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,alpha2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,alpha4,psym=8,symsize=2.5,thick=3.6, color=100
oplot,Fe5,alpha5,psym=8,symsize=2.5,thick=3.6, color=200


device,/close
set_plot,'X'



set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'YFe.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,Y1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.8],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,0.8],ythick=4.9,ycharsize=1.2,ytitle='[Y/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 3, 0.7, /fil
oplot,MFe,MY,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,Y1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,Y2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,Y4,psym=8,symsize=2.5,thick=3.6, color=100


device,/close
set_plot,'X'



set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'ScFe.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,Sc1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.8],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,0.8],ythick=4.9,ycharsize=1.2,ytitle='[Sc/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 3, 0.7, /fil
oplot,MFe,MSc,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,Sc1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,Sc2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,Sc4,psym=8,symsize=2.5,thick=3.6, color=100


device,/close
set_plot,'X'


set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'CrFe.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,Cr1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.8],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,0.8],ythick=4.9,ycharsize=1.2,ytitle='[Cr/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 3, 0.7, /fil
oplot,MFe,MCr,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,Cr1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,Cr2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,Cr4,psym=8,symsize=2.5,thick=3.6, color=100

device,/close
set_plot,'X'



set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'NiFe.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,Ni1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.8],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,0.8],ythick=4.9,ycharsize=1.2,ytitle='[Ni/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 3, 0.7, /fil
oplot,MFe,MNi,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,Ni1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,Ni2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,Ni4,psym=8,symsize=2.5,thick=3.6, color=100


device,/close
set_plot,'X'



set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'ZnFe.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,Zn1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.8],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-0.5,0.8],ythick=4.9,ycharsize=1.2,ytitle='[Zn/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 3, 0.7, /fil
oplot,MFe,MZn,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,Zn1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,Zn2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,Zn4,psym=8,symsize=2.5,thick=3.6, color=100


device,/close
set_plot,'X'

set_plot,'PS'
!P.font=0
;!P.MULTI = [0, 1, 2]
device,filename= dir+'CeFe.eps',font_size=15,decomposed=0,/color,xsize=10,ysize=10
;/encapsulated

plot,Fe1,Ce1,xstyle=1,xtickinterval=0.5,xminor=5,xrange=[-2.0,-0.8],xthick=4.9,xcharsize=1.2,ystyle=1,ytickinterval=0.5,yminor=5,yrange=[-1.0,2.0],ythick=4.9,ycharsize=1.2,ytitle='[Ce/Fe]',xtitle='[Fe/H]',/nodata
loadct,0
plotsym, 0, 0.7, /fil
oplot,NFe,NCe,psym=8,symsize=1.5,thick=1.0, color=200
loadct,4
plotsym, 3, 0.7, /fill
oplot,Fe1,Ce1,psym=8,symsize=2.5,thick=3.6
oplot,Fe2,Ce2,psym=8,symsize=2.5,thick=3.6, color=50
oplot,Fe4,Ce4,psym=8,symsize=2.5,thick=3.6, color=100


device,/close
set_plot,'X'



end
