import numpy as np


vol = {'PSD':0.013614,'head':0.03951,'neck':0.007068, 'dendrite':4.799973}
dend_area = 16.0
vols = [0.013614,.03951,0.007068]
vols_spine = 0.013614+.03951+0.007068
if __name__ == '__main__':
    fname_list = [ 
        'Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_6_and_7_uniform_dendrite_runtime_900000-',
        'Model_long_dendrite_PKAc_times_3_switching_L_pump_neurogranin_4_trains_spaced_3_and_7_uniform_dendrite_runtime_900000-'
        ]
    types_dend = [ 'CaMKII', 'PKAc','AC_dend']
    types_spine = [
        [
            'CaMKII',
            'CaMKII',
            'CaMKII'
            ],
        [
            'PKAc', 
            'PKAc',
            'PKAc'
            ],
        [ 
            '',
            'AC_head',
            ''
            ],
        [
            'Glur',
            '',
            ''
            ]
        ]

    middle = '-conc.txt_concentrations_'
    endings_spine = ['PSD.sa1', 'head.sa1', 'neck.sa1']

    for i in range(8):
        for fname_base in fname_list:
            for types in types_spine:
                d = []
                for j,t in enumerate(types):
                    if t:
                        fname = fname_base+t+middle+endings_spine[i]+'['+str(j)+']'
                        f = open(fname)
                        header = f.readline()
                        data = np.loadtxt(f)*vols[j]
                        d.append(data)
                data = d[0]
                for j,dd in enumerate(d[1:]):
                    data += dd
                data = data/vols_spine
                new_fname = fname_base+t+middle+'PSD_head_neck_'+str(i)
                np.savetxt(new_fname,data,header=header, comment='')
 
