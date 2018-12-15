"""
=============================
Classification of the trials
=============================

This example shows how to extract the epochs from the dataset of a given subject
and then classify them using Machine Learning techniques using Riemannian Geometry

The code also creates a figure with the spectral embedding of the epochs

"""
# Authors: Pedro Rodrigues <pedro.rodrigues01@gmail.com>
#
# License: BSD (3-clause)

import warnings
warnings.filterwarnings("ignore")

import mne
import numpy as np
import matplotlib.pyplot as plt

from utilities import alphawaves
from scipy.signal import welch

from pyriemann.estimation import Covariances
from pyriemann.classification import MDM
from pyriemann.embedding import Embedding

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline

# define the dataset instance
dataset = alphawaves.AlphaWaves()

# get the data from subject of interest
subject = dataset.subject_list[2]
raw = dataset.get_subject_epochs(subject)

# filter data and resample 
fmin = 3; fmax = 40
raw.filter(fmin, fmax, verbose=False)
raw.resample(sfreq=128, verbose=False)

# detect the events and cut the signal into epochs
events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
event_id = {'closed':1, 'open':2}
epochs = mne.Epochs(raw, events, event_id, tmin=2.0, tmax=8.0, baseline=None, verbose=False)

# get trials and labels
X = epochs.get_data()
y = events[:,-1]

# cross validation
skf = StratifiedKFold(n_splits=5)
clf = make_pipeline(Covariances(estimator='lwf'), MDM())
scr = cross_val_score(clf, X, y, cv=skf)

# print results of classification
print('subject', subject)
print('mean accuracy :', scr.mean())

# get the spectral embedding of the epochs
C = Covariances(estimator='lwf').fit_transform(X)
emb = Embedding(metric='riemann').fit_transform(C)

# scatter plot of the embedded points
fig, ax = plt.subplots(facecolor='white', figsize=(5.6,5.2))
colors = {1:'r', 2:'b'}
for embi, yi in zip(emb, y):
	ax.scatter(embi[0], embi[1], s=120, c=colors[yi])
labels = {1:'closed', 2:'open'}	
for yi in np.unique(y):
	ax.scatter([], [], c=colors[yi], label=labels[yi])	
ax.set_xticks([-1, -0.5, 0.0, +0.5, 1.0])	
ax.set_yticks([-1, -0.5, 0.0, +0.5, 1.0])	
ax.legend()
ax.set_title('Spectral embedding of the epochs from subject ' + str(subject), fontsize=10)
fig.show()
