import collections

steady_state = 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_runtime_900000-all_species-conc.txt_concentrations_ave_'

sp = {'spine 7':'k','spine 6': 'b','spine 5':'#F7819F','spine 4':'m','spine 3':'#B40404','spine 2':'#FF0000','spine 1':'y','spine 0':'c'}
      
spine_6_7 = ['6_7_spine0','6_7_spine1','6_7_spine2','6_7_spine3','6_7_spine4','6_7_spine5','6_7_spine6','6_7_spine7']
spine_3_7 = ['3_7_spine0','3_7_spine1','3_7_spine2','3_7_spine3','3_7_spine4','3_7_spine5','3_7_spine6','3_7_spine7']
spine_no = 8
chosen_spines = [7,3,2] 
steady_state_spine = 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ave__runtime_900000-all_species-conc.txt_concentrations_PSD.sa1[0]_head.sa1[0]_neck.sa1[0]'
steady_state_dendrite = 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ave__runtime_900000-all_species-conc.txt_concentrations_dendrite'

window = 1
thresh='g'
base_6_7 = 'long_dend/Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_6_and_7_uniform_dendrite_ave_runtime_900000-'
base_3_7 = 'long_dend/Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_3_and_7_uniform_dendrite_ave_runtime_900000-'
spines_3_7 = 'long_dend/Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_3_and_7_uniform_dendrite_'
spines_6_7 = 'long_dend/Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_6_and_7_uniform_dendrite_'
runtime = 'runtime_900000-'
spine_ending = 'PSD_head_neck_'
dendrite_ending = 'dendrite'
middle = '-conc.txt_concentrations_'
files_spine = ['AC_head','PKAc','CaMKII']
files_dendrite = ['AC_dend','PKAc','CaMKII']
