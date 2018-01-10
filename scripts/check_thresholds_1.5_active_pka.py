import glob
import functions as f
import config_15 as config
import numpy as np

threshold = config.spine_thresh_a
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



output_name ='spine_results.tex'
strings = ''' \documentclass[10pt,letterpage]{article}
\usepackage[utf8x]{inputenc}
\usepackage[T1]{fontenc} 
\usepackage[english]{babel}
\usepackage{amsmath,amssymb}
\usepackage{fixltx2e}
\usepackage{hhline}
\usepackage{multirow}
\date{}
\usepackage[table]{xcolor}
\usepackage{nameref,hyperref}
\usepackage[strict]{changepage}
\setcounter{table}{3}
\\renewcommand{\\thetable}{S\\arabic{table}}
\\begin{document}

\\begin{table} \caption{{\\bf Robustness of the spine signature.} The
kinase-to-phosphatase balance, evaluated by molecular signatures, is
thought to control direction of synaptic plasticity. There are at
least two ways of assessing this balance: either measuring the
quantity of phosphorylated targets of kinases and phosphatases, or
assessing a ratio of kinase activity to phosphatase activity.  In this
table spine molecular signature has an alternative form and evaluates
Epac activity and the ratio of active CaMKII and active PKA to active
phosphatases (PP1 and PP2B). This form of spine signature is very
noisy, hence to induce spine specific changes, the spine signature has
to exceed its threshold for 10 sec uninterrupted.  }

\\begin{tabular}{|p{3.0cm}|p{3cm}|p{3cm}|} \hline stimulation
paradigm&  uniterrupted above the lower threshold& uniterrupted above the higher threshold\\\\ \hline '''
res_file = 'spine_res'
def vari(lista):
    mean = 1.*sum(lista)/len(lista)
    return (sum([(x-mean)**2 for x in lista] )/(len(lista)-1))/len(lista)
if __name__ == '__main__':

    f_2 = open(res_file,'w')
    f_2.write('paradigm, seed, t>l_t,t>u_t\n')
    
    st = f.make_st_spine_active('/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_x_AC_PDE4_ave__runtime_900000-all_species-conc.txt_concentrations_'+config.ending[0])
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
        plt.figure()
       
        for i,fname in enumerate(flist):
            #f_2.write(pars[j]+', '+sseeds[i]+', ')
            time_st,camkii,pkac,epac,pp1 = f.extract_data_active(fname,0)
            if not i:
                plt.plot(time_st/1000., threshold[0]*np.ones(time_st.shape))
                plt.plot(time_st/1000., threshold[1]*np.ones(time_st.shape))
                plt.title(pars[j])
            
            dt = time_st[1]-time_st[0]
            data = []
            data.extend([camkii/st[0],pkac/st[1],epac/st[2],pp1/st[3]])
            new_data = []
            for k,d in enumerate(data):
                new_data.append( d/config.spine_max_a[config.keys[k]])
                 
            if 'no_PKA' in fname:
                out = (new_data[0])/new_data[3]+new_data[2]
            else:
                out = (new_data[0]+new_data[1])/new_data[3]+new_data[2]#f.calculate_signature_spine(new_data)
            low =  sorted([x for x in f.over_the_threshold(out,threshold[0],dt/1000.) if x>10])
            high = sorted([x for x in f.over_the_threshold(out,threshold[1],dt/1000.) if x > 10])
            #low = sum((np.sign(out-threshold[0])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[0])+1)*dt*0.5)/1000
            #high = sum((np.sign(out-threshold[1])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[1])+1)*dt*0.5)/1000
            
            f_2.write(pars[j]+','+str(reg_sseeds[i])+','+str(low)+','+str(high)+'\n')
            
            plt.plot(time_st/1000.,out)
            #f_2.write(str(low)+', '+str(high)+'\n')
            outs_low.append(low)
            outs_high.append(high)                
            if low:
                l+=1
                if high:
                    h+=1
            
            print low, high
      
            
            plt.plot(time_st/1000.,out)
            
            
        # if len(outs_low):
        #     mean_low = round(sum(outs_low)/len(outs_low))
        #     print len(outs_low), mean_low, 
        #     if len(outs_low)>1:
        #         print round(vari(outs_low)**0.5)
        # if len(outs_high):
        #     mean_high = round(sum(outs_high)/len(outs_high))
        #     print len(outs_high), mean_high, 
        #     if len(outs_high)> 1:
        #         print vari(outs_high)**0.5
        print l
        

        strings += pars[j]+'&'+str(l)+'/'+str(len(flist))+'&'

        strings += str(h)+'/'+str(len(flist))+'\\\\'+'\n\hline\n'
                
    strings += '''\end{tabular}\n\end{table}\n\end{document}'''
    
    fout = open(output_name,'w')
    fout.write(strings)
    #plt.show()
