# -*- coding: utf-8 -*-
"""Traffic_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zCo6Lw7Kup2i9aggeV78Dka_yZczGjTT
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

dataframe = pd.read_csv(r'C:\Users\admin\Downloads\TrafficDataset.csv')
dataframe.head()

dataset = np.array(dataframe)

m = dataset.shape[0]

s= int(0.9*m)

train = dataset[:s,:]
test = dataset[s:,:]

train_predictors = train[:,:12]
train_predictors_exp = train[:,16:20]
train_predictors = np.concatenate((train_predictors,train_predictors_exp), axis = 1)

train_labels = train[:,21]

test_predictors = test[:,:12]
test_predictors_exp = test[:,16:20]
test_predictors = np.concatenate((test_predictors,test_predictors_exp), axis = 1)
test_labels = test[:,21]

#print(predictors)
#print(labels)

train_predictors = tf.convert_to_tensor(train_predictors.astype(float))
train_labels = tf.convert_to_tensor(train_labels.astype(float))
test_predictors = tf.convert_to_tensor(test_predictors.astype(float))
test_labels = tf.convert_to_tensor(test_labels.astype(float))

model = tf.keras.models.Sequential([
                                    tf.keras.layers.Dense(units = 512, input_shape = [16], activation='relu'),
                                    tf.keras.layers.Dense(units = 256, activation='relu'),
                                    tf.keras.layers.Dense(units = 128, activation='relu'),
                                    tf.keras.layers.Dense(units = 64, activation='relu'),
                                    tf.keras.layers.Dense(units = 1)
                                   ])
model.summary()
model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  )

history = model.fit(train_predictors, train_labels, epochs = 50, validation_data=(test_predictors, test_labels), batch_size = 150)

model.evaluate(test_predictors, test_labels)

x = np.array(model.predict(test_predictors))

def set_limit(x):
    for i in range(x.shape[0]):
        if x[i] < dataset[s + i, 31]:
            break
        else:
            x[i] = dataset[s + i, 31]
            return x

x = set_limit(x)
y = np.array(test_labels)

t = np.array(range(test_predictors.shape[0]))

print(np.around(x[1:10]))
print(y[1:10])


plt.plot(t,x)
plt.plot(t,y)
plt.title("Comparison between predicted and actual values")
plt.ylabel('Optimum Time Cycle')
plt.xlabel('Time')
plt.legend(['Predicted', 'Actual'], loc='upper left')
plt.show()

plt.plot(t,y)
plt.show()

plt.plot(t,x)
plt.show()
