'''
This is the main function to call in order to make all of the figures of the paper Benomar2022+, 
except Figure 1 and 3
Note that the code rely on many data analysis that are not provided on github due to their size.
Those data can be available upon request
'''
from show_aj_fct_theta_delta import show_aj_fct_theta_delta 
from show_butterflydiag import show_diagram, show_spots_with_model
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
print(' --- Plots of Figure 3 : aj function of theta / delta  ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
#
file_out=dir_core + '/Figures_publish/version_2/Fig3-aj_theta_delta'
#show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=0., epsilon_nl=5*1e-4, dir_core=dir_core, lmax=3, file_out=file_out) # Makes average for all l up to 3
show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=0., epsilon_nl=5*1e-4, dir_grids=None, lmax=3, file_out=file_out) # Makes average for all l up to 3
# Overwrite to get the proper averaging with a2 and a4
#show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=0., epsilon_nl=5*1e-4, dir_core=dir_core, lmax=2, file_out=file_out) # Makes average for all l up to 2 (overwrite previous l=1,l=2 averages)
show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=0., epsilon_nl=5*1e-4, dir_grids=None, lmax=2, file_out=file_out) # Makes average for all l up to 3
#
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
print(' --- Plot of Figure 2 : ButterFly Diagram and projected diagram ---')
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
#
file_out=dir_core + '/Figures_publish/version_2/Fig2ABC-butterfly.jpg'
show_diagram(filein=None, fileout=file_out)
#file_out=dir_core + '/Figures_publish/version_2/Fig2C-butterfly.jpg'
#show_spots_with_model(filein=None, fileout=file_out)

#
print(' --- Plots of Figure 7, 10, 12, 14: The PDF ---')
keep_aj=[True, True, False, True, False, False]
# The Sun 1999-2002
print( '   - Fit of the Sun 1999 - 2002 (Fig 7A)')
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/19992002_incfix_fast_Priorevalrange/'
name= dir_core + '/Figures_publish/version_2/Fig7A-PDFs_aj_19992002.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
# The Sun 2006-2009
print( '   - Fit of the Sun 2006 - 2009 (Fig 7B)')
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/20062009_incfix_fast/'
name= dir_core + '/Figures_publish/version_2/Fig7B-PDFs_aj_20062009.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
print( '   - Fit of the Sun 2006 - 2011 (Fig 14)')
# The Sun 2006 - 2011
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/20062011_incfix_fast/'
name= dir_core + '/Figures_publish/version_2/Fig15-PDFs_aj_20062011.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
#
keep_aj=[True, True, True, True, False, False]
print( '   - Fit of the 16 Cyg A')
# 16 Cyg A (kplr012069424)
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
name= dir_core + '/Figures_publish/version_2/Fig10-PDFs_aj_kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3.jpg'
show_aj_pdfs(dir_mcmc, keep_aj=keep_aj, file_out=name, binning=50)
print( '   - Fit of the 16 Cyg B')
# 16 Cyg B (kplr012069449)
dir_mcmc=dir_core + '/MCMC_Spectrum_data/products/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3/'
name= dir_core + '/Figures_publish/version_2/Fig12-PDFs_aj_kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3.jpg'
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
dir_out=dir_core + '/Figures_publish/version_2/Activity_Fig/' 
dir_mcmc=[dir_core + '/MCMC_Activity_data/version_2/gate/', dir_core + '/MCMC_Activity_data/version_2/triangle/', dir_core + '/MCMC_Activity_data/version_2/gauss/'] # path of the MCMC outputs data (not the products this time)
#legend_names=['Gate', 'Triangle', 'Gaussian']
legend_names=[r'$\Pi(\theta_0, \delta)$', r'$\Lambda(\theta_0, \delta)$', r'$\mathcal{N}(\theta_0,\delta)$']

# --------------------------
# -------- The Sun  --------
# --------------------------

