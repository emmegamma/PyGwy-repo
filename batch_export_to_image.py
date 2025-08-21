# coding=utf-8
# https://github.com/emmegamma/PyGwy-repo

#################
### Libraries ###
#################
# note that sys and gwy are only needed to run as standalone python script
# import sys  
import glob, shutil
import os, itertools
### detect OS so that \ and / are set automatically in paths + set path for gwy library
if os.name == 'nt':
  sys.path.append("C:/Program Files (x86)/Gwyddion/bin")
  windows = 1
elif os.name == 'posix':
  sys.path.append("/var/lib/flatpak/app/net.gwyddion.Gwyddion/current/active/files/lib/python2.7/site-packages")
  windows = 0
#import gwy

############################
######## OPTIONS ###########
############################

### Folder and filetype ###
# Set folder(s) to search (use */* for recursive searches) 
# and filetype (uncomment as needed)
folder = r'D:\DATA\STM'
filetype = '.gwy' 
#filetype = '.sxm'
#filetype = 'both'

# Filter on the filename (keep between ' '; for syntax and wildcards see https://pymotw.com/2/glob/)
filter_filename = '*' 

# OVERWRITE: set to 1 to allow overwrite, otherwise existing files will be skipped
overwrite = 1

# DRY RUN: set to 1 to test without actually writing files
dry_run = 0

############################
####### SCRIPT START #######
############################

# Change the current folder's directory and get the name
os.chdir(folder)
location = os.getcwd()

### search file by name and extension
separator = '\\' if windows==1 else '/'
if filetype == '.gwy' or filetype == '.sxm':
    filelist = glob.glob(filter_filename + filetype) 
elif filetype == 'both':
    filelist = glob.glob(filter_filename + '.sxm') + glob.glob(filter_filename + '.gwy')
else:
  print 'Filetype not recognized'
  
# create list for not-overwritten files
existing_files = []
 

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
    imagefile = filebase + '.jpg'
    print_text = 'Writing ' 
    
    if os.path.exists(imagefile):
         if overwrite != 1: #overwrite will work only if it's exactly 1
             existing_files.append(imagefile)    
    	     continue
    	 else:
    	     print_text = 'Overwriting '
    
    ## Get current file and add them to the data browser
    container = gwy.gwy_file_load(stmfile, gwy.RUN_INTERACTIVE)
    gwy.gwy_app_data_browser_add(container)
    
    # save first channel of file
    if dry_run == 0:
        gwy.gwy_app_data_browser_select_data_field(container, 0)
        gwy.gwy_file_save(container, imagefile, RUN_NONINTERACTIVE)
    
    # Remove the file (container) from the data browser to avoid overloading the memory
    gwy.gwy_app_data_browser_remove(container)
   
    # Print operation
    print print_text + location + separator + imagefile
    
else: ### if no files were found (len(filelist)== 0)  
  print 'No suitable files found in {}, check folder/filters'.format(folder)

# if files were NOT overwritten, list them    
if len(existing_files) != 0:
    print '\nOverwrite was 0, so the following files were skipped (existed already):'
    for i in existing_files:
        print i

# if dry_run, say it
if dry_run == 1:
    print '(Dry run, no files actually written)'