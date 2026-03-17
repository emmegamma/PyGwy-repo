# PyGwy repository

This repository is intended as a collection of **Gwyddion PyGwy scripts**: some [that I made](#scripts-in-this-directory) and some [contributed/available on the web](#scripts-repository) (GitHub).

If you want to contribute by adding scripts, suggestions, or in any other form (or would like your link removed!), you can contact me (emmegamma [at] inventati *dot* org) or file an Issue.

For more information about Gwyddion and PyGwy, see the [official documentation](http://gwyddion.net/documentation/user-guide-en/pygwy.html). See below for [Pygwy installation instructions](#pygwy-installation).

# Scripts in this directory

Currently three scripts are available: [SXM_searchFiles](#sxm_searchfiles), [batch_export_to_image](#batch_export_to_image), and [export_profiles](#export_profiles).

### SXM_searchFiles
This is intended for **searching files and filtering** according to some properties (filename, real image size, setpoint, scantime, comments), through one or multiple folders. It can be useful e.g. when scraping through old data.

It can:
- Search recursively through folders (by using `\*` and escape characters in the folder search)
- Copy the files to a target folder (this can be useful when searching recursively, to collect all files/images in one place for a later check)
- Customize output (print filename, setpoint, size/speed, etc.)

It is designed for Nanonis .SXM files/metadata (so also after saving them as .gwy), but **can be adapted** to other formats (I have never needed this, but if you do, I'd be glad to hear about it: I'd like to make it into a 'modular' search script)

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

The script can also run as standalone in Python, the required libraries are loaded in the first lines of the file (make sure Gwyddion's install folder is correct for your system)

### batch_export_to_image
A script to export .gwy (or .sxm) files in a folder to images, inspired by kugatomodai/gwyddion_convert_many_files (see below in the repo list). 

The filetype/extension of the images is `.jpg` by default (customize variable `imagefile`, line 76).

It can filter filenames (similar to the script above), and has options to overwrite/not overwrite and for dry run (ultrasafe).

### export_profiles
My very first script: to export all the profiles (Graphs) in open files to ASCII .txt files. Intended for export to some other program (IgorPro or similar).

It works with open files only, either recursively (all open files) or the active one. The profiles are exported as OriginaleFilename_prof_xx.txt


# Scripts repository
Here are some scripts contributed by other authors and some that I've collected for ease of use, with no intention to steal anyone's credits (it's mostly the result of a 'pygwy' search in GitHub after discarding obsolete projects). If you want your script added to (or removed from) this list, feel free to contact me.

Note: they are **untested** unless otherwise stated

### Contributed
- [MohamedAzizAllani/AutoProcess_plugin-Gwyddion](https://github.com/MohamedAzizAllani/AutoProcess_plugin-Gwyddion): a full, great plugin equipped with GUI to apply several operations (color gradient and range, crop, renaming, or even custom macros) to a series of files or channels to be selected. 
<br> Tested and working on Gwyddion 2.69
- [rohanplatts/Python-in-Gwyddion](https://github.com/rohanplatts/Python-in-Gwyddion): not really PyGwy, but a very useful tool: a Gwyddion module that executes any python script in any python environment of your choice (e.g. installed with conda/anaconda: so also python 3), in Gwyddion. The script is executed on the open image, and reads the output back in Gwyddion. It's compiled for Windows 64bit only, but that means having some python available also in 64bit installations
- [rohanplatts/nanonis-file-conversion](https://github.com/rohanplatts/nanonis-file-conversion): also not really, but possibly useful: scripts to convert Nanonis .dat files (human-readable) to both .sxm (Gwyddion-readable) and .jpg


### Other scripts in GitHub
- [harripj/pygwy](https://github.com/harripj/pygwy): a series of scripts, seemingly to batch-apply 'basic' Gwyddion operations (Median level, Gaussian filter, etc.)
- [Madhavanlabcode/Gwyddion-Scripts](https://github.com/Madhavanlabcode/Gwyddion-Scripts): three-fold symmetrization of an image (intended for FFT)
- [onakanob/PyGwyBatch](https://github.com/onakanob/PyGwyBatch): a batch handler to apply a single PyGwy/Python function to multiple files
- [Drilack7/Python-Scripts-for-Gwyddion](https://github.com/Drilack7/Python-Scripts-for-Gwyddion): different scripts for
  - batch flattening and mean depth calculation 
  - creating a collage of images
  - simple batch operations (change Color scale, Scale min/max, or Level)
  - file actions (Open all files in a folder, Save all files in a folder to .gwy, etc.)
- [kugatomodai/gwyddion_convert_many_files](https://github.com/kugatomodai/gwyddion_convert_many_files): batch conversion of files in a folder to png. 
<br> Not working and using deprecated methods, use only for inspiration
- [wampiter/gwyscripts](https://github.com/wampiter/gwyscripts): batch image processing scripts to
  - export files in a folder to .gwy+png, sorted by channel
  - stitch images in a line
  - save all open files to a folder, with a png too
- [TomVincentUK/gwy2py](https://github.com/TomVincentUK/gwy2py): a script to export Gwyddion data to numpy (.npy) files


# PyGwy installation

### Windows
To install PyGwy correctly on Windows, follow the official [documentation](http://gwyddion.net/documentation/user-guide-en/installation-ms-windows.html). You can also find the needed installers and short instructions in the **Python 2 dependencies** folder. The installers are also available [on gwyddion's repository](https://sourceforge.net/projects/gwyddion/files/pygtk-win32/). Note that you need Gwyddion 32bit for PyGwy to work (not available in the 64bit installation).

### Linux
Instructions vary depending on the distribution, especially since Python 2 is outdated.
The easiest way (and at least in latest Ubuntu versions, the only one I know of) is to install [Gwyddion's FlatPak](https://flathub.org/apps/net.gwyddion.Gwyddion) (see [forum discussion](https://sourceforge.net/p/gwyddion/discussion/pygwy/thread/24a071efea/))

 If you have instructions for a specific distribution, file an Issue or drop an email at the address indicated above and I'll add them.
