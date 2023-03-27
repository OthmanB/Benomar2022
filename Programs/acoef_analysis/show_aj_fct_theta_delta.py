import numpy as np
from scipy import interpolate
from activity import Qlm
from activity import eta0_fct
from acoefs import eval_acoefs
from termcolor import colored
from eval_aj_range import load_Alm_grids
from eval_aj_range import numax_from_stello2009
from eval_aj_range import Dnu_from_stello2009
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

def grid_aj_mean(numax=None, Dnu=None, Mass=None, Radius=None, Teff=None, epsilon_nl=5*1e-4, a1=1000, 
	dir_grids='/Users/obenomar/Work/tmp/test_a2AR/grids/gate/0.25deg_resol/', lmax=3,
	gridfiles=['grid_Alm_1.npz', 'grid_Alm_2.npz', 'grid_Alm_3.npz']):
	'''
	Make a full grid of aj E [1,6] coefficients for a given star of Mass=Mass, Radius=Radius and Teff=Teff 
	and given an activity level epsilon_nl and a rotation a1
	If one wants a purely observational approach, it can provides directly numax (instead of M, R, Teff) and/or Dnu
	If only numax is provided, Dnu is determined using scaling relation with numax from Stello+2009. Same if only Dnu is provided
	This is usefull to set the range of simulations for aj and for setting priors on aj odds coefficient while fitting
	Note: This function **only** considers the mean value of aj over l and at numax
	'''
	
	R_sun=6.96342e5 #in km
	M_sun=1.98855e30 #in kg
	if numax != None and Dnu == None:
		print('Calculating Dnu(numax)...')
		Dnu=Dnu_from_stello2009(numax)
		print('Dnu = ', numax)
		eta0=eta0_fct(Dnu=Dnu)
	#
	if numax == None and Dnu != None:
		print('Calculating numax(Dnu)...')
		numax=numax_from_stello2009(Dnu)
		eta0=eta0_fct(Dnu=Dnu)
	#
	if numax != None and Dnu != None:
		print('Using numax and Dnu...')
		eta0=eta0_fct(Dnu=Dnu)
	#	
	if numax == None and Dnu == None and Mass != None and Radius != None and Teff !=None:
		print('Using M,R,Teff...')
		numax=numax_fct(Mass=Mass, Radius=Radius, Teff=Teff)
		Volume=np.pi*(Radius*R_sun)**3 * 4./3
		rho=Mass*M_sun/Volume * 1e-12 # Conversion into g/cm-3
		#print('rho =', rho)
		eta0=eta0_fct(rho=rho)
	if numax == None and Dnu == None and (Mass == None or Radius == None or Teff == None):
		print('Error in eval_aj_mean_range: You need to provide (M, R, Teff) or numax and/or Dnu')
		print('                             Please read the description of the function before using it')
		exit()
	
	print('numax =', numax)
	jmax=2*lmax 
	#
	theta, delta, Alm= load_Alm_grids(dir_grids, gridfiles, lmax=lmax)
	#
	aj_grid=np.zeros((jmax, len(theta), len(delta))) # The grid contains
	for j in range(len(theta)):
		for k in range(len(delta)):
			aj=np.zeros(2*lmax)
			for l in range(1,lmax+1):
				nu_nlm=[]
				for m in range(-l, l+1):
					# perturvation from AR		
					dnu_AR=numax*epsilon_nl*Alm[l-1][m+l][j,k] # All Alm(theta, delta) are in [j,k]
					# perturbation from CF
					dnu_CF=eta0*numax * (a1*1e-9)**2 * Qlm(l,m)
					nu_nlm.append(numax + dnu_AR + dnu_CF)
					#print('(j,k) = (', j, ',', k,')  theta =', theta[j]*180./np.pi, "  delta =", delta[k]*180./np.pi, " dnu_AR =", dnu_AR*1000)
				a=eval_acoefs(l, nu_nlm)
				# Averaging over l
				for o in range(len(aj)):
					if o < 2:
						aj[o]=aj[o] + a[o]/lmax
					if o >=2 and o < 4:
						if l>=2:
							aj[o]=aj[o] + a[o]/(lmax-1)
					if o >=3 and o <6:
						if l>=3:
							aj[o]=aj[o] + a[o]/(lmax-2)
			aj_grid[:,j,k]=aj*1000 # aj converted into nHz
	return theta, delta, aj_grid 

