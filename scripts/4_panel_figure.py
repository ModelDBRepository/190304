import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.image as im

import sys
import numpy as np
import collections
import functions as f
import config
import figures_formatting as ff
import math
import matplotlib.patches as patches
ending = config.ending[0]
window = 5
out_name = '4_panel_fig' 
paradigms = [config.comp_lfs_hfs_iso,config.comp_ISO]

if __name__ == '__main__':
   
    matplotlib.rcParams['axes.linewidth'] = .5
    matplotlib.rcParams['lines.linewidth'] = .5
    matplotlib.rcParams['patch.linewidth'] = .5
    st = []
    st.append([])
    st.append([])
    st[0].extend(f.make_st_spine(config.steady_state+config.ending[0]))
    st[1].extend(f.make_st_dendrite(config.steady_state+config.ending[1]))

    p = plt.figure(figsize=(5.4,5.2))
    
    plt.rc('legend',**{'fontsize':6})
        
    ax = []
    ax.append(p.add_subplot(2,2,1))
    ax.append(p.add_subplot(2,2,2))
    ax.append(p.add_subplot(2,2,3))
    ax.append(p.add_subplot(2,2,4))
    maxi = 0
    mini = 0
    for k,par in enumerate(paradigms):
        lines = []
        labels = []
       
        for key in par:
           
            for l, ending in enumerate(config.ending):
                fname = config.sp[key][0]+ending
               
                time_st,camkii,pkac,epac,gibg = f.extract_data(fname,l)
                
                dt = time_st[1]-time_st[0]
                len_ = len(camkii)
                data = []
                data.extend([camkii,pkac,epac,gibg])
                new_data = []
                for i,d in enumerate(data):
                    try:
                        new_data.append( d/st[l][i][:len_]/config.max_val[l][config.keys[i]])
                    except:
                        new_data.append( d/st[l][i]/config.max_val[l][config.keys[i]])
                if l:
                    out = f.calculate_signature_dendrite(new_data)
                else:
                   out = f.calculate_signature_spine(new_data)
     
                if out.max() > maxi:
                    maxi = out.max()
                ax[l*2+k].hold(True)
                ax[l*2+k].plot(time_st/1000,out,config.sp[key][2],label=config.sp[key][1],lw=1)
                ff.simpleaxis_many_panels(ax[l*2+k])
                print fname
              
            #ax[l*2+k].legend(loc=2)

    fig_labels = ['A','C','B','D']
    
    ax[0].plot(time_st/1000,config.spine_thresh[0]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
    ax[0].plot(time_st/1000,config.spine_thresh[1]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
    ax[2].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[0],':',color=config.thresh,lw=1)
    ax[2].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[1],':',color=config.thresh,lw=1)
    ax[1].plot(time_st/1000,config.spine_thresh[0]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
    ax[1].plot(time_st/1000,config.spine_thresh[1]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
    ax[3].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[0],':',color=config.thresh,lw=1)
    ax[3].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[1],':',color=config.thresh,lw=1)

    for m,x in enumerate(ax):
        [i.set_linewidth(1) for i in x.spines.itervalues()]
        for item in (x.get_xticklabels() + x.get_yticklabels()):
            item.set_fontsize(8)
        if m in [0,1]:
            x.axes.get_xaxis().set_ticklabels([])
        start, end = x.get_xlim()
        x.set_ylim([mini,maxi])
        x.xaxis.set_ticks([0,300,600,900])#(np.arange(start, end,math.ceil((end-start)/4.))) 
    ax[0].legend(loc=2)
    ax[1].legend(loc=2)
    
    #ax[0].set_title('Spine signature ',fontsize=10)
    #ax[1].set_title('Dendritic signature ',fontsize=10)
    ax[0].set_ylabel('Spine signature (a.u.)',fontsize=10)
    ax[2].set_ylabel('Dendritic signature (a.u.)',fontsize=10)

    ax[2].set_xlabel('time [s]',fontsize=10)
    ax[3].set_xlabel('time [s]',fontsize=10)
    for nr,wh in enumerate([0,1,2,3]):
        y_lim = ax[wh].get_ylim()
        ax[wh].text(-50,y_lim[-1]+(y_lim[-1]-y_lim[0])/20,fig_labels[nr])   
    #y_lim = ax[0].get_ylim()
    #print y_lim
    #ax[0].text(-50,0+4*y_lim[-1]/50,'B1')
    
    #ax[0].text(-50,y_lim[-1]+2*y_lim[-1]/50,'A1')
    #ax[1].text(-50,0+4*y_lim[-1]/50,'B2')
    
    #ax[1].text(-50,y_lim[-1]+2*y_lim[-1]/50,'A2')   
        
    ax[2].annotate('', xy=(251, 0.45),  xycoords='data', xytext=(250, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3",edgecolor='r',facecolor='r'),fontsize=8,color='r' )       
    # ax[2].annotate('', xy=(330, 0.45),  xycoords='data', xytext=(330, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )
    # ax[2].annotate('', xy=(410, 0.45),  xycoords='data', xytext=(410, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )
    # ax[2].annotate('', xy=(490, 0.45),  xycoords='data', xytext=(490, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )
    ax[2].add_patch(
        patches.Rectangle(
            (250, 0.02),   # (x,y)
            180,          # width
            0.18,     # height
            hatch='|||||',
            linewidth=0.,
            fill=False      
    )
)
    ax[3].add_patch(
        patches.Rectangle(
            (225, 0.5),   # (x,y)
            675,          # width
            0.18,     # height
            color='y' ,
            linewidth = 0
    )
)
    ax[3].add_patch(
        patches.Rectangle(
            (225, 0.3),   # (x,y)
            675,          # width
            0.18,     # height
            color='y',      
            linewidth = 0

    )
)
    ax[3].add_patch(
        patches.Rectangle(
            (225, 0.1),   # (x,y)
            675,          # width
            0.18,     # height
            color='y',      
            linewidth = 0

    )
)
    ax[3].annotate('', xy=(451, 0.51),  xycoords='data', xytext=(451, 0.24), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3",edgecolor='r',facecolor='r'),fontsize=8,color='r' )    
    ax[3].add_patch(
        patches.Rectangle(
            (451, 0.11),   # (x,y)
            180,          # width
            0.17,     # height
            hatch='|||||',
            linewidth=0,
            fill=False      
        )
    )
    ax[2].text(520,0.26,'HFS',color='r',fontsize=8)
    #ax[2].text(520,0.26,'4xHFS-80s',color='k',fontsize=8)
    ax[2].text(520,0.03,'LFS',color='k',fontsize=8)
    ax[3].text(670,0.51,'ISO',color='k',fontsize=8)
    ax[3].text(670,0.31,'ISO+HFS',color='k',fontsize=8)
    ax[3].text(670,0.11,'ISO+LFS',color='k',fontsize=8)
    imlist = ['arrow.png','spine.png','dendrite.png']
    loc_list = [[0.43,0.4,0.15,0.15],[-0.05,0.75,0.1,0.1],[-0.075,0.13,0.15,0.3]]
    new_ax = []

    for i, fn in enumerate(imlist):
        new_ax.append(ff.add_image(p,fn,loc_list[i]))


    p.subplots_adjust(wspace=.5)
    p.subplots_adjust(hspace=.5)
    p.savefig(out_name+'.png',format='png', bbox_inches='tight',pad_inches=0.1)
    p.savefig(out_name+'.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
    p.savefig(out_name+'.svg',format='svg', bbox_inches='tight',pad_inches=0.1)
    p.savefig(out_name+'.eps',format='eps', bbox_inches='tight',pad_inches=0.1)
    
