#%%
from loader import SoundDataset
from prep import ProcessedDataset
import pandas as pd
import torch.nn.functional as F
import torch
import numpy as np
from torch.nn import BCELoss
from audiomentations import AddBackgroundNoise
import librosa


s1,sr1=librosa.load('urban_sound_8k/data/6988-5-0-0.wav',sr=None)

s2,sr2=librosa.load('urban_sound_8k/data/22601-8-0-2.wav',sr=None)


import soundfile as sf
s2[0:len(s1)]+s1

sf.write('s3.wav', s2[0:len(s1)]+s1, sr1)