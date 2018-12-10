from network.branched_network_class import branched_network
import tensorflow as tf
import numpy as np
import scipy.io.wavfile as wav
import librosa
import os
import pickle

import cochleagram as cgram
from PIL import Image
import matplotlib as plt
allowed_words = [
    'also',
    'call',
    'cheese',
    'fresh',
    'into',
    'need',
    'small',
    'store',
    'these',
    'things',
]

def resample(example, new_size):
    im = Image.fromarray(example)
    resized_image = im.resize(new_size, resample=Image.ANTIALIAS)
    return np.array(resized_image)

def plot_cochleagram(cochleagram, title): 
    plt.figure(figsize=(6,3))
    plt.matshow(cochleagram.reshape(256,256), origin='lower',cmap=plt.cm.Blues, fignum=False, aspect='auto')
    plt.yticks([]); plt.xticks([]); plt.title(title); 

def generate_cochleagram(filename):
    # define parameters
    wav_f, sr = librosa.core.load(filename, sr=16000) # note the sampling rate is 16000hz.
    n = 50
    low_lim, hi_lim = 20, 8000
    sample_factor, pad_factor, downsample = 4, 2, 200
    nonlinearity, fft_mode, ret_mode = 'power', 'auto', 'envs'
    strict = True
    # create cochleagram
    c_gram = cgram.cochleagram(wav_f, sr, n, low_lim, hi_lim, 
                               sample_factor, pad_factor, downsample,
                               nonlinearity, fft_mode, ret_mode, strict)

    # rescale to [0,255]
    c_gram_rescaled =  255*(1-((np.max(c_gram)-c_gram)/np.ptp(c_gram)))
    
    # reshape to (256,256)
    c_gram_reshape_1 = np.reshape(c_gram_rescaled, (211,400))
    c_gram_reshape_2 = resample(c_gram_reshape_1,(256,256))
    plot_cochleagram(c_gram_reshape_2, filename)

    # prepare to run through network -- i.e., flatten it
    c_gram_flatten = np.reshape(c_gram_reshape_2, (1, 256*256)) 

    return c_gram_flatten

def test(language):
    data_directory = '/home/davidlee/dev/kelletal2018/data/' + language + '/'
    
    for i in range(1, 103):
        directory = data_directory + language + str(i) + '/'
        for word in allowed_word:
            filepath = directory + word + '.wav'
            if os.path.isfile(filepath):


if __name__=="__main__":
    test('arabic')
