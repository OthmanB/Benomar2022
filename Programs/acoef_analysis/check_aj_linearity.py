# This is a small program that demonstrate the linearity of the aj solutions in terms of n and l (monotonically increase/decrease with frequency)

import matplotlib.pyplot as plt
import os
import numpy as np
from termcolor import colored

def read_mcmcobs(file):
	return read_obsfiles(file, real_data=True)

# Read files that contain observed a2 coefficients
def read_obsfiles(file, read_a4=False, read_a6=False, real_data=False):
	pos_a2_med=4
	pos_a4_med=10
	pos_a6_med=16
	f=open(file, 'r')
	txt=f.read()
	f.close()
	txt=txt.split('\n')
	en=[]
	el=[]
	nu_nl=[]
	a2=[]
	sig_a2=[]
	a4=[]
	sig_a4=[]
	a6=[]
	sig_a6=[]
	skip=0
	#print(txt)
	#print('----')
	if real_data == False:
		for t in txt:
			s=t.split()
			if s != '' and s !=[]:
				#print(s[0])
				if s[0] == '#' or s[0] == [] or s[0] == '':
					skip=skip+1
				else:
					#print(len(en))
					if len(en) != 0:
						en.append(en[-1]+1)
					else:
						en.append(1)
					el.append(int(float(s[0])))
					nu_nl.append(float(s[1]))
					a2.append(float(s[pos_a2_med]))
					em=float(s[pos_a2_med]) - float(s[pos_a2_med-1])
					ep=float(s[pos_a2_med+1]) - float(s[pos_a2_med])
					sig_a2.append(np.sqrt(em**2 + ep**2)/2)
					if read_a4 == True:
						a4.append(float(s[pos_a4_med]))
						em=float(s[pos_a4_med]) - float(s[pos_a4_med-1])
						ep=float(s[pos_a4_med+1]) - float(s[pos_a4_med])
						sig_a4.append(np.sqrt(em**2 + ep**2)/2)
					if read_a6 == True:
						a6.append(float(s[pos_a6_med]))
						em=float(s[pos_a6_med]) - float(s[pos_a6_med-1])
						ep=float(s[pos_a6_med+1]) - float(s[pos_a6_med])
						sig_a6.append(np.sqrt(em**2 + ep**2)/2)
		return en, el, nu_nl, a2, sig_a2, a4, sig_a4, a6, sig_a6
	else:
		a1=[]
		sig_a1=[]
		a3=[]
		sig_a3=[]
		a5=[]
		sig_a5=[]
		for t in txt:
			done=False
			s=t.split()
			if s != '' and s !=[]:
				#print(s[0])
				if s[0] == '#' or s[0] == [] or s[0] == '':
					skip=skip+1
				else:
					if len(en) != 0:
						en.append(en[-1]+1)
					else:
						en.append(1)
					if s[0] == '!' and s[1] == 'l':
						el=np.asarray(s[3:], dtype=int)
						done=True
					if s[0] == '!' and s[1] == 'nu_nl_obs':
						nu_nl=np.asarray(s[3:], dtype=float)
						done=True
					if done !=True:
						a1.append(float(s[0]))
						a2.append(float(s[1]))
						a3.append(float(s[2]))
						a4.append(float(s[3]))
						a5.append(float(s[4]))
						a6.append(float(s[5]))
						sig_a1.append(float(s[6]))
						sig_a2.append(float(s[7]))
						sig_a3.append(float(s[8]))
						sig_a4.append(float(s[9]))
						sig_a5.append(float(s[10]))
						sig_a6.append(float(s[11]))
		#print(a1,  a2, a3, a4, a5, a6)
		#print(sig_a1, sig_a2, sig_a3, sig_a4, sig_a5, sig_a6)
		#exit()
		return en, el, nu_nl, a1, a2, a3, a4, a5, a6, sig_a1, sig_a2, sig_a3, sig_a4, sig_a5, sig_a6


def get_files(dir_data, extension='.data', fullpath=True):
	files=[]
	for file in os.listdir(dir_data):
		# check the extension of files
		if file.endswith(extension):
			if fullpath == True:
				files.append(os.path.join(root, file))
			else:
				files.append(file)
	return files

