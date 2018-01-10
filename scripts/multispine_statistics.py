import matplotlib
import sys
import numpy as np
import collections
import functions as f
import config_long
import config
import os.path

spine_threshold = config.spine_thresh
paradigms = [config_long.spines_6_7,config_long.spines_3_7]
seeds = ['','new_seed_300_','new_seed_450_','new_seed_195_']
fname_out = 'multispine_results.csv'


if __name__ == '__main__':
    
    ckcam_st,pka_st,epac_st = f.make_st_spine(config_long.steady_state_spine)
    fil = open(fname_out,'w')
    for j,key in enumerate(paradigms):
        fil.write(key+'\n')
        fil.write('spine no, stimulated, seed, tlowthresh,thightthresh\n')
        for seed in seeds:
            for i in range(config_long.spine_no):
                fnames_list = f.fnames_seeds(key,seed,i)
                out,time = f.calc_sig(fnames_list,[ckcam_st,pka_st,epac_st])
                dt = time[1]-time[0]
                fil.write(str(i)+',')
                if str(i) in key.split('_spaced')[-1].split('uniform_dendrite')[0]:
                    fil.write('stimulated, ')
                else:
                    fil.write('unstimulated, ')
                fil.write(f.seed_no(seed)+', ')
                low = sum((np.sign(out-spine_threshold[0])+1)*dt)*0.5/1000
                high = sum((np.sign(out-spine_threshold[1])+1)*dt)*0.5/1000
                fil.write(str(low)+', '+str(high)+'\n')
