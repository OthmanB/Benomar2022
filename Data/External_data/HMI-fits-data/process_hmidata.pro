@legend
pro process_hmidata_m6

	file='/Volumes/home/2020/HMI-fits-data/hmi-2020.m6.txt'
	Nmax=24
	Kmax=40
	data=read_Ncolumns(file, Nmax, Kmax, ref_N=2, spectrum=0)
	data=transpose(data)
	
	col_el=0
	col_nu=2

	col_a1=12
	col_a2=13
	col_a3=14
	col_a4=15
	col_a5=16

	col_err_a1=24-6
	col_err_a2=24-5
	col_err_a3=24-4
	col_err_a4=24-3
	col_err_a5=24-2
	col_err_a6=24-1

	pos_lrot=where(data[col_el,*] ge 1)
	pos_l1=where(data[col_el,*] eq 1)
	pos_l2=where(data[col_el,*] eq 2)
	pos_l3=where(data[col_el,*] eq 3)

	fit_a1=poly_fit(data[col_nu, pos_lrot], data[col_a1, pos_lrot], 1, MEASURE_ERRORS=data[col_a1,pos_lrot], sigma=err_fit_a1, /double, yfit=best_fit_a1, yerror=mean_yerr_a1)
	fit_a2=poly_fit(data[col_nu, pos_lrot], data[col_a2, pos_lrot], 2, MEASURE_ERRORS=data[col_a2,pos_lrot], sigma=err_fit_a2, /double, yfit=best_fit_a2, yerror=mean_yerr_a2)
	fit_a3=poly_fit(data[col_nu, [pos_l2,pos_l3]], data[col_a3, [pos_l2,pos_l3]], 2, MEASURE_ERRORS=data[col_a3,pos_lrot], sigma=err_fit_a3, /double, yfit=best_fit_a3, yerror=mean_yerr_a3)

	e=write_on_ps_on('a1_nu')	
	plot, data[col_nu, *], data[col_a1, *], color=fsc_color('Black'), background=fsc_color('White'), /nodata, xtitle='Frequency (microHz)', ytitle='a1 (microHz)', charsize=1.5
	oplot, data[col_nu, pos_l1], data[col_a1,pos_l1], color=fsc_color('Blue')
	oplot, data[col_nu, pos_l2], data[col_a1,pos_l2], color=fsc_color('Red')
	oplot, data[col_nu, pos_l3], data[col_a1,pos_l3], color=fsc_color('Brown')
	errplot, data[col_nu, pos_l1], data[col_a1,pos_l1]-data[col_err_a1,pos_l1], data[col_a1,pos_l1] + data[col_err_a1,pos_l1], color=fsc_color('Blue')
	errplot, data[col_nu, pos_l1], data[col_a1,pos_l2]-data[col_err_a1,pos_l2], data[col_a1,pos_l2] + data[col_err_a1,pos_l2], color=fsc_color('Red')
	errplot, data[col_nu, pos_l1], data[col_a1,pos_l3]-data[col_err_a1,pos_l3], data[col_a1,pos_l3] + data[col_err_a1,pos_l3], color=fsc_color('Brown')
	nu=data[col_nu, pos_lrot]
	s=sort(nu)
	oplot, nu[s], best_fit_a1[s], color=fsc_color('Black'), linestyle=2, thick=2
	;errplot, nu[s[0]], best_fit_a1[s[0]] -best_fit_err_a1[s[0]],  best_fit_a1[s[n_elements(s)-1]] +best_fit_err_a1[s[n_elements(s)-1]], color=fsc_color('Black'), thick=2
	errplot, nu[s[0]], best_fit_a1[s[0]] -mean_yerr_a1,  best_fit_a1[s[0]] + mean_yerr_a1, color=fsc_color('Black'), thick=2
	errplot, nu[s[n_elements(s)-1]], best_fit_a1[s[n_elements(s)-1]] -mean_yerr_a1,  best_fit_a1[s[n_elements(s)-1]] + mean_yerr_a1, color=fsc_color('Black'), thick=2

	legend, ['l=1', 'l=2', 'l=3'], pos=[0.15,0.25], /norm, textcolor=fsc_color('Black'), $
		psym=[1,1,1], colors=[fsc_color('Blue'), fsc_color('Red'),fsc_color('Brown')],$
		charsize=1.4
	e=write_on_ps_off('')

	e=write_on_ps_on('a2_nu')	
	plot, data[col_nu, *], data[col_a2, *], color=fsc_color('Black'), background=fsc_color('White'), /nodata, xtitle='Frequency (microHz)', ytitle='a2 (microHz)', charsize=1.5
	oplot, data[col_nu, pos_l1], data[col_a2,pos_l1], color=fsc_color('Blue')
	oplot, data[col_nu, pos_l2], data[col_a2,pos_l2], color=fsc_color('Red')
	oplot, data[col_nu, pos_l3], data[col_a2,pos_l3], color=fsc_color('Brown')
	errplot, data[col_nu, pos_l1], data[col_a2,pos_l1]-data[col_err_a2,pos_l1], data[col_a2,pos_l1] + data[col_err_a2,pos_l1], color=fsc_color('Blue')
	errplot, data[col_nu, pos_l2], data[col_a2,pos_l2]-data[col_err_a2,pos_l2], data[col_a2,pos_l2] + data[col_err_a2,pos_l2], color=fsc_color('Red')
	errplot, data[col_nu, pos_l3], data[col_a2,pos_l3]-data[col_err_a2,pos_l3], data[col_a2,pos_l3] + data[col_err_a2,pos_l3], color=fsc_color('Brown')
	nu=data[col_nu, pos_lrot]
	s=sort(nu)
	oplot, nu[s], best_fit_a2[s], color=fsc_color('Black'), linestyle=2, thick=2
	;errplot, nu[s[0]], best_fit_a1[s[0]] -best_fit_err_a1[s[0]],  best_fit_a1[s[n_elements(s)-1]] +best_fit_err_a1[s[n_elements(s)-1]], color=fsc_color('Black'), thick=2
	errplot, nu[s[0]], best_fit_a2[s[0]] -mean_yerr_a2,  best_fit_a2[s[0]] + mean_yerr_a2, color=fsc_color('Black'), thick=2
	errplot, nu[s[n_elements(s)-1]], best_fit_a2[s[n_elements(s)-1]] -mean_yerr_a2,  best_fit_a2[s[n_elements(s)-1]] + mean_yerr_a2, color=fsc_color('Black'), thick=2

	legend, ['l=1', 'l=2', 'l=3'], pos=[0.15,0.25], /norm, textcolor=fsc_color('Black'), $
		psym=[1,1,1], colors=[fsc_color('Blue'), fsc_color('Red'),fsc_color('Brown')],$
		charsize=1.4
	e=write_on_ps_off('')

	e=write_on_ps_on('a3_nu')	
	plot, data[col_nu, *], data[col_a3, *], color=fsc_color('Black'), background=fsc_color('White'), /nodata, xtitle='Frequency (microHz)', ytitle='a3 (microHz)', charsize=1.5
	;oplot, data[col_nu, pos_l1], data[col_a3,pos_l1], color=fsc_color('Blue')
	oplot, data[col_nu, pos_l2], data[col_a3,pos_l2], color=fsc_color('Red')
	oplot, data[col_nu, pos_l3], data[col_a3,pos_l3], color=fsc_color('Brown')
	;errplot, data[col_nu, pos_l1], data[col_a3,pos_l1]-data[col_err_a3,pos_l1], data[col_a3,pos_l1] + data[col_err_a3,pos_l1], color=fsc_color('Blue')
	errplot, data[col_nu, pos_l2], data[col_a3,pos_l2]-data[col_err_a3,pos_l2], data[col_a3,pos_l2] + data[col_err_a3,pos_l2], color=fsc_color('Red')
	errplot, data[col_nu, pos_l3], data[col_a3,pos_l3]-data[col_err_a3,pos_l3], data[col_a3,pos_l3] + data[col_err_a3,pos_l3], color=fsc_color('Brown')
	nu=data[col_nu, [pos_l2,pos_l3]]
	s=sort(nu)
	oplot, nu[s], best_fit_a3[s], color=fsc_color('Black'), linestyle=2, thick=2
	;errplot, nu[s[0]], best_fit_a1[s[0]] -best_fit_err_a1[s[0]],  best_fit_a1[s[n_elements(s)-1]] +best_fit_err_a1[s[n_elements(s)-1]], color=fsc_color('Black'), thick=2
	errplot, nu[s[0]], best_fit_a3[s[0]] -mean_yerr_a3,  best_fit_a3[s[0]] + mean_yerr_a3, color=fsc_color('Black'), thick=2
	errplot, nu[s[n_elements(s)-1]], best_fit_a3[s[n_elements(s)-1]] -mean_yerr_a3,  best_fit_a3[s[n_elements(s)-1]] + mean_yerr_a3, color=fsc_color('Black'), thick=2

	legend, ['l=1', 'l=2', 'l=3'], pos=[0.1,0.2], /norm, textcolor=fsc_color('Black'), $
		psym=[1,1,1], colors=[fsc_color('Blue'), fsc_color('Red'),fsc_color('Brown')],$
		charsize=1.4
	e=write_on_ps_off('')
	stop
