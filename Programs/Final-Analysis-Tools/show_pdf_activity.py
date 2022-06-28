'''
	This is the ensemble of function that are used to
	read MCMC files from the EMCMC run (fit_ajsig.py program) 
	and to make paper-ready plots for the activity parameters
	epsilon, theta0 and delta
	At the end of this file, there is a list of calls for the case of:
		- The Sun at minimum and maximum of activity
		- 16 Cyg B for the two solutions of a4
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import interpolate
from scipy.signal import medfilt
from  matplotlib import ticker
from nice_hist import nice_hist
from read_activity_outputs import read_mcmc_posteriors

'''
def read_mcmc_posteriors(file):
	data=np.load(file)
	Nparams=len(data[0,:])
	Nsamples=len(data[:,0])
	labels = ["epsilon_nl0", "epsilon_nl1", "theta0", "delta"]
	return data, labels, Nparams, Nsamples	
'''

def filter_posteriors(data, labels, Nparams, Nsamples, burnin, skip_epsilon_nl1=False):#, keep_positive=False, keep_epsilon=None):
	Nburnin=int(burnin*Nsamples) # USER CAN REMOVE A FRACTION OF THE SAMPLES AT THE BEGINING
	if burnin > 1:
		print("Error in filtering posteriors: You specified a value of the burnin parameteter exceeding 1")
		print("                               This should be a fraction of Nsamples and must be < 1")
		exit()
	# -- Section to skip epsilon_nl1 --
	if skip_epsilon_nl1 == True:
		data1=np.zeros((Nsamples-Nburnin, Nparams-1))
		data1[:,0]=data[Nburnin:,0]
		data1[:,1]=data[Nburnin:,2]
		data1[:,2]=data[Nburnin:,3]
		Nparams=len(data1[0,:])	
	else:
		data1=np.zeros((Nsamples-Nburnin, Nparams))
		for i in range(Nparams):
			data1[:,i]=data[Nburnin:,i]
	labels=["epsilon", "theta", "delta"]
	return data1, labels, Nparams, Nsamples

def get_uncertainties(data, Nparams, labels):
	errors=np.zeros((2,Nparams))
	med=np.zeros(Nparams)
	stats_all=np.zeros((Nparams,5))
	for i in range(Nparams):
		stats = np.percentile(data[:, i], [2.25, 16, 50, 84, 97.75])
		print(' stats[',i,'] = ', stats)
		if labels[i] == 'epsilon':
			errors[0,i]=stats[2] - stats[1]
			errors[1,i]=stats[3] - stats[2]
			med[i]=stats[2]
			stats_all[i,:]=stats
		else:
			errors[0,i]=(stats[2] - stats[1])*180./np.pi
			errors[1,i]=(stats[3] - stats[2])*180./np.pi
			med[i]=stats[2]*180./np.pi
			stats_all[i,:]=stats*180./np.pi
	return med, errors, stats_all

def show_pdf_vpaper(dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/results_activity/gate_8379927_a2a4_fast/'], names=[None], file_out='plots', burnin=0, do_inset=True, logepsilon=[False, False], xlim_epsilon=[[0, 1e-2],[0, 1e-2]], text_index=None):
	'''
		Main function to make the pdfs plots for the paper Benomar2022+ and for the activity parameters: epsilon_nl, theta0, delta
		dir_mcmc: Array with directories that specify where to look at the data. 
		file_out: Name of the output image file
		burnin: Fraction (between 0 and 1) of data points that are discarded at the begning of the serie of samples. Allows to remove some burnin, if necessary
		logepsilon[0]: Show the main plot of epsilon in log, if set to True
		logepsilon[1]: Show the main plot of epsilon in log, if set to True
	'''
	if names[0] == None:
		names=np.linspace(1, len(dir_mcmc), len(dir_mcmc))
	#
	data_s=[]
	labels_s=[]
	Nparams_s=[]
	Nsamples_s=[]
	med_s=[]
	errors=[]
	statistics=[]
	for j in range(len(dir_mcmc)):
		d=dir_mcmc[j]
		print("    - - - - - - dir_mcmc : - - - - - - - ")
		print("        d=", d)
		data, labels, Nparams, Nsamples=read_mcmc_posteriors(d + 'samples.npy')
		if Nparams == 4:
			data, labels, Nparams,Nsamples=filter_posteriors(data, labels, Nparams,Nsamples, burnin, skip_epsilon_nl1=True)
		else:
			data, labels, Nparams,Nsamples=filter_posteriors(data, labels, Nparams,Nsamples, burnin, skip_epsilon_nl1=False)
		#
		# Evaluate uncertainties using the samples
		med,err, stats=get_uncertainties(data, Nparams, labels)
		#
		# Show summary on the statistics
		string='#param   median   err_m     err_p\n'
		for i in range(Nparams):
			print(labels[i], ' =', med[i], '  (-  ', err[0, i], '  ,  +', err[1,i], ')')
			string=string + '  {}  {:0.6f}      {:0.6f}      {:3.6f}\n'.format(labels[i], med[i], err[0,i], err[1,i])
		fsum=open(file_out+'_'+names[j]+'_summary.txt', 'w')
		fsum.write(string)
		fsum.close()
		#
		data_s.append(data)
		labels_s.append(labels)
		Nparams_s.append(Nparams)
		Nsamples_s.append(Nsamples)
		med_s.append(med)
		errors.append(err)
		statistics.append(stats)
	#
	cols=[['black', 'gray', 'darkgray'], ['red', 'tomato','lightsalmon']]
	alphas=[None, 0.4]
	bins=30#75
	for i in range(Nparams):
		fig_1d, ax = plt.subplots(1, figsize=(12, 6))
		fig_bin, ax_bin = plt.subplots(1, figsize=(12, 6))
		for j in range(len(dir_mcmc)):
			if text_index != None:
				ax.annotate(text_index[i], xy=(0.05, 0.92), xycoords=ax.transAxes, fontsize=22)
			if labels_s[j][i] == "epsilon":
				ax.set_xlim([xlim_epsilon[0][0], xlim_epsilon[0][1]])
				if j == 0 and do_inset == True:
					#ax_inset = inset_axes(ax, width="30%", height="40%", loc=1)
					ax_inset = inset_axes(ax, width="30%", height="40%", bbox_to_anchor=(-0.05,-0.05,1,1), bbox_transform=ax.transAxes) 
					ax_inset.set_yticks([])
					ax_inset.axhline(0, linestyle='--', color='black')
					ax_inset.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
				nice_hist(data_s[j][:,i], statistics[j][i,:], ax=ax, intervals=[True,False], binning=10*bins, color=cols[j],alpha=alphas[j])
				if do_inset == True:
					y,x,p=ax_bin.hist(data_s[j][:,i], linestyle='-', bins=70*bins, histtype='step', color=cols[j][0], density=True)
					ax_inset.step(x[0:len(y)],medfilt(y, 1), color=cols[j][0], linestyle='-')
					ax_inset.set_xlim([xlim_epsilon[1][0], xlim_epsilon[1][1]])
					#ax_inset.axvline(med_s[j][i], linestyle='--', color=cols[j][0])
					if logepsilon[1] == True:
						ax_inset.set_xscale('log')
						ax_inset.set_xlim([xlim_epsilon[1][0], xlim_epsilon[1][1]])
				if logepsilon[0] == True:
		 			ax.set_xscale('log')
			else:
				nice_hist(data_s[j][:,i]*180/np.pi, statistics[j][i,:], ax=ax, intervals=[True,False], binning=2*bins,color=cols[j], alpha=alphas[j])
			if labels_s[j][i] == 'epsilon':
				ax.set_xlabel(r'$\epsilon$ (no unit)', fontsize=18)
			if labels_s[j][i] == 'theta':
				ax.set_xlabel(r'$\theta$ (deg)', fontsize=18)
			if labels_s[j][i] == 'delta':
				ax.set_xlabel(r'$\delta$ (deg)', fontsize=18)
			ax.set_ylabel("PDF", fontsize=20)
			ax.tick_params(axis='x', labelsize=18)
			ax.tick_params(axis='y', labelsize=18)		
			fig_1d.savefig(file_out+ '_' + names[0] + '_pdf_'+ str(i) + '.jpg')
	print('Saved files with syntax: ', file_out)
	

# The Sun 1999-2002
dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/19992002_incfix_fast_Priorevalrange_a2ARonly/']
names=['19992002_incfix_fast_Priorevalrange_a2ARonly']
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'])

# The Sun 2006-2009
dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/20062009_incfix_fast_a2ARonly/']
names=['20062009_incfix_fast_a2ARonly']
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'])

# 16 Cyg A (kplr012069424)
dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly/','/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_bias/']
names=['kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly', 'kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_bias']
file_out=dir_mcmc[0]+'plots'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'], file_out=file_out)

# 16 Cyg B (kplr012069449) OLD RUN : (Feb 2022) SOL LOW a4
#dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_below0.02/','/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_below0.02_bias/']
#names=['kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_below0.02', 'kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_below0.02_bias']
#file_out=dir_mcmc[0]+'plots'
#show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'])

# 16 Cyg B (kplr012069449) OLD RUN : (Feb  2022) SOL HIGH a4
#dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_above0.02/','/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_above0.02_bias/']
#names=['kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_above0.02','kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_ARonly_Sola4_above0.02_bias']
#file_out=dir_mcmc[0]+'plots'
#show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 1e-2],[0,5e-4]],text_index=['(d)', '(e)', '(f)'])

# 16 Cyg B (kplr012069449) NEW RUN (Jun 2022): SOL LOW a4
dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_lowersol/','/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_lowersol_bias/']
names=['kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_lowersol', 'kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_lowersol_bias']
file_out=dir_mcmc[0]+'plots'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'])

# 16 Cyg B (kplr012069449) NEW RUN (Jun  2022): SOL HIGH a4
dir_mcmc=['/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_uppersol/','/Users/obenomar/tmp/test_a2AR/tmp/Realdata/activity/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_uppersol_bias/']
names=['kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_uppersol','kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3_GU2_ARonly_uppersol_bias']
file_out=dir_mcmc[0]+'plots'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.1, xlim_epsilon=[[0, 1e-2],[0,5e-4]],text_index=['(d)', '(e)', '(f)'])


exit()