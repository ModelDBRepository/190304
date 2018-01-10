import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib
import sys
import numpy as np
import collections
import functions as f
import figures_formatting as ff
import config
import math
out_name = ['Signature_components_spine_dendrite_no_PKAc','Signature_components_spine_dendrite_avramas','Signature_components_predictions']
paradigms = [config.blocked_PKA,config.avramas,config.predictions]

window = config.window
endi = ['spine','dendrite']
if __name__ == '__main__':
    
    matplotlib.rcParams['axes.linewidth'] = .5
    matplotlib.rcParams['lines.linewidth'] = .5
    matplotlib.rcParams['patch.linewidth'] = .5
    st = []
    st.append([])
    st.append([])
    st[0].extend(f.make_st_spine(config.steady_state+config.ending[0]))
    st[1].extend(f.make_st_dendrite(config.steady_state+config.ending[1]))

    
    for i,par in enumerate(paradigms):
        print out_name[i]
      
        fig = plt.figure(figsize=(5.4,8.))
        plt.rc('legend',**{'fontsize':6})
        ax = []
        ax.append(fig.add_subplot(3,2,1))
        ax.append(fig.add_subplot(3,2,2))
        ax.append(fig.add_subplot(3,2,3))
        ax.append(fig.add_subplot(3,2,4))
        ax.append(fig.add_subplot(3,2,5))
        ax.append(fig.add_subplot(3,2,6))

        if par == config.blocked_PKA:
            mini = [2000000,200000,2000000]
            maxi = [0,0,0]
        else:
            maxi = [1,1,2]
            mini = [0,0,0]
        for j,key in enumerate(par):
            for l,ending in enumerate(config.ending):
                fname = config.sp[key][0]+ending
                if 'no_PKAc' in fname:
                   ax[4].set_ylabel('Signature (a.u.)',fontsize=10)
                else:
                    ax[4].set_ylabel('Concentration (normalized)',fontsize=10)
                    
                time_st,camkii,pkac,epac,gibg = f.extract_data(fname,l)
                
                dt = time_st[1]-time_st[0]

                data = []
                data.extend([camkii,pkac,epac,gibg])
                new_data = []
                len_ = len(camkii)
                for k,d in enumerate(data):
                    if l and k<2:
                        new_data.append( d/st[l][k][:len_]/config.max_val[l][config.keys[k]])
                    else:
                        new_data.append( d/st[l][k]/config.max_val[l][config.keys[k]])
                                    
                titles = ['CaMKII','Epac','PKA targets']
                to_smoothe = []
                
              
                to_smoothe.append(new_data[0])
                to_smoothe.append(new_data[2])
                
                if 'no_PKAc' in fname:
                    if l:
                        out = f.calculate_signature_dendrite(new_data)
                    else:
                        out = f.calculate_signature_spine(new_data)
                    
                    titles = ['CaMKII','Epac','Signature']
                    
                    to_smoothe.append(out)
                else:
                    if l:
                        to_smoothe.append(new_data[1]+new_data[-1])
                    else:
                        to_smoothe.append(new_data[1])
                
                for gugu,smooth in enumerate(to_smoothe):
                    if smooth.max()>maxi[gugu]:
                        maxi[gugu] = smooth.max()
                    if smooth.min()<mini[gugu]:
                        mini[gugu] = smooth.min()

                for k, smooth in enumerate(to_smoothe):
                     
                    ax[k*2+l].hold(True)
                    #ax2.plot(time_st/1000,smooth,config.sp[key][2],label=config.sp[key][1],lw=1)
                    ax[k*2+l].plot(time_st/1000,smooth,config.sp[key][2],label=config.sp[key][1],lw=1)
                    ff.simpleaxis_many_panels(ax[k*2+l])

        if 'no_PKAc' in fname:
            ax[3].legend()
           
            ax[4].plot(time_st/1000,config.spine_thresh[0]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
            ax[4].plot(time_st/1000,config.spine_thresh[1]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
            ax[5].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[0],':',color=config.thresh,lw=1)
            ax[5].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[1],':',color=config.thresh,lw=1)
        elif 'trains' in fname:
            ax[1].legend(loc=4)
        else:
            ax[0].legend()#bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        fig_labels = ['A1','A2','B1','B2','C1','C2']
        if par == config.blocked_PKA:
            fig_labels = ['A1','A2','B1','B2','C','D']
        for m,x in enumerate(ax):
            [c.set_linewidth(1) for c in x.spines.itervalues()]
            
            for item in (x.get_xticklabels() + x.get_yticklabels()):
                item.set_fontsize(8)
            if m in [0,1,2,3]:
                x.axes.get_xaxis().set_ticklabels([])
            start, end = x.get_xlim()
            x.xaxis.set_ticks([0,300,600,900])#(np.arange(start, end,math.ceil(end-start)/4.))
            x.set_ylim([mini[m/2],maxi[m/2]])
            #if m in [3,5]:
            #    x.axes.get_yaxis().set_ticklabels([])
           # if 'no_PKAc' not in fname:
           #    if m == 1:
           #x.axes.get_yaxis().set_ticklabels([])
           #ax[4].set_ylabel('Relative activity ',fontsize=10)
        ax[4].set_xlabel('time [s]',fontsize=10)
        ax[5].set_xlabel('time [s]',fontsize=10)
        ax[0].set_ylabel('Concentration (normalized)',fontsize=10)
        ax[2].set_ylabel('Concentration (normalized)',fontsize=10)

        for nr,wh in enumerate([0,1,2,3,4,5]):
            y_lim = ax[wh].get_ylim()

            print y_lim
           
            ax[wh].text(-50,y_lim[-1]+(y_lim[-1]-y_lim[0])/20,fig_labels[nr]+' '+titles[nr/2]+' '+endi[nr%2])
            if 'no_PKA' in out_name[i]:
                x_lim = ax[wh].get_xlim()
                if nr == 2 or nr == 3:
                    ax[wh].text(x_lim[0]+(x_lim[1]-x_lim[0])/3.,y_lim[1]+(y_lim[-1]-y_lim[0])/5.,'+',fontsize=30)
                elif nr == 4 or nr == 5:
                    ax[wh].text(x_lim[0]+(x_lim[1]-x_lim[0])/3.,y_lim[1]+(y_lim[-1]-y_lim[0])/5.,'=',fontsize=30)
                
        imlist = ['spine.png','dendrite_horizontal.png']
        loc_list = [[0.25,.93,0.1,0.1],[0.53,.93,0.4,0.1]]
        new_ax = []

        for m, fn in enumerate(imlist):
            new_ax.append(ff.add_image(fig,fn,loc_list[m]))
            
       
        if 'no_PKA' in out_name[i]:
            fig.subplots_adjust(hspace=.5)
        fig.savefig(out_name[i]+'.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
        fig.savefig(out_name[i]+'.png',format='png', bbox_inches='tight',pad_inches=0.1)
        fig.savefig(out_name[i]+'.svg',format='svg', bbox_inches='tight',pad_inches=0.1)
        fig.savefig(out_name[i]+'.eps',format='eps', bbox_inches='tight',pad_inches=0.1)


