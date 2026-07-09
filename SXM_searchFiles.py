# coding=utf-8
# https://github.com/emmegamma/PyGwy-repo

#################
### Libraries ###
#################
# note that sys and gwy are only needed to run as standalone python script  
#import sys
import glob, shutil
import os, itertools
### detect OS so that \ and / are set automatically in paths + set path for gwy library
if os.name == 'nt':
  sys.path.append("C:/Program Files (x86)/Gwyddion/bin")
  windows = 1
elif os.name == 'posix':
  sys.path.append("/var/lib/flatpak/app/net.gwyddion.Gwyddion/current/active/files/lib/python2.7/site-packages")
  windows = 0
import gwy


############################
###### SEARCH OPTIONS ######
############################

### Folder and filetype ###
# Set folder(s) to search (use *\* for recursive searches) 
# Uncomment filetype as needed
folder = r'D:\DATA\STM\202*\*\*\\'
#filetype = '.gwy' 
filetype = '.sxm'
#filetype = 'both'

# to check if a file/folder is in the list, use:    
# next((x for x in filelist if x.find('2020') != -1), 'Nothing')
# (throws 'Nothing' if 2020 is not found)


### Search filters ###

# Filename filter (between ' '; for syntax and wildcards see https://pymotw.com/2/glob/)
filter_filename = '*' 

# Metadata filters
# options: size, bias, speed, setpoint, pixelsize,
#          scantime (total in seconds), scantime_min
filter_field1 = 'size' # Field 1, >=
filter_value1 = 0
filter_field2 = 'size' # Field 2, <=
filter_value2 = 1000

# Comment filter
filter_comment1 = '' # filter for comment line #1
filter_comment2 = '' # filter for comment line #2


### Copy to a folder? ###
# If target_folder is uncommented, files are copied to it
if 'target_folder' in locals():
  del target_folder
#target_folder = r'C:\Users\user\myfolder'


############################
###### PRINT OPTIONS #######
############################
# Set which info/metadata to print

filename_or_filenr = 0 # 0: full name with extension, 1: only image number
print_scanparams = 1 # bias and setpoint,  boolean
print_size_speed = 1 # 0: nothing, 1: pixels and image size, 2: also speed and direction
print_scantime = 0 # boolean
print_position = 0 # XY position
print_tilt = 0 # Scan tilt configuration (boolean)


############################
####### SCRIPT START #######
############################

#print 'Starting script'
#counter = 0

### search file by name and extension
separator = '\\' if windows==1 else '/'
if filetype == '.gwy' or filetype == '.sxm':
    filelist = glob.glob(folder + separator + filter_filename + filetype) 
elif filetype == 'both':
    filelist = glob.glob(folder + separator + filter_filename + '.sxm') + glob.glob(folder + separator + filter_filename + '.gwy')
else:
  print 'Filetype not recognized'

# clean duplicates (useless if file extension is included..)
# filelist_unique = set(filelist)

filtered_list = []
errors = []
metadata_errors = []

#groups = {key: set(value)
#      for key, value in itertools.groupby(sorted(filelist,
#                                key = lambda e: os.path.splitext(e)[0]),
#                                key = lambda e: os.path.splitext(e)[0])}

