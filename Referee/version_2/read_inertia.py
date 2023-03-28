import numpy as np
import matplotlib.pyplot as plt

def readfile_inertia(filename):
	'''
		A function that is able to read the text file created when running getstats (the tamcmc program that unpack data from the bin files)
	'''
	f=open(filename)
	txt=f.read()
	f.close()
	data=txt.split('\n')
	header=[]
	l=[]
	n=[]
	freq=[]
	Enl=[]
	for d in data:
		if d != "":
			s=d.split()
			if len(s) !=0:
				if s[0] == '#':
					header.append(d)
				else:
					l.append(int(s[0]))
					n.append(int(s[1]))
					freq.append(float(s[2]))
					Enl.append(float(s[3]))
	l=np.asarray(l, dtype=int)
	n=np.asarray(n, dtype=int)
	freq=np.asarray(freq, dtype=float)
	Enl=np.asarray(Enl, dtype=float)
	return l, n, freq, Enl, header

def Sun_amplitudes():
	fl0=[2362.754652, 2496.207408, 2629.700990, 2764.194734, 2899.031511, 3033.769345, 3168.578778, 3303.519149, 3439.058142, 3574.879492]
	amp=[1.618363, 2.301488, 2.749593, 3.523089, 4.027574, 4.274778, 4.234953, 3.648111, 3.108513, 2.582393]
	err_m=[0.053215, 0.044633, 0.050881, 0.055439, 0.060170, 0.057786, 0.055940, 0.048371, 0.038677, 0.034232]
	err_p=[0.052677, 0.046359, 0.050444, 0.057119, 0.059159, 0.057241, 0.055940, 0.048592, 0.037760, 0.033069]
	err=np.zeros((2,len(err_m)))
	err[0,:]=err_m
	err[1,:]=err_p
	return np.asarray(fl0), np.asarray(amp), err

def CygA_amplitudes():
	fl0=[1287.738892, 1391.634203, 1495.004594, 1598.683101, 1700.955247, 1802.324679, 1904.603287, 2007.584631, 2110.910082, 2214.269283, 2317.323738, 2420.930865, 2524.984352, 2629.322219, 2734.468211, 2839.586678, 2945.062088]
	amp=[1.030822, 1.171271, 1.474194, 1.943198, 2.552678, 3.247293, 4.166310, 4.978876, 6.258428, 5.846397, 5.927594, 4.611643, 3.629551, 2.756326, 2.184808, 1.547202, 1.208433]
	err_m=[0.159187, 0.167631, 0.113678, 0.111304, 0.098276, 0.107168, 0.108029, 0.152502, 0.121841, 0.168225, 0.109684, 0.100547, 0.075628, 0.067979, 0.061839, 0.073298, 0.071621]
	err_p=[0.167942, 0.166927, 0.115093, 0.110832, 0.106500, 0.097768, 0.115531, 0.141650, 0.114337, 0.156543, 0.115193, 0.096055, 0.073806, 0.067979, 0.066437, 0.072170, 0.067514]
	err=np.zeros((2,len(err_m)))
	err[0,:]=err_m
	err[1,:]=err_p
	return np.asarray(fl0), np.asarray(amp), err

def CygB_amplitudes():
	fl0=[1578.284353, 1695.079515, 1812.437430, 1928.917359, 2044.308005, 2159.615004, 2275.987441, 2392.707680, 2509.661293, 2626.417643, 2743.335203, 2860.716767, 2978.337302, 3096.350173, 3215.752708, 3335.444896]
	amp=[0.283019, 1.349569, 1.510762, 2.005872, 2.417896, 2.975010, 3.612221, 4.947690, 4.792772, 5.588420, 4.582097, 3.488650, 2.764784, 2.100429, 1.658860, 1.398136]
	err_m=[0.53380, 0.11374, 0.09568, 0.09023, 0.09306, 0.09436, 0.09386, 0.11421, 0.13264, 0.10976, 0.09867, 0.08061, 0.05716, 0.06297, 0.06537, 0.06578]
	err_p=[0.150447, 0.117736, 0.094059, 0.095546, 0.104331, 0.090523, 0.102971, 0.110298, 0.129730, 0.114255, 0.097206, 0.071522, 0.061514, 0.061524, 0.065729, 0.067237]
	err=np.zeros((2,len(err_m)))
	err[0,:]=err_m
	err[1,:]=err_p
	return np.asarray(fl0), np.asarray(amp), err

