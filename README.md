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
- README.md: this file.

## Prerequisites

Although this repo on its own has no pre-requisites, the submodule, [GenomicModelCreator](https://github.com/Tinyman392/GenomicModelCreator/tree/f09c2720a249b5031e63545dfc6396ff2ac53280), which is included in the repo has it's own requirements.  

It uses the following tools, Anaconda is recommended to install them using the conda install command:
- numpy ([website](https://numpy.org), [anaconda](https://anaconda.org/anaconda/numpy))
- sklearn ([website](https://scikit-learn.org/stable/), [anaconda](https://anaconda.org/anaconda/scikit-learn))
- scipy ([website](https://www.scipy.org), [anaconda](https://anaconda.org/anaconda/scipy))
- xgboost ([website](https://xgboost.readthedocs.io/en/latest/), [anaconda](https://anaconda.org/conda-forge/xgboost))

## Training pipeline

The training pipeline follows a number of steps:
1. Parse the pileup files
2. Generate a matrix from parsed pileup files
3. Bin the features in the matrix to generate a training matrix
4. Train a model

### Parse the Pileup Files

The *parsePileup.py* script is used to parse the pileup files.  This is a python script that can be run as follows:

``` bash
python parsePileup.py [pileup file]
```

The script is passed a pileup file and parses the file and generates an array of numeric values used for training.  This output is sent to standard output, so you'd want to redirect this output to a file.  These files should all be saved to a single directory and named using the following pattern *[genome_id].arr.tab*.  The *[genome_id]* should match back to the genome IDs in the tabular file used to train (see examples in the *tabularFiles* directory).  

``` bash
python parsePileup.py [pileup file] > [directory name]/[genome_id].arr.tab
```

### Generate a Matrix from Parsed Pileup Files

The *makeMatrix.py* script is used to parse the directory of parsed pileup files (from the *parsePileup.py* script) which follow the naming convention *[genome_id].arr.tab*.  It can be run as follows:

```bash
python makeMatrix.py [parsed pileup directory]
```

The script will go through and find all files that follow the pattern *[genome_id].arr.tab* and output a training matrix to standard output.  This output should be sent to a file like follows:

```bash
python makeMatrix.py [parsed pileup directory] > [matrix file name]
```

### Bin the Features in the Matrix to Generate a Training Matrix

Although the matrix created from *makeMatrix.py* can be used to train a model from, the model will be able to hook onto the read depth from that matrix.  It can unfairly train the model to a higher accuracy due to this.  The *binFeatures.py* script is used to mitigate this.  It can be run as follows:

```bash
python binFeatures.py [matrix file name]
```

Like the other scripts, the output is sent to standard output.  This should be redirected to a file which will be trained on.  

```bash
python binFeatures.py [matrix file name] > [binned matrix file name]
```

### Train a Model

The *buildModel.py* script in the [*GenomicModelCreator*](https://github.com/Tinyman392/GenomicModelCreator/tree/f09c2720a249b5031e63545dfc6396ff2ac53280) submodule is used to train the models to produce XGBoost models.  You can train a model with the following:

```bash
python PATH/TO/GenomicModelCreator/buildModel.py -t [tabular file] -o [output model directory] -T [temp directory] -n [threads] -W False -B [binned matrix file name]
```

The *tabular file* is a two-column, tab-delimited file containing genome ID and cycle threshold, the *tabularFiles* directory in this repo contains the the files used for the accompanying paper.  

The *output model directory* is the name of the model directory for the script to output.  This will be used as input into the *predictNormBin.py* script used to make predictions on new pileups.  If the directory is non-empty, it will be emptied.  

The *temp directory* is a temporary directory for the script to use.  If the directory is non-empty, it will be emptied.  

The *threads* is the number of threads to train with.  XGBoost allows you to train using multiple threads; it makes the training faster if you have the compute to do it.  

The *binned matrix file name* is the name of the matrix file created from the *binFeatures.py* script.  

## Predicting on New Pileup Files

The *predictNormBin.py* script is used to make predictions on new pileup files.  It can be run as follows:

```bash
python predictNormBin.py [pileup file] [model directory]
```

It takes two inputs, the pileup file to use to predict with and the model directory output from the *buildModel.py* script in the (*GenomicModelCreator*)[https://github.com/Tinyman392/GenomicModelCreator/tree/f09c2720a249b5031e63545dfc6396ff2ac53280] submodule.  
