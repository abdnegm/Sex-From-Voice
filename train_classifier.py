"""train_classifier.py

This script takes in a command-line argument for the path to a comma-separated value (.csv) file respresenting the training dataset. This script uses the training dataset to train a decision tree classifier.

The training dataset must contain at least two columns: 1) a column with the pitch information, and 2) a column with the sex information. The first row of the pitch column must be named 'pitch' and the first row of the sex column must be named 'sex'. The remaining rows of the pitch column contain floating-point numbers representing pitch information in Hertz (Hz) of the speaker. The remaining rows of the sex column contain `0` for male and `1` for female.

The classifier is saved in the cwd as a pickle (.pickle) file named 'clf.pickle'. An image of the resulting decision tree is saved in the cwd as 'tree.png'. If there are files named 'clf.pickle' or 'tree.png' in the current working directory, they will be overwritten.
"""

import io
import pandas
import pickle
import pydotplus
import sklearn.model_selection
import sklearn.tree
import sys

training_csv = sys.argv[1]

train_data = pandas.read_csv(training_csv)

x = train_data[["pitch"]]
y = train_data[["sex"]]
x_train, x_validation, y_train, y_validation = sklearn.model_selection.train_test_split(x, y, train_size=0.7, random_state=1)

clf = sklearn.tree.DecisionTreeClassifier(max_depth=1).fit(x_train, y_train)
pickle.dump(clf, open("clf.pickle", 'wb'))

validation_scores = sklearn.model_selection.cross_val_score(clf, x_validation, y_validation)
print("validation_scores:", validation_scores)

dot_data = io.StringIO()
sklearn.tree.export_graphviz(clf,
                             out_file=dot_data,  
                             feature_names=["pitch"],
                             class_names=['M','F'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png("tree.png")

