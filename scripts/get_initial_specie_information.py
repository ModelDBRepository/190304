#-*- coding: utf-8 -*-
from __future__ import division
import subprocess
import collections
import sys
import random
import argparse
import re
import numpy as np
import os.path
#import lxml
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  sys.exit("Do install lxml")



default_fn = ['all_species']
#Area calculation is going to be wrong in case of vertical dendrites -- Correct!!!
def calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels):
    ''' Function calculating volume of every segment present in the mesh file and
    the information provided in the header of the results file.  
    '''
    try:
      meshfile = open(mesh_filename)
    except IOError:
      sys.exit('No such file or directory '+meshfile)
    legend = meshfile.readline().split()
    element_index = legend.index('element_index')
    volume_index = legend.index('volume')
    depth2D_index = legend.index('deltaZ')
    x0_index = legend.index('x0')
    y0_index = legend.index('y0')
    z0_index = legend.index('z0')
    x1_index = legend.index('x1')
    y1_index = legend.index('y1')
    z1_index = legend.index('z1')
    volumes_dict = {}
    areas_dict = {}
    print segment_voxels
    print 'submembrane', segment_area_voxels
    for line in meshfile:
        words = line.split()
        voxel_index = int(words[element_index])
        for key in segment_voxels:
            if voxel_index in segment_voxels[key]:
                if key in volumes_dict:
                    volumes_dict[key] = volumes_dict[key] + float(words[volume_index])
                else:
                    volumes_dict[key] = float(words[volume_index])
        for key in segment_area_voxels:
            if voxel_index in segment_area_voxels[key]:
                area = ((float(words[x0_index])-float(words[x1_index]))**2
                        +(float(words[y0_index])-float(words[y1_index]))**2
                        +(float(words[z0_index])-float(words[z1_index]))**2)**0.5*float(words[depth2D_index])
                if key in areas_dict:
                    areas_dict[key] =  areas_dict[key] + area
                else:
                    areas_dict[key] = area

    return areas_dict, volumes_dict

def read_header(headerline):
    '''
    Function parsing the header line of the results file.
    '''
    regions = set()
    segment_voxels = collections.OrderedDict() #numbers of voxels of each segment
    segment_area_voxels = collections.OrderedDict() #numbers of voxels of each segment surface
    special_points = collections.OrderedDict() #labeled voxels
    specie_type_dict = collections.OrderedDict()
    # Return a list of the words in the string, using sep as the delimiter string.

    for col,word in enumerate(headerline.split()[1:]):
        information = word.split('_')
        voxel_number = int(information[1])
        spc_index = information.index('Spc')
        specie_name = information[spc_index+1]
        for part in information[spc_index+2:]:
            specie_name = specie_name +'_' + part
        if 'cytosol' in information:
            voxel_type_index = information.index('cytosol')
        elif 'submembrane' in information:
            voxel_type_index = information.index('submembrane')
        segment_name = information[2]
        for i in range(3,voxel_type_index-1):
            segment_name = segment_name + '_' + information[i]
        if information[voxel_type_index] == 'submembrane':
            if segment_name not in segment_area_voxels:
                segment_area_voxels[segment_name] = [voxel_number]
            elif voxel_number not in segment_area_voxels[segment_name]:
                segment_area_voxels[segment_name].append(voxel_number)

        if voxel_type_index + 1 != spc_index:
            if information[voxel_type_index + 1] not in special_points:
                special_points[information[voxel_type_index + 1]] = [voxel_number]

                
        if segment_name not in segment_voxels:
            segment_voxels[segment_name] = [voxel_number]
        elif voxel_number not in segment_voxels[segment_name]:
        #add the number of the voxel, only if it wasn't already added
            segment_voxels[segment_name].append(voxel_number)
        if segment_name not in regions and 'default' not in segment_name:
            regions.add(segment_name)
        if specie_name not in specie_type_dict:
            specie_type_dict[specie_name] = collections.OrderedDict()
        if segment_name not in specie_type_dict[specie_name]:
            specie_type_dict[specie_name][segment_name] = collections.OrderedDict()
        if  information[voxel_type_index] not in specie_type_dict[specie_name][segment_name]:
             specie_type_dict[specie_name][segment_name][information[voxel_type_index]] = [col+1]
        else:
            specie_type_dict[specie_name][segment_name][information[voxel_type_index]].append(col+1)

        if voxel_type_index + 1 != spc_index:
            specie_type_dict[specie_name][segment_name][information[voxel_type_index+1]] = [col+1]

    return segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions

def get_numbers_from_a_fileline(s,specie_type_dict):
    '''
    Read numbers of specie molecules in each voxel calculate number of each specie 
    molecules in the cytosol and submembrane of the segments
    '''
    if isinstance(s,str):
      words = s.split()
    else:
      words = s
    number_specie_segment = collections.OrderedDict()
    for specie in specie_type_dict:
         number_specie_segment[specie] = collections.OrderedDict()
         for segment in specie_type_dict[specie]:
             number_specie_segment[specie][segment]= collections.OrderedDict()
             for voxel_type in specie_type_dict[specie][segment]:
                 number_specie_segment[specie][segment][voxel_type] = 0
                 for i in specie_type_dict[specie][segment][voxel_type]:
                   try:
                     how_much = int(words[i])
                   except ValueError:
                     sys.exit('Broken -conc.txt file')
         
                   number_specie_segment[specie][segment][voxel_type] = number_specie_segment[specie][segment][voxel_type] + how_much

    return number_specie_segment

