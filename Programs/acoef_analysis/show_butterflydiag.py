import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
from sunpy.coordinates.sun import carrington_rotation_time
from sunpy.coordinates.sun import carrington_rotation_number
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy.signal import medfilt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from activity import gauss_filter, gauss_filter_cte, triangle_filter, gate_filter

def read_dailyarea(file, valid_only=True, date_format='original'):
	'''
		Read the daily average number of spots from 1874 (until 2016 as the date this code is writen - 02/06/2022)
		as per provided at https://solarscience.msfc.nasa.gov/greenwch.shtml
		file: input data file
		valid_only: If True, remove negative (-1) counts corresponding to days without observations
		date_format: Set the output format of the data
			- 'original': Keep the (YY, MM, DD) data for the date as it is
			- 'date': convert the 3 columns giving the time (YY-MM-DD) into a single input of type datetime. 
					  Note that the output here is a list for date and a numpy array for the other data (Total, North, South)
		    - 'timestamp': convert the 3 columns giving the time (YY-MM-DD) into a single timestamp as per defined
		    			   in the datetime python package
	'''
	# Read the file
	f=open(file, 'r')
	txt=f.read()
	f.close()
	txt=txt.split('\n')
	# Separate the first line (header) from the raw data
	header=txt[0]
	raw_data=txt[1:]
	# Parse the raw data into a numpy table
	Ncols=len(raw_data[0].split())
	Nlines=len(raw_data)
	data=np.zeros((Nlines, Ncols))
	cpt=0
	for i in range(Nlines):
		line=raw_data[i].split()
		if line != '' and line !=[]:
			if valid_only == False:
				data[i, :]=line
			else:
				data[cpt, :]=line 
				cpt=cpt+1
	if valid_only == True:
		data=data[0:cpt,:]
		Nlines=cpt-1
	# Handling convert_to_date
	if date_format == 'original':
		return data
	if date_format == 'date':
		date=[]
		outputs=np.zeros((Nlines, Ncols-3))
		for i in range(Nlines):
			date.append(datetime(int(data[i,0]), int(data[i,1]), int(data[i,2])))
			outputs[i,:]=data[i,3:]
		return date, outputs
	if date_format == 'timestamp':
		outputs=np.zeros((Nlines, Ncols-2))
		for i in range(Nlines):
			outputs[i,0]=datetime.timestamp(datetime(int(data[i,0]), int(data[i,1]), int(data[i,2])))
			outputs[i,1:]=data[i,3:]
		return outputs

def read_butterflydata(file, date_format='carrington'):
	# Read the file
	f=open(file, 'r')
	txt=f.read()
	f.close()
	txt=txt.split('\n')
	# Separate the first line (header) from the raw data
	header=txt[0]
	raw_data=txt[1:]
	Ncols=len(raw_data[0].split())
	Nlines=len(raw_data)
	Blocksize=6 # A data block is 1 Carington number, followed by a data block of 5 lines
	Nblocks=int(Nlines/Blocksize) # Determine the Number of blocks
	# Read the Carrington numbers only first
	carrington=np.zeros(Nblocks, dtype=float)
	cpt=0
	for i in range(0,Nlines, Blocksize):
		carrington[cpt]=raw_data[i]
		cpt=cpt+1
	# Read the data within a block. The number of records within a block is 50,
	# distributed within 5 lines of 10 entry each. 
	# Those 50 entries give the number of spots as a function sin(latitude)
	spot_area=np.zeros((Nblocks,50))
	cpt=0
	for i in range(1, Nlines, Blocksize): # For each block
		for j in range(Blocksize-1): # Read each block lines
			line=raw_data[i+j].split(',')[0:-1] # We remove the empty '' at the end due to the last ','
			if line != '' and line !=[]:
				spot_area[cpt, j*len(line):(j+1)*len(line)]=line
		cpt=cpt+1
	# Compute the latitude array in degree: Each 50 records from the file is a sin(latitude) 
	latitude=np.arcsin(np.linspace(-1, 1, 50))*180./np.pi

	# Give the date as per specified by the user
	if date_format == 'carrington':
		time=carrington
		passed=True
	if date_format == 'date': 
		# Convert the Carrington number to an approximate date in datetime package format
		# Exact time is ignored so that we might have an error of 12h
		time=[]
		for c in carrington:
			t=date.fromisoformat(carrington_rotation_time(c).value.split()[0])
			print('     original: ', c, '    value: ', carrington_rotation_time(c).value, '    time:',t)
			time.append(t)
		passed=True
	if date_format == 'timestamp':
		# Convert the Carrington number to an exact timestamp as per defined in the datetime package
		time=[]
		for c in carrington:
			t=datetime.fromisoformat(carrington_rotation_time(c).value).timestamp()
			print('     original: ', c, '    value: ', carrington_rotation_time(c).value, '    time:',t)
			time.append(t)
		time=np.asarray(time)
		passed=True
	if passed != True:
		print("Error: Invalid provided date_format. Set it to either 'carrington', 'date' or 'timestamp'")
	return time, latitude, spot_area.transpose()

