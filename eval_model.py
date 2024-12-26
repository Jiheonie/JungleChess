
import numpy as np
from keras.api.models import load_model


model = load_model('models/model2.keras')

X = np.load('f3.npy')
Y = np.load('l3.npy')

samples = X.shape[0]

board_size = 9 * 7

X = X.reshape(samples, 9, 7, 5)
Y = Y.reshape(samples, board_size * 4)

train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

model.summary()

score = model.evaluate(X_test, Y_test, verbose=0)

print('Test loss: ', score[0])
print('Test accuracy: ', score[1])