def check_aj_linearity(dir_data=None, do_plots=False, full_labels=True, dir_out=None):
	''' 
		This is the main function that gives you the level of agreement in term of linearity
		It scan the 'dir_data' to find .data files (created by fit_a2sig.do_simfile(), read all of them and gives the max delta
		between the data points and their linear fit
		Note that to perform the linearity check, do_simfile() must be used with its default relative error setup (set to None).
		This is to ensure that the created data files do not add any random gaussian error, which obviously bias the evaluation
		of the linearity (there is a column for true inputs, but it is not read by read_obsfiles().
		Furthermore, you may need to set a1=0 otherwise it will incorporate the centrifugal force, which may introduce departure to linearity
	''' 
	txtsize=15
	polorder=1
	cols=['', 'black', 'dimgray', 'silver']
	marks=['', 'D', 'H', 'o']
	lines=['-','-', '--', '-.']

	if dir_data == None:
		print('Error: Please provide the path to the data for check_aj_linearity')
		exit()
	if dir_out == None:
		dir_out = dir_data
	#
	files_only=get_files(dir_data, fullpath=False)
	print('Search in dir :', dir_data)
	for f in files_only:
		print(' ---------------- ')
		print('  file:', f)
		fileout=dir_out + '/' + f
		en, el, nu_nl_obs, a2_obs, sig_a2_obs, a4_obs, sig_a4_obs, a6_obs, sig_a6_obs=read_obsfiles(fileout, read_a4=True, read_a6=True)
		el=np.array(el)
		nu_nl_obs=np.array(nu_nl_obs)
		a2_obs=np.array(a2_obs)
		a4_obs=np.array(a4_obs)
		a6_obs=np.array(a6_obs)
		if do_plots == True:
			fig_a2, ax_a2 = plt.subplots(1)
			fig_a4, ax_a4 = plt.subplots(1)
			fig_a6, ax_a6 = plt.subplots(1)
			if full_labels == True:
				ax_a2.set_title('file :' + str(f))
				ax_a4.set_title('file : ' + str(f))
				ax_a6.set_title('file : '+ str(f))
			ax_a2.set_ylabel('$a_2(n,l)$ (nHz)', fontsize=txtsize)
			ax_a2.set_xlabel('Frequency ($\mu$Hz)', fontsize=txtsize)
			ax_a4.set_ylabel('$a_4(n,l)$ (nHz)', fontsize=txtsize)
			ax_a4.set_xlabel('Frequency ($\mu$Hz)', fontsize=txtsize)
			ax_a6.set_ylabel('$a_6(n,l)$ (nHz)', fontsize=txtsize)
			ax_a6.set_xlabel('Frequency ($\mu$Hz)', fontsize=txtsize)
			ax_a2.tick_params(axis='x', labelsize=txtsize)
			ax_a2.tick_params(axis='y', labelsize=txtsize)
			ax_a4.tick_params(axis='x', labelsize=txtsize)
			ax_a4.tick_params(axis='y', labelsize=txtsize)
			ax_a6.tick_params(axis='x', labelsize=txtsize)
			ax_a6.tick_params(axis='y', labelsize=txtsize)
		#
		for l in range(1, np.max(el)+1):
			print(colored('     l =' + str(l), 'cyan'))
			pos=np.array(np.where(np.array(el) == l)).flatten()
			nu=nu_nl_obs[pos]
			a2=a2_obs[pos]
			a4=a4_obs[pos]
			a6=a6_obs[pos]
			a2_pol=np.polyfit(nu, a2, polorder)
			a2_fit=np.polyval(a2_pol, nu)
			a2_delta=np.max(a2-a2_fit)/np.mean(a2) * 100
			if np.isfinite(a2_delta):
				print(colored('         maxdelta_a2 (%):'+str(a2_delta), 'blue'))
			else:
				print(colored('         maxdelta_a2 (%):'+str(a2_delta), 'red'))
			#
			if l>=2:
				a4_pol=np.polyfit(nu, a4, polorder)
				a4_fit=np.polyval(a4_pol, nu)
				a4_delta=np.max(a4-a4_fit)/np.mean(a4) * 100
				if np.isfinite(a4_delta):
					print(colored('         maxdelta_a4 (%): {}'.format(a4_delta), 'blue'))
				else:
					print(colored('         maxdelta_a4 (%): {}'.format(a4_delta), 'red'))
			#
			if l>=3:
				a6_pol=np.polyfit(nu, a6, polorder)
				a6_fit=np.polyval(a6_pol, nu)
				a6_delta=np.max(a6-a6_fit)/np.mean(a6) * 100
				if np.isfinite(a2_delta):
					print(colored('         maxdelta_a6 (%): {}'.format(a6_delta), 'blue'))
				else:
					print(colored('         maxdelta_a6 (%): {}'.format(a6_delta), 'red'))
			#
			#
			if do_plots == True:
				ax_a2.plot(nu, a2, color=cols[l], marker=marks[l], label="l = " + str(l), linestyle=lines[l])
				#
				if l>=2:
					ax_a4.plot(nu, a4, color=cols[l], marker=marks[l], linestyle=lines[l])
				#
				if l >=3:
					ax_a6.plot(nu, a6, color=cols[l], marker=marks[l], linestyle=lines[l])
			# Handling legends
			ax_a2.legend(fontsize=12, loc='upper left')	
			fig_a2.savefig(fileout + '_a2.jpg', dpi=300, bbox_inches="tight")
			fig_a4.savefig(fileout + '_a4.jpg', dpi=300, bbox_inches="tight")
			fig_a6.savefig(fileout + '_a6.jpg', dpi=300, bbox_inches="tight")
			plt.close('all')
	print('Files saved in:' + dir_out)
