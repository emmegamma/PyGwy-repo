# coding=utf-8
# The first 3 lines are only needed to run in python as standalone script  
import sys
sys.path.append("C:/Program Files (x86)/Gwyddion/bin")
import gwy
import glob
import quantities as pq # see notes on quantities package in python2
import os
import shutil


############################
###### SEARCH OPTIONS ######
############################


### Folder and filetype ###
# Set folder(s) to search (use */* for recursive searches) 
# and filetype (uncomment as needed)
folder = r'\\synology13.jh-inst.cas.cz\NCG\Michele\DATA\STM\2024-10 P127 Valerie\2024-10-22 P127 sputter 5s'
#filetype = '.gwy' 
filetype = '.sxm' 
#filetype = 'both'


### Copy to a folder? ###
# If you want to copy the files found to a specific folder,
# uncomment target_folder and set accordingly
if 'target_folder' in locals():
  del target_folder
#target_folder = r'D:\DATA\STM\2024-10 P127 Valerie\2024-10-09 P127 scan2\defects_30nm'


### Search filters ###

# Filter on the filename (insert between ' ')
filter_filename = '*' 

# Filter on values
# options: size, bias, speed, setpoint, scantime (in seconds),
#  scantime_min (only minutes)

# Field 1, >=
filter_field1 = 'size' # name of the field to apply >= filter 
filter_value1 = 0 # value, pass >=
# Field 2, <=
filter_field2 = 'size'
filter_value2 = 1000

# Filter on comment
filter_comment1 = '' # filter for comment line #1
filter_comment2 = '' # filter for comment line #2


### Print options ###
# Set which info/metadata to print

# Full filename or filenr. only.  0: full, 1: only image number
filename_or_filenr = 0
# Bias and setpoint.  0: no, 1: yes
print_scanparams = 1
# Size and speed.  0: nothing, 1: image size, 2: image size + speed and direction
print_size_speed = 1
# Print the scan time. 0: no, 1: yes
print_time = 0 



############################
####### SCRIPT START #######
############################

#print 'Starting script'
counter = 0

if filetype == '.gwy' or filetype == '.sxm':
  filelist = glob.glob(folder + '\\' + filter_filename + filetype)
elif filetype == 'both':
  filelist = glob.glob(folder + '\\' + filter_filename + '.sxm') + glob.glob(folder + '\\' + filter_filename + '.gwy')
else:
  print 'Filetype not recognized'
  
