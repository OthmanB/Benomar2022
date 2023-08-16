# Summary on acoefs_analysis

A set of python function that evaluate the effects of activity and centrifugal forces on low-l modes

Most functions are for visualisation purpose, but others are for performing tests.

Note: Fitting routines will require you to compile the Alm routine from https://github.com/OthmanB/TAMCMC-C/tree/dev/external/integrate  using the provided cmake file.

# Python Dependencies
    - datetime
    - termcolor
    - extension-helpers
    - jinja2
    - pyerfa
    - numpy
    - scipy
    - astropy
    - sunpy
    - matplotlib

Note: On MacOS, you may need to use the pip3 option '--use-deprecated=legacy-resolver' when attempting to install sunpy (which depends on astropy and pyerfa). They have a metadata issue in pyerfa 2.0.0 that makes pip3 crash.

# How to use it
    A. You first need to ensure that you have compiled version of Alm, bin2txt and getstats inside the cpp_prg directory. For this:
    	1. Compile the TAMCMC program in ../TAMCMC-1.83.8 following the instructions provided there (usage of cmake on linux/mac). This will create the binaries bin2txt and getstats (among others) inside ../TAMCMC-1.83.8/build. You can then copy them in cpp_prg here

	    2. Compile the Alm program in ../Alm following the instruction provided there. Then copy it inside cpp_prg
    B. For some of the programs, you need the full MCMC results. These taking some space, they are not provided here. However, I made available most them on a IPFS-based (https://docs.ipfs.tech/concepts/what-is-ipfs/) database (https://filebase.com).
To stay in a free-to-use system, I am limited to 5 Gb data. All fits in this except the Simulations (MCMC_Simulation_data) used for the bias analysis. The simulation data can be provided on-demand.

Here are the links to compressed version of the data for the Activity analysis and the spectrum analysis:
    
    - Data/MCMC_Activity_data: 
        - Version 1 (initial analysis) : https://ipfs.filebase.io/ipfs/QmdWAn954dswCgvNXEd9hzUFawojyWokRkdS9q49U4A34W
        - Version 2 (after new analyses) : https://ipfs.filebase.io/ipfs/QmSbUvZPZvK4TjXnDdHvyPzTZwHHGGijHTDU9dmLRDNvaM
    
    - Data/MCMC_Spectrum_data: https://ipfs.filebase.io/ipfs/QmeuE6kLGFR5s1uPAQ6eKcbWtJpRXyejdNxxEJVNNYwR5M

	Alternatively, you can download the same files in https://othmanbenomar.dev/Data.html
 
    C. Use the main.py program which will allow you to make all of the figures of the paper except Figure 3. 
    
# Details on each programs
    - show_aj_fct_theta_delta.py : This is an ensemble of function that allow you to compute the mean of aj coefficients and then to show it. It makes the Figure 5 of Benomar+2023 paper. The main function is show_aj_fct_theta_delta()  [NEED CLEANING REF TO fit_a2sig.py]
    - show_butterflydiag.py   : Functions that allow you to visualise the butterfly diagram and overlay colored area for specific time interval. This program can be used to generate the Figure 2 of Benomar+2023 paper.
    - show_pdf_aj_obs         : A program that make the correlation plots for the results of the aj fits made by the TAMCMC program (Figure 9, 12, 14, 16).
    - show_pdf_vpaper.py      : Allows you to read the raw outputs of a TAMCMC analysis for the aj_model and then make the plots of the pdf for epsilon, theta_0 and delta. It is used to generate the plots of the paper (Figure 10, 11, 13, 15).
    - aj_bias_analysis.py    : Its main function is bias_analysis(). That function creates the bias maps based on information from simulations and of the products of the MCMC analysis made using the IDL program IDL_postMCMC.
    - check_aj_linearity.py  : The main function is check_aj_linearity(). It visually demonstrates how much linear are the a-coefficients from the Alm function, in function of the frequencies.
    - acoefs_effects.py      : A set of small functions that can make some basic visualisation. The most important is a2_epsilon_plot, which allows you to reproduce the Figure 3 of Gizon2004 AN 323, 251 and thus check that their/our implementation are consistent.
    - eval_aj_range.py       : Contains a few functions that read an Alm python grid (can be created by make_Alm_grid.py). It also has the aj_mean_range_v1() function that gives an idea of what should be the prior range for a given star as a function of some stellar parameters. 
    - a2CF_a2AR.py : The functions here have for goal to separate the contribution on a2 of the centrifugal force from the activity. Used in particular to make input setup files (ie, get a2(AR) and a4(AR)) for the Activity analysis with MCMC. The main function is main_a2CF_a2AR().
    - make_Alm_grid.py       : A series of programs that call the C++ implementation of Alm and use it to make a grid of Alm. The grid is usefull as it speeds up computations made in this python program. To make grids, the main program is : do_all_grids().
	- acoefs.py              : A python implementation that defines the Pslm terms and the Hslm terms from Ritzoller+1991. It also provides a program to convert any frequency multiplet into Tnlm and Snlm and deduces the aj coefficient from it. The program test_acoef() allows you to test that all those functions do their job properly.
    - activity.py            : An ensemble of functions that implement in python the Alm term in various ways. eg. it contains the implementation in two flavor for the computation of Alm in the case of a F(theta, phi | x) = Gaussian or F(theta, phi | x) = Gate. 
    A small function that allows you to also call the C++ implementation of Alm (20 times faster than the pure-python based function) is also given here.
	- test_convergence.py    : A program that allows you to evaluate the precision difference between the Alm program implemented in Python and the one implemented in C++. The Python routine has in overall the same precision as the C++ function, but run ~20 times slower.
