import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import numpy as np
matplotlib.rcParams['axes.unicode_minus'] = False
import math
from mpl_toolkits.axes_grid.inset_locator import inset_axes
#img = im.imread(imlist[i])
#ax_im = inset_axes(ax[i],width="50%",height=.5,loc=2)
import matplotlib.image as im

def no_frame(ax1):
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    ax1.set_frame_on(False)
def add_image(fig,fname,loc):
    img = im.imread(fname)
    ax1 = fig.add_axes(loc)
    img_1 = ax1.imshow(img)
    no_frame(ax1)
    return ax1
def make_figure3(f,ax,res_1,res_2,fnam,title,i,t1,t2,th):
    vmin = min(res_1.min(),res_2.min())
    vmax = max(res_1.max(),res_2.max())

    if i == 1:
       
        ax[0].set_ylabel('Spine signature a.u.')
    if i == 0:
        ax[1].set_title('Distant stimulation',fontsize=10)
        ax[0].set_title('Adjacent stimulation',fontsize=10)
        ax[0].set_ylabel('Spine no..')
        im = ax[0].imshow(res_1.transpose(),aspect='auto',extent=[0,t1,-0.5,7.5],vmin=vmin,vmax=vmax, interpolation='None',cmap='CMRmap')
    
        im2 = ax[1].imshow(res_2.transpose(),aspect='auto',extent=[0,t2,-0.5,7.5],vmin=vmin,vmax=vmax,interpolation='None',cmap='CMRmap')
        ax[0].set_ylabel('Spine no.',fontsize=10)
        ax[0].annotate('S1', xy=(0, 7.3),  xycoords='data', xytext=(-22, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[0].annotate('S2', xy=(0, 6.3),  xycoords='data', xytext=(-22, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[1].annotate('S1', xy=(0, 7.3),  xycoords='data', xytext=(-22, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[1].annotate('S2', xy=(0, 3.3),  xycoords='data', xytext=(-22, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        start,end = [7,0]
        ax[0].yaxis.set_ticks(np.arange(start, end-1,-1)) 
        ax[1].yaxis.set_ticks(np.arange(start, end-1,-1)) 
    if i == 2:
        im = ax[0].imshow(res_1.transpose(),aspect='auto',extent=[0,t1,0,20],vmin=vmin,vmax=vmax, interpolation='None',cmap='CMRmap')
    
        im2 = ax[1].imshow(res_2.transpose(),aspect='auto',extent=[0,t2,0,20],vmin=vmin,vmax=vmax,interpolation='None',cmap='CMRmap')
        ax[0].set_xlabel('time [s]',fontsize=10)
        ax[0].set_ylabel('Distance along dendrite [um]',fontsize=10)
        ax[0].annotate('S1', xy=(0, 20-1.6),  xycoords='data', xytext=(-20, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[0].annotate('S2', xy=(0, 20-2.66),  xycoords='data', xytext=(-20, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[1].annotate('S1', xy=(0, 20-1.6),  xycoords='data', xytext=(-20, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[1].annotate('S2', xy=(0, 20-11),  xycoords='data', xytext=(-20, 0), textcoords='offset points', arrowprops=dict(arrowstyle="->"),fontsize=8,color='r' )
        ax[0].yaxis.set_ticks([0,5,10,15,20])
        ax[1].yaxis.set_ticks([0,5,10,15,20])
        start, end = ax[0].get_xlim()
        ax[0].xaxis.set_ticks([0,300,600,900])
    
        start, end = ax[1].get_xlim()
        ax[1].xaxis.set_ticks([0,300,600,900])
    
    for m,x in enumerate(ax):
        [c.set_linewidth(1) for c in x.spines.itervalues()]
        
        for item in (x.get_xticklabels() + x.get_yticklabels()):
            item.set_fontsize(8)
    f.subplots_adjust(right=0.8)
    if i == 0:
        cbar_ax = f.add_axes([0.85, 0.67, 0.05, 0.2])
    if i == 1:
        cbar_ax = f.add_axes([0.85, 0.38, 0.05, 0.2])
    if i == 2:
        cbar_ax = f.add_axes([0.85, 0.1, 0.05, 0.2])
    
    h = f.colorbar(im2,cax=cbar_ax)
    [c.set_linewidth(1) for c in cbar_ax.spines.itervalues()]
    for item in (cbar_ax.get_xticklabels() + cbar_ax.get_yticklabels()):
        item.set_fontsize(8)
    if th:
        cbar_ax.annotate('Th', xy=(.2,th), xytext=(-1,th),arrowprops=dict(arrowstyle="->"),fontsize=8,color='r')
    save_name = '_spacial_comparison.png'
           
    
    h.set_label(title,fontsize=10)
    f.savefig(fnam+save_name,bbox_inches='tight')
    f.savefig(fnam+save_name[:-4]+'.pdf',bbox_inches='tight')

def simpleaxis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().set_tick_params(direction='out', right=0, pad=13, width=2, length=10)
    ax.get_yaxis().set_tick_params(direction='out', top=0, pad=13, width=2, length=10)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    #ax.minorticks_on()
    ax.tick_params('both', length=10, width=2, which='major')
    ax.tick_params('both', length=5, width=1, which='minor')
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
def simpleaxis_many_panels(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    #ax.minorticks_on()
    #ax.tick_params('both', length=10, width=2, which='major')
    #ax.tick_params('both', length=5, width=1, which='minor')
    #ax.get_xaxis().get_major_formatter().set_useOffset(False)
