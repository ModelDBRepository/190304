import collections
import numpy as np
import matplotlib.pyplot as plt
import glob
def all_same(items):
    return all(x == items[0] for x in items)

v = [ 0.013614, 0.039531, 0.0070686]
tot = 'total'
v_tot = sum(v)

def make_file(fn):
    
    species = []

    data = []
    for i,fs in enumerate(fn):
        print fs
        
        f = open(fs)
        
        header = f.readline()
        #try:
       
        dat = np.loadtxt(f)
        data.append(dat)
        #if dat.shape[0] == 4500:
        species.append(header.split())
        #    data.append(dat)
        #    print fs
        #except:
        #    d = []
        #    for line in f:
        #        d.append([float(x) for x in line.split()])
        #    dat = np.array(d)
                               
                    

    #res = np.zeros(data[0].shape)
    shapes_x = min([dat.shape[0] for dat in data])
    shapes_y = data[0].shape[1] 

    res = np.zeros((shapes_x,shapes_y))
    for i,dat in enumerate(data):
        for j, specie in enumerate(species[0]):
            k = species[i].index(specie)
            res[:,j] += dat[:shapes_x,k]
    res = res/len(data)
    header =''
    for specie in species[0]:
        header += specie +' '
    header = header[:-1]
    return header,res

if __name__ == '__main__':
    endings = ['PSD.sa1[0]_head.sa1[0]_neck.sa1[0]','dendrite']
    #endings = ['total']
    add = '_runtime_900000-all_species-conc.txt_concentrations_'
    seeds = ['','_new_seed_195','_new_seed_300','_new_seed_450']
    basal_list = [
      
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_1_train_100_Hz',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_3_min_5_Hz_lower_Ca',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_massed',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_1000_nM',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_1_train_100_Hz_1000_nM',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_3_min_5_Hz_higher_Ca_1000_nM',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_LFS',
        #'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_HFS',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_1_train',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_4_trains_massed',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_4_trains_spaced',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_ISO_bath_1_train_100_Hz_1000_nM',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_no_PKAc_ISO_bath_LFS',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_x_AC_PDE4',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced_propranolol',
        'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced_ICI',
        #'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_2xHFS',
        #'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_carvedilol_3xHFS',
]
   
    for e in endings:
        for i,fname in enumerate(basal_list):
            lista = glob.glob(fname+'*')
            new_list = [new_name for new_name in lista if new_name.endswith(e) and 'Epac' not in new_name and 'ave' not in new_name]
            if fname == 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced':
                new_list = [new_name for new_name in new_list if 'propranolol' not in new_name and 'ICI' not in new_name]
        
            head,res = make_file(new_list)
            save_fname = fname+'_ave_'+e
            print save_fname
            np.savetxt(save_fname,res,header=head,comments='')
