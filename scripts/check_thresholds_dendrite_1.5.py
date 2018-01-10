import glob
import functions as f
import config_15 as config
import numpy as np
import matplotlib.pyplot as plt
threshold = config.dend_thresh
ending = 'dendrite'
res_file = 'dendrite_results.csv'
reg_seeds = ['','_new_seed_195','_new_seed_300','_new_seed_450']#,'_ave_']

reg_sseeds = ['245','195','300','450','150','200','250','350']
additional_seeds = ['_new_seed_150','_new_seed_200','_new_seed_250','_new_seed_350']

add = '_runtime_900000-all_species-conc.txt_concentrations_'
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
pars = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','ISO+HFS no PKA','4xHFS-80s no PKA','4xHFS-3s no PKA','ISO+LFS no PKA','Propranolol+4xHFS','ICI-118551+4xHFS','Carvedilol+HFS','Carvedilol+LFS','Carvedilol+2xHFS','Carvedilol+3xHFS']
pars_nice = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','ISO+HFS no PKA','4xHFS-80s no PKA','4xHFS-3s no PKA','ISO+LFS no PKA','Propranolol+4xHFS','ICI-118551+4xHFS','Carvedilol+HFS','Carvedilol+LFS','Carvedilol+2xHFS','Carvedilol+3xHFS']
output_name ='dendrite_results.tex'
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

strings = '''
\\begin{table}
\caption{Robustness of the dendritic signature threshold. Standard error is an abbrevation for standard error of the mean. p value is significance of one-sided t-test comparing time signature is above the amplitude threshold to the 10s duration threshold.  Degrees of freedom = 3 for  t-tests of paradigms with 4 different simulations, 7 for t-tests of paradigms with 8 different simulations. \label{tab:S2_Table}}

\label{tab:dendrite_robustness}

\\begin{tabular}{|p{3.2cm}|p{.9cm}|p{1.9cm}|p{1.1cm}|p{.9cm}|p{1.9cm}|p{1.1cm}|}
\hline
\multirow{2}{*}{stimulation paradigm}& \multicolumn{3}{|c|}{above the lower threshold}&\multicolumn{3}{|c|}{above the upper threshold}\\\\
\hhline{~------}
&stim. no.&mean time $\pm$ standard error&p-value& stim. no.&mean time $\pm$ standard error&p-value\\\\

\hline
'''
p_value_low = {
    'LFS':'1',
    'ISO':'1',
    'HFS':'1',
    '4xHFS-3s':'0.0032',
    '4xHFS-80s':'0.0002',
    'ISO+HFS':'<.0001',
    'ISO+LFS':'<.0001',
    'HFS no PKA':'1',
    '4xHFS-3s no PKA':'<0.0001',
    '4xHFS-80s no PKA':'0.9017',
    'ISO+HFS no PKA':'<0.0001',
    'ISO+LFS no PKA':'1',
    'Carvedilol+HFS':'1',
    'Carvedilol+LFS':'1',
    'Carvedilol+2xHFS':'0.0548',
    'Carvedilol+3xHFS':'0.0002',
    'Propranolol+4xHFS':'<0.0001',
    'ICI-118551+4xHFS':'0.9951'
}
p_value_high = {
    'LFS':'1',
    'ISO':'1',
    'HFS':'1',
    '4xHFS-3s':'0.0089',
    '4xHFS-80s':'0.0044',
    'ISO+HFS':'<0.0001',
    'ISO+LFS':'<0.0001',
    'HFS no PKA':'1',
    '4xHFS-3s no PKA':'<0.0001',
    '4xHFS-80s no PKA':'0.9980',
    'ISO+HFS no PKA':'0.0011',
    'ISO+LFS no PKA':'1',
    'Carvedilol+HFS':'1',
    'Carvedilol+LFS':'1',
    'Carvedilol+2xHFS':'0.2931',
    'Carvedilol+3xHFS':'0.0005',
    'Propranolol+4xHFS':'0.0103',
    'ICI-118551+4xHFS':'1'
}

