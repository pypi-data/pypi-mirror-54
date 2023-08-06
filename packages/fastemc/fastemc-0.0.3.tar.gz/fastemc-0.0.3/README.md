# FastEMC
### Fast Exponential Monte Carlo

FastEMC is a method for dimensionality reduction.
FastEMC was designed for datasets with a small number of samples,
and a large number of features.
This version of FastEMC can only handle numerical features,
and binary classification of samples.
FastEMC can be installed using pip
```
$ pip install fastemc
```
If pip fails on windows try installing scikit-learn manually using conda,
then install fastemc using pip.
You can interact with FastEMC directly using the python module
```
>>> import fastemc
>>> scores, clusters = fastemc.run(features, labels, **kwargs)
```
or through the command line
```
$ python -m fastemc --features features.csv --labels labels.csv
```
The features.csv and labels.csv files can be generated using pandas, e.g.,
```
>>> labels.to_csv("labels.csv")
>>> features.to_csv("features.csv")
```
where labels and features are pandas dataframes with the same index.

FastEMC outputs a list of feature clusters.
The size of each cluster and the number of clusters to collect are optional parameters.
Each cluster is also given a score.
The score is based on k-fold cross-validation of a logistic regression classifier using only features in the cluster.


When using FastEMC in published works, please cite the original manuscript 
and the author of the software:

[1] Stackhouse, C.T.; Rowland, J.R.; Shevin, R.S.; Singh, R.; Gillespie, G.Y.; Willey, C.D. A Novel
Assay for Profiling GBM Cancer Model Heterogeneity and Drug Screening. Cells 2019, 8, 702. (https://www.ncbi.nlm.nih.gov/pubmed/31336733)

[2] Rowland, J.R. FastEMC. 2019. (https://github.com/rowland-208/fastemc)