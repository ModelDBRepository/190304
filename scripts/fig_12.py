import matplotlib.pyplot as plt
import numpy as np
import figures_formatting as ff

import matplotlib.colors
import matplotlib
width = 3.5
paradigms = ['LFS','ISO','HFS','4xHFS-3s','4xHFS-80s','ISO+HFS','ISO+LFS']
positions ={'set1': [width*(i+1) for i in range(len(paradigms))],
            'set2':[width*(i+1)-1 for i in range(len(paradigms))],
            'set3':[width*(i+1)-2 for i in range(len(paradigms))]
            }
colors = {
    'set1':'g',
    'set2':'b',
    'set3':'m'
          }

labels =  {
    'set1':'70% of AC and PDE4',
    'set2':'ctrl',
    'set3':'130% of AC and 120% of PDE4'
          }
dendrite ={'set1':[0.0,226,0,175,200,438,386],
           'set2':[0.,0.0,0.0,167,172,386,309],
           'set3':[0.0,0.0,0.0,78,91,157,224],}

dendrite_std ={'set1':[0.0,16,0,48,55,1,9],
           'set2':[0.,0.0,0.0,51,45,4,5],
           'set3':[0.05,0.0,0.0,4,40,77,35],}


spine ={'set1':[0,0,38.,120,228,74,35],
        'set2':[0.,0.15,50,149,375,95,52],
        'set3':[0,0,40,142,296,66,93],}


spine_std ={'set1':[0,0,4,26,19,8,6],
        'set2':[0.15,0.09,4,16,20,14,14],
        'set3':[0,0,6,30,54,4,24],}

matplotlib.rcParams['axes.linewidth'] = .5
matplotlib.rcParams['lines.linewidth'] = .5
matplotlib.rcParams['patch.linewidth'] = .5


fig = plt.figure(figsize=(5.4,3.5))
plt.rc('legend',**{'fontsize':6})

ax = []
ax.append(fig.add_subplot(1,2,1))
ax.append(fig.add_subplot(1,2,2))
fig.subplots_adjust(wspace=.6)
for key in spine:
    ax[0].barh(positions[key],np.array(spine[key]), color=colors[key],label= labels[key],xerr=spine_std[key],ecolor = 'k')
    ax[1].barh(positions[key],np.array(dendrite[key]),color=colors[key],label=labels[key],xerr=dendrite_std[key],ecolor='k')

ax[0].set_ylim([width-2,width*7+1])
ax[0].set_xlim([450,0.])
ax[1].set_xlim([0,450.])
ax[0].set_xlabel('Mean duration above the upper threshold [s]',x=1)
ax[0].set_title('Spine',fontsize=12)
ax[1].set_title('Dendrite',fontsize=12)
ax[1].xaxis.set_ticks([0,150,300,450])
ax[0].xaxis.set_ticks([0,150,300,450])
ax[1].set_ylim([width-2,width*7+1])
ax[0].yaxis.set_ticks([])
ax[1].yaxis.set_ticks_position('left')
ax[1].yaxis.set_ticks(positions['set2'])

ax[1].yaxis.set_ticklabels(paradigms)
ax[1].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig.savefig('robustness.pdf',format='pdf', bbox_inches='tight',pad_inches=0.1)
fig.savefig('robustness.png',format='png', bbox_inches='tight',pad_inches=0.1)
fig.savefig('robustness.eps',format='eps', bbox_inches='tight',pad_inches=0.1)
fig.savefig('robustness.svg',format='svg', bbox_inches='tight',pad_inches=0.1)

plt.show()