res_file = 'dendrite_res'
more_seeds = [
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_ISO_bath_1_train_100_Hz_1000_nM',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_no_PKAc_4_trains_spaced',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced_propranolol',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_massed',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_4_trains_spaced'
]
def vari(lista):
    mean = 1.*sum(lista)/len(lista)
    return (sum([(x-mean)**2 for x in lista] )/(len(lista)-1))/len(lista)

if __name__ == '__main__':
    #f_2 = open(res_file,'w')
    #f_2.write('Paradigm, seed, time above lower, time above upper\n')

    f_2 = open(res_file,'w')
    f_2.write('paradigm, seed, t>l_t,t>u_t\n')
    st = f.make_st_dendrite('/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_x_AC_PDE4_ave__runtime_900000-all_species-conc.txt_concentrations_'+ending,epac_mean=True) 
    # fig = plt.figure()
    # ax = []
    # titles = ['pCK','PKA','Epac']
    # for i in range(3):
    #     ax.append(fig.add_subplot(3,1,i+1))
    #     ax[i].plot(st[i])
    #     ax[i].set_title(titles[i])
    for j, fbasal in enumerate(basal_list):
        flist = []
        
        seeds = reg_seeds

        for seed in seeds:
            flist.append(fbasal+seed+add+ending)
        if fbasal in more_seeds:
            for seed in additional_seeds:
                flist.append(fbasal+seed+add+ending)
       
        outs_low = []
        outs_high = []
        l = 0
        h = 0
        print fbasal
        plt.figure()
        for i,fname in enumerate(flist):
          
            #f_2.write(pars[j]+', '+sseeds[i]+', ')
            
            time_st,camkii,pkac,epac,gibg = f.extract_data(fname,1)
            dt = time_st[1]-time_st[0]
            
            data = []
                
            #try:         
            data.extend([(camkii/st[0][:len(camkii)]),(pkac/st[1][:len(camkii)]),(epac/st[2]),gibg])
            #except ValueError:
            #    continue
            new_data = []
            for k,d in enumerate(data):
                
                
                if k<3:
                    new_data.append( d/config.max_val[1][config.keys[k]])
                else:
                # if k<3:
                #     new_data.append( d/st[k].mean()/config.max_val[1][config.keys[k]])
                # else:
                    new_data.append( d/st[k]/config.max_val[1][config.keys[k]])
                
                print d.max(),
                
            out = f.calculate_signature_dendrite(new_data)
            
            # print sorted([l for l in f.over_the_threshold(out,threshold[0],dt/1000.) if l>10.])
            # print sorted([l for l in f.over_the_threshold(out,threshold[1],dt/1000.) if l>10.])
            # print sorted(f.over_the_threshold(out,threshold[0],dt/1000.) )
            # print sorted(f.over_the_threshold(out,threshold[1],dt/1000.) )

            low = sum((np.sign(out-threshold[0])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[0])+1)*dt*0.5)/1000
            high = sum((np.sign(out-threshold[1])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[1])+1)*dt*0.5)/1000
            f_2.write(pars[j]+','+str(reg_sseeds[i])+','+str(low)+','+str(high)+'\n')
            #f_2.write(str(low)+', '+str(high)+'\n')
            outs_low.append(low)
            outs_high.append(high)                
            if low> 10.0:
                l+=1
                if high > 10.0:
                    h+=1
            
            print  low, high
            plt.plot(time_st,out)
            plt.plot(time_st,np.ones(time_st.shape)*threshold[0],'g')
            plt.plot(time_st,np.ones(time_st.shape)*threshold[1],'g')
                        
        if len(outs_low):
            mean_low = round(sum(outs_low)/len(outs_low))
            print len(outs_low), mean_low, 
            if len(outs_low)>1:
                print int(vari(outs_low)**0.5)
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
