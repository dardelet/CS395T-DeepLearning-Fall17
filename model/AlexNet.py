
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, Dense, BatchNormalization, Dropout, Flatten, Activation
from keras.layers.convolutional import ZeroPadding2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.regularizers import l2
from keras.layers.core import Lambda
from keras import initializers
from keras.utils import get_file
import tensorflow as tf
import numpy as np
import os
from keras import backend as K
from skimage.io import imread
import numpy as np


 
def listYearbook(train=True, valid=True):
    yearbook_path = '/work/04381/ymarathe/maverick/yearbook/yearbook' 
    r = []
    if train: r = r + [n.strip().split('\t') for n in open(yearbook_path+'_train.txt','r')]
    if valid: r = r + [n.strip().split('\t') for n in open(yearbook_path+'_valid.txt','r')]
    return r

def loadData():
    # Parameter to limit the size of the dataset when working locally
    
    img_paths_train = listYearbook(train=True, valid=False)
    x_train = np.array([ imread('/work/04381/ymarathe/maverick/yearbook/train' + img_path)[:,:,0] for (img_path, _) in img_paths_train ])
    x1, x2, x3 = x_train.shape 
    x_train = np.reshape(x_train, (x1, x2, x3, 1)) 
    y_train = np.array([ int(year) - 1905 for (_, year) in img_paths_train ])
    
    img_paths_valid = listYearbook(train=False, valid=True)
    x_valid = np.array([ imread('/work/04381/ymarathe/maverick/yearbook/valid' + img_path)[:,:,0] for (img_path, _) in img_paths_valid ])
    x_valid = np.reshape(x_valid, (x1, x2, x3, 1))
    y_valid = np.array([ int(year) - 1905 for (_, year) in img_paths_valid ])

    return (x_train, y_train, x_valid, y_valid)

(x_train, y_train, x_valid, y_valid) = loadData()

num_classes = 104
input_shape = 

x_train = x_train.astype('float32')
x_valid = x_valid.astype('float32')
x_train /= 255
x_valid /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_valid.shape[0], 'test samples')

# convert class vectors to binary class matrices
num_classes = 109 #from 1905 to 2013
y_train = keras.utils.to_categorical(y_train, num_classes)
y_valid = keras.utils.to_categorical(y_valid, num_classes)



model = Sequential()
model.add(ZeroPadding2D((1, 1), input_shape=(171, 186, 1)))
model.add(Conv2D(48, (11,11), strides=(4,4)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(1,1), padding='valid'))
model.add(Dropout(0.25))

model.add(Conv2D(128, (5,5), strides=(4,4), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(1,1), padding='valid'))
model.add(Dropout(0.5))
model.add(Conv2D(192, (1,1)))
model.add(Conv2D(192, (1,1)))
model.add(Conv2D(128, (1,1)))
model.add(Dense(2048))
model.add(Dense(2048))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

model.compile(loss=keras.losses.mean_absolute_error,
              optimizer=keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0),
              metrics=['categorical_accuracy'])

model.fit(x_train, y_train,
          batch_size=128,
          epochs=10,
          verbose=2,
          validation_data=(x_valid, y_valid))
score = model.evaluate(x_valid, y_valid, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
#score = model.evaluate(x_test, y_test, batch_size = 16)



