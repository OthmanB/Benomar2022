'''
	The functions here have for goal to separate the contribution
	on a2 of the centrifugal force from the activity
    This is useful in order to properly propagate uncertainties of a1 and Dnu into the a2(AR) term
    And therefore, activity inference just need rely on a2(AR), 
    effectively using a2(AR)=a2 - a2(CF) as observable instead of a2
'''
import numpy as np
from aj_model_analysis import get_aj_inc_star
from fit_a2sig import a2_CF
#from aj_model_analysis import read_rot_aj
#from aj_model_analysis import readsav
#from aj_model_analysis import read_parameters_length


a2_CF(nu_nl, Dnu, a1, l)