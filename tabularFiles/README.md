# Tabular Files

This directory contains the tabular files that were used to train the models in the models directory.  There are a handful of tabular files here:
- gidCt.alinity.tab: only contains Alinity Ct values
- gidCt.cepheid.tab: only contains Cepheid Ct values
- gidCt.HL.tab: contains all Ct values that are binned into either high (>36) and low (<24).  Highs are denoted as 4 while lows are denoted as 1 (for compatiblity with the [*GenomicModelCreator*](https://github.com/Tinyman392/GenomicModelCreator/tree/f09c2720a249b5031e63545dfc6396ff2ac53280) submodule)
- gidCt.panther.tab: only contains Panther Ct values
- gidCt.tab: contains all Ct values

There is an additional directory named *omicronTabs* which contains tabular files for the experiments where we increased the number of omicron genomes within the training set.  Each file follows the pattern of om.[percent omicron].[num omicron].tab where *percent omicron* is the percentage of omicron genomes in the file in decimal form while *num omicron* is the number of omicron genomes in the file.