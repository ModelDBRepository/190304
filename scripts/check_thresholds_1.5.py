import glob
import functions as f
import config_15 as config
import numpy as np

threshold = config.spine_thresh
import matplotlib.pyplot as plt

ending = 'PSD.sa1[0]_head.sa1[0]_neck.sa1[0]'
add = '_runtime_900000-all_species-conc.txt_concentrations_'
res_file = 'spine_results.csv'
reg_seeds = ['','_new_seed_195','_new_seed_300','_new_seed_450']#,'_ave_']
additional_seeds = ['_new_seed_150','_new_seed_200','_new_seed_250','_new_seed_350']

reg_sseeds = ['245','195','300','450','150','200','250','350']
basal_list = [
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_3_min_5_Hz_lower_Ca',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1000_nM',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_1_train_100_Hz',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_massed',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1_train_100_Hz_1000_nM',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_3_min_5_Hz_higher_Ca_1000_nM',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_1_train',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_ISO_bath_1_train_100_Hz_1000_nM',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_4_trains_spaced',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_4_trains_massed',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_ISO_bath_LFS',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced_propranolol',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced_ICI',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_carvedilol_HFS',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_carvedilol_LFS',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_carvedilol_2xHFS',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_carvedilol_3xHFS',
    

]
more_seeds = [
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_ISO_bath_1_train_100_Hz_1000_nM',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_4_trains_spaced',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced_propranolol',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_massed',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced'
]


pars = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','ISO+HFS no PKA','4xHFS-80s no PKA','4xHFS-3s no PKA','ISO+LFS no PKA','Propranolol+4xHFS','ICI-118551+4xHFS','Carvedilol+HFS','Carvedilol+LFS','Carvedilol+2xHFS','Carvedilol+3xHFS']

pars_nice = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','ISO+HFS no PKA','4xHFS-80s no PKA','4xHFS-3s no PKA','ISO+LFS no PKA','Propranolol+4xHFS','ICI-118551+4xHFS','Carvedilol+HFS','Carvedilol+LFS','Carvedilol+2xHFS','Carvedilol+3xHFS']
p_value_low ={
    'LFS':'0.9849',
    'ISO':'0.9986',
    'HFS':'0.0092',
    '4xHFS-3s':'<0.0001',
    '4xHFS-80s':'<0.0001',
    'ISO+HFS':'0.0094',
    'ISO+LFS':'0.0060',
    'HFS no PKA':'0.9906',
    '4xHFS-3s no PKA':'0.0004',
    '4xHFS-80s no PKA':'0.0007',
    'ISO+HFS no PKA':'<0.0001',
    'ISO+LFS no PKA':'1',
    'Carvedilol+HFS':'0.0427',
    'Carvedilol+LFS':'1',
    'Carvedilol+2xHFS':'0.0057',
    'Carvedilol+3xHFS':'0.0007',
    'Propranolol+4xHFS':'<0.0001',
    'ICI-118551+4xHFS':'<0.0001'
}
p_value_high = {
    'LFS':'1',
    'ISO':'1',
    'HFS':'0.0012',
    '4xHFS-3s':'<0.0001',
    '4xHFS-80s':'<0.0001',
    'ISO+HFS':'0.0047',
    'ISO+LFS':'0.0260',
    'HFS no PKA':'0.9993',
    '4xHFS-3s no PKA':'0.0001',
    '4xHFS-80s no PKA':'0.0010',
    'ISO+HFS no PKA':'<0.0001',
    'ISO+LFS no PKA':'1',
    'Carvedilol+HFS':'0.9892',
    'Carvedilol+LFS':'1',
    'Carvedilol+2xHFS':'0.0082',
    'Carvedilol+3xHFS':'0.0011',
    'Propranolol+4xHFS':'<0.0001',
    'ICI-118551+4xHFS':'0.0001'
}
res_file = 'spine_res'

# \documentclass[10pt,letterpage]{article}
# \usepackage[utf8x]{inputenc}
# \usepackage[T1]{fontenc} 
# \usepackage[english]{babel}
# \usepackage{amsmath,amssymb}
# \usepackage{fixltx2e}
# \usepackage{hhline}
# \usepackage{multirow}
# \date{}
# \usepackage{longtable}
# \usepackage{nameref,hyperref}
# \usepackage[strict]{changepage}
# \\begin{document}