# The Sun 1999-2002
process_names=['aj_ARonly_Sun_19992002_l12only_gate', 'aj_ARonly_Sun_19992002_l12only_triangle', 'aj_ARonly_Sun_19992002_l12only_gauss']
names=['aj_ARonly_Sun_19992002_l12only', 'aj_ARonly_Sun_19992002_l12only_triangle', 'aj_ARonly_Sun_19992002_l12only_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig8'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False, False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4], [0,5e-4]], 
    text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, show_average=True)
# The Sun 2006-2009
process_names=['aj_Sun-20062009_l12only_gate', 'aj_Sun-20062009_l12only_triangle', 'aj_Sun-20062009_l12only_gauss']
names=['20062009_incfix_fast_a2ARonly', '20062009_incfix_fast_a2ARonly_triangle', '20062009_incfix_fast_a2ARonly_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig9'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4], [0,5e-4]], 
    text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, show_average=True)

# --------------------------
# ----- 16 Cyg A and B -----
# --------------------------
#
#  16 Cyg A NO BIAS 
yscale=1.4
process_names=['aj_ARonly_16CygA_gate', 'aj_ARonly_16CygA_triangle', 'aj_ARonly_16CygA_gauss']
names=['aj_ARonly_16CygA','aj_ARonly_16CygA_triangle', 'aj_ARonly_16CygA_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig11A'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4], [0,5e-4]], 
    text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, yscale=yscale, show_average=True)
#   16 Cyg A WITH BIAS 
process_names=['aj_ARonly_16CygA_bias_gate', 'aj_ARonly_16CygA_bias_triangle', 'aj_ARonly_16CygA_bias_gauss']
names=['aj_ARonly_16CygA_bias','aj_ARonly_16CygA_bias_triangle', 'aj_ARonly_16CygA_bias_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig11B'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4], [0,5e-4]], 
    text_index=['(d), bias corr.', '(e), bias corr.', '(f), bias corr.'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, yscale=yscale, show_average=True)
#
#  16 Cyg B  LowSol
process_names=['aj_ARonly_16CygB_LowSol_gate', 'aj_ARonly_16CygB_LowSol_triangle', 'aj_ARonly_16CygB_LowSol_gauss']
names=['aj_ARonly_16CygB_LowSol','aj_ARonly_16CygB_LowSol_triangle', 'aj_ARonly_16CygB_LowSol_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig13A1'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], 
    text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, show_average=True)
#
process_names=['aj_ARonly_16CygB_LowSol_bias_gate', 'aj_ARonly_16CygB_LowSol_bias_triangle', 'aj_ARonly_16CygB_LowSol_bias_gauss']
names=['aj_ARonly_16CygB_LowSol_bias','aj_ARonly_16CygB_LowSol_bias_triangle', 'aj_ARonly_16CygB_LowSol_bias_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig13A2'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], 
    text_index=['(d), bias corr.', '(e), bias corr.', '(f), bias corr.'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, show_average=True)

#  16 Cyg B  UpSol
process_names=['aj_ARonly_16CygB_UpSol_gate', 'aj_ARonly_16CygB_UpSol_triangle', 'aj_ARonly_16CygB_UpSol_gauss']
names=['aj_ARonly_16CygB_UpSol','aj_ARonly_16CygB_UpSol_triangle', 'aj_ARonly_16CygB_UpSol_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig14B1'
#
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], 
    text_index=['(a)', '(b)', '(c)'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, show_average=True)