def concentrations(number_specie_segment,specie_location_dict,area_dict, vol_dict ):
    '''
    calculate specie concentrations in the submembrane and the cytosol.
    '''
    conc_dict = collections.OrderedDict()
    conc_dict['cytosol'] = collections.OrderedDict()
    conc_dict['submembrane'] = collections.OrderedDict()

    for voxel_type in specie_location_dict:
      for segment in specie_location_dict[voxel_type]:
        for specie in specie_location_dict[voxel_type][segment]:
          if segment not in  conc_dict[voxel_type]:
            conc_dict[voxel_type][segment] = collections.OrderedDict()
          if  voxel_type == 'submembrane':
            conc_dict['submembrane'][segment][specie] = number_specie_segment[specie][segment]['submembrane']/area_dict[segment]*10/6.022
          elif voxel_type == 'cytosol':
            conc_dict[voxel_type][segment][specie] = number_specie_segment[specie][segment]['cytosol'] 
            if 'submembrane' in  number_specie_segment[specie][segment]:
              conc_dict[voxel_type][segment][specie] += number_specie_segment[specie][segment]['submembrane']
            conc_dict[voxel_type][segment][specie] = conc_dict[voxel_type][segment][specie]/vol_dict[segment]*10/6.022

    return conc_dict

def totals(number_specie_segment,specie_location_dict,area_dict, vol_dict ):
    '''
    calculate total specie amounts in the submembrane and the cytosol.
    '''
    totals_dict = collections.OrderedDict()
    totals_dict['cytosol'] = collections.OrderedDict()
    totals_dict['submembrane'] = collections.OrderedDict()
    for voxel_type in specie_location_dict:
        for segment in specie_location_dict[voxel_type]:
            for specie in specie_location_dict[voxel_type][segment]:
                
                if segment not in  totals_dict[voxel_type]:
                    totals_dict[voxel_type][segment] = collections.OrderedDict()
                if  voxel_type == 'submembrane':
                    totals_dict['submembrane'][segment][specie] = number_specie_segment[specie][segment]['submembrane']
                elif voxel_type == 'cytosol':
                  totals_dict[voxel_type][segment][specie] = number_specie_segment[specie][segment]['cytosol'] 
                  if 'submembrane' in  number_specie_segment[specie][segment]:
                    totals_dict[voxel_type][segment][specie] += number_specie_segment[specie][segment]['submembrane']
                  totals_dict[voxel_type][segment][specie] = totals_dict[voxel_type][segment][specie]

    return totals_dict

def get_all_species(root):
  '''
  Read Initial Conditions file and make a set of species in the Initial Conditions file.
  '''
  species = set()
  submembrane_species = root.xpath('//PicoSD')
  cytosol_species =  root.xpath('//NanoMolarity')
  for specie in submembrane_species:
    species.add(specie.get("specieID"))
  for specie in cytosol_species:
    species.add(specie.get("specieID"))
  return species

def get_all_species_from_reactions_file(root):
  '''
  Read the reactions file and return the set of all species.
  '''
  species = set()
  for son in root:
    if son.tag == 'Specie':
      species.add(son.get('id'))
  return species
def get_diffusible_species(root):
  '''
  Read the reactions file and return the list of all diffusible species.
  '''
  species = set()
  for son in root:
    if son.tag == 'Specie':
      if float(son.get('kdiff')) > 0:
        species.add(son.get('id'))
  return species  

def get_submembrane_species(fname,regions):
    '''
    Read the initial conditions file to gain information which species 
    are solely in the submembrane and which in the whole cytosol. Read the
    reactions file to check, which species are diffusible and account for that.
    '''
    root = xml_root(fname)
    ic_filename = (root.xpath('initialConditionsFile')[-1].text).strip()
    if not ic_filename.endswith('.xml'):
      ic_filename += '.xml'
    root_ic = xml_root(ic_filename)
    all_species = get_all_species(root_ic)
    reac_filename = (root.xpath('reactionSchemeFile')[-1].text).strip()
    if not reac_filename.endswith('.xml'):
      reac_filename += '.xml'

    root_reac = xml_root(reac_filename)

    diff_species = get_diffusible_species(root_reac)

    specie_location_dict = collections.OrderedDict()
    specie_location_dict['submembrane'] = collections.OrderedDict()
    specie_location_dict['cytosol'] = collections.OrderedDict()

    for region in regions:
      specie_location_dict['cytosol'][region] = []
      if '.' not in region:
        specie_location_dict['submembrane'][region] = []

    for specie in diff_species:
      for region in regions:
        specie_location_dict['cytosol'][region].append(specie)
  
    for son in root_ic:
        reg = son.get('region')
        if not reg:
            where = regions.copy()
        else:
            where = []
            for region in regions:
              if region.startswith(reg):
                where.append(region)
        for grandson in son:
            specie = grandson.get('specieID')
            tag = grandson.tag
            if specie not in diff_species:
              if tag == 'NanoMolarity':
                for region in where:
                  if region in specie_location_dict['submembrane']:
                    if specie in specie_location_dict['submembrane'][region]:
                      specie_location_dict['submembrane'][region].remove(specie)
                  if specie not in specie_location_dict['cytosol'][region]:
                    specie_location_dict['cytosol'][region].append(specie)

              if tag == 'PicoSD':
                for region in where:
                  if specie in specie_location_dict['cytosol'][region]:
                    specie_location_dict['cytosol'][region].remove(specie) 
                  if specie not in specie_location_dict['submembrane'][region]:
                    specie_location_dict['submembrane'][region].append(specie)

    return specie_location_dict

def xml_root(filename):
    '''get root of an xml file. 
    '''
    tree = etree.parse(filename)
    root = tree.getroot()
    return root

def xml_write_to_file(filename,root):
    '''
    write xml tree to a file
    '''
    f = open(filename,'w')
    f.write(etree.tostring(root, pretty_print=True))

def write_output_file(specie_set,output_file,dt,output_filename,species='all'):
 
    root = etree.Element('OutputScheme')
    son = etree.SubElement(root,'OutputSet')
    son.set('filename',output_filename)
    son.set('dt',dt)
    for specie in specie_set:
        grandson = etree.SubElement(son,'OutputSpecie')
        grandson.set('name',specie)
    xml_write_to_file(output_file,root)