if len(filelist) != 0:
  for stmfile in filelist:
    
    ## Get current file
    container = gwy.gwy_file_load(stmfile, gwy.RUN_INTERACTIVE)
    # metadata will contain the metadata as keys; str(0) is the number of the image in file
    metadata = container['/' + str(0) +'/meta']
        

    ### GET METADATA ###
    ## Get feedback mode, setpoint, scan speed and direction, acquisition time, and comment
    controller_status = metadata.get_string_by_name('Z-Controller::Controller status')
    feedback = metadata.get_string_by_name('Z-Controller::Controller name')
    setpoint = float(metadata.get_string_by_name('Z-Controller::Setpoint'))
    setpoint_unit = metadata.get_string_by_name('Z-Controller::Setpoint unit')
    bias = float(metadata.get_string_by_name('Bias::Bias (V)'))*pq.V
    osc =  metadata.get_string_by_name('Oscillation Control::output off')
    osc_ampli = metadata.get_double_by_name('Oscillation Control::Amplitude Setpoint (m)') * pq.m
    speed_m = float(metadata.get_string_by_name('Scan::speed forw. (m/s)'))*pq.m/pq.s
    speed = round(speed_m.rescale(pq.nm/pq.s),0)*pq.nm/pq.s
    direction = metadata.get_string_by_name('Direction')
    scantime_str = metadata.get_string_by_name('Acquistion time')
    scantime = float(scantime_str.replace(',', '.').split()[0])#*pq.s
    scantime_min = int(scantime//60)
    scantime_s = int(scantime%60)
    time = metadata.get_string_by_name('Time')
    #time_min = int(divmod(time_s,60)[0])
    #time_secs = int(divmod(time_s,60)[1])
    comment = metadata.get_string_by_name('Comment')

    ## Make the setpoint string according to mode (STM, AFM or combined)
    if controller_status == 'OFF': # constant height
        height = metadata.get_double_by_name('Z-Controller::TipLift (m)')*pq.m
        if osc == 'TRUE':
            mode = 'CH STM+osc %i' % osc_ampli.rescale(pq.pm) + 'pm, dz= %.1f' % height.rescale(pq.angstrom) + 'Ã…'
        elif osc == 'FALSE':
            mode = 'CH, dz= %.1f' % height.rescale(pq.angstrom) + 'Ã…'
    elif controller_status == 'ON': # constant current/df
        #mode = 'CC'
        if feedback.startswith("log"): #STM
            if osc == 'TRUE':
                mode = 'STM+osc %i' % osc_ampli.rescale(pq.pm) + 'pm'
            elif osc == 'FALSE':
                mode = ''
            setpt = setpoint * pq.A
            setpt_txt = ' I=%.2f' % setpt.rescale(pq.nA) + ' nA'
        elif feedback.startswith("FM"): #AFM
            mode = 'AFM osc %i' % osc_ampli.rescale(pq.pm) + 'pm'
            setpt = setpoint * pq.Hz
            setpt_txt = ' df=%.2f' % setpt + ' Hz'


    ### GET IMAGE PROPERTIES ###
    ## Scan size
    #scanfield = metadata.get_string_by_name('Scan::Scanfield')
    # get the topo channel ("Z (Forward)")
    ids = gwy.gwy_app_data_browser_find_data_by_title(container, 'Z*')#(container, 'Z (Forward)')
    # create the DataField with the image
    data_field = container[gwy.gwy_app_get_data_key_for_id(ids[0])]
    # get x,y scan size
    sizeX_m = data_field.get_xreal()*pq.m # in m
    sizeX = round(sizeX_m.rescale(pq.nm)) # in nm, float
    sizeY_m = data_field.get_yreal()*pq.m 
    sizeY = round(sizeY_m.rescale(pq.nm)) 
    size = sizeX


    ### COPY FILES AND PRINT OUTPUT ###

    ## Apply filters
    if locals()[filter_field1] >= filter_value1 and locals()[filter_field2] <= filter_value2 and comment.find(filter_comment1) != -1 and comment.find(filter_comment2) != -1:
     
     counter += 1
     
     ## Get filename/number
     # split the full path into a list
     # last element of the list is the filename
     # the number is the last two digits (before . and extension)
     path_as_list = stmfile.split("\\")
     filename_ext = path_as_list[-1]
     

     ## Copy files if target_folder exists
     if 'target_folder' in locals(): # if variable exists
        target_file = target_folder + '\\' + filename_ext
        try:
          shutil.copyfile(stmfile, target_file)
        except IOError as io_err:
          os.makedirs(target_folder)#os.path.dirname(target_folder))
          shutil.copyfile(stmfile, target_file)
        

     ## Print 

     # build "file number/name: comment" and justification params
     if filename_or_filenr == 0: # if using filename
        filename = filename_ext[0:-4]
        longest = max(filelist, key = len) # longest filename with path; filelist.index() to find its index
        length = len(longest.split('\\')[-1][0:-4])
        justify = [length, length+2]
        intestation = filename.ljust(justify[0]), ':', comment 
     elif filename_or_filenr == 1: # if using filenr
        filenr = filename_ext[-8:-4] # ==filename[-6:-4]
        justify = [3,6]
        intestation = filenr.ljust(justify[0]), ':', comment
     
     # Actual print commands
     print "\r" + " ".join(intestation)
     if print_scanparams == 1:
        scanparams = ' '.ljust(justify[1]), str("V=%.2f V," %bias), setpt_txt
        print " ".join(scanparams)
     if print_size_speed == 1:
        print ' '.ljust(justify[1]), 'size: {0:}x{1:} nm'.format(sizeX,sizeY)
     elif print_size_speed > 1:
        print ' '.ljust(justify[1]), 'size: {0:}x{1:} nm'.format(sizeX,sizeY), 'at {0:}, {1:}'.format(speed,direction) 
     if print_time == 1:
        print ' '.ljust(justify[1]),time, '+ {0:}\'{1:}\"'.format(scantime_min,scantime_s)

  ###endfor
  

  ### Final message ###

  print '\rTotal number of files found: ', counter
  if 'target_folder' in locals():
    print '\r copied to ', target_folder
   
else: # (goes with initial 'if len(filelist) != 0: ')
  print 'No suitable files found in {}, check filters!'.format(folder)
