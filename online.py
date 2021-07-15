#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal as ss
from model import *

###
#Originally includes a part of code responsible for connecting to amplifier and taking packets of samples from EEG set in real time - not showed here, 
#because this part wasn't written by me.
###



Fs = 256
packet_length = int(4*Fs)
n_chan = 8
b1,a1 = ss.butter(4,(3/(Fs/2),5/(Fs/2)), 'bandpass')
b2,a2 = ss.butter(4,(12/(Fs/2),14/(Fs/2)), 'bandpass')
#zi1 = ss.lfilter_zi(b1,a1)
#zi2 = ss.lfilter_zi(b2,a2)


zi1 = np.matlib.repmat(ss.lfilter_zi(b1,a1),7,1).T
zi2 = np.matlib.repmat(ss.lfilter_zi(b2,a2),7,1).T

mu = np.load('mean.npy')
sig = np.load('sig.npy')
wyniki = np.zeros((2,7))
regr = model()
amp.start_sampling()
gains = np.array(amp.current_description.channel_gains)
offsets = np.array(amp.current_description.channel_offsets)

def samples_to_microvolts(samples):  # z jednostek wzmacniacza do mikrowoltów
    return samples * gains + offsets
   
while True:
    packet = amp.get_samples(packet_length) 
    packet_m = samples_to_microvolts(packet.samples)
           #print(packet_m.shape)
           #print(packet_m)
           #print(packet.ts[0])
           #print(packet.samples.shape, amp.current_description.channel_names)
    packet_new =packet_m[:,:7].T - packet_m[:,7]
    packet_new = packet_new.T
           #print(packet_new)
    sig_16,zi1 = ss.lfilter(a1,b1,packet_new,axis=0,zi=zi1)
    sig_22,zi2 = ss.lfilter(a2,b2,packet_new,axis=0,zi=zi2)
           #print(zi1,zi2)
    RSM_16 = np.sqrt(np.mean((sig_16[:,:7])**2,axis=0)) 
    RSM_22 = np.sqrt(np.mean((sig_22[:,:7])**2,axis=0))
           #print(RSM_16)
           #print(RSM_22)

    wyniki[0,:] = RSM_16
    wyniki[1,:] = RSM_22         



    RMS_norm = np.zeros((wyniki.shape))
    for pasmo in range(0,2):
        for channel in range(0,7):
            rms_norm = (wyniki[pasmo,channel] - mu[channel,pasmo])/sig[channel,pasmo]
            RMS_norm[pasmo,channel] = rms_norm

    #print(RMS_norm)


    new_matrix = np.zeros(14)
    for pasmo in range(0,2):
        if pasmo == 0:
            new_matrix[:7] = RMS_norm[0,:]
        else:
            new_matrix[7:] = RMS_norm[1,:]
    print(new_matrix)
    result = regr.predict(new_matrix.reshape((1,14)))
    
    print('Strona w którą patrzy osoba',result)
                    
    





    
sp.blinkSSVEP([0, 0],1,1)

