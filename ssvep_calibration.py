#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import scipy.signal as ss


''''''
Originally includes a part of code responsible for connecting to amplifier and taking packets of samples from EEG set in real time - not showed here, because this part wasn't written by me.
''''''


Fs = 256
packet_length = int(1*Fs)
#n_chan = 38
b1,a1 = ss.butter(4,(6/(Fs/2),8/(Fs/2)), 'bandpass')
b2,a2 = ss.butter(4,(16/(Fs/2),18/(Fs/2)), 'bandpass')
#zi1 = ss.lfilter_zi(b1,a1)
#zi2 = ss.lfilter_zi(b2,a2)

zi1 = np.matlib.repmat(ss.lfilter_zi(b1,a1),7,1).T
zi2 = np.matlib.repmat(ss.lfilter_zi(b2,a2),7,1).T

wyniki = np.zeros((5,2,3,10,7)) #2pasma, 3 sides, 8 channels, 10 packets
sides = ['LEFT', 'MIDDLE', 'RIGHT']
amp.start_sampling()
gains = np.array(amp.current_description.channel_gains)
offsets = np.array(amp.current_description.channel_offsets)

def samples_to_microvolts(samples):  # z jednostek wzmacniacza do mikrowoltów
    return samples * gains + offsets
   
for trial in range(0,5):
   print('Podejście nr ' +str(trial+1))
   for side in range(0,3):
       for packet_number in range(0,10): 
           print('LOOK AT ' +sides[side])
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
           wyniki[trial,0,side,packet_number,:] = RSM_16
           wyniki[trial,1,side,packet_number,:] = RSM_22
print("Wyniki:     ", wyniki)           


np.save("kalibracja_wyniki_7_17_Ola",wyniki)   
#load('kalibracja_wyniki.npy')      
sp.blinkSSVEP([0, 0],1,1)


#RMS_normalized = np.zeros(2,8)
           
