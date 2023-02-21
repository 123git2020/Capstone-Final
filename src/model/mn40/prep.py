# process the raw audio data, make them have unified sampling rate
# get their mel-spectrograms


from audiomentations import *
import os
import numpy as np

import librosa
from torch.utils.data import Dataset, DataLoader, ConcatDataset, random_split
import torchaudio
import torch


class ProcessedDataset(Dataset):

     def __init__(self, rawdata,mask): # class initialization
        self.data = rawdata    
        self.mask=mask

     def __len__(self):          # the size of datasets
        return len(self.data)


     def __getitem__(self, index):    # processing
        cid=self.data[index][1]
        sr=self.data[index][2]
        sig=self._resampling(self.data[index][0], sr)
        sig=self._length_adjust(sig, 20500)
        #mel_spec=self._get_melspec(sig,20500)
        return sig[None,:], int(cid)    # make sound-data 2d array


     def _resampling(self, signal, sr):          # resample the signal if the sampling frequency doesn't match
        if sr!= 20500 :          
            res_sig=librosa.resample(signal,sr,20500)
        else:
            res_sig=signal
        return res_sig

     
     def _length_adjust(self, signal,sr):
        if 0 < len(signal):                                          # workaround: 0 length causes error
              data, _ = librosa.effects.trim(signal) # trim, top_db=default(60)
        
        # make it unified length to 4 second
        if len(signal) > sr*4:     # long enough
             signal = signal[0:0+sr*4]

        elif len(signal) < sr*4:       # repeat itself until 4 second
             repts = int(sr*4/len(signal))
             rem=sr*4%len(signal)
             signal=np.append(np.tile(signal,repts),signal[0:rem])
        return signal


    