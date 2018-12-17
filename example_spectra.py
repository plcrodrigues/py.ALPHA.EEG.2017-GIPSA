from scipy.signal import welch
from utilities import alphawaves
import matplotlib.pyplot as plt
import numpy as np
import mne
"""
================================
Spectral analysis of the trials
================================

This example shows how to extract the epochs from the dataset of a given
subject and then do a spectral analysis of the signals. The expected behavior
is that there should be a peak around 10 Hz for the 'closed' epochs, due to the
Alpha rhythm that appears when a person closes here eyes.

"""
# Authors: Pedro Rodrigues <pedro.rodrigues01@gmail.com>
#
# License: BSD (3-clause)

import warnings
warnings.filterwarnings("ignore")


# define the dataset instance
dataset = alphawaves.AlphaWaves()

# get the data from subject of interest
subject = 1
raw = dataset.get_subject_epochs(subject)

# filter data and resample
fmin = 3
fmax = 40
raw.filter(fmin, fmax, verbose=False)
raw.resample(sfreq=128, verbose=False)

# detect the events and cut the signal into epochs
events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
event_id = {'closed': 1, 'open': 2}
epochs = mne.Epochs(raw, events, event_id, tmin=2.0, tmax=8.0, baseline=None,
                    verbose=False)
epochs.load_data().pick_channels(['Oz'])

# estimate the averaged spectra for each condition
X_closed = epochs['closed'].get_data()
f, S_closed = welch(X_closed, fs=epochs.info['sfreq'], axis=2)
S_closed = np.mean(S_closed, axis=0).squeeze()
X_opened = epochs['open'].get_data()
f, S_opened = welch(X_opened, fs=epochs.info['sfreq'], axis=2)
S_opened = np.mean(S_opened, axis=0).squeeze()

# plot the results
fig, ax = plt.subplots(facecolor='white', figsize=(8, 6))
ax.plot(f, S_closed, c='k', lw=4.0, label='closed')
ax.plot(f, S_opened, c='r', lw=4.0, label='open')
ax.set_xlim(0, 40)
ax.set_xlabel('frequency', fontsize=14)
ax.set_title('PSD on both conditions (averaged over 5 trials)', fontsize=16)
ax.legend()
fig.show()
