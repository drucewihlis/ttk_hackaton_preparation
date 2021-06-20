# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 13:20:44 2021

@author: Mi
"""

from filtering import filtering
import pickle

import numpy as np
from scipy.io import wavfile
from scipy.fftpack import rfft
import os
from tensorly.decomposition import parafac
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler


def Speaker_Recognizing(path="./audio-chunks"):
    n = 32768
    file_list = os.listdir(path=path)
    with open('filter.pkl', 'rb') as f:
        taps, w, h = pickle.load(f)
    data_list = np.zeros((len(file_list), n // 2))
    for i, file in enumerate(file_list):
        samplerate, data = wavfile.read("./audio-chunks/" + file)
        data = filtering(taps, wav=("./audio-chunks/" + file))
        data_spec = rfft(data, n=n)
        data_list[i, :] = (np.abs(2.0 / n * np.abs(data_spec[0:n // 2])))

    decomp = parafac(data_list, rank=5)
    factors = decomp.factors[0]

    scaler = MinMaxScaler()
    factors = scaler.fit_transform(factors)
    clustering = DBSCAN(eps=0.2, min_samples=4).fit_predict(factors)
    clustering += 1

    operator = str(clustering[file_list.index('chunk1.wav')])
    out = {'0': [], '1': []}
    for n, i in enumerate(clustering):
        files = out[str(i)]
        files.append(file_list[n])
        out[str(i)] = files

    out['operator'] = out.pop(operator)
    key = list(out.keys())
    key.remove('operator')
    out['client'] = out.pop(key[0])
    return out
