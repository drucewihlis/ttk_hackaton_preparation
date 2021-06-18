# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:46:06 2021

@author: Mi
"""

from scipy import signal
import numpy as np
from logmmse import logmmse_from_file
import pickle
from scipy.io import wavfile
import matplotlib.pyplot as plt 

def filtering(filt, wav='03.03_19.wav'):
    out = logmmse_from_file(wav)
    sig_ff = np.array(signal.lfilter(filt,[1], out[:,0]), dtype = 'int16')
    return sig_ff
if __name__ =='__main__':
    with open('filter.pkl', 'rb') as f:
        taps, w, h = pickle.load(f)

    wav = '03.03_19.wav'
    #result = filtering(filt, wav)

    out = filtering(taps, wav)

    #plt.plot(out[0:10000])
    wavfile.write("example.wav", 48000, out)
