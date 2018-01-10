import glob
import functions as f
import config_20 as config
import numpy as np
import matplotlib.pyplot as plt
threshold = config.dend_thresh
ending = 'dendrite'
print threshold

add = '_runtime_900000-all_species-conc.txt_concentrations_'

basal_list = [
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_3_min_5_Hz_lower_Ca',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_1000_nM',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_1_train_100_Hz',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_massed',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_1_train_100_Hz_1000_nM',
    'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_ISO_bath_3_min_5_Hz_higher_Ca_1000_nM',
     

]
pars = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','4xHFS-3s no PKA','4xHFS-80s no PKA','ISO+HFS no PKA','ISO+LFS no PKA','Carvedilol+HFS','Carvedilol+LFS','Propranolol+4xHFS','Carvedilol+4xHFS','ICI-118551+4xHFS']
output_name ='dendrite_results.tex'
strings = '''
\\begin{table}
\caption{Robustness of the dendritic signature threshold. STD is an abbrevation for standard deviation. p value is significance of one-sided t-test comparing time signature is above the amplitude threshold to the 10s duration threshold.  Degrees of freedom = 3 for all t-tests.}

\label{tab:dendrite_robustness}

\\begin{tabular}{|p{3.2cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|}
\hline
\multirow{2}{*}{stimulation paradigm}& \multicolumn{3}{|c|}{above the upper threshold}&\multicolumn{3}{|c|}{above the lower threshold}\\\\
\hhline{~------}
&stim. no.&mean time $\pm$ STD&p-value& stim. no.&mean time $\pm$ STD&p-value\\\\

\hline
'''
p_value_high = {'LFS':'1','ISO':'0.0006','HFS':'1','4xHFS-3s':'0.0416','4xHFS-80s':'0.0065','ISO+HFS':'<.0001','ISO+LFS':'<.0001','HFS no PKA':'1','4xHFS-3s no PKA':'0.0003','4xHFS-80s no PKA':'0.4065','ISO+HFS no PKA':'0.0119','ISO+LFS no PKA':'1','Carvedilol+HFS':'1.5122','Carvedilol+LFS':'1','Propranolol+4xHFS':'0.0134','ICI-118551+4xHFS':'0.1669'}
p_value_low = {'LFS':'1','ISO':'0.0006','HFS':'1','4xHFS-3s':'0.0488','4xHFS-80s':'0.0117','ISO+HFS':'<.0001','ISO+LFS':'<.0001','HFS no PKA':'1','4xHFS-3s no PKA':'<.0001','4xHFS-80s no PKA':'0.8982','ISO+HFS no PKA':'0.0072','ISO+LFS no PKA':'1','Carvedilol+HFS':'1.0','Carvedilol+LFS':'1','Propranolol+4xHFS':'0.1300','ICI-118551+4xHFS':'0.2851'}

def vari(lista):
    mean = 1.*sum(lista)/len(lista)
    return (sum([(x-mean)**2 for x in lista] )/(len(lista)-1))/len(lista)

if __name__ == '__main__':
    #f_2 = open(res_file,'w')
    #f_2.write('Paradigm, seed, time above lower, time above upper\n')

   
    st = f.make_st_dendrite('Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_x_AC_PDE4_ave_'+config.ending[1],epac_mean=True) 
    # fig = plt.figure()
    # ax = []
    # titles = ['pCK','PKA','Epac']
    # for i in range(3):
    #     ax.append(fig.add_subplot(3,1,i+1))
    #     ax[i].plot(st[i])
    #     ax[i].set_title(titles[i])
    for j, fbasal in enumerate(basal_list):
        lista = glob.glob(fbasal+'*')
        new_list = [new_name for new_name in lista if new_name.endswith(config.ending[1]) and  'Epac' not in new_name and 'ave' not in new_name]
        if fbasal == 'Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_2.0_4_trains_spaced':
            new_list = [new_name for new_name in new_list if 'propranolol' not in new_name and 'ICI' not in new_name]
        
        outs_low = []
        outs_high = []
        l = 0
        h = 0
        print fbasal
        plt.figure()
        
        for i,fname in enumerate(new_list):
            
            #f_2.write(pars[j]+', '+sseeds[i]+', ')
            
            time_st,camkii,pkac,epac,gibg = f.extract_data(fname,1)
            dt = time_st[1]-time_st[0]
            
            data = []
                
            
            data.extend([(camkii/st[0][:len(camkii)]),(pkac/st[1][:len(pkac)]),(epac/st[2]),gibg])
            
            new_data = []
            for k,d in enumerate(data):
                new_data.append( d/config.max_val[1][config.keys[k]])
                #print max(d),
                
            out = f.calculate_signature_dendrite(new_data)
            
            # print sorted([l for l in f.over_the_threshold(out,threshold[0],dt/1000.) if l>10.])
            # print sorted([l for l in f.over_the_threshold(out,threshold[1],dt/1000.) if l>10.])
            # print sorted(f.over_the_threshold(out,threshold[0],dt/1000.) )
            # print sorted(f.over_the_threshold(out,threshold[1],dt/1000.) )

            low = sum((np.sign(out-threshold[0])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[0])+1)*dt*0.5)/1000
            high = sum((np.sign(out-threshold[1])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[1])+1)*dt*0.5)/1000
            print low,high
            #f_2.write(str(low)+', '+str(high)+'\n')
            outs_low.append(low)
            outs_high.append(high)                
            if low> 10.0:
                l+=1
                if high > 10.0:
                    h+=1
            
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
        
    #     strings += pars[j]
    #     strings +='&'

    #     if len(outs_high):
    #         strings += str(h)+'&'+str(mean_high)
    #         if len(outs_high)>1:
    #             strings += '$\pm$'+ str(round(vari(outs_high)**0.5))
                
    #         strings +='&'

    #     strings += str(p_value_low[pars[j]])+'&'
    #     if len(outs_low):
    #         strings += str(l)+'&'+str(mean_low)
    #         if len(outs_low)>1:
    #             strings += '$\pm$'+ str(round(vari(outs_low)**0.5))
    #     strings += '&'+str(p_value_high[pars[j]])
    #     strings +='\\\\'

    #     strings += '\n\hline\n'
    # strings += '''\end{tabular}\n\end{table}'''
    
    # fout = open(output_name,'w')
    # fout.write(strings)

   
    plt.show()
