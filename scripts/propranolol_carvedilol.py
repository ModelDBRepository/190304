#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.colors
import sys
import numpy as np
import collections
import functions as f
import config
import figures_formatting as ff
import math
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
ending = config.ending[0]
window = 5
out_name = ['4_panel_fig_predictions_ici' ,'4_panel_fig_predictions_carv']
paradigms = [[config.trains_4,config.ici],[config.comp_lfs_hfs_iso,config.carvedilol]]
arrow = ['arrow_propr.png','arrow_carvedilol.png']
if __name__ == '__main__':
   
    matplotlib.rcParams['axes.linewidth'] = .5
    matplotlib.rcParams['lines.linewidth'] = .5
    matplotlib.rcParams['patch.linewidth'] = .5
    st = []
    st.append([])
    st.append([])
    st[0].extend(f.make_st_spine(config.steady_state+config.ending[0]))
    st[1].extend(f.make_st_dendrite(config.steady_state+config.ending[1]))
   
    for j,fig in enumerate(paradigms):
        p = plt.figure(figsize=(5.4,5.2))
        plt.rc('legend',**{'fontsize':6})
        
        ax = []
        ax.append(p.add_subplot(2,2,1))
        ax.append(p.add_subplot(2,2,2))
        ax.append(p.add_subplot(2,2,3))
        ax.append(p.add_subplot(2,2,4))
        
        
        maxi = 0
        mini = 2000000000

        for k,par in enumerate(fig):
            lines = []
            labels = []
            for key in par:
                for l, ending in enumerate(config.ending):
                    fname = config.sp[key][0]+ending
                    time_st,camkii,pkac,epac,gibg = f.extract_data(fname,l)
                    print fname
                    dt = time_st[1]-time_st[0]
                    if l:
                        len_ = len(camkii)
                    
                    
                    data = []
                    data.extend([camkii,pkac,epac,gibg])
                    new_data = []
                    for i,d in enumerate(data):
                        if l and i<2:
                            
                            new_data.append( d/st[l][i][:len_]/config.max_val[l][config.keys[i]])
                            
                            
                        else:
                            new_data.append( d/st[l][i]/config.max_val[l][config.keys[i]])
                        
                    if l:
                        out = f.calculate_signature_dendrite(new_data)
                        
                    else:
                        out = f.calculate_signature_spine(new_data)

                    if out.max() > maxi:
                        maxi = out.max()
                    if out.min() < mini:
                        mini = out.min()
                    ax[l*2+k].hold(True)
                

                    ax[l*2+k].plot(time_st/1000,out,config.sp[key][2],label=config.sp[key][1],lw=1)
                    ff.simpleaxis_many_panels(ax[l*2+k])
                    ax[3].legend(loc=4)
                    ax[2].legend(loc=4)
        

        
        for m,x in enumerate(ax):
            [i.set_linewidth(1) for i in x.spines.itervalues()]
            for item in (x.get_xticklabels() + x.get_yticklabels()):
                item.set_fontsize(8)
            if m in [0,1]:
                x.axes.get_xaxis().set_ticklabels([])
            start, end = x.get_xlim()
            x.xaxis.set_ticks([0,300,600,900])#np.arange(start, end,math.ceil(end-start)/4.)) 
            x.set_ylim([mini,maxi])
        fig_labels = ['A','C','B','D']
        for nr,wh in enumerate([0,1,2,3]):
            y_lim = ax[wh].get_ylim()
            #print y_lim
            ax[wh].text(-50,y_lim[-1]+(y_lim[-1]-y_lim[0])/20,fig_labels[nr])   
    
        ax[2].set_xlabel('time [s]',fontsize=10)
        ax[3].set_xlabel('time [s]',fontsize=10)
        ax[0].set_ylabel('Spine signature (a.u.)',fontsize=10)
        ax[2].set_ylabel('Dendritic signature (a.u.)',fontsize=10)
        imlist = [arrow[j],'spine.png','dendrite.png']
        loc_list = [[0.43,0.4,0.15,0.15],[-0.05,0.75,0.1,0.1],[-0.075,0.13,0.15,0.3]]
        new_ax = []
        ax[0].plot(time_st/1000,config.spine_thresh[0]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
        ax[0].plot(time_st/1000,config.spine_thresh[1]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
        ax[2].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[0],':',color=config.thresh,lw=1)
        ax[2].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[1],':',color=config.thresh,lw=1)
        ax[1].plot(time_st/1000,config.spine_thresh[0]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
        ax[1].plot(time_st/1000,config.spine_thresh[1]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
        ax[3].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[0],':',color=config.thresh,lw=1)
        ax[3].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[1],':',color=config.thresh,lw=1) 
        for i, fn in enumerate(imlist):
            new_ax.append(ff.add_image(p,fn,loc_list[i]))

        p.subplots_adjust(wspace=.5)
        p.subplots_adjust(hspace=.5)
        print out_name[j]+'.png'
        p.savefig(out_name[j]+'.png',format='png', bbox_inches='tight',pad_inches=0.1)
        p.savefig(out_name[j]+'.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
        p.savefig(out_name[j]+'.svg',format='svg', bbox_inches='tight',pad_inches=0.1)
        p.savefig(out_name[j]+'.eps',format='eps', bbox_inches='tight',pad_inches=0.1)
        p.savefig('reproduce'+str(j)+'.png',format='png', bbox_inches='tight',pad_inches=0.1)
