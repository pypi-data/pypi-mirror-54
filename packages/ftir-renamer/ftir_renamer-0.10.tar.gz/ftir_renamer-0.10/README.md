FTIR File Renamer
==============
### Introduction

Renames files from the FTIR based on strict naming scheme

### Virtual Environment

Activate your FTIR renamer virtual environment

`source ftir_rename/bin/activate`

If that does not work, your environment may not exist. Create it as follows:

```
python3 -m venv ftir_rename
source ftir_rename/bin/activate
```

### Installation

From the command line in the folder in which you would like to install the program:

`pip install ftir_renamer`

### Upgrade

`pip install --upgrade ftir_renamer`

### Requirements
- Unix-like environment
- Spreadsheet of FTIR-related metadata (with .XLSX extension)
- The .spc output files corresponding to the FTIR IDs in the spreadsheet


## ftir_rename

Shell script automating the renaming of files from a USB stick

### Required Argument

```
-f
The absolute path to the folder containing the .spc files. Note that either this folder or its parent must contain an Excel file named FTIR.XLSX 
that contains all the required metadata for renaming.

```

### Optional Argument

```
-c
Use the "classic method of renaming the files: 
Original File Name: FTIR0182-1_2017-05-26T11-13-47.spc
New File Name: GN_Klebsiella_BHI_AN_CFIA_FTIR0182_C2_2017_May_26_CA01_OLC0027_2017-05-26T11-13-47.spc
```

### Running

##### Example command to run the script

`ftir_rename -f /path/to/FTIR_files`

## renamer.py

Python script that renames .spc files

### Required Arguments

```
-s
The path of the folder containing the FTIR output files
-f 
Absolute path to the spreadsheet containing the FTIR metadata
-o
The absolute path of the folder to store the renamed files
```

### Running 

##### Example command to run the script

`renamer.py -f /path/to/FTIR.xlsx -s /path/to/files -o /path/to/outputs`
    
##### Usage

```
usage: renamer.py [-h] -s SPECTRA_PATH -f FILENAME -o OUTPUTPATH

Rename files for FTIR experiments using strict naming scheme

  -h, --help            show this help message and exit
required arguments:
  -s SPECTRA_PATH, --sequencepath SPECTRA_PATH
                        Path of .spc files to process.
  -f FILENAME, --filename FILENAME
                        Name of .xls(x) file with renaming information. Must
                        conform to agreed upon format. This file must be in the
                        supplied sequencepath.
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Optionally specify the folder in which the renamed
                        files are to be stored. Provide the full path e.g.
                        /path/to/output/files
```
