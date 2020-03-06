import scipy
from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn import preprocessing
import sklearn as sk


def log_specgram(audio, sample_rate, window_size=20,
                 step_size=10, eps=1e-10):
    nperseg = int(round(window_size * sample_rate / 1e3))
    noverlap = int(round(step_size * sample_rate / 1e3))
    freqs, _, spec = signal.spectrogram(audio,
                                    fs=sample_rate,
                                    window='hann',
                                    nperseg=nperseg,
                                    noverlap=noverlap,
                                    detrend=False)
    return freqs, np.log(spec.T.astype(np.float32) + eps)



def wav2img(wav_path, targetdir='', figsize=(45,45)):
    """
    takes in wave file path
    and the fig size. Default 4,4 will make images 288 x 288
    """

    fig = plt.figure(figsize=(15,4))    
    # use soundfile library to read in the wave files
    samplerate, test_sound  = wavfile.read(wav_path)
    _, spectrogram = log_specgram(test_sound, samplerate)
    
    print('shape',spectrogram.shape)
    ## create output path
    output_file = wav_path.split('/')[-1].split('.wav')[0]
    output_file = targetdir +'/'+ output_file
    plt.imsave('%s.jpg' % output_file, spectrogram)
    plt.close()

def wav2spect(wav_path, targetdir='', figsize=(45,45)):
    """
    takes in wave file path
    and the fig size. Default 4,4 will make images 288 x 288
    """

    # use soundfile library to read in the wave files
    samplerate, x  = wavfile.read(wav_path)    
    
    x_normalize=sk.preprocessing.minmax_scale(x, axis=0) 
    
    x = pad_audio(x_normalize)
    
    _, spectrogram = log_specgram(x, samplerate)
    
    
    
    return spectrogram

"""
path_wav : path de los audios
path_png: donde se guardaran las imagenes
"""

def wav2spectFolder(path_wav, path_png):
    entries = os.listdir(path_wav)
    for entry in entries:        
        wav2img(entry,path_png)
    
    
### rellenará audios de menos de 16000 (1 segundo) con ceros para que todos tengan la misma longitud.
def pad_audio(samples):
    L = 16000
    if len(samples) >= L: return samples
    else: return np.pad(samples, pad_width=(L - len(samples), 0), mode='constant', constant_values=(0, 0))   
    

