import numpy as np
import sys
# import config
# import config_long
v_factor = 0.12*5/2

def over_the_threshold(row,thresh,dt=1):
    res = []
    i = 0
    for a in row:
        if a >= thresh:
            i+=dt
        else:
            
            if i > 0:
                res.append(i)
            i = 0
    if i > 0:
        res.append(i)
        
    return res

def f_open(fname):
    try:
        fil = open (fname)
    except IOError:
        sys.exit('Could not open file' + fname)

    header = fil.readline().split()

    try:
        data = np.loadtxt(fname,skiprows=1)
    except:
        sys.exit('A problem with the file '+fname)
    return data, header

def find_pckcam(data,header):
    #print 'pCaMKII'
    ckcam_indexes = [ ]
    for i,x in enumerate(header):
        #if   'CKpCa' in x or 'pComplex' in x:
        #if 'CKp' in x or 'pComplex' in x:
        if 'CKp'in x  or 'pComplex' in x or '831' in x:
          
            # if 'PP' not in x:
            #     #print x
            ckcam_indexes.append(i)
     
                
                
    output = np.zeros(data[:,0].shape)
    for i in ckcam_indexes:
        output += data[:,i]
        if 'Complex' in x:
            output += data[:,i]
    
    return output, data[:,0]

def find_bound_ckcam(data,header):
    output = np.zeros(data[:,0].shape)
    for i,x in enumerate(header):
        if 'CKC'in x  or 'Complex' in x or 'CKc' in x or 'CKpCa' in x:
            if 'PP' not in x:
                output += data[:,i]
                
    return output, data[:,0]
def find_epac(data,header):
    try:
        return data[:,header.index('Epac1cAMP')], data[:,0]
    except:
        return np.zeros(data[:,0].shape), data[:,0]

def find_gibg(data,header):
    ind = []
    if 'CarvedilolR' in header:
        try:
            ind.append(header.index('CarvedilolRGi'))
        
        except:
            pass
        
        #return data[:,header.index('CarvedilolRGi')],data[:,0]
    if 'ici' in header:
        ind.append(header.index('iciRGi'))
        print 'ici'
        #return data[:,header.index('ICIRGi')],data[:,0]
    if 'Gibg' in header:
                  
        indexes = [i for i,x in enumerate(header) if 'Gibg' in x]
        ind.extend(indexes)
        output = np.zeros(data[:,0].shape)
        for i in ind:
            output  +=  data[:,i]
    else:
        
        output = data[:,0]*0

    return output, data[:,0]
def find_pkac_phospho(data,header,dend):
    
    output1 = np.zeros(data[:,0].shape)
    output2 = np.zeros(data[:,0].shape)
   
    for i,x in enumerate(header):
        if 'Ip' in x and 'PP2B' not in x:
            output1 += data[:,i]
        elif 'S845' in x and 'PP' not in x:
            output1 += data[:,i]
        elif 'pPDE' in x: 
            output1 += data[:,i]
        elif ('pL' in x or 'pR' in x) and not dend:
            output2 += data[:,i]
        # elif  ('pL' in x or 'pR' in x) and dend:
        #     output2 += data[:,i]/v_factor

    return (output1+output2), data[:,0]
def find_pkac(data,header,dend):
    ckcam_indexes = [i for i, x in enumerate(header) if 'PKAc' in x and 'AcAMP' not in x]

    
    output1 = np.zeros(data[:,0].shape)
    output2 = np.zeros(data[:,0].shape)
    for i in ckcam_indexes:
        x = header[i]
        #print x,
        if ('PKAcL' in x or 'PKAcR' in x) and not dend:
            output2 += data[:,i]
        elif  ('PKAcL' in x or 'PKAcR' in x) and dend:
            output2 += data[:,i]/v_factor
        else:
            output1 += data[:,i]
        

    return (output1+output2), data[:,0]
def find_phosphatases(data,header):
       

    ind = [i for i,x in enumerate(header) if 'PP1' in x and 'Ip' not in x]
    output = np.zeros(data[:,0].shape)
    for i in ind:
        output += data[:,i]
       
    return output, data[:,0]
def find_pp1(data,header):
    pp1 = ['CKpCaMCa4PP1','CKpPP1','GluR1_S831_PP1','GluR1_S845_PP1','GluR1_S845_S831_PP1','PP1']
    pp2b = ['Ip35PP2BCaMCa4','GluR1_S845_PP2B','GluR1_S845_S831_PP2B','PP2BCaMCa4','Ip35PP1PP2BCaMCa4',]
    ind = [i for i,x in enumerate(header) if x in pp1]
    ind2 = [i for i,x in enumerate(header) if x in pp2b]
    output = np.zeros(data[:,0].shape)
    for i in ind:
        output += data[:,i]
        #print header[i],
    for i in ind2:
        output += data[:,i]
        #print header[i],
    return output, data[:,0]

def file_list(f_base,sp_list,dire='/home/asia/NeuroRD/long_dend'):

    f_list = []
    os.path.walk(dire, lambda arg,dirname,fnames:[arg.append(os.path.join(dirname, name)) for name in fnames if name.startswith(f_base) and name[len(f_base):-4] in sp_list],f_list)
    
    return f_list