end


; N: number of columns
; K: maximum number of lines
function read_Ncolumns, file,N, K, skip=skip, ref_N=ref_N, spectrum=spectrum

if n_elements(skip) eq 0 then skip=1 ; defaut we skip one line only
if n_elements(ref_N) eq 0 then ref_N=1 ; defaut we identify the zero non-used tab elements with column 1
if n_elements(spectrum) eq 0 then spectrum=1
openr, 3, file

	param=dblarr(K,N)
	a=''
	i=0d
      while EOF(3) ne 1 do begin
      	if i lt skip then readf,3,format='(q)'
        if i ge skip then begin
          	readf,3,a ; read data
          	uu=strsplit(a)
          	N_uu=N_elements(uu)-1
          	for j=0,N_uu-1 do begin
          		param(i,j)=float(strmid(a,uu(j),uu(j+1)-uu(j)-1))
          	endfor
			param(i, N_uu)= float(strmid(a,uu(N_uu),uu(N_uu)-uu(N_uu-1)+ 10))
		endif
		i=i+1
      endwhile

close,3
param0=param
test=where(param[*,ref_N] ne 0)

param=param[test,*]
print, 'END read'
if spectrum eq 0 then begin
	save, param, filename=file+'.sav'
endif else begin
	freq=dblarr(1, n_elements(param[*,0]))
	spec_reg=freq
	freq[0,*]=param[*,0]
	spec_reg[0,*]=param[*,1]
	save, freq, spec_reg, filename=file+'.sav'
endelse

return,param
end
