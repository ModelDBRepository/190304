import glob
import functions as f
import config_10 as config
import numpy as np

threshold = config.spine_thresh
import matplotlib.pyplot as plt

ending = 'PSD.sa1[0]_head.sa1[0]_neck.sa1[0]'
add = '_runtime_900000-all_species-conc.txt_concentrations_'
res_file = 'spine_results.csv'
reg_seeds = ['','_new_seed_195','_new_seed_300','_new_seed_450']
reg_sseeds = ['245','195','300','450']

basal_list = [
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_3_min_5_Hz_lower_Ca',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ISO_bath_1000_nM',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1_train_100_Hz',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_massed',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ISO_bath_1_train_100_Hz_1000_nM',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_ISO_bath_3_min_5_Hz_higher_Ca_1000_nM',
                
 
                  
]
#{'LFS':0,'ISO':0,'4x-HFS-3s':0,'4xHFS-80s':0,'ISO+HFS':0,'ISO+LFS':0,'HFSnoPKA':0,'4xHFS-3snoPKA':0,'4xHFS-80snoPKA':0,'ISO+HFSnoPKA':0,'ISO+LFSnoPKA':0,'Carvedilol+HFS':0,'Carvedilol+LFS':,'propranolol+4xHFS':0,'ICI-118551+4xHFS':0}
pars = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','4xHFS-3s no PKA','4xHFS-80s no PKA','ISO+HFS no PKA','ISO+LFS no PKA','Carvedilol+HFS','Carvedilol+LFS','Propranolol+4xHFS','ICI-118551+4xHFS']
p_value_low ={'LFS':'1','ISO':'0.9998','HFS':'0.0043','4xHFS-3s':'0.01','4xHFS-80s':'0.0007','ISO+HFS':'0.0028','ISO+LFS':'0.0146','HFS no PKA':'0.9018','4xHFS-3s no PKA':'0.0013','4xHFS-80s no PKA':'0.0007','ISO+HFS no PKA':'0.0051','ISO+LFS no PKA':'1','Carvedilol+HFS':'0.0704','Carvedilol+LFS':'1','Propranolol+4xHFS':'0.0110','ICI-118551+4xHFS':'0.0027'}
p_value_high = {'LFS':'1','ISO':'1.0000','HFS':'0.0114','4xHFS-3s':'0.01','4xHFS-80s':'0.0010','ISO+HFS':'0.0032','ISO+LFS':'0.0501','HFS no PKA':'0.9556','4xHFS-3s no PKA':'0.0036','4xHFS-80s no PKA':'0.0010','ISO+HFS no PKA':'0.0119','ISO+LFS no PKA':'1','Carvedilol+HFS':'0.1451','Carvedilol+LFS':'1','Propranolol+4xHFS':'0.0129','ICI-118551+4xHFS':'0.0073'}
output_name ='spine_results.tex'
strings = '''
\\begin{table}
\caption{Robustness of the spine signature threshold. STD is an abbrevation for standard deviation. p value is significance of one-sided ttest comparing time signature is above the amplitude threshold to the 10s duration threshold.  Degrees of freedom = 3 for all T-Tests.}
\label{tab:spine_robustness}
\\begin{tabular}{|p{3.2cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|}
\hline
\multirow{2}{*}{stimulation paradigm}& \multicolumn{3}{|c|}{above the upper threshold}&\multicolumn{3}{|c|}{above the lower threshold}\\\\
\hhline{~------}
&stim. no.&mean time $\pm$ STD&p-value& stim. no.&mean time $\pm$ STD&p-value\\\\

\hline
'''
def vari(lista):
    mean = 1.*sum(lista)/len(lista)
    return sum([(x-mean)**2 for x in lista] )/(len(lista)-1)
if __name__ == '__main__':

    f_2 = open(res_file,'w')
    f_2.write('Paradigm, seed, time above lower, time above upper\n')
    st = f.make_st_spine(config.steady_state+config.ending[0])
    for j, fbasal in enumerate(basal_list):
        flist = []

        seeds = reg_seeds
        sseeds = reg_sseeds
        for seed in seeds:
            flist.append(fbasal+seed+add+ending)
        outs_low = []
        outs_high = []
        l = 0
        h = 0
        
        for i,fname in enumerate(flist):
            f_2.write(pars[j]+', '+sseeds[i]+', ')
            time_st,camkii,pkac,epac,gibg = f.extract_data(fname,0)
            dt = time_st[1]-time_st[0]
            data = []
            data.extend([camkii,pkac,epac,gibg])
            new_data = []
            for k,d in enumerate(data):
                new_data.append( d/st[k]/config.max_val[0][config.keys[k]])
                
            out = f.calculate_signature_spine(new_data)
            
            low = sum((np.sign(out-threshold[0])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[0])+1)*dt*0.5)/1000
            high = sum((np.sign(out-threshold[1])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[1])+1)*dt*0.5)/1000
            
            f_2.write(str(low)+', '+str(high)+'\n')
            outs_low.append(low)
            outs_high.append(high)                
        
            
            print low, high
            outs_low.append(low)
            outs_high.append(high)
            if low >10.0:
                l += 1
                if high> 10.0:
                    h += 1

        if len(outs_low):
            mean_low = int(sum(outs_low)/len(outs_low))
            print len(outs_low), mean_low, 
            if len(outs_low)>1:
                print int(vari(outs_low)**0.5)
        if len(outs_high):
            mean_high = int(sum(outs_high)/len(outs_high))
            print len(outs_high), mean_high, 
            if len(outs_high)> 1:
                print vari(outs_high)**0.5
        
        

        strings += pars[j]
        strings +='&'

        if len(outs_high):
            strings += str(h)+'&'+str(mean_high)
            if len(outs_high)>1:
                strings += '$\pm$'+ str(int(vari(outs_high)**0.5))
                
            strings +='&'

        strings += str(p_value_low[pars[j]])+'&'
        if len(outs_low):
            strings += str(l)+'&'+str(mean_low)
            if len(outs_low)>1:
                strings += '$\pm$'+ str(int(vari(outs_low)**0.5))
        strings += '&'+str(p_value_high[pars[j]])
        strings +='\\\\'

        strings += '\n\hline\n'


    strings += '''\end{tabular}\n\end{table}'''
    
    fout = open(output_name,'w')
    fout.write(strings)
    #plt.show()
