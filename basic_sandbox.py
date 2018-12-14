
import mne
import numpy as np
import matplotlib.pyplot as plt

from scipy.io import loadmat
from scipy.signal import welch

subject_list = list(range(7)) + list(range(8, 20+1))

for subject in subject_list:

    filepath = '/localdata/coelhorp/Datasets/alphawaves/alpha/zenodo/subject_' + str(subject).zfill(2) + '.mat'

    data = loadmat(filepath)

    S = data['SIGNAL'][:,1:17]
    stim_close = data['SIGNAL'][:,17]
    stim_open = data['SIGNAL'][:,18]
    stim = 1*stim_close + 2*stim_open

    chnames = ['Fp1','Fp2','Fc5','Fz','Fc6','T7','Cz','T8','P7','P3','Pz','P4','P8','O1','Oz','O2','stim']
    chtypes = ['eeg'] * 16 + ['stim']
    X = np.concatenate([S, stim[:,None]], axis=1).T

    sfreq = 512
    info = mne.create_info(ch_names=chnames, sfreq=512, ch_types=chtypes, montage='standard_1020')
    raw = mne.io.RawArray(data=X, info=info)
    raw.filter(l_freq=4, h_freq=30)
    raw.resample(sfreq=128)

    events = mne.find_events(raw=raw, shortest_event=1)
    event_id = {'closed':1, 'open':2}
    epochs = mne.Epochs(raw, events, event_id, tmin=2.0, tmax=8.0, baseline=None)
    epochs.load_data().pick_channels(['Oz'])

    fig, ax = plt.subplots(facecolor='white', figsize=(9.2,7.4))
    f, S = welch(epochs.get_data(), fs=epochs.info['sfreq'], axis=2)
    colors = {1:'b', 2:'r'}
    for Si, yi in zip(S, epochs.events[:,-1]):
        ax.plot(f, 20*np.log10(Si.squeeze()), color=colors[yi], lw=2.0)
    for event in event_id.keys():
        ax.plot([], color=colors[event_id[event]], label=event)
    ax.set_xlim(8,16)
    ax.set_ylim(-90, 50)
    ax.set_title('subject ' + str(subject).zfill(2), fontsize=16)
    fig.legend()

    filename = 'psd_subject_' + str(subject).zfill(2) + '.pdf'
    fig.savefig(filename, format='pdf')
    fig.clf()
