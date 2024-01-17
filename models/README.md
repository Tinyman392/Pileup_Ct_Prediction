# Models

This directory contains models that were trained for the accompanying paper.  It contains 4 models in this directory:
- model_alinity
- model_all
- model_cepheid
- model_panther

These are the models for their respective instruments while model_all contains models trained on all instruments.  

There is also an additional directory named omicronModels which contain 6 models that are trained with increasing amounts of omicron genomes.  The model names follow the following pattern: *om.[percent omicron].[num omicron].model.  *Percent omicron* is the percentage of omicron genomes (in decimal format) used in the training data while *num omicron* is the number of omicron genomes used in the training data.  