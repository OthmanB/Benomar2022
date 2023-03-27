import numpy as np
from scipy.special import gammaln
import matplotlib.pyplot as plt
import scipy.stats

def signal_significance_chi2p(background=100, p=4, level=90, fall_back=False, do_fall_back=False, exit_on_error=True):
    # given a background value and a frequency value,
    # calculate the threshold
    # p: smoothing coefficient
    # background : level of the background
    # level: rejection level in percent: typicially 90% or 95% (level = 0.90 or 0.95).
    #
    level_input=level
    level=level/100
    u=background*p*np.linspace(0, 26.25, 8400) # to obtain a constant window
    #
    lnf=(p-1)*np.log(u) - gammaln(p) - u/background # the computation is done in log to avoid round off errors
    f=np.exp(lnf)
    #
    du=u[1]-u[0]
    sum0=0
    i=0
    while i < len(u): # compute the normalisation constant
        sum0=sum0+f[i]*du
        i=i+1
    #
    sum1=0.
    i=0
    while sum1 <= level and i < len(u):  # until the probability has reached level compute the sum
        sum1=sum1+f[i]*du/sum0
        s=u[i]
        i=i+1
        #print(sum1)
    Proba=100.*sum1
    #
    s=s/p # normalisation !
    '''
    fig, ax= plt.subplots(1)
    ax.plot(u,f)
    #ax.axvline(x=0, linestyle='--', linewidth=1.5, color='black')
    plt.show()
    '''
    if np.isfinite(Proba) == False and do_fall_back==False:
        if fall_back == False:
            print(' Warning: p exceeds the limit and the computation returned a nan probability')
            print(' Note that with p>>1, the distribution follows the gaussian statistics in virtue of the central-limit theorem')
            print(' If you want to use that property, please set the option fall_back = True')
            if exit_on_error==True:
                exit()
        else:
            # Find the maximum p values that works here
            pmax=10000
            pmin=5
            pg=pmax
            i=0
            # Get a first guess for the p that works by iterative division
            while np.isfinite(Proba) == False and p>=pmin:
                s, Proba=signal_significance_chi2p(background=background, p=pg, level=level_input, fall_back=True, do_fall_back=True)
                pg=int(pg/2)
                i=i+1
            if i == 1:
                print('pmax={} seems to small... trying to increase it...'.format(pmax))
                pmax=2*pmax
                pg=pmax
                i=0
                while np.isfinite(Proba) == False and p>=pmin:
                    s, Proba=signal_significance_chi2p(background=background, p=pg, level=level_input, fall_back=True, do_fall_back=True)
                pg=int(pg/2)
                i=i+1
            if pg <pmin:
                print('Error: sucessive divisions lead to p<{} which is below the accepted lower limit threshold that make sense'.format(pmin))
                print('       Debug required in signa_significance_chi2p()')
                exit()
            else:
                print('    Suitable p found. ==> p ={}'.format(pg))
    return s, Proba
