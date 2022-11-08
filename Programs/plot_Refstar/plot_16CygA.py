import numpy as np
import matplotlib.pyplot as plt
from scipy.io import readsav

def read_sav_synthese_l0(file):
	'''
		Function that read the synthese file, but returns only l=0 modes
	'''
	d=readsav(file)

	return d['stat_synthese_freq'][:,0,2:5], d['local_noise'][:,0], d['stat_synthese_height'][:,0,2:5],d['stat_synthese_width'][:,0,2:5]

def errors(x, y):
	'''
		Propagate errors assuming x/y, with 
		x = cte and y = np.array((3, K)) 
	'''
	dy_m=y[:,1]-y[:,0]
	dy_p=y[:,2]-y[:,1]
	err_m=x*dy_m/y[:,1]**2
	err_p=x*dy_p/y[:,1]**2
	err=np.zeros((2, len(err_m)))
	err[0,:]=err_m
	err[1,:]=err_p
	return err

def error_HNR(Noise, Heights):
	dy_m=Heights[:,1]-Heights[:,0]
	dy_p=Heights[:,2]-Heights[:,1]
	err_m=dy_m/Noise
	err_p=dy_p/Noise
	err=np.zeros((2, len(err_m)))
	err[0,:]=err_m
	err[1,:]=err_p
	return err

def error_a1ovGamma(a1,Widths):
	return errors(a1, Widths)

def main(file_synthese, fileout):
	a1=0.50349461 # 16 Cyg A a1
	fl0, N, H, W=read_sav_synthese_l0(file_synthese)
	HNR=H[:,1]/N
	err_HNR=error_HNR(N, H)
	a1ovGamma=a1/W[:,1]
	err_a1ovGamma=error_a1ovGamma(a1,W)
	numax=fl0[np.where(HNR == np.max(HNR))[0][0],1]
	fig, ax= plt.subplots(1)
	ax_right = ax.twinx()
	ax.errorbar(fl0[:,1], HNR, yerr=err_HNR, color='black', capsize=3)
	ax.axhline(0, linestyle='--', color='black')
	ax.set_xlim([np.min(fl0)*0.99, np.max(fl0)*1.01])
	ax.set_xlabel('Frequency ' + r"($\mu$" + 'Hz)', fontsize=12)
	ax.set_ylabel('HNR ', fontsize=12)	
	ax_right.tick_params(axis='y', colors='red')
	ax_right.errorbar(fl0[:,1], a1ovGamma, yerr=err_a1ovGamma, color='r', capsize=3)
	ax_right.set_ylabel(r'$a_1 / \Gamma$', color='r', fontsize=12)	
	ax_right.set_yticks(np.arange(0, 1.1, 0.1)) #np.max(np.ceil(a1ovGamma))
	ax.axvline(numax, linestyle='--', color='blue')
	#
	ax.annotate(r"$\nu_{max}$", xy=(numax, 1), va="bottom", ha="left", rotation=90, color='blue', fontsize=12)#, xytext=(inc_true[i], a1ovGamma_true[i]), color=colormap(cols[i]), va="center", ha="center", arrowprops=dict(arrowstyle="-", color=colormap(cols[i])))
	ax.annotate("16 Cyg A", xy=(2800, 30), va="center", ha="center", color='blue', fontsize=14)
	fig.tight_layout()
	plt.savefig(fileout, dpi=300)

file_synthese='/Users/obenomar/tmp/test_a2AR/plot_Refstar/data/16CygA_shoya_synthese.sav'
file_out='/Users/obenomar/tmp/test_a2AR/plot_Refstar/data/plot'
main(file_synthese, file_out)