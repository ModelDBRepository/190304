import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib
import sys
import numpy as np
import collections
import functions as f
import figures_formatting as ff
import config_long
import config
import os.path
out_name = ['Signatures_spine']
paradigms = [config_long.base_6_7,config_long.base_3_7]

window = config_long.window
endi = ['Adjacent stimulation','Distant stimulation']
keys = ['PKAc','CaMKII','Epac','Gibg']
N = 10
PKAc_species = ['PKAcR','PKAcLR','PKAcpR','PKAcpLR','PKAcppR','PKAcppLR','PKAcpppLR','PKAcpppR','PKAc',"PKAcPDE4","I1PKAc",'PKAc_PDE4_cAMP']
PKAc_phos = ['Ip35PP1','Ip35','pPDE4cAMP','pPDE4']
CamKII = ['CKCaMCa4']
pCaMKII = ['CKp','CKpCaMCa4','pComplex']#, 'CKp']
PP1CaMKII = ['CKpCaMCa4PP1', 'CKpPP1']
Epac = ['Epac1cAMP']
PP2B = ['Ip35PP2BCaMCa4','Ip35PP1PP2BCaMCa4','PP1PP2BCaMCa4']
gibg = ['Gibg','ppppLRGibg','ppppRGibg']
sp_list = [PKAc_phos,pCaMKII, Epac,gibg]

