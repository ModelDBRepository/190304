import glob
import functions as f
import config_10 as config
import numpy as np
import matplotlib.pyplot as plt
import check_thresholds as ct
threshold = config.dend_thresh
ending = 'dendrite'
res_file = 'dendrite_results.csv'
reg_seeds = ['','_new_seed_195','_new_seed_300','_new_seed_450']
reg_sseeds = ['245','195','300','450']

add = '_runtime_900000-all_species-conc.txt_concentrations_'
basal_list =ct.basal_list
pars = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS','HFS no PKA','4xHFS-3s no PKA','4xHFS-80s no PKA','ISO+HFS no PKA','ISO+LFS no PKA','Carvedilol+HFS','Carvedilol+LFS','Propranolol+4xHFS','ICI-118551+4xHFS']
output_name ='dendrite_results.tex'
strings = '''
\\begin{table}
\caption{Robustness of the dendritic signature threshold. STD is an abbrevation for standard deviation. p value is significance of one-sided ttest comparing time signature is above the amplitude threshold to the 10s duration threshold.  Degrees of freedom = 3 for all T-Tests.}

\label{tab:dendrite_robustness}

\\begin{tabular}{|p{3.2cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|p{1.9cm}|}
\hline
\multirow{2}{*}{stimulation paradigm}& \multicolumn{3}{|c|}{above the upper threshold}&\multicolumn{3}{|c|}{above the lower threshold}\\\\
\hhline{~------}
&stim. no.&mean time $\pm$ STD&p-value& stim. no.&mean time $\pm$ STD&p-value\\\\

\hline
'''
p_value_high = {'LFS':'1','ISO':'0.0006','HFS':'1','4xHFS-3s':'0.0416','4xHFS-80s':'0.0065','ISO+HFS':'<.0001','ISO+LFS':'<.0001','HFS no PKA':'1','4xHFS-3s no PKA':'0.0003','4xHFS-80s no PKA':'0.4065','ISO+HFS no PKA':'0.0119','ISO+LFS no PKA':'1','Carvedilol+HFS':'0.7122','Carvedilol+LFS':'1','Propranolol+4xHFS':'0.0134','ICI-118551+4xHFS':'0.1505'}
p_value_low = {'LFS':'1','ISO':'0.0006','HFS':'1','4xHFS-3s':'0.0488','4xHFS-80s':'0.0117','ISO+HFS':'<.0001','ISO+LFS':'<.0001','HFS no PKA':'1','4xHFS-3s no PKA':'<.0001','4xHFS-80s no PKA':'0.8982','ISO+HFS no PKA':'0.0072','ISO+LFS no PKA':'1','Carvedilol+HFS':'1.0','Carvedilol+LFS':'1','Propranolol+4xHFS':'0.1300','ICI-118551+4xHFS':'0.5153'}

def vari(lista):
    mean = 1.*sum(lista)/len(lista)
    return sum([(x-mean)**2 for x in lista] )/(len(lista)-1)

if __name__ == '__main__':
    f_2 = open(res_file,'w')
    f_2.write('Paradigm, seed, time above lower, time above upper\n')

   
    st = f.make_st_dendrite(config.steady_state+ending)
    
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
            
            time_st,camkii,pkac,epac,gibg = f.extract_data(fname,1)
            dt = time_st[1]-time_st[0]
            len_ = len(camkii)
            #print len_
            data = []
            data.extend([camkii,pkac,epac,gibg])
            new_data = []
            for k,d in enumerate(data):

                if k<2:
                    new_data.append( d/st[k][:len_]/config.max_val[1][config.keys[k]])
                else:
                    new_data.append( d/st[k]/config.max_val[1][config.keys[k]])
                    
            out = f.calculate_signature_dendrite(new_data)
            
            low = sum((np.sign(out-threshold[0])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[0])+1)*dt*0.5)/1000
            high = sum((np.sign(out-threshold[1])+1)*dt)*0.5/1000#sum((np.sign(out-spine_threshold[1])+1)*dt*0.5)/1000
            
            f_2.write(str(low)+', '+str(high)+'\n')
            outs_low.append(low)
            outs_high.append(high)                
            if low> 10.0:
                l+=1
                if high > 10.0:
                    h+=1
            
            print fname, low, high
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

   
