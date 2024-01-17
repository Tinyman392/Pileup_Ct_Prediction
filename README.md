# Pileup_Ct_Prediction

This repo includes everything required to train an XGBoost model to predict Ct values for COVID-19 genomes based on pileup files.  Pileup files must be produced by the user by following the instructions on the accompanying paper.  

## Repo Contents

The following directories exist in the repo:
- fullCSV: contains a single file, *full_csv.csv* which contains 5 columns: genome ID, sample date, cycle threshold value, instrument for test, and variant code/name.  
- tabularFiles: contains training tabular files that are 2-column, tab-delimited files containing genome ID and cycle threshold value.
- models: pre-trained models from the accompanying paper.

The following files exist in the repo:
- binFeatures.py: file used to bin matrix features into discrete bins.  This is used to reduce the ability of the model to hook onto read depth in a non-binned matrix.  
- init.sh: used to init the repo.  
- makeMatrix.py: builds a matrix based on a directory containing parsed pileup files from the script *parsePileup.py*.  The directory should contain files that follow the following naming pattern *[genome_id].arr.tab*.
- parsePileup.py: takes the name of a pileup file as a command line argument and parses it.  Outputs a single array of values to standard output.  This will be run on all pileup files to train on.  The output from this script should be redirected to a file which should be saved to a single directory with the output file names matching the pattern *[genome_id].arr.tab*.  
- predictNormBin.py: predicts the Ct value for a single pileup file.  Requires a saved model to predict with.  Input to this script is a pileup file, and the model directory.  
- README.md: this file


## Training pipeline

The training pipeline follows a number of steps:
1. Parse the pileup files
2. Generate a matrix from the parsed pileup files
3. Bin the features values in the matrix to generate a training matrix

### Parse the Pileup Files

The *parsePileup.py* script is used to parse the pileup files.  This is a python script that can be run as follows:

``` bash
python parsePileup.py [pileup file]
```

The script is passed a pileup file and parses the file and generates an array of numeric values used for training.  This output is sent to standard output, so you'd want to redirect this output to a file.  These files should all be saved to a single directory and named using the following pattern *[genome_id].arr.tab*.  The *[genome_id]* should match back to the genome IDs in the tabular file used to train (see examples in the *tabularFiles* directory).  

``` bash
python parsePileup.py [pileup file] > [directory name]/[genome_id].arr.tab
```

