from show_bestfit import main

def Sun19992002_main():
    process_info={'dir_mcmc':'../..//Data/MCMC_Spectrum_data/outputs/', 
                  'process_name': '19992002_incfix_fast_Priorevalrange',
                  'file_data':'../../Data/MCMC_Spectrum_data/inputs/19992002_incfix_fast_Priorevalrange.data',
                  'phase': 'A',
                  'chain': 0,
                  'model_name': 'model_MS_Global_aj_HarveyLike',
                  'data_i_x': 0,
                  'data_i_y': 1}
    rendering_info={'main':{
                        'xmin': 2880,
                        'xmax': 2975,
                        'scoef':0.05
                        },
                    'inset':{
                        'do_inset': True,
                        'location':[0.30, 0.5, 0.55, 0.45],
                        'xmin':2500,
                        'xmax':3680,
                        'scoef':0.05
                    }
    }
    outfile='../../Data/Figures_publish/version_2/Best_Fit/Fig20_Sun19992002.jpg'
    filter_params=[]
    main(process_info, rendering_info, outfile, filter_params)

def Sun20062009_main():
    process_info={'dir_mcmc':'../../Data/MCMC_Spectrum_data/outputs/',  
                  'process_name': '20062009_incfix_fast',
                  'file_data':'../..//Data/MCMC_Spectrum_data/inputs/20062009_incfix_fast.data',
                  'phase': 'A',
                  'chain': 0,
                  'model_name': 'model_MS_Global_aj_HarveyLike',
                  'data_i_x': 0,
                  'data_i_y': 1}
    rendering_info={'main':{
                        'xmin': 2880,
                        'xmax': 2975,
                        'scoef':0.05
                        },
                    'inset':{
                        'do_inset': True,
                        'location':[0.30, 0.5, 0.55, 0.45],
                        'xmin':2500,
                        'xmax':3680,
                        'scoef':0.05
                    }
    }
    outfile='../../Data/Figures_publish/version_2/Best_Fit/Fig20_Sun20062009.jpg'
    filter_params=[]
    main(process_info, rendering_info, outfile, filter_params)

def Sun20062011_main():
    process_info={'dir_mcmc':'../../Data/MCMC_Spectrum_data/outputs/', 
                  'process_name': '20062011_incfix_fast',
                  'file_data':'../../Data/MCMC_Spectrum_data/inputs/20062011_incfix_fast.data',
                  'phase': 'A',
                  'chain': 0,
                  'model_name': 'model_MS_Global_aj_HarveyLike',
                  'data_i_x': 0,
                  'data_i_y': 1}
    rendering_info={'main':{
                        'xmin': 2880,
                        'xmax': 2975,
                        'scoef':0.05
                        },
                    'inset':{
                        'do_inset': True,
                        'location':[0.30, 0.5, 0.55, 0.45],
                        'xmin':2500,
                        'xmax':3680,
                        'scoef':0.05
                    }
    }
    outfile='../../Data/Figures_publish/version_2/Best_Fit/Fig20_Sun20062011.jpg'
    filter_params=[]
    main(process_info, rendering_info, outfile, filter_params)

def CygA_main():
    process_info={'dir_mcmc':'../../Data/MCMC_Spectrum_data/outputs/', 
                  'process_name': 'kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3',
                  'file_data':'../../Data/MCMC_Spectrum_data/inputs/kplr012069424_kasoc-wpsd_slc_v1_a2a3a4_nol3.data',
                  'phase': 'A',
                  'chain': 0,
                  'model_name': 'model_MS_Global_aj_HarveyLike',
                  'data_i_x': 0,
                  'data_i_y': 1}
    rendering_info={'main':{
                        'xmin': 2100,
                        'xmax': 2165,
                        'scoef':0.05
                        },
                    'inset':{
                        'do_inset': True,
                        'location':[0.30, 0.5, 0.55, 0.45],
                        'xmin':1500,
                        'xmax':2800,
                        'scoef':0.05
                    }
    }
    outfile='../../Data/Figures_publish/version_2/Best_Fit/Fig20_16CygA.jpg'
    filter_params=[]
    main(process_info, rendering_info, outfile, filter_params)

def CygB_main():
    process_info={'dir_mcmc':'../..//Data/MCMC_Spectrum_data/outputs/', 
                  'process_name': 'kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3',
                  'file_data':'../..//Data/MCMC_Spectrum_data/inputs/kplr012069449_kasoc-wpsd_slc_v1_a2a3a4_nol3.data',
                  'phase': 'A2',
                  'chain': 0,
                  'model_name': 'model_MS_Global_aj_HarveyLike',
                  'data_i_x': 0,
                  'data_i_y': 1}
    rendering_info={'main':{
                        'xmin': 2265,
                        'xmax': 2335,
                        'scoef':0.05
                        },
                    'inset':{
                        'do_inset': True,
                        'location':[0.30, 0.5, 0.55, 0.45],
                        'xmin':1800,
                        'xmax':3000,
                        'scoef':0.05
                    }
    }
    outfile='../../Data/Figures_publish/version_2/Best_Fit/Fig20_16CygB_Lowsol.jpg'
    filter_params=[[72, -1, -0.021]] # Lower a4 solution
    main(process_info, rendering_info, outfile, filter_params)
    #
    outfile='../../Data/Figures_publish/version_2/Best_Fit/Fig20_16CygB_Upsol.jpg'
    filter_params=[[72,-0.021, 1]] # Higher a4 solution
    main(process_info, rendering_info, outfile, filter_params)

Sun19992002_main()
Sun20062009_main()
Sun20062011_main()
CygA_main()
CygB_main()
print(' All plot done ')
#exit()