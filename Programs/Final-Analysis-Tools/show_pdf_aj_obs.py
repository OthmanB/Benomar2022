import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import interpolate
from scipy.signal import medfilt
from  matplotlib import ticker
import matplotlib.cm as cm
from read_aj_mcmcdata import get_aj_inc_star
from read_aj_mcmcdata import make_stats
from nice_hist import nice_hist_matrix
from a2CF_a2AR import do_a2CF_a2AR

def show_aj_pdfs(dir_mcmc, keep_aj=None, file_out='test.jpg', binning=40):
	'''
		Basic function to show the pdfs for the activity parameters: epsilon_nl, theta0, delta
		dir_mcmc: directory that specify where to look at the data. 
		file_out: Name of the output image file
		burnin: Fraction (between 0 and 1) of data points that are discarded at the begning of the serie of samples. Allows to remove some burnin, if necessary
		logepsilon: Show plot in log, if set to True
	'''
	labels=[r'$a_1$ (nHz)', r'$a_2$ (nHz)', r'$a_3$ (nHz)', r'$a_4$ (nHz)', r'$a_5$ (nHz)', r'$a_6$ (nHz)']
	unit_nHz=1000 # To convert into nHz
	confidence=[2.25,16,50,84,97.75]
	aj_stats, inc_stats, aj_samples, inc_samples, Nsamples=get_aj_inc_star(dir_mcmc, confidence=confidence)
	Nparams=len(aj_stats[:,0])
	if keep_aj==None:
		keep_aj=np.repeat(True, Nparams)
	#
	# -- Filter according to keep_aj --
	poskeep=np.where(np.asarray(keep_aj, dtype=bool) == True)[0]
	Nparams_keep=len(poskeep)
	aj_stats_keep=np.zeros((Nparams_keep, len(confidence)))
	aj_samples_keep=np.zeros((Nparams_keep, Nsamples))
	labels_keep=[]
	# -- Apply unit conversion and filter --
	cpt=0
	for i in range(Nparams):
		if keep_aj[i] == True:
			aj_stats_keep[cpt,:]=aj_stats[i,:]*unit_nHz
			aj_samples_keep[cpt,:]=aj_samples[i,:]*unit_nHz
			labels_keep.append(labels[i])
			cpt=cpt+1
	#
	# Add the a2_CF (centrifugal term to a2) for reference
	a2_CF_all, a2_CF_l, a2_CF_mean12, a2_AR_mean=do_a2CF_a2AR(dir_mcmc, step_factor=10, first_sample=0, use_Anl_weight=True)
	a2_CF_stats=make_stats(a2_CF_mean12, confidence=[2.25,16,50,84,97.75])
	extra_data=[]
	a2_extra=np.zeros((1, len(a2_CF_mean12)))
	a2_CF_extra=np.zeros((1, len(a2_CF_stats)))
	#
	a2_extra[0,:]=a2_CF_mean12
	a2_CF_extra[0,:]=a2_CF_stats
	#
	extra_data.append([1]) # Index for a2
	extra_data.append(a2_extra)
	extra_data.append(a2_CF_extra)
	# -- Perform the plotting --
	nice_hist_matrix(aj_samples_keep, aj_stats_keep, labels_keep, binning=binning, posplots=None, file_out=file_out, extra_data=extra_data)
	#print('Saved files with syntax: ', file_out)
	exit()

# The Sun 1999-2002
#dir_mcmc='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/19992002_incfix_fast_Priorevalrange/'
#name='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/19992002_incfix_fast_Priorevalrange/PDFs_aj_19992002_incfix_fast_Priorevalrange.jpg'
#keep_aj=[True, True, False, True, False, False]

# The Sun 2006-2009
#dir_mcmc='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/20062009_incfix_fast/'
#name='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/20062009_incfix_fast/PDFs_aj_20062009_incfix_fast.jpg'
#keep_aj=[True, True, False, True, False, False]

# 16 Cyg A (kplr012069424)
#dir_mcmc='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
#keep_aj=[True, True, True, True, False, False]

# 16 Cyg B (kplr012069449) 
#dir_mcmc='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
#name='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3/PDFs_aj_kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3.jpg'
#keep_aj=[True, True, True, True, False, False]

# 16 Cyg B (kplr012069449) Alternative run
dir_mcmc='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2-A2/'
name='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2-A2/PDFs_aj_kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2.jpg'
keep_aj=[True, True, True, True, False, False]


show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=40)

#exit()