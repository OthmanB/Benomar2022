'''
	The functions here have for goal to separate the contribution
	on a2 of the centrifugal force from the activity
    This is useful in order to properly propagate uncertainties of a1 and Dnu into the a2(AR) term
    And therefore, activity inference just need rely on a2(AR), 
    effectively using a2(AR)=a2 - a2(CF) as observable instead of a2
'''
import numpy as np
from  scipy.io import readsav
from read_aj_mcmcdata import read_sav
from read_aj_mcmcdata import read_parameters_length
from read_aj_mcmcdata import get_Dnu
from read_aj_mcmcdata import reduce_samples
from read_aj_mcmcdata import get_Dnu_samples
from read_aj_mcmcdata import get_nu_samples
from fit_a2sig import a2_CF

def get_a2_CF_samples(nu_nl_samples, a1_samples, dnu_samples, weight=None):
    '''
        Function that takes all of the samples for each mode and for a1 and derive from it
        The average a2(CF) term
        nu_nl_samples: A tensor of data containing frequencies and of size [0,lmax],[0:Nmodes],[0:Nsamples]
        a1_samples: samples for the a1 coefficient 
    '''
    Nsamples=len(nu_nl_samples[0,0,:])
    Nmodes=len(nu_nl_samples[0,:,0])
    lmax=len(nu_nl_samples[:,0,0])-1
    try:
        if weight == None:
            w=np.ones((lmax+1,Nmodes))
    except:
        w=weight
    print("         a. Configuration:")
    print("             - Nsamples    : ", Nsamples)
    print("             - Nmodes      : ", Nmodes)
    print("             - lmax        : ", lmax)
    print("             - weights     : ", weight)
    #
    print("         b. Derive a2(CF) for each modes and averaging over n...")
    a2_CF_l=np.zeros((lmax+1,Nsamples))
    a2_CF_all=np.zeros((lmax+1, Nmodes,Nsamples))
    a2_CF_mean12=np.zeros(Nsamples)
    s=0
    Norm_nl=np.sum(w[1:3, :]) # Norm of l=1,2 only
    for s in range(Nsamples):
        for l in range(1,lmax+1):
            Norm_l=np.sum(w[l,:])
            for n in range(Nmodes):
                r=a2_CF(nu_nl_samples[l,n,s], dnu_samples[s], a1_samples[s], l)
                a2_CF_l[l,s]=a2_CF_l[l,s]+w[l,n]*r/Norm_l   # Averaging over Nmodes the a2_CF coefficient. Uses weights w[l,n] defined by default to 1
                a2_CF_all[l,n,s]=r
                if l<=2:
                    a2_CF_mean12[s]=a2_CF_mean12[s] + w[l,n]*r/Norm_nl
    return a2_CF_all, a2_CF_l, a2_CF_mean12


def compute_a2_AR(a2, a2_CF_mean):
    '''
        Function that takes the average a2_CF and remove it from the a2 in order to evaluate a2_AR
    '''
    a2_AR_mean=a2-a2_CF_mean   
    return a2_AR_mean 


