import mne
import numpy as np
import os
import glob
import zipfile
import yaml
from utilities import download as dl
from scipy.io import loadmat

ALPHAWAVES_URL = 'https://sandbox.zenodo.org/record/256020/files/'

class AlphaWaves():
    '''
    '''

    def __init__(self):

        self.subject_list = list(range(7)) + list(range(8, 20+1))

    def get_subject_epochs(self, subject):
        """return data for a single subject"""        

        file_path_list = self.data_path(subject)
        for filepath in file_path_list:

            data = loadmat(filepath)

            S = data['SIGNAL'][:,1:17]
            stim_close = data['SIGNAL'][:,17]
            stim_open = data['SIGNAL'][:,18]
            stim = 1*stim_close + 2*stim_open

            chnames = ['Fp1','Fp2','Fc5','Fz','Fc6','T7','Cz','T8','P7','P3','Pz','P4','P8','O1','Oz','O2','stim']
            chtypes = ['eeg'] * 16 + ['stim']
            X = np.concatenate([S, stim[:,None]], axis=1).T

            sfreq = 512
            info = mne.create_info(ch_names=chnames, sfreq=512, 
                                   ch_types=chtypes, montage='standard_1020', verbose=False)
            raw = mne.io.RawArray(data=X, info=info, verbose=False)

        return raw

    def data_path(self, subject, path=None, force_update=False,
                  update_path=None, verbose=None):

        if subject not in self.subject_list:
            raise(ValueError("Invalid subject number"))

        #check if has the .zip
        url = '{:s}subject_{:02d}.mat'.format(ALPHAWAVES_URL, subject)
        file_path = dl.data_path(url, 'ALPHAWAVES')

        return [file_path]
