"""test_classifier.py

This script takes in a command-line argument for the path to a comma-separated value (.csv) file respresenting a testing dataset. This script tests the testing dataset on a decision tree classifier.

The testing dataset (.csv) file must contain at least two columns: 1) a column with the pitch information, and 2) a column with the sex information. The first row of the pitch column must be named 'pitch' and the first row of the sex column must be named 'sex'. The remaining rows of the pitch column contain floating-point numbers representing pitch information in Hertz (Hz) of the speaker. The remaining rows of the sex column contain `0` for male and `1` for female.

This script assumes that there is pickle file (.pickle) in the current working directory named 'clf.pickle' representing the classifier.
"""

import pandas
import pickle
import sys

testing_csv = sys.argv[1]

test_data = pandas.read_csv(testing_csv)

x_test = test_data[["pitch"]]
y_test = test_data[["sex"]]

clf = pickle.load(open("clf.pickle", 'rb'))

test_score = clf.score(x_test, y_test)
print("test score:", test_score)