def do_a2CF_a2AR(dir_core, step_factor=1, first_sample=0, use_Anl_weight=False):
    '''
        Main function that compute the average a2_CF and a2_AR from a serie of samples of a1, a2, nu_nl
        nu_nl is used to derive Dnu
        a1 approximates the average internal rotation
        All of the samples must have been acquired using the TAMCMC program and must have been
        saved into sav IDL files (using eg. IDLPostMCMC code)
        dir_core: directory on which the products of the IDLPostMCMC analysis can be found
        step_factor: Control how many samples are skipped within the ensemble of samples inside sav files. Greatly enhance the computation time is set to >1
        first_sample: Control the initial samples that is used for the analysis. Can be used to remove a potential Burn-in phase
        use_Anl_weight: If True, uses the median of the Amplitudes of the modes in order to weight the <a2_CF>_nl computation
    '''
    dir_sav=dir_core + '/Files/'
    print("A. Processing star with the following inputs:")
    print("  - dir_core      : ", dir_core)
    print("  - dir_files     : ", dir_sav)
    print("  - step_factor   : ", step_factor)
    print("  - first_sample  : ", first_sample)
    print("  - use_Anl_weight: ", use_Anl_weight)
    #
    print("B. Extracting relevant information...")
    #
    print("   1. plength...")
    plength=read_parameters_length(dir_sav, 'plength.txt')
    i0_aj=sum(plength[0:6]) # First Position after Nf_el list
    print("   2. Extract and reduce samples of a1...(ASSUMES NO SLOPE: a1_1=0)")
    a1_samples, Nsize=read_sav(dir_sav, i0_aj)
    a1_samples=reduce_samples(a1_samples, step_factor, first_sample)
    a1_samples=a1_samples*1e3 # conversion to nHz
    print("   3. Extract and reduce samples of a2... (ASSUMES NO SLOPE: a2_1=0)")
    a2_samples, Nsize=read_sav(dir_sav, i0_aj+2)
    a2_samples=reduce_samples(a2_samples, step_factor, first_sample)
    a2_samples=a2_samples*1e3
    print("   4. Extract and reduce samples of nu(n,l)...")
    nu_nl_samples=get_nu_samples(dir_sav, plength, Nsize, verbose=True, step_factor=step_factor, first_sample=first_sample)
    print("   5. Extract A(n,l) from synthese files...")
    r=readsav(dir_core+'/synthese.sav')
    Anl=r['STAT_SYNTHESE_AMPLITUDE'][:,:,3] # Keep only the median
    if use_Anl_weight == True:
        Nmodes=len(nu_nl_samples[0,:,0])
        try:
            lmax=3
            weight=np.zeros((lmax+1, Nmodes))
            for l in range(lmax+1):
                for n in range(Nmodes):
                    weight[l,n]=Anl[n,l]
        except:
            lmax=2
            weight=np.zeros((lmax+1, Nmodes))
            for l in range(lmax+1):
                for n in range(Nmodes):
                    weight[l,n]=Anl[n,l]
        print("weight:", weight)
    else:
        weight=None
    #
    Nsamples=len(a1_samples)
    lmax=len(nu_nl_samples[:,0,0])-1
    print("C. Compute...")
    print("     1. Dnu...")
    dnu_samples=get_Dnu_samples(nu_nl_samples[0,:,:])
    print("       - Dnu = {0:0.3f} +/- {1:0.3f}".format(np.median(dnu_samples), np.std(dnu_samples)) )
    print("     2. a2_CF...")
    a2_CF_all, a2_CF_l, a2_CF_mean12=get_a2_CF_samples(nu_nl_samples, a1_samples, dnu_samples, weight=weight) # NOTE: a2 IS RETURNED IN MICROHZ
    print("               <a2>nl             :  ~ {} +/- {} (nHz)".format(np.median(a2_samples), np.std(a2_samples))) 
    print(" -- ")
    for l in range(1, lmax+1): 
        print("             a2_CF(l={})                 :  ~ {} +/- {}  (nHz)".format(l, np.median(a2_CF_l[l,:])*1e3, np.std(a2_CF_l[l,:])*1e3))
    print("             <a2_CF>nl (l=1,2 only)          :  ~ {} +/- {} (nHz)".format(np.median(a2_CF_all[1:3,:,:])*1e3, np.std(a2_CF_all[1:3,:,:])*1e3)) 
    print("          <a2_CF>nl (l=1,2 only) (a2_mean12) :  ~ {} +/- {} (nHz)".format(np.median(a2_CF_mean12)*1e3, np.std(a2_CF_mean12)*1e3)) 
    print("             <a2_CF>nl (all l)               :  ~ {} +/- {} (nHz)".format(np.median(a2_CF_all[1:,:,:])*1e3, np.std(a2_CF_all[1:,:,:])*1e3)) 
    print(" -- ")
    print("     3. a2_AR...")
    a2_AR_mean=compute_a2_AR(a2_samples, a2_CF_mean12*1e3)
    print("             <a2_AR>nl             :  ~ {} +/- {} (nHz)".format(np.median(a2_AR_mean), np.std(a2_AR_mean))) 
    print(" Note: From all of these values, it is recommended to use a2_mean12 as it involves the proper error propagation")
    return a2_CF_all*1e3, a2_CF_l*1e3, a2_CF_mean12*1e3, a2_AR_mean*1e3
 
def main_a2CF_a2AR():
    #dir_core='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/19992002_incfix_fast_Priorevalrange/'
    #dir_core='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/20062009_incfix_fast/'
    #dir_core='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
    dir_core='/Users/obenomar/tmp/test_a2AR/tmp/Realdata/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
    step_factor=3
    first_sample=0
    use_Anl_weight=True #False
    a2_CF_all, a2_CF_l, a2_CF_mean12, a2_AR_mean=do_a2CF_a2AR(dir_core, step_factor=step_factor, first_sample=first_sample, use_Anl_weight=use_Anl_weight)
    #
    print("All data are saved in:")
    # Need to save a2_AR, a2_CF, a2 in a single PLOT
    # Need to save Dnu, a2_AR, a2_CF, a2 in a single FILE
    exit()