def aj_mean_from_theta_delta(theta_star, delta_star, numax=2150., Dnu=103.11, a1=1000, epsilon_nl=5*1e-4, 
				dir_grids='/Users/obenomar/Work/tmp/test_a2AR/grids/gate/0.25deg_resol/'):
	'''
		This function gives the value of aj_mean for an interval of a given set of star parameters and for theta,delta
	'''
	if theta_star > np.pi/2 or theta_stars < 0 or delta_star > np.pi/4 or delta_star < 0:
		print('theta and delta must be in radians, but inputs are outside expected boundaries (theta: [0, pi/2], delta: [0, pi/4]')
		print('Cannot proceed. The program will exit now')
		exit()
	
	theta_grid, delta_grid, aj_grid=grid_aj_mean(numax=numax, Dnu=Dnu, Mass=None, Radius=None, Teff=None, epsilon_nl=epsilon_nl, a1=a1, 
			dir_grids=dir_grids)
		
	# Initialise the interpolator once
	Ndelta=len(delta_grid)
	Ntheta=len(theta_grid)
	print("  - Initializing the interpolators for l=1,2,3...")
	ajgrid_flat=[]
	for j in range(Ndelta):
		ajgrid_flat.append(aj_grid[1][:,j])
	func_a2=interpolate.interp2d(theta_grid, delta_grid, ajgrid_flat, kind='cubic')
	ajgrid_flat=[]
	for j in range(Ndelta):
		ajgrid_flat.append(aj_grid[3][:,j])
	func_a4=interpolate.interp2d(theta_grid, delta_grid, ajgrid_flat, kind='cubic')
	ajgrid_flat=[]
	for j in range(Ndelta):
		ajgrid_flat.append(aj_grid[5][:,j])
	func_a6=interpolate.interp2d(theta_grid, delta_grid, ajgrid_flat, kind='cubic')

	a2=func_a2(theta_star, delta_star)
	a4=func_a4(theta_star, delta_star)
	a6=func_a6(theta_star, delta_star)
	print('<a2>l = ', a2)
	print('<a4>l = ', a4)
	print('<a6>l = ', a6)
	return a2,a4,a6

