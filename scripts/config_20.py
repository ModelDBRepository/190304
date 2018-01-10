import collections

steady_state = '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_x_AC_PDE4_ave__runtime_900000-all_species-conc.txt_concentrations_'

sp = collections.OrderedDict([
    ('LFS',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_3_min_5_Hz_lower_Ca_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','LFS','c']),
    ('ISO',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_1000_nM_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','ISO','y']),
    ('HFS',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_1_train_100_Hz_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','HFS','#FF0000']),
    ('ISO+HFS',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_1_train_100_Hz_1000_nM_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','ISO+HFS','#B40404']),
    ('massed',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_massed_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','4xHFS-3s','m']),
    ('spaced',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','4xHFS-80s', 'k']),
    ('ISO+LFS',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_3_min_5_Hz_higher_Ca_1000_nM_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_',  'ISO+LFS','b' ]),
    ('ISO+HFS bP',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_ISO_bath_1_train_100_Hz_1000_nM_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','ISO+HFS','#B40404']),
    ('massed bP',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_4_trains_massed_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','4xHFS-3s','m']),
    ('spaced bP',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_4_trains_spaced_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','4xHFS-80s', 'k']),
    ('ISO+LFS bP',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_simple_2.0_no_PKAc_ISO_bath_LFS_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_',  'ISO+LFS','b' ]),
    ('HFS bP',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_simple_2.0_no_PKAc_1_train','HFS_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','#FF0000']),
    ('ICI+4xHFS(80s)',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced_ICI_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','ICI-118,551+4xHFS', 'lightgray']),
    ('Carvedilol+2xHFS(80s)',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_2xHFS_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','Carvedilol+2xHFS', 'orange']),
    ('Carvedilol+3xHFS(80s)',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_3xHFS_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','Carvedilol+3xHFS', 'gold']),
    ('Propranolol+4xHFS(80s)',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced_propranolol_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','Propranolol+4xHFS', 'gray']),
    ('Carvedilol+HFS',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_HFS_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','Carvedilol+HFS','#FF0000']),
    ('Carvedilol+LFS',['/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_LFS_new_seed_195_runtime_900000-all_species-conc.txt_concentrations_','Carvedilol+LFS','c']),
    
    ])
E_LTP = ['HFS','ISO+HFS','massed','spaced','ISO+LFS','ISO+HFS bP','massed bP','spaced bP','HFS bP']
LTP = ['HFS','ISO+HFS','massed','spaced','ISO+LFS']
L_LTP = ['ISO+HFS','massed','spaced','ISO+LFS']
comp_ISO = ['ISO','ISO+LFS','ISO+HFS']
comp_lfs_hfs_iso = ['LFS','HFS']
carvedilol = ['Carvedilol+LFS','Carvedilol+HFS','Carvedilol+2xHFS(80s)','Carvedilol+3xHFS(80s)']
ici = ['ICI+4xHFS(80s)','Propranolol+4xHFS(80s)']
ending = ['PSD.sa1[0]_head.sa1[0]_neck.sa1[0]','dendrite']#,'total']
everything = ['LFS','ISO','HFS','ISO+HFS','massed','spaced','ISO+LFS']
comp_trains = ['spaced','massed']
trains_4 = ['spaced']
iso_el = ['LFS','HFS']
avramas = ['LFS','HFS','ISO','ISO+HFS','ISO+LFS']
predictions = ['ICI+4xHFS(80s)','Propranolol+4xHFS(80s)','spaced']
predictions_comp = ['spaced','ISO+HFS','ISO+LFS']
blocked_PKA = ['ISO+HFS bP','massed bP','spaced bP','ISO+LFS bP']
thresh = 'g' 
# dend_max_p = {'CaMKII':3.25,
#             'PKAc':2.82,
#             'Epac':28.43,
#             'Gibg':812.41,
#             'Phos':1.3
# }
# dend_max_p = {'CaMKII':3.23169046522,#3.23,
#               'PKAc':2.85575048733,#2.37,
#               'Epac':42.7142857143,#28.4319356692,
#               'Gibg':812.645195565,
#             'Phos':1.3
# }
# dend_max_p = {'CaMKII':3.23169046522,#3.22382729501,#3.23,
#               'PKAc':2.85575048733,#2.82537236207,
#               'Epac':28.4319356692,
#               'Gibg':812.64,
#             'Phos':1.3
# }
dend_max_p = {'CaMKII':3.0535304020325,#3.2372,#3.22382729501,#3.23,
              'PKAc':2.1886283943025,#2.8670360505425,#2.85575048733,#2.82537236207,
              'Epac':35.36,#29.72,#28.4319356692,
              'Gibg':819.39139820675,#818.353537031,#812.64,
            'Phos':1.3
}
spine_max_p = {'CaMKII':2.918611770105,#,3.5560625992,#3.38483344567,
               'PKAc':2.84703996311,#3.1635842605800004,#3.04299921029,
               'Epac':45.4633767242,#31.2925170068,
            'Gibg':1303.,
            'Phos':1.3}
dend_max_a = {'CaMKII':3.23,
            'PKAc':2.37,
            'Epac':2.29,
            'Gibg':792.,
            'Phos':1.3
}
max_val = [spine_max_p,
           dend_max_p]
spine_max_a = {'CaMKII':11.33,
            'PKAc':21.14,
            'Epac':31.18,
            'Gibg':5.11,
               'Phos':2.30}


window = 1
spine_thresh = [1.22,1.32]#[1.1,1.15]# without duration threshold

#dend_thresh = [1.795,1.83]
dend_thresh = [1.63,1.73]

spine_thresh_a = [1.9,1.96]
keys = ['CaMKII','PKAc','Epac','Gibg']
