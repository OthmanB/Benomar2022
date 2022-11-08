function write_on_ps_off,file, setplot=setplot

if n_elements(setplot) eq 0 then setplot='X'

device,/close
set_plot, setplot
!p.thick=2.

e=0
return,e
end