def show_aj_fct_theta_delta(numax=2150., Dnu=103.11, a1=1000., epsilon_nl=5*1e-4, dir_grids=None, file_out='aj_theta_delta', lmax=3):
	'''
		Function that plots the a2, a4, a6 coefficient for a serie of theta and delta values. This allows a visualisation
		of the potential uniqueness of a solution in the aj parameter space and thus serves as a basis to explain why a2 
		and a4 are enough to ensure the uniqueness/gaussianity of the solution when Alm is made using a 'gate' function.
		Note that other functions (e.g. 'gauss' filter) may not have the same aj coefficients in function of theta and delta.
		Information about the default numax and Dnu: These are those from 16 Cyg A
		for which l=0 modes are taken as: 1391.62917, 1494.98697, 1598.65899, 1700.89058 ,1802.28949,1904.58551,2007.55442,2110.93592,2214.21018,2317.33199,2420.92615,2525.18818,2629.41124,2734.00654
	'''
	cwd = os.getcwd()
	if file_out == None:
		file_out=cwd + '/../../Data/Figures_publish/Fig5-aj_theta_delta'
	if dir_grids == None:
		dir_grids=[]
		dir_grids.append(cwd + '/../../Data/grids/gate/0.25deg_resol/')
		dir_grids.append(cwd + '/../../Data/grids/triangle/0.25deg_resol/')
		dir_grids.append(cwd + '/../../Data/grids/gauss/0.25deg_resol/')
		grid_name=['gate', 'triangle', 'gauss']
	txtsize=15
	theta_all=[]
	delta_all=[]
	aj_grid_all=[]
	for dir_g in dir_grids:
		theta, delta, aj_grid=grid_aj_mean(numax=numax, Dnu=Dnu, Mass=None, Radius=None, Teff=None, epsilon_nl=epsilon_nl, a1=a1, dir_grids=dir_g, lmax=lmax)
		theta_all.append(theta)
		delta_all.append(delta)
		aj_grid_all.append(aj_grid)

	fig_a2, ax_a2 = plt.subplots(1)
	fig_a4, ax_a4 = plt.subplots(1)
	fig_a6, ax_a6 = plt.subplots(1)
	ax_a2.set_ylabel('$a^{(AR)}_2$ (nHz)', fontsize=txtsize)
	ax_a2.set_xlabel(r'$\theta_0$ ($^\circ$)', fontsize=txtsize)
	ax_a2.tick_params(axis='x', labelsize=txtsize)
	ax_a2.tick_params(axis='y', labelsize=txtsize)
	ax_a2.axhline(y=0, color='gray', linestyle='--')
	ax_a2.set_xlim([-1, 91])
	ax_a2.set_xticks(np.arange(0, 100, 10))
	if lmax==1: 
		ax_a2.annotate("Averaged over l=1", xy=(0.70, 0.05), fontsize=10, ha="left", xycoords=ax_a2.transAxes, color='r')
	if lmax==2: 
		ax_a2.annotate("Averaged over l=1,2", xy=(0.70, 0.05), fontsize=10, ha="left", xycoords=ax_a2.transAxes, color='r')
	if lmax==3: 
		ax_a2.annotate("Averaged over l=1,2,3", xy=(0.70, 0.05), fontsize=10, ha="left", xycoords=ax_a2.transAxes, color='r')
	if lmax >= 2:
		ax_a4.set_ylabel('$a^{(AR)}_4$ (nHz)', fontsize=txtsize)
		ax_a4.set_xlabel(r'$\theta_0$ ($^\circ$)', fontsize=txtsize)
		ax_a4.tick_params(axis='x', labelsize=txtsize)
		ax_a4.tick_params(axis='y', labelsize=txtsize)
		ax_a4.axhline(y=0, color='gray', linestyle='--')	
		ax_a4.set_xlim([-1, 91])
		ax_a4.set_xticks(np.arange(0, 100, 10))
		if lmax==2: 
			ax_a4.annotate("Averaged over l=2", xy=(0.70, 0.05), fontsize=10, ha="left", xycoords=ax_a4.transAxes, color='r')
		if lmax==3: 
			ax_a4.annotate("Averaged over l=2,3", xy=(0.70, 0.05), fontsize=10, ha="left", xycoords=ax_a4.transAxes, color='r')
	if lmax >= 3:
		ax_a6.set_ylabel('$a^{(AR)}_6$ (nHz)', fontsize=txtsize)
		ax_a6.set_xlabel(r'$\theta_0$ ($^\circ$)', fontsize=txtsize)
		ax_a6.tick_params(axis='x', labelsize=txtsize)
		ax_a6.tick_params(axis='y', labelsize=txtsize)
		ax_a6.axhline(y=0, color='gray', linestyle='--')
		ax_a6.set_xlim([-1, 91])
		ax_a6.set_xticks(np.arange(0, 100, 10))
		if lmax==3: 
			ax_a6.annotate("Averaged over l=3", xy=(0.74, 0.05), fontsize=10, ha="left", xycoords=ax_a6.transAxes, color='r')
	# Show all aj(theta) at a given delta = delta_show
	# a2 is in [1], a4 is in [3] and a6 is in [5]
	#print(delta)
	#delta_show_list=[5, 10, 20, 40]
	delta_show_list=[5, 10, 20]
	labels=[r'$\delta=5$ deg', r'$\delta=10$ deg', r'$\delta=20$ deg']#, r'$\delta=40$ deg']
	tol=theta[1] - theta[0]
	lines=['-', '--', '-.', ':']
	colors_for_filter=['black', 'red', 'blue']
	labels_filter=[r'$\Pi(\theta_0, \delta)$', r'$\Lambda(\theta_0, \delta)$', r'$\mathcal{N}(\theta_0, \delta)$']
	for k in range(len(dir_grids)):
		delta=delta_all[k]
		theta=theta_all[k]
		aj_grid=aj_grid_all[k]
		for i in range(len(delta_show_list)): 
			delta_show=delta_show_list[i]*np.pi/180.
			pos_delta=np.where(np.bitwise_and(delta >= delta_show - tol, delta <= delta_show + tol))[0]
			pos_delta=pos_delta[0]
			#pos_theta=np.where(theta > delta_show/2)[0] # We ensure that we show only results that match the condition theta0 > delta/2 
			if grid_name[k] == 'gate':
				pos_theta=np.where(np.bitwise_and(theta > delta_show/2, theta < np.pi/2-delta_show/2))[0] # We ensure that we show only results that match the condition theta0 > delta/2 AND theta0 > 90. - delta/2
			else:
				pos_theta=np.where(theta > 0)[0] # No restriction in the case of a gaussian or triangular shape as truncation of the function happens then
			#print('pos_delta = ', pos_delta, '  delta =', delta[pos_delta]*180./np.pi)
			ax_a2.plot(theta[pos_theta]*180./np.pi, aj_grid[1][pos_theta, pos_delta], color=colors_for_filter[k], linestyle=lines[i], label=labels[i])
			if grid_name[k] == 'gate':
				ax_a2.plot(theta[pos_theta][0]*180./np.pi, aj_grid[1][pos_theta[0], pos_delta], color=colors_for_filter[k], marker='|', markersize=14, linewidth=2)
				ax_a2.plot(theta[pos_theta][-1]*180./np.pi, aj_grid[1][pos_theta[-1], pos_delta], color=colors_for_filter[k], marker='|', markersize=14, linewidth=2)
			if lmax >= 2:
				ax_a4.plot(theta[pos_theta]*180./np.pi, aj_grid[3][pos_theta, pos_delta], color=colors_for_filter[k], linestyle=lines[i], label=labels[i])
				if grid_name[k] == 'gate':
					ax_a4.plot(theta[pos_theta][0]*180./np.pi, aj_grid[3][pos_theta[0], pos_delta], color=colors_for_filter[k], marker='|', markersize=14, linewidth=2)
					ax_a4.plot(theta[pos_theta][-1]*180./np.pi, aj_grid[3][pos_theta[-1], pos_delta], color=colors_for_filter[k], marker='|', markersize=14, linewidth=2)
			if lmax >= 3:
				ax_a6.plot(theta[pos_theta]*180./np.pi, aj_grid[5][pos_theta, pos_delta], color=colors_for_filter[k], linestyle=lines[i], label=labels[i])
				if grid_name[k] == 'gate':
					ax_a6.plot(theta[pos_theta][0]*180./np.pi, aj_grid[5][pos_theta[0], pos_delta], color=colors_for_filter[k], marker='|', markersize=14, linewidth=2)
					ax_a6.plot(theta[pos_theta][-1]*180./np.pi, aj_grid[5][pos_theta[-1], pos_delta], color=colors_for_filter[k], marker='|', markersize=14, linewidth=2)
	# Manually setting the legend in order to have two legends: One for the color and another for the line type
	lin1=[]
	lin2=[]
	for c in range(len(lines)):
		lin1.append(Line2D([0], [0], linestyle=lines[c], color='black', lw=2))
	for c in range(len(colors_for_filter)):
		lin2.append(Line2D([0], [0], color=colors_for_filter[c], lw=2))
	legend1=ax_a2.legend(lin1, labels, fontsize=12, loc="upper left")
	legend2=ax_a2.legend(lin2, labels_filter, fontsize=12, loc="upper center")
	ax_a2.add_artist(legend1) # We add back the first legend that was automatically removed by the second call of ax_a2.legend()
	#ax_a2.legend(fontsize=12, loc="upper left")
	fig_a2.tight_layout()
	fig_a2.savefig(file_out + '_a2.jpg', dpi=300, bbox_inches="tight")
	if lmax>=2:
		fig_a4.tight_layout()
		fig_a4.savefig(file_out + '_a4.jpg', dpi=300, bbox_inches="tight")
	if lmax>=3:
		fig_a6.tight_layout()
		fig_a6.savefig(file_out + '_a6.jpg', dpi=300, bbox_inches="tight")
	plt.close('all')
	print('Files are:')
	print('    ' + file_out + '_a2.jpg')
	if lmax>=2:
		print('    ' + file_out + '_a4.jpg')
	if lmax>=3:
		print('    ' + file_out + '_a6.jpg')	