def select_dates(date_interval, carrington_time, spot_area):
	'''
		Function that retrieve a provided date interval
		date_interval: Array of string with a date in the ISO format ('YY-MM-DD')
		carrington_time: Time as read in the Greenwich table for the butterfly diagram: In Carrington Units
		spot_area: A 2D numpy array as per returned by read_butterflydata()
	'''
	# Convert the date interval into a Carrington time
	tmin=carrington_rotation_number(datetime.fromisoformat(date_interval[0]))
	tmax=carrington_rotation_number(datetime.fromisoformat(date_interval[1]))
	posOK=np.where(np.bitwise_and(carrington_time >= tmin, carrington_time <= tmax))
	return carrington_time[posOK[0]], spot_area[:,posOK[0]]

def select_latitudes(latitude_interval, latitude, spot_area):
	'''
		Function that retrieve a provided latitude interval
		latitude_interval: Array with two values: A minimum and maximum latitude
		latitude: The full latitude range associated to spot_area
		spot_area: A 2D numpy array as per returned by read_butterflydata()
	'''
	posOK=np.where(np.bitwise_and(latitude >= latitude_interval[0], latitude <= latitude_interval[1]))
	return latitude[posOK[0]], spot_area[posOK[0],:]


def get_year_frac(date_in):
	try:
		start = date(date_in.year, 1, 1).toordinal()
	except: # In case the date was actually provided as a string an not as a datetime object... try to convert it and retry
		date_in=datetime.fromisoformat(date_in)
		start = date(date_in.year, 1, 1).toordinal()
	year_length = date(date_in.year+1, 1, 1).toordinal() - start
	return date_in.year + float(date_in.toordinal() - start) / year_length

def carrington2fracyear(carrington_time):
	d=datetime.fromisoformat(carrington_rotation_time(int(carrington_time)).value)
	return get_year_frac(d)

def do_diagram(ax, date_interval, latitude, spot_area, latitude_range=[-90, 90], timezones = [], text_index=None):
	unit=1e-3 
	vmin=0
	vmax=np.max(spot_area*unit)/10
	# Convert map in % of the Hemispheric area. Raw units are in 10^-6 of Hemisphere, so we need 
	# to multiply them by 10^-3 to get % of Hemisphere
	l, s = select_latitudes(latitude_range, latitude, spot_area*unit)
	im = ax.imshow(s, aspect='auto', cmap='Reds', vmin=vmin, vmax=vmax, extent = [date_interval[0] , date_interval[1], latitude_range[0] , latitude_range[1]])
	ax.set_xlabel('Year', fontsize=12)
	ax.set_ylabel('Latitude (deg)', fontsize=12)
	ax.tick_params(axis='x', labelsize=12)
	ax.tick_params(axis='y', labelsize=12)
	ax.axhline(0, linestyle='--', color='black')
	cbaxes = inset_axes(ax, width="20%", height="2%", loc='upper right') 
	bar1 = plt.colorbar(im, orientation='horizontal', cax=cbaxes, ticks=[round(vmin,2), round(vmax,2)])
	bar1.ax.tick_params(labelsize=9)
	if text_index != None:
		ax.annotate(text_index, xy=(0.85, 0.05), xycoords=ax.transAxes, fontsize=18)
	# If colored zones are requested, handle them
	# One expects zones to be a list of lists. The lower level list
	# must be of the format [min_date, max_date, color_name]
	# min and max dates are in string of the ISO format 'YY-MM-DD' or datetime objects
	if timezones != []:
		alpha=0.4
		for z in timezones:
			rectangle = Rectangle((get_year_frac(z[0]), latitude_range[0]), get_year_frac(z[1])-get_year_frac(z[0]), latitude_range[1]- latitude_range[0], edgecolor=None, facecolor=z[2], linewidth=None, alpha=alpha)
			ax.add_patch(rectangle)
 
