import collections

steady_state = 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ave__runtime_900000-all_species-conc.txt_concentrations_'
# 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ave_runtime_600000-all_species-conc.txt_concentrations_'
sp = collections.OrderedDict([
    ('LFS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_3_min_5_Hz_lower_Ca_ave__runtime_900000-all_species-conc.txt_concentrations_','LFS','c']),
    ('ISO',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ISO_bath_1000_nM_ave__runtime_900000-all_species-conc.txt_concentrations_','ISO','y']),
    ('HFS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1_train_100_Hz_ave__runtime_900000-all_species-conc.txt_concentrations_','HFS','#FF0000']),
    ('ISO+HFS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ISO_bath_1_train_100_Hz_1000_nM_NE_release_ave__runtime_900000-all_species-conc.txt_concentrations_','ISO+HFS','#B40404']),
    ('massed',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_massed_ave__runtime_900000-all_species-conc.txt_concentrations_','4xHFS-3s','m']),
    ('TBS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_theta_ave__runtime_900000-all_species-conc.txt_concentrations_','TBS','#F7819F']),
    ('spaced',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_ave__runtime_900000-all_species-conc.txt_concentrations_','4xHFS-80s', 'k']),
   ('ISO+LFS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ISO_bath_3_min_5_Hz_higher_Ca_1000_nM_ave__runtime_900000-all_species-conc.txt_concentrations_',  'ISO+LFS','b' ]),
 ('ISO+HFS bP',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_no_PKAc_ISO_1_train_ave__runtime_900000-all_species-conc.txt_concentrations_','ISO+HFS','#B40404']),
    ('massed bP',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_no_PKAc_4_trains_massed_ave__runtime_900000-all_species-conc.txt_concentrations_','4xHFS-3s','m']),
    ('TBS bP',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_no_PKAc_theta_ave__runtime_900000-all_species-conc.txt_concentrations_','TBS','#F7819F']),
    ('spaced bP',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_no_PKAc_4_trains_spaced_ave__runtime_900000-all_species-conc.txt_concentrations_','4xHFS-80s', 'k']),
    ('ISO+LFS bP',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_no_PKAc_ISO_3_min_5_Hz_ave__runtime_900000-all_species-conc.txt_concentrations_',  'ISO+LFS','b' ]),
    ('HFS bP',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_no_PKAc_1_train_ave__runtime_900000-all_species-conc.txt_concentrations_','HFS','#FF0000']),
    ('ICI+4xHFS(80s)',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_ICI_asias_ave__runtime_900000-all_species-conc.txt_concentrations_','ICI-118,551+4xHFS', 'k']),
    ('Propranolol+4xHFS(80s)',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_proprnolol_asias_ave__runtime_900000-all_species-conc.txt_concentrations_','Propranolol+4xHFS', 'gray']),
    ('ICI+TBS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_theta_ICI_ave__runtime_900000-all_species-conc.txt_concentrations_','ICI+TBS','#F7819F']),
    ('Carvedilol+HFS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_carvedilol_bath_1_train_100_Hz_asias_ave__runtime_900000-all_species-conc.txt_concentrations_','Carvedilol+HFS','#FF0000']),
    ('Carvedilol+LFS',['Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_carvedilol_bath_3_min_5_Hz_asias_ave__runtime_900000-all_species-conc.txt_concentrations_','Carvedilol+LFS','c'])
    ])
E_LTP = ['HFS','ISO+HFS','massed','spaced','ISO+HFS bP','massed bP','spaced bP','HFS bP']
LTP = ['HFS','ISO+HFS','massed','spaced','ISO+LFS']
L_LTP = ['ISO+HFS','massed','spaced','ISO+LFS']
comp_ISO = ['ISO','ISO+LFS','ISO+HFS']
comp_lfs_hfs_iso = ['LFS','HFS']
carvedilol = ['Carvedilol+LFS','Carvedilol+HFS']
ici = ['ICI+4xHFS(80s)','Propranolol+4xHFS(80s)']
ending = ['PSD.sa1[0]_head.sa1[0]_neck.sa1[0]','dendrite']#,'total']
everything = ['LFS','ISO','HFS','ISO+HFS','massed','spaced','ISO+LFS']
comp_trains = ['spaced','massed']
trains_4 = ['spaced']
iso_el = ['LFS','HFS']
avramas = ['LFS','HFS','ISO','ISO+HFS','ISO+LFS']
predictions = ['ICI+4xHFS(80s)','Propranolol+4xHFS(80s)','Carvedilol+LFS','Carvedilol+HFS']
predictions_comp = ['spaced','ISO+HFS','ISO+LFS']
blocked_PKA = ['ISO+HFS bP','massed bP','spaced bP','ISO+LFS bP']
thresh = 'g' 
dend_max_p = {'CaMKII':3.44,
            'PKAc':2.8,
            'Epac':27.59,
            'Gibg':792.41,
            'Phos':1.3
}
spine_max_p = {'CaMKII':4.21,
            'PKAc':3.46,
            'Epac':31.18,
            'Gibg':3.,
            'Phos':1.3}
dend_max_a = {'CaMKII':3.41,
            'PKAc':3.08,
            'Epac':23.29,
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
spine_thresh = [1.31,1.37]

dend_thresh = [1.71,1.755]
spine_thresh_a = [1.91,1.96]
keys = ['CaMKII','PKAc','Epac','Gibg']
