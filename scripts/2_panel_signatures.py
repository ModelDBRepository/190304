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
out_name = ['Signatures_trains','Signatures_everything']
paradigms = [config.comp_trains,config.everything]
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
    
    mini = 20000000
    maxi = 0
    for i,par in enumerate(paradigms):
        
      
        fig = plt.figure(figsize=(5.4,2.6))
        plt.rc('legend',**{'fontsize':6})
        ax = []
        ax.append(fig.add_subplot(1,2,1))
        ax.append(fig.add_subplot(1,2,2))
       

        for j,key in enumerate(par):
            for l,ending in enumerate(config.ending):
                fname = config.sp[key][0]+ending

                time_st,camkii,pkac,epac,gibg = f.extract_data(fname,l)
                data = []
                data.extend([camkii,pkac,epac,gibg])
                new_data = []
                for k,d in enumerate(data):
                    new_data.append( d/st[l][k]/config.max_val[l][config.keys[k]])
                if l:
                    out = f.calculate_signature_dendrite(new_data)
                else:
                   out = f.calculate_signature_spine(new_data)
     
                if out.max() > maxi:
                    maxi = out.max()
                if out.min()<mini:
                    mini = out.min()
                ax[l].hold(True)
                    
                ax[l].plot(time_st[:-90]/1000,out[:-90],config.sp[key][2],label=config.sp[key][1],lw=1)
                ff.simpleaxis_many_panels(ax[l])
                ax[l].set_title(endi[l],fontsize=10)

                
            ax[0].legend()#bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        fig_labels = ['A','B']
        ax[0].plot(time_st/1000,config.spine_thresh[0]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
        ax[0].plot(time_st/1000,config.spine_thresh[1]*np.ones(time_st.shape),':',color=config.thresh,lw=1)
        ax[1].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[0],':',color=config.thresh,lw=1)
        ax[1].plot(time_st/1000,np.ones(time_st.shape)*config.dend_thresh[1],':',color=config.thresh,lw=1) 
        for m,x in enumerate(ax):
            [c.set_linewidth(1) for c in x.spines.itervalues()]
            
            for item in (x.get_xticklabels() + x.get_yticklabels()):
                item.set_fontsize(8)
            
            start, end = x.get_xlim()
            x.xaxis.set_ticks([0,300,600,900])#(np.arange(start, end,math.ceil((end-start)/4.))) 
            ylim = [0.,3.2]
            x.set_ylim(ylim)
            x.set_xlabel('time [s]',fontsize=10)
            x.text(-40,ylim[-1]+2*ylim[-1]/50,fig_labels[m])
            
        ax[0].text(610,0.22,'4xHFS-80s',color='k',fontsize=8)
        ax[0].annotate('', xy=(300, 0.45),  xycoords='data', xytext=(300, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )       
        ax[0].annotate('', xy=(380, 0.45),  xycoords='data', xytext=(380, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )
        ax[0].annotate('', xy=(460, 0.45),  xycoords='data', xytext=(460, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )
        ax[0].annotate('', xy=(540, 0.45),  xycoords='data', xytext=(540, 0.22), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),fontsize=8,color='r' )
        ax[0].text(610,0.04,'4xHFS-3s',color='m',fontsize=8)
        ax[0].annotate('', xy=(300, 0.25),  xycoords='data', xytext=(300, 0.02), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3",edgecolor='m',facecolor='r'),fontsize=8,color='r' )       
        ax[0].annotate('', xy=(303, 0.25),  xycoords='data', xytext=(303, 0.02), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3",edgecolor='m',facecolor='r'),fontsize=8,color='r' )
        ax[0].annotate('', xy=(306, 0.25),  xycoords='data', xytext=(306, 0.02), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3",edgecolor='m',facecolor='r'),fontsize=8,color='r' )
        ax[0].annotate('', xy=(309, 0.25),  xycoords='data', xytext=(309, 0.02), textcoords='data',  arrowprops=dict(arrowstyle="->", connectionstyle="arc3",edgecolor='m',facecolor='r'),fontsize=8,color='r' )
        imlist = ['spine.png','dendrite_horizontal.png']
        loc_list = [[0.25,.97,0.1,0.1],[0.53,.97,0.4,0.1]]
        new_ax = []

        ax[0].set_ylabel('Signature (a.u.)',fontsize=10)


        for m, fn in enumerate(imlist):
            new_ax.append(ff.add_image(fig,fn,loc_list[m]))
        fig.savefig(out_name[i]+'.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1,dpi=300)
        fig.savefig(out_name[i]+'.png',format='png', bbox_inches='tight',pad_inches=0.1,dpi=300)
  
        fig.savefig(out_name[i]+'.svg',format='svg', bbox_inches='tight',pad_inches=0.1,dpi=300)
        fig.savefig(out_name[i]+'.eps',format='eps', bbox_inches='tight',pad_inches=0.1,dpi=300)
  
   # plt.show()