def make_st_spine(fname):
    
    data_st,header_st = f_open(fname)
    pkac_st, time_st = find_pkac_phospho(data_st,header_st,dend=False)
    epac_st, time_st = find_epac(data_st,header_st)
    ckcam_st, time_st = find_pckcam(data_st,header_st)
    pkac_st_m = pkac_st.mean()
    epac_st_m = epac_st.mean()
    ckcam_st_m = ckcam_st.mean()
    return [ckcam_st_m,pkac_st_m,epac_st_m,1]

def make_st_spine_active(fname):
    
    data_st,header_st = f_open(fname)
    pkac_st, time_st = find_pkac(data_st,header_st,dend=False)
    epac_st, time_st = find_epac(data_st,header_st)
    ckcam_st, time_st = find_bound_ckcam(data_st,header_st)
    phos_st,time_st  = find_pp1(data_st,header_st)
    pkac_st_m = pkac_st.mean()
    epac_st_m = epac_st.mean()
    ckcam_st_m = ckcam_st.mean()
    return [ckcam_st_m,pkac_st_m,epac_st_m,phos_st.mean()]

def make_st_dendrite(fname,epac_mean=False):
    
    data_st,header_st = f_open(fname)
    pkac_st, time_st = find_pkac_phospho(data_st,header_st,dend=True)
    epac_st, time_st = find_epac(data_st,header_st)
    ckcam_st, time_st = find_pckcam(data_st,header_st)
    if epac_mean:
        epac_st_m = epac_st.mean()
    else:
        epac_st_m = epac_st
    return [ckcam_st,pkac_st,epac_st_m,1]

# def fnames_seeds(key,s,i):
#     fname_camkii = key+s+config_long.runtime+'CaMKII'+config_long.middle+config_long.spine_ending+str(i)
#     fname_pkac = key+s+config_long.runtime+'PKAc'+config_long.middle+config_long.spine_ending+str(i)
#     fname_AC = key+s+config_long.runtime+'AC_head'+config_long.middle+config_long.spine_ending+str(i)
#     fname_glur = key+s+config_long.runtime+'Glur'+config_long.middle+config_long.spine_ending+str(i)
#     return fname_camkii,fname_pkac, fname_AC,fname_glur

# def fnames_ave(key,i):
    
#     fname_camkii = key+'CaMKII'+config_long.middle+config_long.spine_ending+str(i)
#     fname_pkac = key+'PKAc'+config_long.middle+config_long.spine_ending+str(i)
#     fname_AC = key+'AC_head'+config_long.middle+config_long.spine_ending+str(i)
#     fname_glur = key+'Glur'+config_long.middle+config_long.spine_ending+str(i)
#     return fname_camkii,fname_pkac, fname_AC,fname_glur

# def calc_sig(fnames_list,st_list):
#     fname_camkii, fname_pkac, fname_AC,fname_glur = fnames_list
#     ckcam_st_m,pkac_st_m,epac_st_m = st_list
#     data,header = f_open(fname_camkii)
#     dt = (data[1,0]-data[0,0])
#     ckcam_1,t = find_pckcam(data,header)
#     data,header = f_open(fname_pkac)
#     pkac_1, time = find_pkac_phospho(data,header,dend=False)
#     epac,time  = find_epac(data,header)
#     data,header = f_open(fname_AC)
#     pkac_2, time = find_pkac_phospho(data,header,dend=False)
#     data,header = f_open(fname_glur)
#     pkac_3,time = find_pkac_phospho(data,header,dend=False)
#     ckcam_2,time = find_pckcam(data,header)
#     pkac = pkac_1+pkac_2+pkac_3
#     ckcam = ckcam_2+ckcam_1
#     pkac = pkac/pkac_st_m/config.max_val[0]['PKAc']
#     ckcam = ckcam/ckcam_st_m/config.max_val[0]['CaMKII']
#     epac = epac/epac_st_m/config.max_val[0]['Epac']
#     out = pkac+ckcam+epac

#     return out,data[:,0]

def extract_data(fname,l):
    data,header = f_open(fname)
    pkac, time = find_pkac_phospho(data,header,dend=l)
    epac,time  = find_epac(data,header)
    gibg, time = find_gibg(data,header)
    ckcam,t = find_pckcam(data,header)
    if 'time' in header:
        return data[:,0],ckcam,pkac,epac,gibg
    else:
        return 1,ckcam,pkac,epac,gibg

def extract_data_active(fname,l):
    data,header = f_open(fname)
    pkac, time = find_pkac(data,header,dend=l)
    epac,time  = find_epac(data,header)
    gibg, time = find_pp1(data,header)
    ckcam,t = find_bound_ckcam(data,header)
    if 'time' in header:
        return data[:,0],ckcam,pkac,epac,gibg
    else:
        return 1,ckcam,pkac,epac,gibg
    
def calculate_signature_spine(data):
    out = data[0].copy()
    for d in data[1:-1]:
        out += d
    return out

def calculate_signature_dendrite(data):
    out = data[0].copy()
    for d in data[1:]:
        out += d
    return out

def seed_no(seed):
    if seed == '':
        return '245'
    else:
        return seed.split('_')[-2]
def moving_average(a, n=500) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def average(a,n=50):
    shape = a[::n].shape
    res = np.zeros(shape)
    for i in range(shape[0]):
        res[i] = a[i*n:(i+1)*n].mean()
    return res
    