def do_projection(ax, date_filters, carrington_time, latitude, spot_area, rotate=False, latitude_range=[-45,45], 
		smooth_lvl=1, norm=None, pos_val='in', 
		text_index=None, ft_size_legend=5, do_legend=True, ft_size_text=8, ft_size_text2=8, ft_size_labels=12, ln_width=1):
	Nzones=len(date_filters)
	Nlatitudes=len(spot_area[:,0])
	norms=[]
	for i in range(Nzones):
		if len(date_filters[i]) == 2:
			dates=date_filters[i]
		else:
			dates=date_filters[i][0:2]
		c, s=select_dates(dates, carrington_time, spot_area)
		collapsogram=np.zeros(Nlatitudes)
		# by default the collapsogram uses the 'mean' for the normalisation 
		# and convert into % of the Hemispheric area raw units are in 10^-6 of Hemisphere, so we need 
		# to multiply them by 10^3 to get % of Hemisphere
		if norm == None:
			norm=len(s[0,:])*1e3
		#	
		for j in range(Nlatitudes):
			collapsogram[j]=np.sum(s[j,:])/norm # Collapse the time axis to have the total spot area over period
		# Add indication of the median
		pos_north=np.where(latitude > 0)
		pos_south=np.where(latitude < 0)
		med_north=np.average(latitude[pos_north], weights=collapsogram[pos_north])
		med_south=np.average(latitude[pos_south], weights=collapsogram[pos_south])
		collapsed = medfilt(collapsogram,smooth_lvl)
		norms.append(np.max(collapsed))
		if rotate == False:
			ymax=np.max(collapsed)
			ax.plot(latitude, collapsed, color=date_filters[i][2], label=date_filters[i][0] + ' to ' + date_filters[i][1], linewidth=ln_width)
			ax.set_xlim(latitude_range)
			ax.set_ylim(0, ymax*1.1)
			ax.set_xlabel('Latitude (deg)', fontsize=ft_size_labels)
			ax.set_ylabel('Area '+ r'($\%$)', fontsize=ft_size_labels)	
			ax.tick_params(axis='both', labelsize=ft_size_labels)
			ax.axvline(0, linestyle='--', color='black')	
			if date_filters[i][3] != False:
				ax.axvline(med_north, linestyle='-', color=date_filters[i][2], ymin=0.95, ymax=1, linewidth=2*ln_width)
				ax.axvline(med_south, linestyle='-', color=date_filters[i][2], ymin=0.95, ymax=1, linewidth=2*ln_width)
				ax.annotate("{0:.0f}".format(med_north), xy=(med_north, ymax*1.04), fontsize=ft_size_text, va="center", ha='left')
				if i ==0:
					ax.annotate("{0:.0f}".format(med_south), xy=(med_south, ymax*1.04), fontsize=ft_size_text, va="center", ha='left')
		else:
			ax.plot(collapsed, -latitude, color=date_filters[i][2],label=date_filters[i][0] + ' to ' + date_filters[i][1], linewidth=ln_width)
			ax.set_ylim(latitude_range)	
			ax.set_ylabel('Latitude (deg)', fontsize=ft_size_labels)
			ax.set_xlabel('Area '+ r'($\%$)', fontsize=ft_size_labels)	
			ax.tick_params(axis='x', labelsize=ft_size_labels)
			ax.axhline(0, linestyle='--', color='black')
			if date_filters[i][3] != False:
				ax.axhline(med_north, linestyle='-', color=date_filters[i][2], xmin=0.9, xmax=1, linewidth=2*ln_width)
				ax.axhline(med_south, linestyle='-', color=date_filters[i][2], xmin=0.9, xmax=1, linewidth=2*ln_width)
				if pos_val == 'out':
					ax.annotate("{0:.0f}".format(med_north), xy=(0.188, med_north), fontsize=ft_size_text, va="center")
					if i ==0:
						ax.annotate("{0:.0f}".format(med_south), xy=(0.188	, med_south), fontsize=ft_size_text, va="center")
				else:
					ax.annotate("{0:.0f}".format(med_north), xy=(0.155, med_north), fontsize=ft_size_text, va="bottom")
					if i ==0:
						ax.annotate("{0:.0f}".format(med_south), xy=(0.155	, med_south), fontsize=ft_size_text, va="top")
					
			ax.get_yaxis().set_visible(False)
	# Handling legends
	if do_legend == True:
		ax.legend(fontsize=ft_size_legend, loc='upper left')	
	if text_index != None:
		if rotate == True:
			ax.annotate(text_index, xy=(0.65, 0.05), xycoords=ax.transAxes, fontsize=18)
		else:
			ax.annotate(text_index, xy=(0.92, 0.92), xycoords=ax.transAxes, fontsize=ft_size_text2)
	return norms

