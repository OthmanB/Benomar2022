'''
This is the main function to call in order to make all of the figures of the paper Benomar2022+, 
except Figure 1 and 3
Note that the code rely on many data analysis that are not provided on github due to their size.
Those data can be available upon request
'''
from show_aj_fct_theta_delta import show_aj_fct_theta_delta 
from show_butterflydiag import show_diagram
from show_pdf_aj_obs import show_aj_pdfs
from show_pdf_activity import show_pdf_vpaper
from aj_bias_analysis import bias_analysis
from acoefs_effects import a2_epsilon_plot
from check_aj_linearity import check_aj_linearity
import os

print(' Detected Working directory:')
cwd = os.getcwd()
print('  ', cwd)
print (' Directory where all In/Out data are expected:')
dir_core=cwd + '/../../Data/'
print('  ', dir_core)
print(' ----- ')
#
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
print(' --- Plots of Figure 5 : aj function of theta / delta  ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
#
file_out=dir_core + '/Figures_publish/Fig5-aj_theta_delta'
show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=0., epsilon_nl=5*1e-4, dir_core=dir_core, lmax=3, file_out=file_out) # Makes average for all l up to 3
# Overwrite to get the proper averaging with a2 and a4
show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=0., epsilon_nl=5*1e-4, dir_core=dir_core, lmax=2, file_out=file_out) # Makes average for all l up to 2 (overwrite previous l=1,l=2 averages)
#
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
print(' --- Plot of Figure 2 : ButterFly Diagram ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
#
show_diagram(filein=None, fileout=None)
#
print(' --- Plots of Figure 9, 12, 14, 16: The PDF ---')
keep_aj=[True, True, False, True, False, False]
# The Sun 1999-2002
print( '   - Fit of the Sun 1999 - 2002 (Fig 9A)')
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/19992002_incfix_fast_Priorevalrange/'
name= dir_core + '/Figures_publish/Fig9A-PDFs_aj_19992002.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
# The Sun 2006-2009
print( '   - Fit of the Sun 2006 - 2009 (Fig 9B)')
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/20062009_incfix_fast/'
name= dir_core + '/Figures_publish/Fig9B-PDFs_aj_20062009.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
print( '   - Fit of the Sun 2006 - 2011 (Fig 16)')
# The Sun 2006 - 2011
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/20062011_incfix_fast/'
name= dir_core + '/Figures_publish/Fig16-PDFs_aj_20062009.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
#
keep_aj=[True, True, True, True, False, False]
print( '   - Fit of the 16 Cyg A')
# 16 Cyg A (kplr012069424)
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
name= dir_core + '/Figures_publish/Fig12-PDFs_aj_kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
print( '   - Fit of the 16 Cyg B')
# 16 Cyg B (kplr012069449)
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
name= dir_core + '/Figures_publish/Fig14-PDFs_aj_kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
#
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
print(' --- Plots for activity zones ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
#
# Common out directory
dir_out=dir_core + '/Figures_publish/Activity_Fig/' 
#dir_out='/Users/obenomar/Work/tmp/test_a2AR/tmp/Realdata/activity_TAMCMC/PostMCMC/'
dir_mcmc=[dir_core + '/MCMC_Activity_data/'] # path of the MCMC outputs data (not the products this time)

# --------------------------
# -------- The Sun  --------
# --------------------------

# The Sun 1999-2002
#dir_mcmc=['/Users/obenomar/Work/tmp/test_a2AR/tmp/Realdata/activity_TAMCMC/TAMCMC/'] # Must be an array
process_names=['aj_ARonly_Sun_19992002_l12only']
names=['19992002_incfix_fast_Priorevalrange_a2ARonly']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig10'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out)
# The Sun 2006-2009
process_names=['aj_Sun-20062009_l12only']
names=['20062009_incfix_fast_a2ARonly']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig11'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out)

# --------------------------
# ----- 16 Cyg A and B -----
# --------------------------
dir_mcmc.append(dir_core + '/MCMC_Activity_data/') # There is two plots superimposed here (with bias and without), we need two path
#
#  16 Cyg A
process_names=['aj_ARonly_16CygA', 'aj_ARonly_16CygA_bias']
names=['aj_ARonly_16CygA','aj_ARonly_16CygA_bias']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig13'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out)
#  16 Cyg B  LowSol
process_names=['aj_ARonly_16CygB_LowSol', 'aj_ARonly_16CygB_LowSol_bias']
names=['aj_ARonly_16CygB_LowSol','aj_ARonly_16CygB_LowSol_bias']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig15A'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out)
#  16 Cyg B  UpSol
process_names=['aj_ARonly_16CygB_UpSol', 'aj_ARonly_16CygB_UpSol_bias']
names=['aj_ARonly_16CygB_UpSol','aj_ARonly_16CygB_UpSol_bias']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig15B'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out)
#
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
print(' --- Plots for bias maps ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
dir_data = dir_core + '/MCMC_Simulation_data/'
dir_out = dir_core + '/Figures_publish/Bias_MAPs/'
numax_star=2150.
## ---- PROCESS ALL ----
# -------- HNR 30 Tobs=730 days Polar -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs730_Polar/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Polar/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs730_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs730_Polar/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Polar/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs730_Polar/products/']
fileout_all=dir_out + 'Fig7-Bias_map_HNR30_Tobs730_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------- HNR 30 Tobs=730 days Equatorial -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs730_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs730_Equatorial/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Equatorial/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs730_Equatorial/products/']
fileout_all=dir_out + 'Fig6-Bias_map_HNR30_Tobs730_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------- HNR 20 Tobs=730 days Polar -------
combi_files=[dir_data +'HNR20_a1ovGamma0.4_Tobs730_Polar/Combinations.txt', dir_data+'HNR20_a1ovGamma0.5_Tobs730_Polar/Combinations.txt', dir_data+'HNR20_a1ovGamma0.6_Tobs730_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR20_a1ovGamma0.4_Tobs730_Polar/products/', dir_data+'HNR20_a1ovGamma0.5_Tobs730_Polar/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs730_Polar/products/']
fileout_all=dir_out + 'Fig20-Bias_map_HNR20_Tobs730_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------- HNR 20 Tobs=730 days Equatorial -------
combi_files=[dir_data +'HNR20_a1ovGamma0.4_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR20_a1ovGamma0.5_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR20_a1ovGamma0.6_Tobs730_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR20_a1ovGamma0.4_Tobs730_Equatorial/products/', dir_data+'HNR20_a1ovGamma0.5_Tobs730_Equatorial/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs730_Equatorial/products/']
fileout_all=dir_out + 'Fig19-Bias_map_HNR20_Tobs730_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------- HNR 10 Tobs=730 days Polar -------
combi_files=[dir_data +'HNR10_a1ovGamma0.4_Tobs730_Polar/Combinations.txt', dir_data+'HNR10_a1ovGamma0.5_Tobs730_Polar/Combinations.txt', dir_data+'HNR10_a1ovGamma0.6_Tobs730_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR10_a1ovGamma0.4_Tobs730_Polar/products/', dir_data+'HNR10_a1ovGamma0.5_Tobs730_Polar/products/',dir_data+'HNR10_a1ovGamma0.6_Tobs730_Polar/products/']
fileout_all=dir_out + 'Fig18-Bias_map_HNR10_Tobs730_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------- HNR 10 Tobs=730 days Equatorial -------
combi_files=[dir_data +'HNR10_a1ovGamma0.4_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR10_a1ovGamma0.5_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR10_a1ovGamma0.6_Tobs730_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR10_a1ovGamma0.4_Tobs730_Equatorial/products/', dir_data+'HNR10_a1ovGamma0.5_Tobs730_Equatorial/products/',dir_data+'HNR10_a1ovGamma0.6_Tobs730_Equatorial/products/']
fileout_all=dir_out + 'Fig17-Bias_map_HNR10_Tobs730_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------------
# -------------
# -------- HNR 30 Tobs=1460 days Polar -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs1460_Polar/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs1460_Polar/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs1460_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs1460_Polar/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs1460_Polar/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs1460_Polar/products/']
fileout_all=dir_out + 'Fig7-Bias_map_HNR30_Tobs1460_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(d)','(e)', '(f)'])
# -------- HNR 30 Tobs=1460 days Equatorial -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs1460_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs1460_Equatorial/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs1460_Equatorial/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs1460_Equatorial/products/']
fileout_all=dir_out + 'Fig6-Bias_map_HNR30_Tobs1460_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(d)','(e)', '(f)'])
# -------- HNR 20 Tobs=1460 days Polar -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Polar/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/Combinations.txt', dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Polar/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Polar/products/']
fileout_all=dir_data + 'Fig20-Bias_map_HNR20_Tobs1460_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=20, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
# -------- HNR 20 Tobs=1460 days Equatorial -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Equatorial/products/']
fileout_all=dir_out + 'Fig19-Bias_map_HNR20_Tobs1460_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=20, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
# -------- HNR 10 Tobs=1460 days Polar -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Polar/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/Combinations.txt', dir_data+'HNR10_a1ovGamma0.6_Tobs1460_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Polar/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/products/',dir_data+'HNR10_a1ovGamma0.6_Tobs1460_Polar/products/']
fileout_all=dir_out + 'Fig18-Bias_map_HNR10_Tobs1460_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=10, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
# -------- HNR 10 Tobs=1460 days Equatorial -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR10_a1ovGamma0.6_Tobs1460_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Equatorial/products/']
fileout_all=dir_out + 'Fig17-Bias_map_HNR10_Tobs1460_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=10, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
#
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
print(' --- Plots for Linearity of aj ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
dir_data=dir_core + '/Extra_data/grids_posterior/gate/epsilon_nl0.0005_0.0/raw_ajnl/'
dir_out =dir_data
check_aj_linearity(dir_data=dir_data, do_plots=True, full_labels=False, dir_out=dir_out)

# ---- EXTRA PLOTS ----
fileout=dir_core + 'Extra_data/Extra_Figures/Fig3-Gizon2004.jpg'
a2_epsilon_plot(lrange=[1,2], colors=['Blue', 'Orange', 'Red'], ftype='gate', fileout=fileout)
