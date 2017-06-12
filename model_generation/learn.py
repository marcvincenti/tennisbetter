#!/usr/bin/env python

from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import StratifiedKFold
import numpy

train_file_name = "train.csv"
test_file_name = "test.csv"
nb_vars = 35 #without binary output

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load dataset
train_dataset = numpy.loadtxt(train_file_name, delimiter=",")
test_dataset = numpy.loadtxt(test_file_name, delimiter=",")

# split into input (X) and output (Y) variables
X_train = train_dataset[:,0:nb_vars].astype(float)
Y_train = train_dataset[:,nb_vars]
X_test = test_dataset[:,0:nb_vars].astype(float)
Y_test = test_dataset[:,nb_vars]

# create model
model = Sequential()
model.add(Dense(100, input_dim=nb_vars, init='uniform', activation='relu'))
model.add(Dense(200, init='uniform', activation='relu'))
model.add(Dense(100, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	
print("Train model...")
# Fit the model
model.fit(X_train, Y_train, validation_data=(X_test,Y_test), nb_epoch=100000, batch_size=100000)

# evaluate the model
scores = model.evaluate(X_test, Y_test)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
