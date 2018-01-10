import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib
import figures_formatting as ff
import sys
import numpy as np
import collections
import functions as f
import config
import math
ending = config.ending[0]
window = 50
out_name = ['Glur_phospho_comparison_2_panel']#,'Glur_phospho_comparison_2_panel_blocked_PKA']#,'Carvedilol_ICI_spine','Synaptic_tag_comparison_ISO','Synaptic_tag_comparison_trains','synaptic_signature_no_PKAc']
paradigms = [config.everything]#,config.blocked_PKA]#,config.predictions,config.comp_ISO,config.comp_trains, config.blocked_PKA]



def glurs(data,header):
    
    header_831 = ['GluR1_S831','GluR1_S831_PKAc','GluR1_S845_S831']#,'GluR1_S845_S831_PP2B'
    header_845 = ['GluR1_S845_S831','GluR1_S845_CKCam','GluR1_S845_CKp','GluR1_S845_CKpCam']
    header_unphos = ['GluR1','GluR1_CKp','GluR1_CKCam','GluR1_CKpCam','GluR1_S831_PP1','GluR1_PKAc','GluR1_S845_PP1','GluR1_S845_PP2B']
    
    output_831 = np.zeros(data[:,0].shape)
    output_845 = np.zeros(data[:,0].shape)
    output_unp =  np.zeros(data[:,0].shape)
    
    for i,x in enumerate(header):
        if x in header_831:
            
            output_831 += data[:,i]
        elif x in header_845:
            output_845 += data[:,i]
        elif x in header_unphos:
            output_unp += data[:,i]
        elif x == 'GluR1_S845_S831_PP1':
            output_831 += data[:,i]/2.
            output_845 += data[:,i]/2.
            
    return output_831,output_845, output_unp, data[:,0]

                   
if __name__ == '__main__':
    
    mini = 20000000
    maxi = 0
    data_st,header_st = f.f_open(config.steady_state+ending)
    st_831, st_845,st_unp,t = glurs(data_st,header_st)
    dt = (t[1]-t[0])
    st = st_831#+st_845
    for k,par in enumerate(paradigms):

        p = plt.figure(figsize=(5.4,2.6))
        plt.rc('legend',**{'fontsize':6})
        ax = []
        ax.append(p.add_subplot(1,2,1))
        ax.append(p.add_subplot(1,2,2))
        lines = []
        labels = []

        for key in par:
            fname = config.sp[key][0]+ending
            
            data,header = f.f_open(fname)
            gl_831, gl_845,gl_u,time = glurs(data,header)
            
            gl = gl_831 #+gl_845
            gl = gl[100:]/st[100:len(gl)]#.mean()
           
            gl = np.convolve(gl, np.ones(window)/window,'same')
            if gl.max() > maxi:
                maxi = gl.max()
            if gl.min()< mini:
                mini = gl.min()
            time_smoothed = np.linspace(time[0],time[-1],len(gl))
            
            if key  in config.E_LTP:
                ax[0].hold(True)
                l, = ax[0].plot(time_smoothed/1000,gl,config.sp[key][2],lw=1)
                
                lines.append(l)
                labels.append(config.sp[key][1])
                        
                            
            else:
                ax[1].hold(True)
                l, = ax[1].plot(time_smoothed/1000,gl,config.sp[key][2],lw=1)
                lines.append(l)
                labels.append(config.sp[key][1])
     
        
        ax[1].legend(lines,labels,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        amplitudes = [2.7,2.7]
        amplitudes_2 = [3.2,3.2]
        fig_labels = ['A E-LTP  paradigms','B non E-LTP  paradigms']
        for l,x in enumerate(ax):
            x.set_ylim([mini,maxi])
            x.plot(time/1000,amplitudes[l]* np.ones(time.shape),'g',lw=1)
            x.plot(time/1000,amplitudes_2[l]* np.ones(time.shape),'g',lw=1)

            x.plot(time/1000, np.ones(time.shape),'gray',lw=1)

            [i.set_linewidth(1) for i in x.spines.itervalues()]
            for item in (x.get_xticklabels() + x.get_yticklabels()):
                item.set_fontsize(8)
            # if l==0 or l==1:
            #     x.set_ylim([gl_min,gl_max])
            # else:
            #     x.set_ylim([non_p_min,non_p_max])
            ff.simpleaxis_many_panels(x)
            start, end = x.get_xlim()
            x.xaxis.set_ticks([0,300,600,900])#(np.arange(start, end,math.ceil((end-start)/4.)))
        
            x.set_xlabel('time [s]',fontsize=10)
            ylim = x.get_ylim()
            x.text(-50,ylim[-1]+(ylim[-1]-ylim[0])/20,fig_labels[l])
            

        ax[0].set_ylabel('AMPAr phosphorylation',fontsize=10)
       
        
        #ax[2].set_ylabel('pGluR ',fontsize=20)
        ax[0].set_xlabel('time [s]',fontsize=10)
        ax[1].set_xlabel('time [s]',fontsize=10)
        #ax[0].set_title('E-LTP  paradigms',fontsize=10)
        #ax[1].set_title('non E-LTP  paradigms',fontsize=10)
        print out_name[k]+'.png'
        #p.tight_layout()
        p.savefig(out_name[k]+'.png',format='png', bbox_inches='tight',pad_inches=0.1)
        p.savefig(out_name[k]+'.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
        p.savefig(out_name[k]+'.svg',format='svg', bbox_inches='tight',pad_inches=0.1)
        p.savefig(out_name[k]+'.eps',format='eps', bbox_inches='tight',pad_inches=0.1)
        plt.show()
    
    
