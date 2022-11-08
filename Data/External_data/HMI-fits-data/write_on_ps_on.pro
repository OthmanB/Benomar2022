function write_on_ps_on,file

set_plot,'ps'
device,/landscape,font_size=12,filename=file+'.ps',/color,bits=8
device,/isolatin1,set_font='Times',/tt_font;,/encaps
!p.thick=4
!p.charthick=3

e=-1
return,e
end