output_name ='spine_results.tex'
strings = '''
\\begin{table}
\caption{Robustness of the spine signature threshold. Standard error is an abbrevation for standard error of the mean. p value is significance of one-sided t-test comparing time signature is above the amplitude threshold to the 10 sec duration threshold.  Degrees of freedom = 3 for t-tests of paradigms with 4 different simulations, 7 for t-tests of paradigms with 8 different simulations. \label{tab:S1_Table}}
\label{tab:spine_robustness}
\\begin{tabular}{|p{3.1cm}|p{.9cm}|p{1.9cm}|p{1.1cm}|p{.9cm}|p{1.9cm}|p{1.1cm}|}
\hline
\multirow{2}{*}{stimulation paradigm}& \multicolumn{3}{|c|}{above the lower threshold}&\multicolumn{3}{|c|}{above the upper threshold}\\\\
\hhline{~------}
&stim. no.&mean time $\pm$ standard error&p-value& stim. no.&mean time $\pm$ standard error&p-value\\\\

\hline
'''
res_file = 'spine_res'
def vari(lista):
    mean = 1.*sum(lista)/len(lista)
    return (sum([(x-mean)**2 for x in lista] )/(len(lista)-1))/len(lista)
if __name__ == '__main__':

    f_2 = open(res_file,'w')
    f_2.write('paradigm, seed, t>l_t,t>u_t\n')
    
    st = f.make_st_spine('/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_x_AC_PDE4_ave__runtime_900000-all_species-conc.txt_concentrations_'+config.ending[0])
    for j, fbasal in enumerate(basal_list):
        flist = []

        seeds = reg_seeds
       
        for seed in seeds:
            flist.append(fbasal+seed+add+ending)
        outs_low = []
        outs_high = []
        l = 0
        h = 0
        print fbasal
        if fbasal in more_seeds:

            for seed in additional_seeds:
                flist.append(fbasal+seed+add+ending)
        # plt.figure()
        # plt.plot(time_st/1000., threshold[0]*np.ones(time_st.shape))
        # plt.plot(time_st/1000., threshold[1]*np.ones(time_st.shape))
        # plt.title(fname)
        for i,fname in enumerate(flist):
            
            #f_2.write(pars[j]+', '+sseeds[i]+', ')
            time_st,camkii,pkac,epac,gibg = f.extract_data(fname,0)
            dt = time_st[1]-time_st[0]
            data = []
            data.extend([camkii/st[0],pkac/st[1],epac/st[2],gibg])
            new_data = []
            for k,d in enumerate(data):
                new_data.append( d/config.max_val[0][config.keys[k]])
                #if 'ave' in fname:
                print max(d),
                
            out = f.calculate_signature_spine(new_data)
            
            low = sum((np.sign(out-threshold[0])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[0])+1)*dt*0.5)/1000
            high = sum((np.sign(out-threshold[1])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[1])+1)*dt*0.5)/1000
            
            f_2.write(pars[j]+','+str(reg_sseeds[i])+','+str(low)+','+str(high)+'\n')
            #print sorted([l for l in f.over_the_threshold(out,threshold[0],dt/1000.) if l>5])
            #print sorted([l for l in f.over_the_threshold(out,threshold[1],dt/1000.) if l > 10])

            #f_2.write(str(low)+', '+str(high)+'\n')
            outs_low.append(low)
            outs_high.append(high)                
            if low> 10.0:
                l+=1
                if high > 10.0:
                    h+=1
            
            print low, high
      
            
            plt.plot(time_st/1000.,out)
            
            
        if len(outs_low):
            mean_low = round(sum(outs_low)/len(outs_low))
            print len(outs_low), mean_low, 
            if len(outs_low)>1:
                print round(vari(outs_low)**0.5)
        if len(outs_high):
            mean_high = round(sum(outs_high)/len(outs_high))
            print len(outs_high), mean_high, 
            if len(outs_high)> 1:
                print vari(outs_high)**0.5
        
        

        strings += pars[j]+'&'+str(l)+'&'+str(mean_low)
        if len(outs_low)>1:
            strings += '$\pm$'+ str(round(vari(outs_low)**0.5))

        strings += '&'+(p_value_low[pars[j]])+'&'+str(h)+'&'+str(mean_high)

        if len(outs_high)>1:
                strings += '$\pm$'+ str(round(vari(outs_high)**0.5))
        strings+='&'+str(p_value_high[pars[j]])+'\\\\'+'\n\hline\n'
                
    strings += '''\end{tabular}\n\end{table}\n'''
    
    fout = open(output_name,'w')
    fout.write(strings)
    #plt.show()
