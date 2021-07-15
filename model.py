#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sklearn import svm
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn import metrics
def model():
    rms = np.load('nowa_macierz.npy')
    y = np.load('y.npy')

    X_train,X_test,Y_train,Y_test = train_test_split(rms,y,test_size=0.2, stratify=y)

    regr = linear_model.LogisticRegression(solver = 'lbfgs')
    #regr = svm.SVC(C = 0.1)
    regr.fit(X_train,Y_train)
    print(X_test)
    print(Y_test)
    y_pred = regr.predict(X_test)
    ACC = metrics.accuracy_score(Y_test, y_pred)
    print(y_pred)
    print(ACC)
    return regr

model()

#online
# syg (128,38)
