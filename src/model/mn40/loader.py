import os
import numpy as np

import librosa
from torch.utils.data import Dataset
import torchaudio

#Import the whole sound dataset




class SoundDataset(Dataset):
  
    def __init__(self, metadata, audio_dir): # class initialization
        self.meta = metadata
        self.audio_dir = audio_dir
        
     # Data Loading

    def __len__(self):          # the size of datasets
        return len(self.meta)

    def __getitem__(self, index):    # fetch the audio samples from the path
        audio_sample_path = self._get_audio_sample_path(index)
        cid=self._get_audio_sample_classID(index)
        signal, sr = librosa.load(audio_sample_path,sr=None)  # same as torchaudio.load, but it loads only 1 channel

        return signal, cid, sr
 
    def _get_audio_sample_path(self,index):   # join the file name with the path name
        path=os.path.join((self.audio_dir),self.meta.iloc[index,1]) #to get complete path 
        return path
    
    def _get_audio_sample_classID(self, index):  # get the label for each audio sample
        return self.meta.iloc[index,3]  # urban
        #return self.meta.iloc[index,2:6] # sonyc