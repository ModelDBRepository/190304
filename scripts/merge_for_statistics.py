fname1 = 'spine_res'
fname2 = 'dendrite_res'
fname_out = 'results_spine_dendrite'

f1 = open(fname1)
f2 = open(fname2)
f3 = open(fname_out,'w')
f1.readline()
f2.readline()
f3.write('paradigm, seed, spine t>t_l,spine t>t_u,dendrite t>t_l,dendrite t>t_u\n')

for line1 in f1:
    w2 = f2.readline().split(',')
    w1 = line1.split(',')
    if w1[0] == w2[0] and w1[1] == w2[1]:
        f3.write(line1[:-1]+','+w2[2]+','+w2[3])
