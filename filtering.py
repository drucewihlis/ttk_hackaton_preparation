# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:46:06 2021

@author: Mi
"""

from scipy import signal
import numpy as np
from logmmse import logmmse_from_file


def filtering(filt, wav):
    out = logmmse_from_file(wav)
    sig_ff = np.array(signal.lfilter(filt, [1], out[:, 0]), dtype='int16')
    return sig_ff
