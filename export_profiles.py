# coding=utf-8
import glob
#import shutil


############################
######### OPTIONS ##########
############################

## Run blank search (0), or write the profile .txt files (1)
write_profiles = 0 

## Filter: 0 to print/write all profiles, otherwise the number of the profile 
## The number is NOT the Graph title (necessarily), but rather the order shown in the Data Browser
## You can uncomment #print ascii[0:9] later in this file to help associating number/title if needed
only_prof = 2 # 0 to print them all

## Export the profiles for all open files (line 1) or active file only (line 2)
## (uncomment as needed)
files = gwy.gwy_app_data_browser_get_containers() # all open files
#files = [gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)] # only active file


############################
####### SCRIPT START #######
############################

# iterate through open files (containers)
for c in files:
    # get the folder and print the filename
    stmfile = gwy_file_get_filename_sys(c)
    path_as_list = stmfile.replace('\\',"/").split("/")# stmfile.split("/")
    filename = path_as_list[-1]
    folder = '/'.join(path_as_list[0:len(path_as_list)-1])

    # get the list of graphs in the container
    graphlist = gwy_app_data_browser_find_graphs_by_title(c, "Profile*")

    ## Print initial information (folder, file, # of profiles)
    print 'Folder: {}'.format(folder)
    print 'File: ' + filename#, ' and ', filename == stmfile#stmfile[0:-4]
    #print gwy_app_data_browser_get_graph_ids(c)
    if len(graphlist) != 0:
        print "Found {} profiles:".format(len(graphlist))
        
        # Iterate through the graphs
        for i in graphlist:
            # access the name of the graph and open it
            key = gwy.gwy_app_get_graph_key_for_id(i)
            #name = gwy.gwy_name_from_key(key)#(gwy.gwy_app_get_graph_key_for_id(i))
            graph = c[key]
            
            # Get the values in ascii
            # export_ascii(export_units, export_labels, export_metadata, export_style)
            ascii = graph.export_ascii(True,False,True, GRAPH_MODEL_EXPORT_ASCII_PLAIN)
            
            ## make the file string _prof_xx using the Graph title
            prof_title = graph.get_property('title') #ascii[0:10] # the Title of the graph in Gwyddion
            profnr = prof_title[8:10].rstrip(' ') ## only the number in it ('Profile XX'; a space removed for single digit profiles)
            prof_string = '_prof_' + profnr + '_' + str(i) # _prof_xx filestring
            
            ## Print useful data
            ## Very brute ouput
            #print ascii[0:9] # print name of the specific profile in a graph ("Profile XX")
            #print ascii[8] # print only the number XX of it (single digit)
            print '  {}: {}'.format(prof_title,prof_string) # print Graph title and corresponding output filename _prof_xx
            
            
            ## Write the profiles as OriginalFileName_prof_xx.txt
            if write_profiles:
              if only_prof==0 or only_prof==i:
                # Save to text file (name is stmfile + _prof + i)
      		only_prof_str = prof_string # for closing message
                prof_file = stmfile[0:-4] + prof_string + '.txt'
                f= open(prof_file, 'w')
                f.write(ascii)
                f.close()
                
        ## Print closing message
        if write_profiles:
          extramsg = "Writing ascii "#.format(folder)
          if only_prof == 0:
            extramsg += "for all"
          else:
            extramsg += "for " + only_prof_str
        else:
            extramsg = "Only naming."
        print extramsg

    elif len(graphlist) == 0:
        print "Found no graph\n"

    else: # seemingly to manage some unexpected Gwyddion/script error
        print "Found no graph and gwyddion doesn't know it\n"