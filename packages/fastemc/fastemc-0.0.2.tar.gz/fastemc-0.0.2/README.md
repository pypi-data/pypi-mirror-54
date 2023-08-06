# FastEMC
### Fast Exponential Monte Carlo

FastEMC is a modified version of exponential Monte Carlo.
FastEMC takes class features and labels as input,
and returns a list of scores and a list of selected features.
The score is based on logistic regression.
Two logistic regression classifiers are used:
1) a fast classifier with limited training,
2) and a slow classifier with full training.

The fast classifier is used to explore feature space rapidly.
Features are occasionaly compared using the slow classifier.
