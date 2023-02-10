# Generic imports
import sys
from datetime import datetime
import torch, torchaudio, timm
import librosa
import numpy as np
from torch.cuda.amp import autocast
import IPython
import soundfile as sf
import pandas as pd
from dotenv import dotenv_values
import glob
import os
import math

# Recording imports
import sounddevice as sd
from scipy.io.wavfile import write
import pydub

# Classification model imports
sys.path.insert(0, 'C:\Users\Jeremy\capstone-final\src\database')
sys.path.insert(0, 'C:\Users\Jeremy\capstone-final\src\model/beats')
sys.path.insert(0, 'C:\Users\Jeremy\capstone-final\src\metrics')

import BEATs_eval
import DBInterface
import calculate_metrics

AUDIO_LENGTH = 2

if __name__ == '__main__':
    # initial values
    env = dotenv_values('.env')
    db = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    
    # Recording loop
    while(True):
        fs = 44100  # Sample rate
        duration = 2  # Duration of recording
        threshold = -10 #dB

        # Record audio
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished

        # Convert to pydub audio segment
        channel1 = recording[:,0]
        audio_segment = pydub.AudioSegment(
            channel1.tobytes(), 
            frame_rate=fs,
            sample_width=channel1.dtype.itemsize, 
            channels=1
        )
        
        # Calculate dBFS (dBFS is dB relative to the maximum possible loudness)
        max_loudness = audio_segment.max_dBFS
        average_loudness = audio_segment.dBFS

        print("Peak ({}s):".format(duration), max, "dB. Threshold is", threshold, "dB.")

        if(max_loudness > threshold): # Proceed to analyze audio

            # Get timestamp
            timestamp = datetime.now()
            
            # Write to file 
            fileName = timestamp.strftime('%Y%m%d%H%M%S')
            fname = f'{fileName}.wav'
            write('audio/{}.wav'.format(fileName), fs, recording)
            print("\nWRITTEN TO FILE\n")

            # Calculate metrics - LAeq, LAmax, LCpeak, TWA, etc
            LAeq, LAmax, LCpeak, twa = calculate_metrics(sig=recording, audio_segment=audio_segment, sr=fs, n=4096)
            
            # change sampling rate to 16 khz before passing into BEATs
            data_path = '/src/demo/audio'
            list_of_files = glob.glob(data_path)
            latest_file = max(list_of_files, key=os.path.getctime)
            audio_path = data_path + f'/{latest_file}'
            data, sr = librosa.load(audio_path, sr=None)
            fname=librosa.resample(data,sr,16000)
            
            # Classification - BEATs
            BEATs_model = BEATs_eval()
            top5_label, top5_label_prob = BEATs_model.predict(fname)
            labels = []
            for i, label in enumerate(top5_label):
                if top5_label_prob[i] >= 0.6:
                    labels.append(label)
            
            # Database
            db.insert_audio_frag(timestamp, AUDIO_LENGTH, audio_path, LAeq, LAmax, LCpeak, twa, labels)