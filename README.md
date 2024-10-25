# PyGwy repository

This repository is intended as a collection of Gwyddion PyGwy scripts available in GitHub (and possibly elsewhere).

For more information about Gwyddion and PyGwy, see the official [Gwyddion website](http://gwyddion.net) and [documentation](http://gwyddion.net/documentation/user-guide-en/pygwy.html).

If you find any bugs/issues, feel free to contact me.


# PyGwy installation

### Windows
To install PyGwy correctly on Windows, follow the official [documentation](http://gwyddion.net/documentation/user-guide-en/installation-ms-windows.html). The needed installers (and short instructions) are available in the **Python 2 dependencies** folder in this repo.

### Linux
Instructions may vary depending on the distribution, especially since Python 2 is outdated.
The easiest way (and at least in latest Ubuntu versions, the only one I know) is to install [Gwyddion's FlatPak](https://flathub.org/apps/net.gwyddion.Gwyddion) ([ref.](https://sourceforge.net/p/gwyddion/discussion/pygwy/thread/24a071efea/))


# Scripts available

Currently there's only 2, quite basic scripts available: [SXM_searchFiles](sxm_searchfiles) and [export_profiles](export_profiles).

### SXM_searchFiles
This script is intended for searching files and filtering according to some properties (filename, real image size, setpoint, scantime, comments) through one or multiple folders. It can be useful e.g. when scraping through old data.

It is designed for Nanonis .SXM files, also after saving them as .gwy, but can be easily adapted to other formats.

Also it can:
- Search recursively through folders (by using `*` in the folder search)
- Copy the files found to a different folder
  - this can be useful when searching recursively for a specific image or set of images, e.g. an overview for a presentation/publication or all images of - say - defects available, to collect them in one place for a later check
- Customize output (print filename, setpoint, size/speed, etc.)

It uses package [quantities](https://pypi.org/project/quantities/) to convert units, though it can be scraped out. Note that `pip` seemingly tries to install v.0.13 which gives an error, so I suggest trying v. 0.12:

`python -m pip install quantities==0.12`

The first part of the file contains the options/customizations available, with comments that should make them understandable
```
### Folder and filetype ###
# Set folder(s) to search (use *\* for recursive searches) 
# and filetype (uncomment as needed)
folder = r'C:\Users\Myuser\DATA\STM\*\2024*'
#filetype = '.gwy' 
filetype = '.sxm' 
#filetype = 'both' 
```

The script can also run as standalone in Python, the required libraries are loaded in the first 3 lines of the file

### export_profiles
My very first script: used to export the profiles (Graphs) in ASCII .txt files.
I needed it for a very tedious job which hopefully nobody else has to ever do, but it may come useful as codebase/to export many profiles to import in another program (Igor or similar).

It works with open files only, either recursively (all open files) or the active one. It exports the profiles as OriginaleFilename_prof_xx.txt
