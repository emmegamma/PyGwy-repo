# PyGwy repository

This repository is intended as a collection of **Gwyddion PyGwy scripts**: [some that I made](#scripts-in-this-repository) and those that I [found on GitHub](#scripts-available-on-github).

If you want to contribute by adding suggestions, scripts, or in any other form, or simply would like your link added/removed, you can file an Issue or **contact me** at: emmegamma [at] inventati *dot* org.

For more information about Gwyddion and PyGwy, see the [official documentation](http://gwyddion.net/documentation/user-guide-en/pygwy.html). See below for [Pygwy installation instructions](#pygwy-installation).

# Scripts in this repository

Currently the scripts available are: [SXM_searchFiles](#sxm_searchfiles), [batch_export_to_image](#batch_export_to_image), and [export_profiles](#export_profiles).

### SXM_searchFiles
This script is intended for **searching files** and **filtering according to some properties** (filename, real image size, setpoint, scantime, comments) through one or multiple folders. It can be useful e.g. when scraping through old data.

It is designed for **Nanonis .SXM** files, also after saving them as .gwy, but can be easily adapted to other formats (in this case, **you can email me to ask or send the final result**: I'd love to make a full search function of this)

It can also:
- Search recursively through folders (by using `\*` and escape characters in the folder search)
- Copy the files to a target folder (this can be useful when searching recursively, to collect all files/images in one place for a later check)
- Customize output (print filename, setpoint, size/speed, etc.)

The first part of the file contains the options/customizations available, with comments that should make them understandable:
```python
### Folder and filetype ###
# Set folder(s) to search (use *\* for recursive searches) 
# and filetype (uncomment as needed)
folder = r'C:\Users\Myuser\DATA\STM\2024-10-*'
#filetype = '.gwy' 
filetype = '.sxm' 
#filetype = 'both' 
```

The script can also run as standalone in Python, the required libraries are loaded in the first lines of the file (make sure Gwyddion's install folder corresponds in your system)

### batch_export_to_image
A script to batch export .gwy (or .sxm) files in a folder to images, inspired by kugatomodai/gwyddion_convert_many_files (see below in the repo list). 

The filetype/extension of the images is `.jpg` by default but can be changed in variable `imagefile`, line 76.

It can filter filenames (similar to the script above), and has options to overwrite/not overwrite and for dry run (ultrasafe).

### export_profiles
My very first script: to **export all the profiles** (Graphs) in open files **to ASCII .txt files**. Intended for import in another program (IgorPro or similar).

It works with open files only, either recursively (all open files) or the active one. The profiles are exported as OriginaleFilename_prof_xx.txt


# Scripts available on GitHub
I've collected some links here for ease of use, with no intention to steal anyone's credits. You can also do a 'pygwy' search in GitHub, but I filtered out the unfinished/unclear projects. Note that, unless otherwise stated, they are **untested**.
- [harripj/pygwy](https://github.com/harripj/pygwy): a series of scripts, seemingly to batch-apply 'basic' Gwyddion operations (Median level, Gaussian filter, etc.)
- [Madhavanlabcode/Gwyddion-Scripts](https://github.com/Madhavanlabcode/Gwyddion-Scripts): three-fold symmetrization of an image (intended for FFT)
- [onakanob/PyGwyBatch](https://github.com/onakanob/PyGwyBatch): a batch handler to apply a single PyGwy/Python function to multiple files
- [Drilack7/Python-Scripts-for-Gwyddion](https://github.com/Drilack7/Python-Scripts-for-Gwyddion): different scripts for
  - batch flattening and mean depth calculation 
  - creating a collage of images
  - simple batch operations (change Color scale, Scale min/max, or Level)
  - file actions (Open all files in a folder, Save all files in a folder to .gwy, etc.)
- [kugatomodai/gwyddion_convert_many_files](https://github.com/kugatomodai/gwyddion_convert_many_files): batch conversion of files in a folder to png (not working and using deprecated methods, use only for inspiration)
- [wampiter/gwyscripts](https://github.com/wampiter/gwyscripts): batch image processing scripts to
  - export files in a folder to .gwy+png, sorted by channel
  - stitch images in a line
  - save all open files to a folder, with a png too
- [TomVincentUK/gwy2py](https://github.com/TomVincentUK/gwy2py): a script to export Gwyddion data to numpy (.npy) files

If you want your script removed from this list (or added!), please contact me


# PyGwy installation

### Windows
To install PyGwy correctly on Windows, follow the official [documentation](http://gwyddion.net/documentation/user-guide-en/installation-ms-windows.html). You can also find the needed installers and short instructions in the **Python 2 dependencies** folder. The installers are also available [on gwyddion's repository](https://sourceforge.net/projects/gwyddion/files/pygtk-win32/).

### Linux
Instructions vary depending on the distribution, especially since Python 2 is outdated.
The easiest way (and at least in latest Ubuntu versions, the only one I know of) is to install [Gwyddion's FlatPak](https://flathub.org/apps/net.gwyddion.Gwyddion) (see [forum discussion](https://sourceforge.net/p/gwyddion/discussion/pygwy/thread/24a071efea/))

 If you have instructions for a specific distribution, file an Issue or drop an email at the address indicated above and I'll add them.