def prepare_initial_information(model_file, run_time,dt,every_specie=True,new_seed=False,new_add=''):
    root_mf = xml_root(model_file)
    initial_conditions_file = (root_mf.xpath('initialConditionsFile')[-1].text).strip()
    if  not initial_conditions_file.endswith('.xml'):
      initial_conditions_file += '.xml'
    reactions_file = (root_mf.xpath('reactionSchemeFile')[-1].text).strip()
    if not reactions_file.endswith('xml'):
      reactions_file += '.xml'
    root_ic = xml_root(initial_conditions_file)
    root_reac = xml_root(reactions_file)

    all_species = get_all_species(root_ic)
    all_species_reactions = get_all_species_from_reactions_file(root_reac)
    
    if all_species != all_species_reactions:
      print 'There are different species in the initial conditions file, than in the reactions file'
      print 'Excessive species in the Initial Conditions file:'
      print all_species.difference(all_species_reactions)
      print 'Spiecies from the Reactions file not present in the Initial conditions file:'
      print all_species_reactions.difference(all_species)
      sys.exit('Do fix your xml files, please.')
      
    if every_specie:
      output_file = model_file[:-4]+'_whole_output'
      former_output_file =  root_mf.xpath('outputSchemeFile')[-1]
      former_output_file.text = output_file
      write_output_file(all_species,output_file+'.xml',dt,'all_species')
      default_fn = ['all_species']
    else:
      
      output_file =  root_mf.xpath('outputSchemeFile')[-1].text
      if '.xml' not in output_file:
        output_file += '.xml'
      output_root = xml_root(output_file)
      default_fn = [elem.get('filename') for elem in output_root.xpath('OutputSet')]
      print default_fn
    #change runtime to
    if run_time == 'short':
      run_time = (root_mf.xpath('fixedStepDt')[-1].text).strip()
    elif not  isinstance(run_time, basestring):
      run_time = str(run_time)
      if not run_time.isdigit():
        sys.exit('Not a proper run time')
    length = root_mf.xpath('runtime')[-1]
    length.text = run_time
    if new_seed:
      seed_tag = root_mf.xpath('simulationSeed')
      seed_tag[-1].text = str(new_seed)
      if new_add == '':
        new_add = 'new_seed_'+str(new_seed)
      else:
        new_add += new_add+'_new_seed_'+str(new_seed)
    if not new_add:
      new_model_fname = model_file[:-4] + '_runtime_' + run_time + '.xml'
    else:
      new_model_fname = model_file[:-4] +'_'+new_add+'_runtime_' + run_time + '.xml'
    
    xml_write_to_file(new_model_fname,root_mf)
    conc_file = [new_model_fname[:-4]+'-'+default+'-conc.txt' for default in default_fn]
    mesh_file = new_model_fname[:-4]+'-mesh.txt'
    return new_model_fname, default_fn

def short_run(filename,NeuroRD_path='home/asia/NeuroRD/stochdiff2.1.10.jar'):
    
    process = subprocess.Popen(['java','-jar',NeuroRD_path,filename])
    ret = process.wait()
    
    return ret


def write_totals(fname, number_specie_segment):
  f = open(fname,'w')
  f.write('Totals\n')
  
  for specie in number_specie_segment:
    total = 0
    for segment in number_specie_segment[specie]:
      for voxel_type in number_specie_segment[specie][segment]:
        if voxel_type in ['cytosol','submembrane']:
          total += number_specie_segment[specie][segment][voxel_type]
    f.write( specie +' '+str(total) +'\n')

