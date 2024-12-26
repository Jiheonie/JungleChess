import numpy as np
import argparse
import h5py
from keras.api.callbacks import ReduceLROnPlateau, ModelCheckpoint
from keras.api.optimizers import Adam


# def main():
from keras.api.models import load_model

np.random.seed(1)

X = np.load('f3.npy')
Y = np.load('l3.npy')

samples = X.shape[0]

board_size = 9 * 7

X = X.reshape(samples, 9, 7, 5)
Y = Y.reshape(samples, board_size * 4)

train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

model = load_model('model0.keras')

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.7, patience=10, min_delta=0.001, min_lr=1e-5)

checkpoint = ModelCheckpoint('model0.keras', monitor='val_loss', verbose=1, save_best_only=True, mode='min')

model.compile(loss='categorical_crossentropy',
              # optimizer=SGD(learning_rate=0.02),
              optimizer=Adam(learning_rate=1e-4),
              metrics=['accuracy'])

model.fit(X_train, Y_train,
          batch_size=128,
          epochs=50,
          verbose=1,
          validation_data=(X_test, Y_test),
          callbacks=[reduce_lr, checkpoint])

score = model.evaluate(X_test, Y_test, verbose=0)

print('Test loss: ', score[0])
print('Test accuracy: ', score[1])

model.save('model2.keras')
