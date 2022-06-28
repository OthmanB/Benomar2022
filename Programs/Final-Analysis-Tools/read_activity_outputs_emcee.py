import numpy as np

def read_logposterior(file_name='logposterior.npy'):
	'''
		Read the logposterior file and return all of the logposterior probabilities
	'''
	lpdf=np.load(file_name)
	return lpdf


def read_params(file, relax=np.asarray([True, True, False, True])):
	'''
		Use read_mcmc_posteriors and shape them in a suitable way for MLCJ.py
	'''
	smcmc, labels, Nparams, Nsamples=read_mcmc_posteriors(file)
	sinput=smcmc[0,:] # recover the initial values... this will be used to construct pref_all
	#pvars=np.where(relax == True)
	return smcmc, sinput,labels#, pvars, labels

def read_mcmc_posteriors(file):
	'''
		Reads the samples of the posteriors for each parameters
	'''
	smcmc=np.load(file)
	Nparams=len(smcmc[0,:])
	Nsamples=len(smcmc[:,0])
	labels = ["epsilon_nl0", "epsilon_nl1", "theta0", "delta"]
	return smcmc, labels, Nparams, Nsamples	