def write_new_initial_conditions(fname,conc, area_dict,vol_dict,tolerance,threshold_small):

    submembrane_species = set()
    cytosol_species = set()

    for segment in conc['submembrane']:
        for specie in conc['submembrane'][segment]:
                submembrane_species.add(specie)

    for segment in conc['cytosol']:
        for specie in conc['cytosol'][segment]:
                cytosol_species.add(specie)

        
    new_conc = collections.OrderedDict()
    new_conc['all'] = collections.OrderedDict()
    new_conc['submembrane'] = collections.OrderedDict()
    new_conc['cytosol'] = collections.OrderedDict()

    for specie in submembrane_species:
        new_conc['submembrane'][specie] = collections.OrderedDict()
        for segment in conc['submembrane']:
            if specie in  conc['submembrane'][segment]:
              if conc['submembrane'][segment][specie] > 0:
                new_conc['submembrane'][specie][segment] = conc['submembrane'][segment][specie]
              else:
                new_conc['submembrane'][specie][segment] = 0
                

    for specie in cytosol_species:
        new_conc['cytosol'][specie] = collections.OrderedDict()
        for segment in conc['cytosol']:
            if specie in conc['cytosol'][segment]:
              if conc['cytosol'][segment][specie] > 0:
                new_conc['cytosol'][specie][segment] = conc['cytosol'][segment][specie]
              else:
                new_conc['cytosol'][specie][segment] = 0

             

    full_area = 0
    all_area_segments = []
    for segment in area_dict:
        full_area +=  area_dict[segment]
        all_area_segments.append(segment)

    for specie in new_conc['submembrane']:
        average_conc = 0
        for segment in new_conc['submembrane'][specie]:
            average_conc += new_conc['submembrane'][specie][segment]*area_dict[segment]
        average_conc = average_conc/full_area

        similar_segment_list = []
        for segment in new_conc['submembrane'][specie]:
            if new_conc['submembrane'][specie][segment]  < threshold_small:
                similar_segment_list.append(segment)
            else:
                if abs(new_conc['submembrane'][specie][segment]-average_conc)/average_conc <= tolerance:
                    similar_segment_list.append(segment)


        if similar_segment_list != [] and sorted(similar_segment_list)!=sorted(all_area_segments):
            average_conc = 0
            area_denominator = 0
            for segment in similar_segment_list:
                average_conc += new_conc['submembrane'][specie][segment]*area_dict[segment]
                area_denominator += area_dict[segment]
            average_conc = average_conc /area_denominator
            
        for segment in similar_segment_list:
            new_conc['submembrane'][specie][segment] = average_conc
        
    full_volume = 0
    all_volume_segments = []
    for segment in vol_dict:
        full_volume +=  vol_dict[segment]
        all_volume_segments.append(segment)
    all_volume_segments_no_defaults = []
    for region in all_volume_segments:
      if 'fake' not in region:
        all_volume_segments_no_defaults.append(region)
    for specie in new_conc['cytosol']:            
        average_conc = 0
        for segment in new_conc['cytosol'][specie]:
            average_conc += new_conc['cytosol'][specie][segment]*vol_dict[segment]
        average_conc = average_conc/full_volume
        similar_segment_list = []
        for segment in new_conc['cytosol'][specie]:
            if new_conc['cytosol'][specie][segment] < threshold_small:
                similar_segment_list.append(segment)
            elif abs(new_conc['cytosol'][specie][segment]-average_conc)/average_conc <= tolerance:
              similar_segment_list.append(segment)

        if similar_segment_list != [] and sorted(similar_segment_list)!=sorted(all_volume_segments):
            average_conc = 0
            volume_denominator = 0
            for segment in similar_segment_list:
                average_conc += new_conc['cytosol'][specie][segment]*vol_dict[segment]
                volume_denominator += vol_dict[segment]
            average_conc = average_conc /volume_denominator
        
        similar_segment_list_no_defaults = []
        
        for region in similar_segment_list:
          if 'fake' not in region:
            similar_segment_list_no_defaults.append(region)
        
        if sorted(similar_segment_list_no_defaults) == sorted(all_volume_segments_no_defaults):
        
          new_conc['all'][specie] = average_conc
          del new_conc['cytosol'][specie]
        else:
          for segment in similar_segment_list:
            new_conc['cytosol'][specie][segment] = average_conc
            


    v_type_dict = {'cytosol':'ConcentrationSet',
                   'submembrane':'SurfaceDensitySet',
                   'all':'ConcentrationSet'
                   }
    conc_type_dict = {'cytosol':'NanoMolarity',
                      'submembrane':'PicoSD',
                      'all':'NanoMolarity'
                      }
    root = etree.Element('InitialConditions')
    new_conc_2 = collections.OrderedDict()
    new_conc_2['submembrane'] = collections.OrderedDict()
    new_conc_2['cytosol'] = collections.OrderedDict()
    new_conc_2['all'] = collections.OrderedDict()

    for specie in new_conc['all']:
      new_conc_2['all'][specie] = new_conc['all'][specie]

    for voxel_type in ['cytosol','submembrane']:
      for specie in new_conc[voxel_type]:
        for segment in new_conc[voxel_type][specie]:
          if 'fake' not in segment:
            if segment not in new_conc_2[voxel_type]:
              new_conc_2[voxel_type][segment] = collections.OrderedDict()
            new_conc_2[voxel_type][segment][specie] = new_conc[voxel_type][specie][segment]

    son = etree.SubElement(root,v_type_dict['all'])

    for specie in new_conc_2['all']:
      grandson = etree.SubElement(son,conc_type_dict['all'])
      grandson.set('specieID',specie)
      grandson.set('value',str(round(new_conc_2['all'][specie],0)))

    for voxel_type in ['cytosol','submembrane']:
        for segment in new_conc_2[voxel_type]:
          son = etree.SubElement(root,v_type_dict[voxel_type])
          son.set("region",segment.split('.')[0])
          for specie in new_conc_2[voxel_type][segment]:
            grandson = etree.SubElement(son,conc_type_dict[voxel_type])
            grandson.set('specieID',specie)
            grandson.set('value',str(round(new_conc_2[voxel_type][segment][specie],0)))

    fname = fname+'_new_conc.xml'
    
    print fname
    xml_write_to_file(fname,root)



def get_concentrations(number_specie_segment, species_voxels, area,volume):

  totals = collections.OrderedDict()
  for specie in number_specie_segment:
    total = 0
    for segment in number_specie_segment[specie]:
      for voxel_type in number_specie_segment[specie][segment]:
        if voxel_type in ['cytosol','submembrane']:
          total += number_specie_segment[specie][segment][voxel_type] 
    totals[specie] = total
  for specie in totals:
    if specie in species_voxels['cytosol']:
      totals[specie] = totals[specie]/volume*10/6.022
    else:
      totals[specie] = totals[specie]/area*10/6.022
  return totals

def get_totals(number_specie_segment):

  totals = collections.OrderedDict()
  for specie in number_specie_segment:
    total = 0
    for segment in number_specie_segment[specie]:
      for voxel_type in number_specie_segment[specie][segment]:
        if voxel_type in ['cytosol','submembrane']:
          total += number_specie_segment[specie][segment][voxel_type] 
    totals[specie] = total
  return totals

def initial_totals(model_fname):
  for defa in default_fn:
    conc_filename = model_fname[:-4] +'-'+ defa + '-conc.txt'
    f = open(conc_filename,'r')
    header = f.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    totals_filename = conc_filename+'_initial_totals'
    fl = open(totals_filename,'w')
    first_line = f.readline()
    number_specie_segment =  get_numbers_from_a_fileline(first_line,specie_type_dict)
    totals = get_totals(number_specie_segment)
    for specie in totals:
      fl.write(specie+' '+str(totals[specie])+'\n')
    print totals_filename

def write_header(fil,all_species):
  fil.write('time ')
  for specie in all_species:
    fil.write(specie+' ')
  fil.write('\n')

def long_totals(model_fname):
  for default in default_fn:
    conc_filename = model_fname[:-4] +'-'+ default + '-conc.txt'
    f = open(conc_filename,'r')
    header = f.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    totals_filename = conc_filename+'_totals'
    totals_file = open(totals_filename,'w')
    specie_list = []
    for specie in specie_type_dict:
      specie_list.append(specie)
    write_header(totals_file,specie_list)

    try:
      conc_data = np.loadtxt(conc_filename, skiprows=1)
      for conc_line in conc_data:
        number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
        totals = get_totals(number_specie_segment)
        try:
          totals_file.write(str(conc_line[0])+' ')
        except IndexError:
          print "Broken file", conc_filename
          break
        for specie in specie_list:
          totals_file.write(str(totals[specie])+' ')
        totals_file.write('\n')
    except ValueError:
      for conc_line in f:
        try:
          number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
          totals = get_totals(number_specie_segment)
        except:
          print('Broken file'+conc_filename)
          return
        totals_file.write(str(conc_line.split()[0])+' ')
        for specie in specie_list:
          totals_file.write(str(totals[specie])+' ')
        totals_file.write('\n')
    print totals_file.name

