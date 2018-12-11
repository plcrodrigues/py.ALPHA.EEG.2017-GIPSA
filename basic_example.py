
from utilities import alphawaves

dataset = alphawaves.AlphaWaves()

subject = 3
epochs = dataset.get_subject_epochs(subject)

fmin = 4; fmax = 20
epochs.filter(fmin, fmax, verbose=False)
epochs.resample(sfreq=128, verbose=False)
ch_picks = ['Oz']
epochs.pick_channels(ch_picks)

from scipy.signal import welch

X_closed = epochs['closed'].get_data()
f, S_closed = welch(X_closed, fs=epochs.info['sfreq'], axis=2)
X_opened = epochs['open'].get_data()
f, S_opened = welch(X_opened, fs=epochs.info['sfreq'], axis=2)

import numpy as np

S_closed = np.mean(S_closed, axis=0).squeeze()
S_opened = np.mean(S_opened, axis=0).squeeze()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(facecolor='white', figsize=(8,6))
ax.plot(f, S_closed, c='k', lw=4.0, label='closed')
ax.plot(f, S_opened, c='r', lw=4.0, label='open')
ax.set_xlim(0, 40)
ax.set_xlabel('frequency', fontsize=14)
ax.set_title('PSD on both conditions (averaged over 5 trials)', fontsize=16)
ax.legend()
fig.show()
