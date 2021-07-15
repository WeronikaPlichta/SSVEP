#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
wyniki = np.load('kalibracja_wyniki_7_17_Ola.npy')
print(wyniki.shape)
mu = np.zeros((7,2))
sig = np.zeros((7,2))

#for trial in range(0,5):
#    for pasmo in range(0,2):
#        for side in range(0,3):
#            for packet_number in range(0,10):
#                for channel in range(0,7):
#                    wyniki[trial,pasmo,side,packet_number,channel] = wyniki[trial,pasmo,side,packet_number,channel] - wyniki[trial,pasmo,side,packet_number,7] 



for pasmo in range(0,2):
   for channel in range(0,7):
       RMS_s = wyniki[:,pasmo, 1,:,channel]
       mu[channel,pasmo] = np.mean(RMS_s)
       sig[channel,pasmo] = np.std(RMS_s)
RMS_norm = np.zeros((wyniki.shape))
for trial in range(0,5):
    for pasmo in range(0,2):
        for side in range(0,3):
            for packet_number in range(0,10):
                for channel in range(0,7):
                    rms_norm = (wyniki[trial,pasmo,side,packet_number,channel] - mu[channel,pasmo])/sig[channel,pasmo]
                    RMS_norm[trial,pasmo,side,packet_number,channel] = rms_norm


##((5,2,3,10,8))
labels = ['left', 'middle','right']
channels = ['O1','O2','T5','P3','Pz','P4','T6','Fz']
idx = 1
N=0
plt.figure(figsize=(8, 20))
for m in range(0,7):
    for k in range(0,2):
        plt.subplot(7,2,idx)
        data = np.zeros((50,3))
        for i in range(0,5):
            for j in range(0,3):
                data[(10*i):(10*(i+1)),j] = RMS_norm[i,k,j,:,m]
        plt.boxplot(data,vert=True, patch_artist=True, labels=labels)
        if idx==1:
            plt.title("Freq 16Hz")
        if idx==2:
            plt.title("Freq 22Hz")
        idx+=1
        
plt.plot()
        

#print(RMS_norm)
np.save("mean",mu)
np.save("sig",sig)
np.save("normalisation",RMS_norm)

new_matrix = np.zeros((150,14))
y = np.zeros(150)
start = 0
for trial in range(0,5):
    for side in range(0,3):
        for packet_number in range(0,10):
            y[start] = side
            for pasmo in range(0,2):
                if pasmo == 0:
                    new_matrix[start,:7] = RMS_norm[trial,pasmo,side,packet_number,:]
                else:
                    new_matrix[start,7:] = RMS_norm[trial,pasmo,side,packet_number,:]
                
            start+=1
#print(new_matrix)
#print(new_matrix.shape)
#print(y)


#n, bins, patches = plt.hist(new_matrix[:,0], 50, density=True, facecolor='g', alpha=0.75)

np.save("nowa_macierz",new_matrix)
np.save("y",y)