import numpy as np
import sys

def fopen(fname):
    try:
        f = open(fname)
    except IOError:
        sys.exit('Could not open file '+fname)
    header = f.readline().split()
    try:
        data = np.loadtxt(f)
    except:
        sys.exit('Could not load data from '+fname)
    return data, header

def parse_header(header,specie):
    idx = []
    vox = ''
    for i,x in enumerate(header):
        what = x.split('Spc_')[-1]
        if what == specie:
            where = x.split('_')[2]
            if where == 'dendrite':
                idx.append(i)
                vox +=('Vox_'+x.split('_')[1]+'_'+specie+' ')
    print idx, 
    print vox
    return idx, vox
            


if __name__ == '__main__':
    specie_list = [['CKp','CKpCaMCa4','pComplex'],['pPDE4','pPDE4cAMP','Ip35','Ip35PP1','Epac1cAMP'],['Gibg','ppppLRGibg','ppppRGibg']]
    
    fname_list = ['Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_6_and_7_uniform_dendrite_',
                  'Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_3_and_7_uniform_dendrite_']

    seeds = ['','new_seed_300_','new_seed_450_','new_seed_195_',]
    middle = 'runtime_900000-'
    whats = ['CaMKII','PKAc','AC_dend']
    end = '-conc.txt'
    for fname_base in fname_list:
        for seed in seeds:
            for i,wh in enumerate(whats):
                fname = fname_base+seed+middle+wh+end
                data,header = fopen(fname)
                for sp in specie_list[i]:
                    print sp
                    new_fname =  fname_base+seed+middle+sp+'_only'+end
                    new_fname_head = fname_base+seed+middle+sp+'_only_header'
                    print new_fname
                    ind, head = parse_header(header,sp)
                    fh = open(new_fname_head,'w')
                    fh.write(head)
                    new_data = np.zeros((len(data[:,0]),len(ind)))
                    print new_data.shape, data[:,ind].shape
                    new_data = data[:,ind]
                    np.savetxt(new_fname,new_data)
    
