#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import figures_formatting as ff
import matplotlib.colors
import matplotlib

import functions as f
beta = 0.35
gamma = 0.12
delta = 0.67
colors = ['b','m','r','cyan','k']
labels = ['195','245','300','450','average']
fnames = [

    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1000_nM_8_x_Epac_new_seed_195_runtime_1200000-all_species-conc.txt_concentrations_total',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1000_nM_8_x_Epac_runtime_1200000-all_species-conc.txt_concentrations_total',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1000_nM_8_x_Epac_new_seed_300_runtime_1200000-all_species-conc.txt_concentrations_total',
    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1000_nM_8_x_Epac_new_seed_450_runtime_1200000-all_species-conc.txt_concentrations_total',

    '/home/asia/NeuroRD/new_model_half_spine_neck_four_times_longer_diff_PDE4/Model_one_short_dendrite_PKAc_times_3_switching_L_pump_neurogranin_1.5_ISO_bath_1000_nM_8_x_Epac_ave__runtime_1200000-all_species-conc.txt_concentrations_total',

    
]
raw_ratios = "/home/asia/PKA_paper/20160830_EPACsh150_100nMISO_RawRatios.csv"
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
if __name__ == '__main__':
    matplotlib.rcParams['axes.linewidth'] = .5
    matplotlib.rcParams['lines.linewidth'] = .5
    matplotlib.rcParams['patch.linewidth'] = .5
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    new_f = open(raw_ratios)
    header = new_f.readline().split(', ,')
    header[0] = header[0][1:]
    header[-1] = header[-1][:-1]
    raw_data = np.loadtxt(new_f)
    dt = raw_data[1,0]-raw_data[0,0]
    fig = plt.figure(figsize=(2.7,5.2))
    plt.rc('legend',**{'fontsize':6})
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    data = []
    j = 0
    for i in range(2,raw_data.shape[1]):
        if 'Soma' in header[i] or 'Prox' in header[i] or 'Inter' in header[i]:
            continue
        if '12' in header[i] or '13'  in header[i] or '11'  in header[i] or '9'  in header[i]:
            
       
            rd = raw_data[:,i]
            base = rd[0:600/dt].mean()
            raw = (rd-base)/base*100
            
            t0 = raw_data[0,1]
            time = raw_data[(-200-t0)/dt:(600-t0)/dt,1]
            raw = raw[(-200-t0)/dt:(600-t0)/dt]
            ax1.plot(time,raw,label=header[i],lw=1,color=colors[j])
            data.append(raw)
            j = j+1

    new_data = np.array(data).mean(axis=0)
    print time.shape, new_data.shape
    #new_data = new_data[(-200-t0)/dt:(600-t0)/dt]

    ax1.plot(time,new_data,'k',label='average',lw=2)
 
    for i,fname in enumerate(fnames):
        print fname
        data, head = f.f_open(fname)
        epac_c = head.index('Epac1cAMP')
        epaccamps = data[:,epac_c]
    
        time = data[:,0]
        dt = time[1]-time[0]
        #cs = (1-beta)*epac + epaccamps
        #ys = beta*epac+gamma*(epac+epaccamps)+cs*delta

        #r = cs/ys
        r = epaccamps
      
        n = 30
      

        r = f.average(r,n=n)
        
       
        time_ = np.linspace(time[0],time[-1],len(r))/1000.-250
        
        new_dt = time_[1] - time_[0]
        base = r[150/new_dt:250/new_dt].mean()
        print new_dt
        res = (r-base)/base*100
        if i<4:
            ax2.plot(time_,res,label=labels[i],lw=1,color=colors[i])
        else:
            ax2.plot(time_,res,label=labels[i],lw=2,color=colors[i])
         
        # else:
        #     ax2.plot(time_,res,label='simplified model',lw=1)
    ax2.set_xlabel('time (s)',fontsize=10)
    ax1.set_ylabel(u'Fluorescence ratio (%)',fontsize=10)
    ax2.set_ylabel(u'Epac (%)',fontsize=10)
    ff.simpleaxis_many_panels(ax1)
    ff.simpleaxis_many_panels(ax2)
    ax1.legend(loc=2)
    ax2.legend(loc=2)
    ax = [ax1,ax2]
    for m,x in enumerate(ax):
        [i.set_linewidth(1) for i in x.spines.itervalues()]
        for item in (x.get_xticklabels() + x.get_yticklabels()):
            item.set_fontsize(8)
        x.set_xlim([-300,600])
        x.xaxis.set_ticks([-300,0,300,600])
        if m in [0]:
            x.axes.get_xaxis().set_ticklabels([])
            start, end = x.get_xlim()
            #x.xaxis.set_ticks([-200,0,250,500])#np.arange(start, end,math.ceil(end-start)/4.))
            x.yaxis.set_ticks([0,20,40,60])
            
        else:
            #x.set_ylim([mini,maxi])
            x.yaxis.set_ticks([0,100,200])
            #x.axes.get_xaxis().set_ticklabels([-300,0,300, 600])
    fig_labels = ['A. Experimental data','B. Model results']
    for nr,wh in enumerate([0,1]):
        y_lim = ax[wh].get_ylim()
        ax[wh].text(-50-300,y_lim[-1]+(y_lim[-1]-y_lim[0])/20,fig_labels[nr])  
    
    out_name = 'cAMP_calibration'
    plt.savefig(out_name+'.png',format='png', bbox_inches='tight',pad_inches=0.1)
    plt.savefig(out_name+'.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
    plt.savefig(out_name+'.svg',format='svg', bbox_inches='tight',pad_inches=0.1)
    plt.savefig(out_name+'.eps',format='eps', bbox_inches='tight',pad_inches=0.1)
    
    plt.show()               