if __name__ == '__main__':
    
    matplotlib.rcParams['axes.linewidth'] = .5
    matplotlib.rcParams['lines.linewidth'] = .5
    matplotlib.rcParams['patch.linewidth'] = .5

    ckcam_st,pka_st,epac_st, gist = f.make_st_spine(config_long.steady_state_spine)
    
    fig = plt.figure(figsize=(5.4,8.0))
    plt.rc('legend',**{'fontsize':6})
    ax = []
    ax.append(fig.add_subplot(3,2,1))
    ax.append(fig.add_subplot(3,2,2))
    ax.append(fig.add_subplot(3,2,3))
    ax.append(fig.add_subplot(3,2,4))
    ax.append(fig.add_subplot(3,2,5))
    ax.append(fig.add_subplot(3,2,6))
    all_traces = [[],[]]    
    times = [[],[]]
    for i in range(config_long.spine_no):
        for j,key in enumerate(paradigms):
            fnames_list = f.fnames_ave(key,i)
            out, time = f.calc_sig(fnames_list,[ckcam_st,pka_st,epac_st])
            title = ''
            times[j].append(time)
            all_traces[j].append(out)

    save_name = 'spine_spatial_comparison.png'
    
    for m,x in enumerate(ax):
        [c.set_linewidth(1) for c in x.spines.itervalues()]
            
        for item in (x.get_xticklabels() + x.get_yticklabels()):
            item.set_fontsize(8)
    l_a = min([len(d) for d in all_traces[0]])
    l_b = min([len(d) for d in all_traces[1]])
    time = [times[0][0][:l_a], times[1][0][:l_b]]

    adjacent_spines = np.zeros((8,l_a))
    distant_spines = np.zeros((8,l_b))
    for i in range(8):
        adjacent_spines[i,:] = all_traces[0][i][:l_a]
        distant_spines[i,:] = all_traces[1][i][:l_b]

    ff.make_figure3(fig,ax[0:2],adjacent_spines.transpose()[:,::-1],distant_spines.transpose()[:,::-1],save_name,'',0,times[0][0][l_a-1]/1000,times[1][0][l_b-1]/1000,.65)
    

    for i,out in enumerate([adjacent_spines,distant_spines]):
        ax[i].hold(True)
                    
        ax[2+i].plot(time[i]/1000,config.spine_thresh[0]*np.ones(time[i].shape),':',color=config_long.thresh,lw=1)
        ax[2+i].plot(time[i]/1000,config.spine_thresh[-1]*np.ones(time[i].shape),':',color=config_long.thresh,lw=1)
        for j in [7,3,2]:
            key = 'spine '+str(j)
            
            ax[2+i].plot(time[i][:-90]/1000,out[j][:-90],config_long.sp[key],label=key,lw=1)
        ff.simpleaxis_many_panels(ax[i+2])
        if i>0:
            ax[3].legend(loc=4)
        start, end = 0, 2
        ax[2+i].set_ylim([start,end])
        ax[2+i].set_xlim([0,time[i][-1]/1000])
        #


    ax[2].set_ylabel('Spine signature a.u.',fontsize=10)


    ax[1].yaxis.set_ticks([])
    ax[3].yaxis.set_ticks([])
    ax[5].yaxis.set_ticks([])
    ax[0].xaxis.set_ticks([])
    ax[1].xaxis.set_ticks([])
    ax[2].xaxis.set_ticks([])
    ax[3].xaxis.set_ticks([])


    data_st,header_st = f.f_open(config_long.steady_state_dendrite)
    
    pkac_st, time_st = f.find_pkac_phospho(data_st,header_st,dend=False)
    epac_st, time_st = f.find_epac(data_st,header_st)
    ckcam_st, time_st = f.find_pckcam(data_st,header_st)
    vol = 0.0057831
    spec_list = [['CKp','CKpCaMCa4','pComplex'],['pPDE4','pPDE4cAMP','Ip35','Ip35PP1'],['Epac1cAMP'],['Gibg','ppppLRGibg','ppppRGibg']]
    steady_state = {'CaMKII':ckcam_st,'PKAc':pkac_st,'Epac':epac_st}
    mols = ['CaMKII','PKAc','Epac','Gibg']
    
    # #Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_6_and_7_uniform_dendrite_runtime_900000-CKp_only-conc.txt
    # #fname_base+specie+'_only-conc.txt'
    all_data = []

    for i,fname_base in enumerate(paradigms):
        all_data.append([])
        for j, specie in enumerate(mols):
            fname = fname_base+spec_list[j][0]+'_only-conc.txt'
            data =  np.loadtxt(fname)
            print fname, i,j
            for sp in spec_list[j][1:]:
                fname = fname_base+sp+'_only-conc.txt'
                print fname
                h_data = np.loadtxt(fname)
                data += h_data
                if specie == 'pComplex':
                    data += h_data
               
            all_data[i].append(data[:,:830]/vol*10./6.022)
            #830 voxels
            
    l = 830
    sig_1 = np.zeros((len(all_data[0][0]),N))
    sig_2 = np.zeros((len(all_data[0][0]),N))
     
    for i, d1 in enumerate(all_data[0]):
        for j in range(sig_1.shape[1]):
          
            if mols[i] == 'Epac':
                sig_1[:,j] += d1[:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/steady_state['Epac'].mean()/config.max_val[1]['Epac']#/vol*10/6.02
                sig_2[:,j] += all_data[1][i][:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/steady_state['Epac'].mean()/config.max_val[1]['Epac']#/vol*10/6.02
            elif mols[i] == 'Gibg':
                sig_1[:,j] += d1[:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/config.max_val[1]['Gibg']#/vol*10/6.02
                sig_2[:,j] += all_data[1][i][:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/config.max_val[1]['Gibg']#/vol*10/6.02
                            
            elif mols[i] == 'PKAc':
                sig_1[:,j] += d1[:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/steady_state['PKAc']/config.max_val[1]['PKAc']#/vol*10/6.02
                sig_2[:,j] += all_data[1][i][:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/steady_state['PKAc']/config.max_val[1]['PKAc']#/vol*10/6.02
            elif mols[i] == 'CaMKII':
                sig_1[:,j] += d1[:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/steady_state['CaMKII']/config.max_val[1]['CaMKII']#/vol*10/6.02
                sig_2[:,j] += all_data[1][i][:,j*l/N:(j+1)*l/N].sum(axis=1)/(l/N)/steady_state['CaMKII']/config.max_val[1]['CaMKII']#/vol*10/6.02

    ff.make_figure3(fig,ax[4:6],sig_1[:,::-1],sig_2[:,::-1],save_name,'',2,900,900,.58)
   
    
    ax[0].set_ylabel('Spine no.',fontsize=10)

    fig_labels = ['A1','A2','B1','B2','C1','C2']
    for nr,x in enumerate(ax):
        y_lim = x.get_ylim()
        x_lim = x.get_xlim()
        if y_lim[-1] < y_lim[0]:
            
            increment = -y_lim[0]
        else:
            increment = y_lim[-1]
      
        x.text(-x_lim[1]/12.,y_lim[-1]+2*increment/50,fig_labels[nr])

    fig.savefig('spine_spatial_comparison.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
    fig.savefig('spine_spatial_comparison.png',format='png', bbox_inches='tight',pad_inches=0.1)
    
    fig.savefig('spine_spatial_comparison.svg',format='svg', bbox_inches='tight',pad_inches=0.1)

    
