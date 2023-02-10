# Generic imports
from datetime import datetime
import librosa
from dotenv import dotenv_values
import glob
import os

# Recording imports
import sounddevice as sd
from scipy.io.wavfile import write
import pydub
import soundfile as sf

from src.model.beats.BEATs_eval import BEATs_eval
from src.database.DBInterface import DBInterface
from src.metrics.calculate_metrics import calculate_metrics

AUDIO_LENGTH = 2

if __name__ == '__main__':
    # initial values
    env = dotenv_values('.env')
    db = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    
    print("setup done")
    
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

        if (max_loudness > threshold): # Proceed to analyze audio

            # Get timestamp
            timestamp = datetime.now()
            
            # Write to file 
            fname = timestamp.strftime('%Y%m%d%H%M%S')
            fname = f'{fname}.wav'
            write('audio/{}'.format(fname), fs, recording)
            print("\nWRITTEN TO FILE\n")

            # Calculate metrics - LAeq, LAmax, LCpeak, TWA, etc
            LAeq, LAmax, LCpeak, twa = calculate_metrics(sig=recording, audio_segment=audio_segment, sr=fs, n=4096)
            
            # change sampling rate to 16 khz before passing into BEATs
            audio_path = 'audio' + f'/{fname}'
            data, sr = librosa.load(audio_path, sr=None)
            resamp_signal = librosa.resample(data, orig_sr=sr, target_sr=16000)
            # TODO: sf.write vs write, ALSO rewriting the file here
            sf.write(audio_path, resamp_signal, 16000, subtype='PCM_24')
            
            # Classification - BEATs
            # Download model (Fine-tuned BEATs_iter3+ (AS2M) (cpt2)) from the BEATs README
            BEATs_model = BEATs_eval()
            top5_label, top5_label_prob = BEATs_model.predict(audio_path)
            labels = []
            for i, label in enumerate(top5_label):
                if top5_label_prob[i] >= 0.6:
                    labels.append(label)
            
            # Database
            db.insert_audio_frag(timestamp, AUDIO_LENGTH, audio_path, LAeq, LAmax, LCpeak, twa, labels)
            print("\n")
            print("WRITTEN TO DATABASE")