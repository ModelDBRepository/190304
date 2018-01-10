import numpy as np

seeds = ['','_new_seed_195','_new_seed_300','_new_seed_450']
fname_list = [
    'Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_6_and_7_uniform_dendrite',
    'Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_3_and_7_uniform_dendrite'
]
middle = '_runtime_900000-'
species = ['CaMKII','PKAc','AC_head','Glur']
species_dend = ['CKpCaMCa4_only','CKp_only','Epac1cAMP_only','Gibg_only','ppppRGibg_only','ppppLRGibg_only','Ip35_only','Ip35PP1_only','pComplex_only','pPDE4cAMP_only','pPDE4_only']
endings = ['-conc.txt']
es = '-conc.txt_concentrations_PSD_head_neck_'
for i in range(8):
    endings.append(es+str(i))

def average(fname_base,endings,species,seed):
    for ending in endings:
        for specie in species:
            d = []
            for s in seeds:
                fname = fname_base+s+middle+specie+ending
                try:
                    f = open(fname)
                    header = f.readline()
                    data = np.loadtxt(f)
                    d.append(data)
                except IOError:
                    print 'Could not find '+fname
            if d!=[]:
                data = d[0]
                for dat in d[1:]:
                    data += dat
                data = data/len(d)
                new_fname = fname_base+'_ave'+middle+specie+ending
                print new_fname
                np.savetxt(new_fname,data,header=header,comments='')
                
      
if __name__ == '__main__':
    print endings
    for fname_base in fname_list:
        average(fname_base,endings[:1],species_dend,seeds)
        #average(fname_base,endings[1:],species,seeds)

        
        
