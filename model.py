import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_validate as cv
from sklearn.model_selection import cross_val_score
import matplotlib.pylab as plt
import warnings
from sklearn.model_selection import train_test_split
import pickle

def get_nonstring_cols(data_cols):
	cols_to_keep=[]
	train_cols=[]
	for col in data_cols:
		if col!='URL' and col!='host' and col!='path':
			cols_to_keep.append(col)
			if col!='malicious' and col!='result':
				train_cols.append(col)
	return [cols_to_keep,train_cols]

df=pd.read_csv('url_features.csv')

cols_to_keep,train_cols=get_nonstring_cols(df.columns)
X=df[train_cols]
y=df['malicious']

rf = RandomForestClassifier(n_estimators=150)

rf.fit(X,y)

scores=cross_val_score(rf, X,y , cv=30)

print('Estimated score RandomForestClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))
Pkl_Filename = "my_model.pkl"

#Store model to file
with open(Pkl_Filename, 'wb') as file:
    pickle.dump(rf, file)

'''
#Load model from pickled file
with open(Pkl_Filename, 'rb') as file:
    rf_model = pickle.load(file)

rf_model
'''