def show_spot_model(ax, model_params, norm=1, rotate=True, color='Black', linestyle='-', linewidth=1, label=None):
	'''
		The core function that plots the model of the spots
		ax: The plot zone
		model_params: a 3-element lists with:
			[0] the type of model (triange, gate, gauss)
			[1] the theta0 parameter of the model (COLATITUDE)
			[2] the delta parameter of the model (ACTIVE ZONE EXTENSION)
		latitude_range: The range of latitudes to be computed and showed
		norm: The maximum height of the model. Used to scale when superimposing
		on another plot
	'''
	cte=180./np.pi # To convert the native pi units into degrees
	theta_min=0
	theta_max=np.pi
	theta=np.linspace(theta_min, theta_max, 1000)
	if model_params[0] == 'triangle':
		F=triangle_filter(theta, model_params[1]/cte, model_params[2]/cte)
	if model_params[0] == 'gate':
		F=gate_filter(theta, model_params[1]/cte, model_params[2]/cte)
	if model_params[0] == 'gauss':
		F=gauss_filter(theta, model_params[1]/cte, model_params[2]/cte)
		F=F/gauss_filter_cte(model_params[1]/cte, model_params[2]/cte)
	theta_colat=90 - theta*cte # Convert the colatitudes in latitudes
	if rotate == False:
		ax.plot(theta_colat, F*norm, color=color, linestyle=linestyle, linewidth=linewidth, label=label)
	else:
		ax.plot(F*norm, -theta_colat, color=color, linestyle=linestyle, linewidth=linewidth, label=label)


def show_diagram(filein=None, fileout=None):
	cwd = os.getcwd()
	if filein == None:
		filein = cwd + '/../../Data/External_data/Greenwich-data/butterflydata.txt'
	if fileout == None:
		fileout = cwd + '/../../Data/Figures_publish/Fig2AB-butterfly.jpg'
	date_filter_butterfly=['1985-01-01', '2022-01-01']
	#
	date_filters_projection=[]
	date_filters_projection.append(['1988-01-01', '1992-01-01', 'purple', True])
	date_filters_projection.append(['1999-01-01', '2002-01-01', 'blue',  True])
	#date_filters_projection.append(['2006-06-01', '2010-06-01', 'cyan', True])
	#date_filters_projection.append(['2007-01-01', '2011-06-01',  'green', True])
	date_filters_projection.append(['2006-01-01','2009-01-01',   'orange', False])
	#
	carrington_time, latitude, spot_area=read_butterflydata(filein, date_format='carrington')
	carrington_time, spot_area=select_dates(date_filter_butterfly, carrington_time, spot_area)

	# Compute the min and max date of the data set, assuming it was provided in Carrington units
	date_interval=[carrington2fracyear(carrington_time[0]), carrington2fracyear(carrington_time[-1])]
	print('Initial Carrington_time =', int(carrington_time[0]),  '    Date: ', date_interval[0])
	print('Final   Carrington_time =',int(carrington_time[-1]), '     Date: ', date_interval[1])
	#fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})
	#fig, ax = plt.subplots(1, 3, gridspec_kw={'width_ratios': [3, 1, 1]})
	fig = plt.figure(layout=None, num=1, clear=True)
	gs = fig.add_gridspec(nrows=1, ncols=14, left=0.1, right=0.90, hspace=0.05, wspace=0.1)
	ax_butterfly = fig.add_subplot(gs[0, 0:7]) # ZONE FOR THE BUTTERFLY
	ax_projection = fig.add_subplot(gs[0, 7:10]) # ZONE FOR THE FIRST PROJECTION
	ax_model = fig.add_subplot(gs[0, 10:14]) # ZONE FOR THE SECOND PROJECTION
	ax_model.tick_params(left = False, right = False , labelleft = False , labelbottom = True, bottom = True)
	ax_projection.tick_params(left = False, right = False , labelleft = False , labelbottom = True, bottom = True)
	ax=[ax_butterfly, ax_projection, ax_model]
	do_diagram(ax[0], date_interval, latitude, spot_area, latitude_range=[-60, 60], timezones=date_filters_projection, text_index='(a)')
	do_projection(ax[1], date_filters_projection, carrington_time, latitude, spot_area, 
		rotate=True, latitude_range=[-60, 60], text_index='(b)', do_legend=False)
	# Manually setting the legend in order to have two legends: One for the color and another for the line type
	lin1=[]
	lbl1=[]
	for d in date_filters_projection:
		lin1.append(Line2D([0], [0], linestyle='-', color=d[2], lw=2))
		lbl1.append(d[0] + ' to ' + d[1])
	ax_butterfly.legend(lin1, lbl1, fontsize=6, loc="upper left")
	#
	show_spots_with_model(ax[2], add_model=[['gate', 74, 20], ['triangle', 74, 30], ['gauss', 74, 6]])
	fig.tight_layout()
	plt.savefig(fileout, dpi=300)

	print('file save at: ', fileout)
	
