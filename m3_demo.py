# Generic imports
from datetime import datetime
import numpy as np
import librosa
import os
from dotenv import dotenv_values
import warnings
warnings.filterwarnings("ignore")

# Recording imports
import sounddevice as sd
from scipy.io.wavfile import write
import pydub
import soundfile as sf

from src.model.beats.BEATs_eval import BEATs_eval
from src.database.DBInterface import DBInterface
from src.metrics.calculate_metrics import calculate_metrics

AUDIO_LENGTH = 2
PROBABILITY_THRESHOLD = 0.6
DB_THRESHOLD = -10
DURATION = 2                    # Duration of recording

# isolatePeak(audio, sr, t)
# Given an audio snippet, sampling rate, and time in seconds, isolate a smaller snippet around the peak of the audio, of time t
# Inputs: audio - audio snippet, sr - sampling rate, t - time in seconds
# Outputs: peakSnippet - audio snippet around the peak of the audio
def isolatePeak(audio, sr, t):
    # Calculate the number of samples in the Snippet
    samples = int(t * sr)
    
    # Calculate the number of samples to the left and right of the peak
    samplesLeft = int((samples - 1) / 2)
    samplesRight = int(samples / 2)
    
    # Find the peak of the audio
    peak = np.argmax(audio)
    
    # Isolate the audio around the peak
    # If not enough samples to the left or right, pad with zeros
    if peak - samplesLeft < 0:
        peakSnippet = np.concatenate((np.zeros(samplesLeft - peak), audio[:peak + samplesRight]))
    elif peak + samplesRight > len(audio):
        peakSnippet = np.concatenate((audio[peak - samplesLeft:], np.zeros(peak + samplesRight - len(audio))))
    else:
        peakSnippet = audio[peak - samplesLeft:peak + samplesRight]
    
    return peakSnippet

if __name__ == '__main__':
    # initial values
    env = dotenv_values('.env')
    db = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    
    print("setup done")
    
    # Recording loop
    while(True):
        fs = 16000  # Sample rate

        # Record audio
        recording = sd.rec(int(DURATION * fs), samplerate=fs, channels=2)
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

        print("Peak ({}s):".format(DURATION), max_loudness, "dB. Threshold is", DB_THRESHOLD, "dB.")

        if (max_loudness > DB_THRESHOLD): # Proceed to analyze audio

            # Get timestamp
            timestamp = datetime.now()
            
            # Write to file 
            fname = timestamp.strftime('%Y%m%d%H%M%S')
            audio_path = f'data/database/{fname}.wav'
            # TODO: just directly change sampling rate here without using librosa to resample?
            write(audio_path, fs, recording)
            print("\nWRITTEN TO FILE")

            # Calculate metrics - LAeq, LAmax, LCpeak, TWA, etc
            LAeq, LAmax, LCpeak, twa = calculate_metrics(sig=recording, audio_segment=audio_segment, sr=fs, n=4096)
            
            # change sampling rate to 16 khz before passing into BEATs
            '''
            data, sr = librosa.load(audio_path, sr=None)
            resamp_signal = librosa.resample(data, orig_sr=sr, target_sr=16000)
            # TODO: sf.write vs write, ALSO rewriting the file here
            sf.write(audio_path, resamp_signal, 16000, subtype='PCM_24')
            '''
            
            # Classification - BEATs
            BEATs_model = BEATs_eval()
            top5_label, top5_label_prob = BEATs_model.predict(audio_path)
            labels = []
            for i, label in enumerate(top5_label):
                if top5_label_prob[i] >= PROBABILITY_THRESHOLD:
                    labels.append(label)
                
            print("\n")
            # Database    
            if len(labels) == 0:
                print(f"PREDICTION PROBABILITIES ALL BELOW THRESHOLD {PROBABILITY_THRESHOLD}")
                os.remove(audio_path)
            else:
                db.insert_audio_frag(timestamp, AUDIO_LENGTH, audio_path, LAeq, LAmax, LCpeak, twa, labels)
                print("WRITTEN TO DATABASE")
            
            
            