def show_inertia(filename, frange_inertia, frange_obs, fileout, fl0, amp, err_a, title='', ylim_inertia=[0, 4e-8], ylim_amp=[0,5]):
	posOK=np.where(np.bitwise_and(fl0 >= frange_obs[0], fl0 <= frange_obs[1]))[0]
	fl0=fl0[posOK]
	amp=amp[posOK]
	err_a=err_a[:,posOK]
	#
	l,n,freq, Enl,header=readfile_inertia(filename)
	fig, ax=plt.subplots(1)
	ax2=ax.twinx()
	posOK=np.where(np.bitwise_and(freq >= frange_inertia[0], freq <= frange_inertia[1]))[0]
	l=l[posOK]
	n=n[posOK]
	freq=freq[posOK]
	Enl=Enl[posOK]
	#
	els=[1,2,3]
	mark=['p','o','x','s']
	col=['gray','black', 'red', 'blue']
	msize=[8, 8,8,8]
	#
	for el in els:
		posl=np.where(l == el)[0]
		#print(l[posl])
		#ax.plot(freq[posl], Enl[posl], marker=mark[el], color=col[el], markersize=msize[el], fillstyle='none', label="l={}".format(el))
		ax.plot(freq[posl], Enl[posl], color=col[el], label="l={}".format(el))
	ax.set_ylabel(r'$I_{nl}$')
	ax.set_xlabel('Frequency (' + r'$\mu$'+ 'Hz)')
	ax.set_ylim(ylim_inertia)
	ax.set_title(title)
	ax.legend()
	ax2.errorbar(fl0, amp, yerr=err_a)
	ax2.set_ylim(ylim_amp)
	ax2.set_ylabel(r'$A_{l=0} \propto \sqrt{\pi H \Gamma}$ (ppm)')
	fig.savefig (fileout, dpi=300)

	
dir0='/Users/obenomar/Work/Benomar2022/Referee-reply/inertia_models/'
fileSun_inertia=dir0 + '/SUN_fkrn_modelsx_l0-3_info.dat'
frange_inertia=[2300, 3700]
frange_obs=[2300, 3700]
fileout=dir0 + '/SUN_fkrn_modelsx_l0-3_info.jpg'
fl0, amp, err_a=Sun_amplitudes()
show_inertia(fileSun_inertia, frange_inertia, frange_obs, fileout, fl0, amp, err_a, title='Sun 1999-2002', ylim_inertia=[0, 4e-8], ylim_amp=[0,5])

'''
dir0='/Users/obenomar/Work/Benomar2022/Referee-reply/inertia_models/'
file16CygA_inertia=dir0 + '/16CygA_obs.0113.Z250.01.pg2'
frange_inertia=[1450, 3100]
frange_obs=[1400, 3000]
fileout=dir0 + '/16CygA_obs.0113.Z250.01.jpg'
fl0, amp, err_a=CygA_amplitudes()
show_inertia(file16CygA_inertia, frange_inertia, frange_obs, fileout, fl0, amp, err_a, title='16 Cyg A', ylim_inertia=[0, 7e-9], ylim_amp=[0,7])

dir0='/Users/obenomar/Work/Benomar2022/Referee-reply/inertia_models/'
file16CygB_inertia=dir0 + '/16CygB_obs.0107.Z226.01.pg2'
frange_inertia=[1700, 3400]
frange_obs=[1700, 3300]
fileout=dir0 + '/16CygB_obs.0107.Z226.01.jpg'
fl0, amp, err_a=CygB_amplitudes()
show_inertia(file16CygB_inertia, frange_inertia, frange_obs, fileout, fl0, amp, err_a, title='16 Cyg B', ylim_inertia=[0, 5e-9], ylim_amp=[0,6])
'''