def show_spots_with_model(ax=None, filein=None, fileout=None, add_model=[['gate', 74, 20], ['triangle', 74, 30], ['gauss', 74, 6]]):
	'''
		Contrary to show_diagram that shows the butterfly diagram + projection on the side,
		this function show only the projection and superimpose a series models on top of it
		Used to illustrate the accuracy of the representations
	'''
	cwd = os.getcwd()
	if filein == None:
		filein = cwd + '/../../Data/External_data/Greenwich-data/butterflydata.txt'
	if fileout == None:
		fileout = cwd + '/../../Data/Figures_publish/Fig2C-butterfly.jpg'

	date_filter_butterfly=['1985-01-01', '2022-01-01']
	#
	date_filters_projection=[]
	date_filters_projection.append(['1986-01-01', '2016-01-01', 'black', True])
	#
	carrington_time, latitude, spot_area=read_butterflydata(filein, date_format='carrington')
	carrington_time, spot_area=select_dates(date_filter_butterfly, carrington_time, spot_area)

	# Compute the min and max date of the data set, assuming it was provided in Carrington units
	date_interval=[carrington2fracyear(carrington_time[0]), carrington2fracyear(carrington_time[-1])]
	print('Initial Carrington_time =', int(carrington_time[0]),  '    Date: ', date_interval[0])
	print('Final   Carrington_time =',int(carrington_time[-1]), '     Date: ', date_interval[1])
	if ax == None:
		fig, ax= plt.subplots(1, figsize=(12, 12))
		norm_collapsogram=do_projection(ax, date_filters_projection, carrington_time, latitude, spot_area, rotate=False, 
			latitude_range=[-60, 60], text_index='(c)', do_legend=False, ft_size_labels=18, ft_size_text=20, ft_size_text2=30, ln_width=2)
	else:
		norm_collapsogram=do_projection(ax, date_filters_projection, carrington_time, latitude, spot_area, rotate=True, 
			latitude_range=[-60, 60], text_index='(c)', do_legend=False, ft_size_labels=12, ft_size_text=6, ft_size_text2=6, ln_width=1)
	cols=['red', 'blue', 'skyblue']
	norms=[np.max(norm_collapsogram)*0.8, np.max(norm_collapsogram), np.max(norm_collapsogram)]
	lbs=[r'$\Pi(\theta_0=74,\delta=20)$',r'$\Lambda(\theta_0=74,\delta=30)$', r"$\mathcal{N}(\theta_0=16,\delta=6)$"]
	# Add a gate function
	if add_model != []:
		for m in range(len(add_model)):
			if ax == None:
				show_spot_model(ax, add_model[m], norm=norms[m], rotate=False, color=cols[m], linestyle='--', linewidth=3, label=lbs[m])
			else:
				show_spot_model(ax, add_model[m], norm=norms[m], rotate=True, color=cols[m], linestyle='--', linewidth=1.5, label=lbs[m])
	# MANUALLY SET ANOTATION AS IT DOES NOT SHOW DUE TO LACK OF FLEXIBILITY IN ANNOTATION LOCATION IN DO_PROJECTION()
	ax.annotate("{0:.0f}".format(16), xy=(0.064, 16), fontsize=8, va="bottom", ha='left')
	ax.annotate("{0:.0f}".format(16), xy=(0.064, -16), fontsize=8, va="bottom", ha='left')
	#
	ax.legend(fontsize=5.5, loc='upper right')	
	if ax == None:
		fig.tight_layout()
		plt.savefig(fileout, dpi=300)
		print('file save at: ', fileout)
	
