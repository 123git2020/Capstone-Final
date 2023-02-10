import librosa
import numpy as np
import math

def calculate_metrics(sig, audio_segment, sr, n):
    ff=librosa.stft(sig,n_fft=n,hop_length=n)
    freqs=(np.linspace(0,sr,n))[0:n//2+1]
    mag=librosa.power_to_db(abs(ff)**2)

    weights = librosa.multi_frequency_weighting(freqs, kinds='AC').T

    A=(mag+weights[:,:1])[0:,:]
    C=(mag+weights[:,1:])[0:,:]
    
    LAmax = np.max(A); # LAmax
    LCpeak = np.max(C); # C-weighted peak level
    LAeq = np.mean(A); # LAeq
    twa = 16.61 * math.log10(abs(LAeq)/100) + 90
    max_loudness = audio_segment.max_dBFS
    average_loudness = audio_segment.dBFS

    print("\n")
    print("LAeq =",LAeq,"dB")
    print("LAmax =",LAmax,"dB")
    print("LCpeak =",LCpeak,"dB")
    print("Time-weighted average =",twa,"dB")
    print("Average dBFS =", average_loudness, "dB")
    print("Peak dBFS =", max_loudness, "dB")
    print("\n")
    
    return (LAeq, LAmax, LCpeak, twa)