process_names=['aj_ARonly_16CygB_UpSol_bias_gate', 'aj_ARonly_16CygB_UpSol_bias_triangle', 'aj_ARonly_16CygB_UpSol_bias_gauss']
names=['aj_ARonly_16CygB_UpSol','aj_ARonly_16CygB_UpSol_bias_triangle', 'aj_ARonly_16CygB_UpSol_bias_gauss']
data_format=['tamcmc', process_names, 'A', 0, 0, 1]#, dir_mcmc_CFonly, process_name_CFonly, 'A', 0, 0, 1] # data_type, process_name, phase, chain, period + Priors info: dir_mcmc_CFonly, process_name, 'A', 0,0,1
file_out=dir_out+'Fig14B2'
show_pdf_vpaper(dir_mcmc=dir_mcmc,names=names, logepsilon=[False,False], burnin=0.0, xlim_epsilon=[[0, 5e-3],[0,5e-4]], 
    text_index=['(d), bias corr.', '(e), bias corr.', '(f), bias corr.'], data_format=data_format, file_out=file_out, legend_names=legend_names, show_intervals=False, show_average=True)


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
dir_out = dir_core + '/Figures_publish/version_2/Bias_MAPs/'
numax_star=2150.
## ---- PROCESS ALL ----
# -------- HNR 30 Tobs=730 days Polar -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs730_Polar/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Polar/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs730_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs730_Polar/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Polar/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs730_Polar/products/']
fileout_all=dir_out + 'Fig5-Bias_map_HNR30_Tobs730_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(a)','(b)', '(c)'])
# -------- HNR 30 Tobs=730 days Equatorial -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs730_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs730_Equatorial/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs730_Equatorial/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs730_Equatorial/products/']
fileout_all=dir_out + 'Fig4-Bias_map_HNR30_Tobs730_Equatorial'
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
fileout_all=dir_out + 'Fig5-Bias_map_HNR30_Tobs1460_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(d)','(e)', '(f)'])
# -------- HNR 30 Tobs=1460 days Equatorial -------
combi_files=[dir_data +'HNR30_a1ovGamma0.4_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.5_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR30_a1ovGamma0.6_Tobs1460_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR30_a1ovGamma0.4_Tobs1460_Equatorial/products/', dir_data+'HNR30_a1ovGamma0.5_Tobs1460_Equatorial/products/',dir_data+'HNR30_a1ovGamma0.6_Tobs1460_Equatorial/products/']
fileout_all=dir_out + 'Fig4-Bias_map_HNR30_Tobs1460_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=None, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True, text_index=['(d)','(e)', '(f)'])
# -------- HNR 20 Tobs=1460 days Polar -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Polar/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/Combinations.txt', dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Polar/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Polar/products/']
fileout_all=dir_out + 'Fig19-Bias_map_HNR20_Tobs1460_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=20, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
# -------- HNR 20 Tobs=1460 days Equatorial -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Equatorial/products/']
fileout_all=dir_out + 'Fig18-Bias_map_HNR20_Tobs1460_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=20, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
# -------- HNR 10 Tobs=1460 days Polar -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Polar/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/Combinations.txt', dir_data+'HNR10_a1ovGamma0.6_Tobs1460_Polar/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Polar/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Polar/products/',dir_data+'HNR10_a1ovGamma0.6_Tobs1460_Polar/products/']
fileout_all=dir_out + 'Fig17-Bias_map_HNR10_Tobs1460_Polar'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=10, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
# -------- HNR 10 Tobs=1460 days Equatorial -------
combi_files=[dir_data +'HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/Combinations.txt', dir_data+'HNR10_a1ovGamma0.6_Tobs1460_Equatorial/Combinations.txt']
MCMCdir=[dir_data+'/HNR1020_a1ovGamma0.4_Tobs1460_Equatorial/products/', dir_data+'HNR1020_a1ovGamma0.5_Tobs1460_Equatorial/products/',dir_data+'HNR20_a1ovGamma0.6_Tobs1460_Equatorial/products/']
fileout_all=dir_out + 'Fig16-Bias_map_HNR10_Tobs1460_Equatorial'
bias_analysis(MCMCdir, combi_files, numax_star,  fileout=fileout_all, abs_err=True, filter_HNR=10, saturate_colors=[True, 'user-defined', 3, 3, 3], sigma_norm=True,  text_index=['(d)','(e)', '(f)'])
#

#
'''
# This plot is not anymore in the paper
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
'''

# ---- EXTRA PLOTS ----
print(" ----  Extra plots ---- ")
fileout=dir_core + 'Extra_data/Extra_Figures/Fig3-Gizon2004.jpg'
a2_epsilon_plot(lrange=[1,2], colors=['Blue', 'Orange', 'Red'], ftype='gate', fileout=fileout)

print("ALL DONE")