def long_concentrations(filename, species_voxels, area,volume,add='concentrations'):
  f = open(filename,'r')
  header = f.readline()
  [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
  totals_filename = filename+'_'+add
  totals_file = open(totals_filename,'w')
  specie_list = []
  print filename
  for specie in specie_type_dict:
    specie_list.append(specie)
  write_header(totals_file,specie_list)
  try:
    conc_data = np.loadtxt(filename,skiprows=1)
    for conc_line in conc_data:
      number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
      totals = get_concentrations(number_specie_segment,species_voxels, area,volume)
      try:
        totals_file.write(str(conc_line[0])+' ')
      except IndexError:
        print 'Errors in file', filename 
        break
      for specie in specie_list:
        totals_file.write(str(totals[specie])+' ')
      totals_file.write('\n')
  except ValueError:
    for conc_line in f:
      try:
        number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
      except:
        print('Broken conc file')
        return
      totals = get_concentrations(number_specie_segment,species_voxels, area,volume)
      try:
        totals_file.write(str(conc_line.split()[0])+' ')
      except IndexError:
        print 'Errors in file', filename 
        break
      for specie in specie_list:
        totals_file.write(str(totals[specie])+' ')
      totals_file.write('\n')

def write_concentrations_in_segment(all_species,species_with_numbers,totals_file,conc,cytosol_species,time,target_list,total_volume,total_area,area_dict,vol_dict):
  for specie in all_species:
    species_with_numbers[specie] = 0

  totals_file.write(str(time)+' ')
  
  for region in target_list:
    if region in conc['submembrane']:
      for specie in conc['submembrane'][region]:
        species_with_numbers[specie] += conc['submembrane'][region][specie]*area_dict[region]
    if region in conc['cytosol']:
      for specie in conc['cytosol'][region]:
        species_with_numbers[specie] += conc['cytosol'][region][specie]*vol_dict[region]
  for specie in all_species:
    if specie in cytosol_species:
      totals_file.write(str(species_with_numbers[specie]/total_volume)+' ')
    else:
      totals_file.write(str(species_with_numbers[specie]/total_area)+' ')
  totals_file.write('\n')

def concentrations_in_segment(model_fname,segment_list):
  '''
  Writes cumulative concentrations in chosen segments (given in segment list). 
  '''
  mesh_filename = model_fname[:-4] + '-mesh.txt'
  
  
  for default in default_fn:

    filename = model_fname[:-4] +'-'+ default + '-conc.txt'
  
    try:
      f = open(filename,'r')
    except IOError:
      sys.exit('No such file or directory '+filename)

    header = f.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    target_list = set()
    [area_dict, vol_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)
  #Find NeuroRD region names corresponding with names given in running gisi
    for region in segment_list:
      for reg in regions:
        if region in reg:
          target_list.add(reg)
    if target_list == set():
      print "Segment list is empty"
      continue
  
    total_volume = 0
    total_area = 0
    for region in target_list:
      total_volume +=  vol_dict[region]
      try:
        total_area +=  area_dict[region]
      except:
        pass

    add = 'concentrations'
    for region in target_list:
      add += '_' 
      add +=region
  
    all_species_mem =  get_submembrane_species(model_fname,regions)
    totals_filename = filename + '_' + add
    totals_file = open(totals_filename,'w')
    all_species = []
    cytosol_species = []
    species_mem = collections.OrderedDict()

    for region in target_list:
      for specie in all_species_mem['cytosol'][region]:
        if specie in specie_type_dict:
          if specie not in all_species:
            all_species.append(specie)
          if 'cytosol' not in species_mem:
            species_mem['cytosol'] = collections.OrderedDict()
          if region not in species_mem['cytosol']:
            species_mem['cytosol'][region] = []
          species_mem['cytosol'][region].append(specie)
      if region in all_species_mem['submembrane']:
        for specie in all_species_mem['submembrane'][region]:
          if specie in  specie_type_dict:
            if specie not in all_species:
              all_species.append(specie)
            if 'submembrane' not in species_mem:
              species_mem['submembrane'] = collections.OrderedDict()
            if region not in species_mem['submembrane']:
              species_mem['submembrane'][region] = []
            species_mem['submembrane'][region].append(specie)

    for region in regions:
      for specie in all_species_mem['cytosol'][region]:
        if specie not in cytosol_species:
          cytosol_species.append(specie)
    write_header(totals_file,all_species)

    species_with_numbers = {}

    print totals_filename
    
    try:
      conc_data = np.loadtxt(filename,skiprows=1)
      print '1'
      for conc_line in conc_data:
        number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
        conc = concentrations(number_specie_segment,species_mem,area_dict, vol_dict)
        write_concentrations_in_segment(all_species,species_with_numbers,totals_file,conc,cytosol_species,conc_line[0],target_list,total_volume,total_area,area_dict,vol_dict)
    except ValueError:
      print '2'
      for conc_line in f:
        try:
          number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
        except:
          print('Broken conc file')
          return
        conc = concentrations(number_specie_segment,species_mem,area_dict, vol_dict)
        write_concentrations_in_segment(all_species,species_with_numbers,totals_file,conc,cytosol_species,conc_line.split()[0],target_list,total_volume,total_area,area_dict,vol_dict)
 

def write_long_segments(totals_files,regions,conc,time,specie_list_in_regions):
  for region in regions:
    totals_files[region].write(str(time)+' ')
  for region in regions:
    if region in conc['submembrane']:
      for specie in specie_list_in_regions[region]:
        if specie in conc['submembrane'][region]:
          if specie in conc['cytosol'][region]:
            totals_files[region].write(str(conc['cytosol'][region][specie])+' ')
          else:
            totals_files[region].write(str(conc['submembrane'][region][specie])+' ')
        else:
          totals_files[region].write(str(conc['cytosol'][region][specie])+' ')
    else:
      for specie in specie_list_in_regions[region]:
        try:
          totals_files[region].write(str(conc['cytosol'][region][specie])+' ')
        except KeyError:
          totals_files[region].write('0 ')
    totals_files[region].write('\n')

def get_species_mem(regions,specie_list_in_regions,all_species_mem):

  species_mem = collections.OrderedDict()
  #make sure that the dictionary species_mem contains only the species that are in the result file
  for region in regions:
    for specie in specie_list_in_regions[region]:
      if specie in all_species_mem['cytosol'][region]:
        if 'cytosol' not in species_mem:
          species_mem['cytosol'] = collections.OrderedDict()
        if region not in species_mem['cytosol']:
          species_mem['cytosol'][region] = []
        species_mem['cytosol'][region].append(specie)
      else:
        if specie in all_species_mem['submembrane'][region]:
          if 'submembrane' not in species_mem:
            species_mem['submembrane'] = collections.OrderedDict()
          if region not in species_mem['submembrane']:
            species_mem['submembrane'][region] = []
          species_mem['submembrane'][region].append(specie)
  return species_mem

def prepare_for_segments(model_fname,specie_type_dict,filename,regions,add):
  totals_files = {}
  specie_list_in_regions = {}
  all_species_mem =  get_submembrane_species(model_fname,regions)
  for region in regions:
    totals_filename = filename+'_'+add+'_'+region
    totals_file = open(totals_filename,'w')
    totals_files[region]=totals_file
    specie_list = []

    for specie in all_species_mem['cytosol'][region]:
      if specie in specie_type_dict:
        specie_list.append(specie)
    if region in all_species_mem['submembrane']:
      for specie in all_species_mem['submembrane'][region]:
        if specie in specie_type_dict:
          specie_list.append(specie)


    write_header(totals_file,specie_list)
    specie_list_in_regions[region] = specie_list[:]

  species_mem = get_species_mem(regions,specie_list_in_regions,all_species_mem)

  return totals_files,specie_list_in_regions,species_mem

def long_totals_segments(model_fname,add='totals'):

  mesh_filename = model_fname[:-4] +'-mesh.txt'
  for default in default_fn:
    filename = model_fname[:-4] +'-'+ default + '-conc.txt'
    try:
      f = open(filename,'r')
    except IOError:
      sys.exit('No such file or directory '+filename)

    header = f.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    [area_dict, vol_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)
    [totals_files,specie_list_in_regions,species_mem] = prepare_for_segments(model_fname,specie_type_dict,filename,regions,add=add)
    try:
      conc_data = np.loadtxt(filename,skiprows=1)
      for conc_line in conc_data:
        number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
        conc = totals(number_specie_segment,species_mem,area_dict, vol_dict)
        try:
          write_long_segments(totals_files,regions,conc,conc_line[0],specie_list_in_regions)
        except IndexError:
          print 'Broken file', filename
          break
    except ValueError:
      for conc_line in f:
        try:
          number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
        except:
          print('Broken conc file')
          break
        conc = totals(number_specie_segment,species_mem,area_dict, vol_dict)
        try:
          write_long_segments(totals_files,regions,conc,conc_line.split()[0],specie_list_in_regions)
        except IndexError:
          print 'Broken file', filename
          break
    for fil in totals_files:
      print fil


def long_concentrations_segments_array(model_fname):
  totals_array_list = []
 
  mesh_filename = model_fname[:-4] + '-mesh.txt'
  for default in default_fn:
    filename = model_fname[:-4] +'-'+ default + '-conc.txt'
    try:
      f = open(filename,'r')
    except IOError:
      try:
        print 'No such file or directory',filename, mesh_filename
        filename = model_fname[:-4] +'.out-'+ default + '-conc.txt'
        mesh_filename = model_fname[:-4] + '.out-mesh.txt'
        f = open(filename,'r')
      except IOError:
        sys.exit('No such file or directory '+filename)

    header = f.readline()
    try:
      conc_data = np.loadtxt(filename,skiprows=1)
    except ValueError:
      print('Broken conc file '+filename)
      total = np.array([float(item) for item in f.readline().split()])
      row_len = total.shape[0]
      for line in f:
        total_new = np.array([float(item) for item in line.split()])
        if total_new.shape[0] == row_len:
          total = np.concatenate((total,total_new),axis=0)
      col_len= total.shape[0]/row_len
      conc_data = total.reshape((col_len,row_len))

    time = conc_data[:,0]

    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    [area_dict, vol_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)

    totals_array = {}
    specie_list_in_regions = {}
    all_species_mem =  get_submembrane_species(model_fname,regions)
    
    l_conc = conc_data.shape[0]

    for region in regions:
      specie_list = []
      for specie in all_species_mem['cytosol'][region]:
        if specie in specie_type_dict:
          specie_list.append(specie)
      if region in all_species_mem['submembrane']:
        for specie in all_species_mem['submembrane'][region]:
          if specie in specie_type_dict:
            specie_list.append(specie)
    
      specie_list_in_regions[region] = specie_list[:]
      totals_array[region] = {}
      for specie in specie_list:
        totals_array[region][specie] = np.zeros((l_conc,1))
    
    species_mem = get_species_mem(regions,specie_list_in_regions,all_species_mem)
            
    for i, conc_line in enumerate(conc_data):
      number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
      conc = concentrations(number_specie_segment,species_mem,area_dict, vol_dict)
      for region in regions:
        if region in conc['submembrane']:
          for specie in specie_list_in_regions[region]:
            if specie in conc['submembrane'][region]:
              if specie in conc['cytosol'][region]:
                totals_array[region][specie][i] = conc['cytosol'][region][specie]
              else:
                totals_array[region][specie][i] = conc['submembrane'][region][specie]
            else:
              totals_array[region][specie][i] = conc['cytosol'][region][specie]
        else:
          for specie in specie_list_in_regions[region]:
            try:
              totals_array[region][specie][i] = conc['cytosol'][region][specie]
            except KeyError:
              totals_array[region][specie][i] = 0
    totals_array_list.append(totals_array)
  return totals_array_list,time

def write_long_concentrations_segments(regions,totals_files,conc,specie_list_in_regions,time):
  for region in regions:
    totals_files[region].write(str(time)+' ')
  for region in regions:
    if region in conc['submembrane']:
      for specie in specie_list_in_regions[region]:
        if specie in conc['submembrane'][region]:
          if specie in conc['cytosol'][region]:
            totals_files[region].write(str(conc['cytosol'][region][specie])+' ')
          else:
            totals_files[region].write(str(conc['submembrane'][region][specie])+' ')
        else:
          totals_files[region].write(str(conc['cytosol'][region][specie])+' ')
    else:
      for specie in specie_list_in_regions[region]:
        try:
          totals_files[region].write(str(conc['cytosol'][region][specie])+' ')
        except KeyError:
          totals_files[region].write('0 ')
    totals_files[region].write('\n')

def long_concentrations_segments(model_fname,add='concentrations'):
   mesh_filename = model_fname[:-4] + '-mesh.txt'
   for default in default_fn:
     filename = model_fname[:-4] +'-'+ default + '-conc.txt'
     
     try:
       f = open(filename,'r')
     except IOError:
       try:
         print 'No such file or directory',filename, mesh_filename
         filename = model_fname[:-4] +'.out-'+ default + '-conc.txt'
         mesh_filename = model_fname[:-4] + '.out-mesh.txt'
         f = open(filename,'r')
         
       except IOError:
         sys.exit('No such file or directory '+filename)
     
     header = f.readline()
     
     [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
     
     [area_dict, vol_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)
     [totals_files,specie_list_in_regions,species_mem] = prepare_for_segments(model_fname,specie_type_dict,filename,regions,add=add)
     for fil in totals_files:
       print totals_files[fil].name
     try:
       conc_data = np.loadtxt(filename,skiprows=1)
       for conc_line in conc_data:
         number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
         conc = concentrations(number_specie_segment,species_mem,area_dict, vol_dict)
         try:
           write_long_concentrations_segments(regions,totals_files,conc,specie_list_in_regions,conc_line[0])
         except IndexError:
           break
     except ValueError:
       for conc_line in f:
         try:
           number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
         except:
           print('Broken conc file')
           break
         conc = concentrations(number_specie_segment,species_mem,area_dict, vol_dict)
         try:
           write_long_concentrations_segments(regions,totals_files,conc,specie_list_in_regions,conc_line.split()[0])
         except IndexError:
           break
         
def just_concentrations(model_fname,tolerance,threshold):
  """
  Calculates new initial conditions from the last state of the model 
  described in model file and writes them in the -new_conc.xml file.
  """
  mesh_filename = model_fname[:-4] + '-mesh.txt'
  for default in default_fn:
    conc_filename = model_fname[:-4] +'-'+ default + '-conc.txt'
    try:
        conc_file = open(conc_filename)
    except IOError:
      sys.exit('No such file or directory '+conc_filename)

    header = conc_file.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    [area_dict, vol_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)

    conc_line = conc_file.readline()
    true_len = len(conc_line.split())
    counter = 0
    while True:
      old_line = conc_line
      conc_line = conc_file.readline()

      if  len(conc_line.split()) < true_len:
        break

    try:

      number_specie_segment = get_numbers_from_a_fileline(conc_line,specie_type_dict)
    except IndexError:
      try:

        number_specie_segment = get_numbers_from_a_fileline(old_line,specie_type_dict)
      except IndexError:
        print('Broken -conc.txt file')
        break


    all_species_mem =  get_submembrane_species(model_fname,regions)
    species_mem = {}
    for voxel in ['cytosol','submembrane']:
      for region in all_species_mem[voxel]:
        for specie in all_species_mem[voxel][region]:
          if specie in specie_type_dict:
            if voxel not in species_mem:
              species_mem[voxel] = {}
            if region not in species_mem[voxel]:
              species_mem[voxel][region] = []
            species_mem[voxel][region].append(specie)
          
      

    conc = concentrations(number_specie_segment,species_mem,area_dict, vol_dict)
    fname = model_fname[:-4]+'_'+default
    write_new_initial_conditions(fname,conc, area_dict,vol_dict,tolerance,threshold)

def area_and_volume(model_fname):
  for default in default_fn:
    conc_filename = model_fname[:-4]+'-'+default+'-conc.txt'
    mesh_filename = model_fname[:-4]+'-mesh.txt'
    conc_file = open(conc_filename)
    header = conc_file.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    [area_dict, volume_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)
    total_volume = 0
    total_area = 0
    for segment in area_dict:
      print segment, 'area', area_dict[segment]
      total_area += area_dict[segment]
    print 'total area', total_area, 'um^2'
    for segment in volume_dict:
      print segment, 'volume', volume_dict[segment]
      total_volume += volume_dict[segment]
    print 'total volume', total_volume, 'um^3'
    #return total_area, total_volume


def generate_concentration_files(model_fname):
  mesh_filename = model_fname[:-4]+'-mesh.txt'
  for default in default_fn:
    conc_filename = model_fname[:-4]+'-'+default+'-conc.txt'
    
    try:
      conc_file = open(conc_filename,'r')
    except IOError:
      try:
        print 'No such file or directory',conc_filename, mesh_filename
        conc_filename = model_fname[:-4] +'.out-'+ default + '-conc.txt'
        mesh_filename = model_fname[:-4] + '.out-mesh.txt'
        conc_file = open(conc_filename,'r')
      except IOError:
        sys.exit('No such file or directory '+conc_filename)


    header = conc_file.readline()
    [segment_voxels,segment_area_voxels,special_points, specie_type_dict, regions] = read_header(header)
    [area_dict, vol_dict] = calculate_volume_and_area(mesh_filename,segment_voxels,segment_area_voxels)

    species_mem =  get_submembrane_species(model_fname,regions)

    species_voxels = collections.OrderedDict()
    species_voxels['submembrane'] = set()
    species_voxels['cytosol'] = set()

    for voxel in species_mem:
      for regions in species_mem[voxel]:
        for specie in species_mem[voxel][regions]:
          species_voxels[voxel].add(specie)

    area = 0
    for region in area_dict:
      area += area_dict[region]
    volume = 0
    for region in vol_dict:
      volume += vol_dict[region]
    long_concentrations(conc_filename, species_voxels, area,volume,add='concentrations_total')

def different_stimulation_100_Hz(model_fname):
  root = xml_root(model_fname)
  stim_file = (root.xppath('stimulationFile')[-1].text).strip()+'.xml'
  root_stim = xml_root(stim_file)

def compare_measures_totals(model_fname):
  for default in default_fn:
    totals_fname =  model_fname[:-4]+'-'+default+'-conc.txt_concentrations_'
    list1 = []
    os.path.walk('.', lambda arg,dirname,fnames:[arg.append(os.path.join(dirname, name)) for name in fnames if name.startswith(totals_fname)], list1)

    for name in list1:
      
      if 'default' in name:
        continue
      if name.endswith('change'):
        continue
      try:
        f = open(name)
      except IOError:
        print 'could not open or generate concentration files ', name
        continue
      print name
      header = f.readline()
      f.close()
      data = np.loadtxt(name,skiprows=1)

      root_mf = xml_root(model_fname)
      stimulation_file = (root_mf.xpath('stimulationFile')[-1].text).strip()
      if stimulation_file[-4:] != '.xml':
        stimulation_file += '.xml'
      stim_root = xml_root(stimulation_file)
      stimulation_start = float((stim_root.xpath('InjectionStim')[0]).xpath('onset')[-1].text)
      stimulation_time = int(stimulation_start/(data[1,0] - data[0,0]))
      means = data[:stimulation_time,:].mean(axis=0)

      wynik = (data.sum(axis=0)*(data[1,0]-data[0,0])-means*data[-1,0])/1000

      result_fname = name + '_change'
      print result_fname
      nf = open(result_fname,'w')
      specie_list = header.split()[1:]
      sort = sorted(specie_list)
      
      for specie in sort:
        nf.write(specie +' '+ str(wynik[specie_list.index(specie)+1])+'\n')

def Parser():
  parser = argparse.ArgumentParser(description='Script helping running NeuroRD models and analyzing the results')
  parser.add_argument('input',
                      help='(NeuroRD) model master file')
  parser.add_argument('length', nargs='?', default='short',
                      help='length of the simulation')
  parser.add_argument('--dt',  default='200',
                      help='output step')
  parser.add_argument('--no_run', action='store_true',
                      help='sets flag for postprocessing only')
  parser.add_argument('--concentrations', action='store_true',
                      help='generate concentrations file')
  parser.add_argument('--segment_concentrations', action='store_true',
                      help='generate concentrations files for every segment')
  parser.add_argument('--segment_totals', action='store_true',
                      help='generate total amount of specie molecules files for every segment')
  parser.add_argument('--totals', action='store_true',
                      help='generate totals file')
  parser.add_argument('--initial', action='store_true',
                      help='generate initial totals file')
  parser.add_argument('--info', action='store_true',
                      help='print area and volume information')
  parser.add_argument('--new_ic', action='store_true',
                      help='generate new initial conditions file')
  parser.add_argument('--tolerance',type=float, default=0.5,
                      help='maximum fluctuation  for smoothing in the new initial conditions')
  parser.add_argument('--threshold',type=int, default=1000,
                      help='maximum number of molecules in the segment for automatic smoothing in the new initial conditions')
  parser.add_argument('--path', default='/home/asia/NeuroRD/stochdiff2.1.10.jar', help='NeuroRD path')
  parser.add_argument('--add', default='', help='A custom string added to the model file name and result filenames')
  parser.add_argument('--new_seed', default=False,help='Run with a different seed')
  parser.add_argument('--segment_list', default=None,help='Calculate cumulative concentrations of species in chosen segments. List segments using a comma.')
  parser.add_argument('--change',action='store_true',help='Calculate cumulative change in specie concentration in all concentration files that have been already generated')
  parser.add_argument('--chosen_species',action='store_true',help='Do not overwrite output file')
  return parser

if __name__ == '__main__':
  args = Parser().parse_args()
  model_file = args.input

  if args.chosen_species:
    every_specie = False
  else:
    every_specie = True
  if args.no_run:
    new_model_fname = model_file
    root = xml_root(new_model_fname)
    output_file = (root.xpath('outputSchemeFile')[-1].text).strip()
    if not output_file.endswith('.xml'):
      output_file +='.xml'
    root_output = xml_root(output_file)
    default_fn = [elem.get('filename') for elem in root_output.xpath('OutputSet')]
    
  else:
    new_model_fname, default_fn = prepare_initial_information(model_file, run_time=args.length,dt=args.dt,new_seed=args.new_seed,new_add=args.add,every_specie=every_specie)
    short_run(new_model_fname,NeuroRD_path=args.path)
  if args.segment_list:
    print args.segment_list.split(',')
  print default_fn
  if args.totals:
    long_totals(new_model_fname)
  if args.concentrations:
    generate_concentration_files(new_model_fname)
  if args.info:
    area_and_volume(new_model_fname)
  if args.initial:
    initial_totals(new_model_fname)
  if args.new_ic:
    just_concentrations(new_model_fname,tolerance=args.tolerance,threshold=args.threshold)
  if args.segment_concentrations:
    long_concentrations_segments(new_model_fname)
  
  if args.segment_totals:
    long_totals_segments(new_model_fname)
  if args.segment_list:
    concentrations_in_segment(new_model_fname,args.segment_list.split(','))
  if args.change:
    compare_measures_totals(new_model_fname)
    
