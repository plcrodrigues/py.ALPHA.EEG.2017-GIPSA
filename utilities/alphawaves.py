import mne
import numpy as np
import os
import glob
import zipfile
import yaml
from utilities import download as dl
from scipy.io import loadmat

ALPHAWAVES_URL = 'https://sandbox.zenodo.org/record/255797/files/'

class AlphaWaves():
    '''
    '''

    def __init__(self):

        self.subject_list = range(1, 20+1)

    def get_subject_epochs(self, subject):
        """return data for a single subject"""

        file_path_list = self.data_path(subject)
        for filepath in file_path_list:

            # load the .mat and reshape it for becoming an epochs object instance
            data = loadmat(filepath)
            Xop = data['OPEN'].T
            Xcl = data['CLOSE'].T
            X = np.concatenate([Xop, Xcl])

            ch_names = ['FP1', 'FP2', 'FC5', 'AFz', 'FC6', 'T7', 'Cz', 'T8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'O1', 'Oz', 'O2']
            ch_types = ['eeg'] * len(ch_names)
            info = mne.create_info(ch_names=ch_names, sfreq=512, ch_types=ch_types, montage='standard_1020')

            event_id = {'open':1, 'closed':2}
            events = [[i*5120, 0, 1] for i in np.arange(5)] + [[i*5120, 0, 2] for i in 5+np.arange(5)]
            
            events = np.stack(events)
            epochs = mne.EpochsArray(X, info=info, event_id=event_id, events=events, verbose=False)

        return epochs

    def data_path(self, subject, path=None, force_update=False,
                  update_path=None, verbose=None):

        if subject not in self.subject_list:
            raise(ValueError("Invalid subject number"))

        #check if has the .zip
        url = '{:s}subject{:02d}.mat'.format(ALPHAWAVES_URL, subject)
        file_path = dl.data_path(url, 'ALPHAWAVES')

        return [file_path]
