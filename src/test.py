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

from multiprocessing.dummy import Pool as ThreadPool

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
    #plot_cochleagram(c_gram_reshape_2, filename)

    # prepare to run through network -- i.e., flatten it
    c_gram_flatten = np.reshape(c_gram_reshape_2, (1, 256*256)) 

    return c_gram_flatten

def test(language):
    pool = ThreadPool(4)
    data_directory = '/home/davidlee/dev/kelletal2018/data/' + language + '/'
    coch_directory = '/home/davidlee/dev/kelletal2018/cochleagrams/' + language + '/'
    if not os.path.exists(coch_directory):
        os.makedirs(coch_directory)

    for i in range(1, 103):
        pool = ThreadPool(4)
        directory = data_directory + language + str(i) + '/'

        if not os.path.exists(coch_directory + language + str(i) + '/'):
            os.makedirs(coch_directory + language + str(i) + '/')
        print "Trying " + directory
        wav_to_coch = []
        for word in allowed_words:
            filepath = directory + word + '.wav'
            coch_filepath = coch_directory + language + str(i) + '/' + word + '.npy'
            if os.path.isfile(filepath) and not os.path.isfile(coch_filepath):
                wav_to_coch.append((filepath, coch_filepath))
        if wav_to_coch:
            results = pool.map(write_cochleagram, wav_to_coch)
        pool.close()
        pool.join()

def write_cochleagram(filepaths):
    filepath, coch_filepath = filepaths
    try:
        print "[INFO]: Reading from " + filepath
        print "[INFO]: Writing to " + coch_filepath
        c_gram = generate_cochleagram(filepath)  
        np.save(coch_filepath, c_gram)
        print "[PASS]: Successfully wrote " + coch_filepath
    except:
        print "[FAIL]: Couldn't generate cochleagram for " + filepath




def score(language, top_n=50):
    tf.reset_default_graph()
    net_object = branched_network()
    word_key = np.load('./demo_stim/logits_to_word_key.npy') # load logits to word key
    music_key = np.load('./demo_stim/logits_to_genre_key.npy') # load logits to word key 
    
    coch_directory = '/home/davidlee/dev/kelletal2018/cochleagrams/' + language + '/'
    if not os.path.exists(coch_directory):
        raise Exception(language + ' cochleagrams not found')

    num_words = 0
    num_in_top_n = 0
    for i in range(1, 103):
        language_directory = coch_directory + language + str(i) + '/'
        if not os.path.exists(language_directory):
            print "Couldn't find " + language_directory
            continue

        for word in allowed_words:
            coch_filepath = language_directory + word + '.npy'
            if os.path.isfile(coch_filepath):
                num_words += 1
                c_gram = np.load(coch_filepath)
                logits = net_object.session.run(net_object.word_logits, feed_dict={net_object.x: c_gram})
                indices = logits[0].argsort()[-top_n:]
                sorted_words = [word_key[i] for i in indices]
                if word in sorted_words:
                    num_in_top_n += 1
    print "Num words in top " + str(top_n) + ": " + str(num_in_top_n)
    print "Num total words: " + str(num_words)
    print "Percentage: " + str(float(num_in_top_n)/num_words)



if __name__=="__main__":
    #test('arabic')
    score('arabic', top_n=25)

