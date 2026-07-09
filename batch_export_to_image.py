# coding=utf-8
# https://github.com/emmegamma/PyGwy-repo

#################
### Libraries ###
#################
# note that sys and gwy are only needed to run as standalone python script
# import sys  
import glob, shutil
import os, itertools
### set path for gwy library and set \ or / in paths
if os.name == 'nt':
  windows = 1
  sys.path.append("C:/Program Files (x86)/Gwyddion/bin")
  split_char = "\\"
elif os.name == 'posix':
  windows = 0
  sys.path.append("/var/lib/flatpak/app/net.gwyddion.Gwyddion/current/active/files/lib/python2.7/site-packages")
  split_char = "/"
#import gwy

############################
######## OPTIONS ###########
############################

# Set folder(s) and filetype to search (use */* for recursive searches) 
folder = r'C:\Users\STM\Documents\DATA\atomic res\P148'
#filetype = '.gwy' 
#filetype = '.sxm'
filetype = 'both'

# Filter on the filename (keep between ' '; for syntax and wildcards see https://pymotw.com/2/glob/)
filter_filename = '*' 

# OVERWRITE: set to 1 to allow overwrite, 0 to skip existing files
overwrite = 1

# DRY RUN: set to 1 to test without actually writing files
dry_run = 0

############################
####### SCRIPT START #######
############################

# Change the working directory (os.getcwd() to check)
os.chdir(folder)
print 'Working dir: ' + os.getcwd()

### search file by name and extension
if filetype == '.gwy' or filetype == '.sxm':
    filelist = glob.glob(filter_filename + filetype) 
elif filetype == 'both':
    filelist = glob.glob(filter_filename + '.sxm') + glob.glob(filter_filename + '.gwy')
else:
  print 'Filetype not recognized'
  
# create list for not-overwritten files
not_overwritten = []
 

if len(filelist) != 0:
  #filelist.sort()
  for stmfile in filelist:
  
    ## Get filename/number
    # split the full path into a list, the last element is the filename
    path_as_list = stmfile.split(split_char)
    filename = path_as_list[-1]
    filebase = filename[0:-4]
    imagefile = filebase + '.jpg'
    
    if os.path.exists(imagefile) == False:
      output_text = 'Writing '
    else:
      if overwrite == 1:
        output_text = 'Overwriting '
      else:
    	not_overwritten.append(imagefile)    
    	continue
      
    
    ## Get current file and add them to the data browser
    container = gwy.gwy_file_load(stmfile, gwy.RUN_INTERACTIVE)
    gwy.gwy_app_data_browser_add(container)
    
    # if not in dry run, save first channel to image
    if dry_run == 0:
      gwy.gwy_app_data_browser_select_data_field(container, 0)
      if stmfile==filelist[0]: #at first iteration, run interactive to set image params
        gwy.gwy_file_save(container, imagefile, RUN_INTERACTIVE)
      else:
        gwy.gwy_file_save(container, imagefile, RUN_NONINTERACTIVE)
    
    # Remove the container from the data browser
    gwy.gwy_app_data_browser_remove(container)
   
    # Print operation
    print output_text + imagefile # + folder + split_char
    
else: ### if no files were found (len(filelist)== 0)  
  print 'No suitable files found in {}, check folder/filters'.format(folder)

# list NOT overwritten files
if len(not_overwritten) != 0:
    print '\nFiles skipped (overwrite = 0):'
    for i in not_overwritten:
        print ' {}'.format(i)

# if dry_run, say it
if dry_run == 1:
    print '\r(Dry run, no files were actually written)'