; given a background value and a frequency value,
; calculate the threshold
; p: smoothing coefficient
; background : level of the background
; level: rejection level in percent: typicially 90% or 95% (level = 0.90 or 0.95).
function proba_calc_smooth_signal, background, p, level
;; **** DEBUG ONLY ****
;background=100 & level=90 & p=4
;; ********************
level=level/100
;u=background*p*findgen(2100)/80 ; to obtain a constant window
u=background*p*findgen(8400)/320. ; to obtain a constant window

;f=u^(p-1) * exp(-u/background) / Gamma(p)

lnf=(p-1)*alog(u) - lngamma(p) - u/background ; the computation is done in log to avoid round off errors
f=exp(lnf)

du=u[1]-u[0]
sum0=0d & i=long(0)
while i lt n_elements(u) do begin ; compute the normalisation constant
	sum0=sum0+f[i]*du
	i=i+1
endwhile

sum=0d & i=long(0)
while sum le level AND i lt n_elements(u) do begin ; until the probability has reached level compute the sum
	sum=sum+f[i]*du/sum0
	s=u[i]
	i=i+1
endwhile
Proba=100d*sum

s=s/p ; normalisation !
;plot, u,f
;wait,0.75
print, Proba, s

;stop

return,s
end


function proba_calc_smooth_signal_simple, background, p
;; **** DEBUG ONLY ****
;background=100 & level=90 & p=4
;; ********************

;u=background*p*findgen(2100)/80 ; to obtain a constant window
;f=u^(p-1) * exp(-u/background) / Gamma(p)
;f=f*p^(p-1)/background^p ; modif according to Eq.2.7 of my PhD

u=background*findgen(2100)/80 ; to obtain a constant window
f=u^(p-1) * exp(-u*p/background) / Gamma(p)
f=f*p^(p-1)/background^p ; modif according to Eq.2.7 of my PhD

du=u[1]-u[0]
sum0=0d & i=long(0)
while i lt n_elements(u) do begin ; compute the normalisation constant
	sum0=sum0+f[i]*du
	i=i+1
endwhile

fout=f ;/sum0

output=dblarr(2, n_elements(u))
output[0,*]=u
output[1,*]=fout
return, output
end