if len(filelist) != 0:
  #filelist.sort()
  for stmfile in filelist:
  
    ## Get filename/number
    # split the full path into a list
    # last element of the list is the filename
    # the number is the last two digits (before . and extension)
    if windows:
      path_as_list = stmfile.split("\\")
    elif linux:
      path_as_list = stmfile.split("/")
    filename = path_as_list[-1]
    filebase = filename[0:-4]

    
    ## Get current file
    try: 
    	container = gwy.gwy_file_load(stmfile, gwy.RUN_INTERACTIVE)
    except:
        errors.append(stmfile)
        filelist.remove(stmfile)
        continue
    	
    # metadata will contain the metadata as keys; str(0) is the number of the image in file
    metadata = container['/' + str(0) +'/meta']
        

    try:
        ### GET METADATA ###
        ## Get feedback mode, setpoint, scan speed and direction, acquisition time, and comment
        controller = metadata.get_string_by_name('Z-Controller::Controller status')
        feedback = metadata.get_string_by_name('Z-Controller::Controller name')
        setpoint = float(metadata.get_value_by_name('Z-Controller::Setpoint'))
        setpoint_unit = metadata.get_string_by_name('Z-Controller::Setpoint unit')
        height = metadata.get_double_by_name('Z-Controller::TipLift (m)') * 10000000000 # in Å
        bias = float(metadata.get_value_by_name('Bias::Bias (V)')) # in V 
        osc =  metadata.get_string_by_name('Oscillation Control::output off')
        if osc == 'TRUE':
            osc_ampli_m = metadata.get_double_by_name('Oscillation Control::Amplitude Setpoint (m)') # in m
            osc_ampli = osc_ampli_m*(1000000000000) # in pm 
        speed_m = float(metadata.get_value_by_name('Scan::speed forw. (m/s)')) # in m/s
        speed = round(speed_m*1000000000,0) # in nm/s
        direction = metadata.get_string_by_name('Direction')
        scantime_str = metadata.get_string_by_name('Acquistion time')
        scantime = float(scantime_str.replace(',', '.').split()[0]) # float in seconds
        scantime_min = int(scantime//60) # only minutes components
        scantime_s = int(scantime%60) # only seconds after dividing in mins
        time = metadata.get_string_by_name('Time')
        #time_min = int(divmod(time_s,60)[0])
        #time_secs = int(divmod(time_s,60)[1])
        comment = metadata.get_string_by_name('Comment')
        pixelsize = int(metadata.get_value_by_name('Scan::pixels/line'))
        tiltX = metadata.get_string_by_name('Piezo Configuration::Tilt X (deg)')
        tiltY = metadata.get_string_by_name('Piezo Configuration::Tilt Y (deg)')
        
        ### GET IMAGE PROPERTIES ###
        # get the topo channel ("Z (Forward)")
        ids = gwy.gwy_app_data_browser_find_data_by_title(container, 'Z*')#(container, 'Z (Forward)')
        # create the DataField with the image
        data_field = container[gwy.gwy_app_get_data_key_for_id(ids[0])]
        # get x,y scan size
        #sizeX_m =  # in m
        sizeX = round(data_field.get_xreal()*1000000000,2) # in nm, float
        #sizeY_m = *pq.m 
        sizeY = round(data_field.get_yreal()*1000000000,2) # in nm 
        size = sizeX
        Xoffset = round(data_field.get_xoffset()*1000000000,2) # in nm
        Yoffset = round(data_field.get_yoffset()*1000000000,2)
    except:
        #print 'Error on ' + stmfile
        metadata_errors.append(stmfile)
        #filelist.remove(stmfile)
        continue

    ## Make the setpoint string according to mode (STM, AFM or combined)
    if controller == 'OFF': # constant height
        if osc == 'TRUE':
            mode = 'CH STM+osc %i' % osc_ampli + 'pm, dz= %.1f' % height + 'Ã…'
        elif osc == 'FALSE':
            mode = 'CH, dz= %.1f' % height + 'Ã…'
    elif controller == 'ON': # constant current/df
        #mode = 'CC'
        if feedback.startswith("log"): #STM
            if osc == 'TRUE':
                mode = 'STM+osc %i' % osc_ampli + 'pm'
            elif osc == 'FALSE':
                mode = ''
            setpt = setpoint*1000000000 # in nA
            setpt_txt = ' I=%.2f' % setpt + ' nA'
        elif feedback.startswith("FM"): #AFM
            mode = 'AFM osc %i' % osc_ampli + 'pm'
            #setpt = setpoint * pq.Hz
            setpt_txt = ' df=%.2f' % setpoint + ' Hz'


    ### COPY FILES AND PRINT OUTPUT ###
    
    ## Filters are applied here:
    if locals()[filter_field1] >= filter_value1 and locals()[filter_field2] <= filter_value2 and comment.find(filter_comment1) != -1 and comment.find(filter_comment2) != -1:
      
      # Add to list of filtered files
      filtered_list.append(stmfile)

      ## Create target_folder if it doesn't exist, and copy files to it
      if 'target_folder' in locals():
        target_file = target_folder + '\\' + filename
        try:
          shutil.copyfile(stmfile, target_file)
        except IOError as io_err:
          os.makedirs(target_folder)#os.path.dirname(target_folder))
          shutil.copyfile(stmfile, target_file)
        

      ## Print section
     
      # build "file number/name: comment" and justification params
      if filename_or_filenr == 0: # if using filename
        longest = max(filelist, key = len) # longest filename with path; filelist.index() to find its index
        length = len(longest.split(separator)[-1])# to deindent 2nd line: (separator)[-1][0:-4])
        justify = [length, length+2]
        intestation = filename.ljust(justify[0]), ':', comment 
      elif filename_or_filenr == 1: # if using filenr
        filenr = filename[-8:-4] # ==filename[-6:-4]
        justify = [3,6]
        intestation = filenr.ljust(justify[0]), ':', comment
     
      # Actual print commands
      print " ".join(intestation) # "\r" +  for extra spacing
      if print_scanparams == 1:
        scanparams = ' '.ljust(justify[1]), str("V=%.2f V," %bias), setpt_txt
        print " ".join(scanparams)
      if print_size_speed == 1:
        print ' '.ljust(justify[1]), '{0:.0f}x{1:.0f} nm, {2} px'.format(sizeX,sizeY,pixelsize)
      elif print_size_speed > 1:
        print ' '.ljust(justify[1]), '{0:.0f}x{1:.0f} nm, {2} px'.format(sizeX,sizeY,pixelsize), ', speed {0} nm/s {1:}'.format(speed,direction) 
      if print_scantime == 1:
        print ' '.ljust(justify[1]),time, '+ {mins}\'{sec}\"'.format(mins = scantime_min, sec = scantime_s)
      if print_position == 1:
     	print ' '.ljust(justify[1]), 'Position: X {0} nm, Y {1} nm'.format(Xoffset,Yoffset)
      if print_tilt == 1:
     	print ' '.ljust(justify[1]), 'tilt: X {0}, Y {1}'.format(tiltX,tiltY)
    ## end of filtered list
  ###end of for cycle

  
  ### Final messages ###

  print '\rNumber of files found: {0} (before metadata filtering: {1})'.format(len(filtered_list),len(filelist)) 
  
  if len(errors)>0:
    print 'Load errors: {0:} \n  {1}'.format(len(errors), '\n  '.join(errors))
    
  if len(metadata_errors)>0 & len(metadata_errors)<= 20: 
    print 'Metadata read errors: {0} \n  {1}'.format(len(metadata_errors), '\n  '.join(metadata_errors))
  elif len(metadata_errors)> 20: 
    print 'Metadata read errors: {0} \n  (too many, print with \'print metadata_errors\') '.format(len(metadata_errors))
  
  if 'target_folder' in locals():
    print '\rTarget folder exists: files copied to ', target_folder

# if filelist is empty
else: 
  print 'No suitable files found in {}, check folder/filters'.format(folder)