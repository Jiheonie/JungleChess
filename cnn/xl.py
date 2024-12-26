from keras.api.layers import Dense, Activation, Flatten, Conv2D, ZeroPadding2D, MaxPooling2D, ReLU, BatchNormalization, GlobalAveragePooling2D, Dropout
from keras.api.models import Sequential

def layers(input_shape):
    return [
        # model 0
        #1
        Conv2D(64, (3, 3), input_shape=input_shape, padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #2
        Conv2D(64, (3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),
        #3
        Conv2D(128, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #4
        Conv2D(128, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),
        #5
        Conv2D(256, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #6
        Conv2D(256, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #7
        Conv2D(256, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),
        #8
        Conv2D(512, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #9
        Conv2D(512, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #10
        Conv2D(512, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),
        #11
        Conv2D(512, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #12
        Conv2D(512, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #13
        Conv2D(512, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),
        #14
        Conv2D(1024, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #15
        Conv2D(1024, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #16
        Conv2D(1024, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),
        #17
        Conv2D(2048, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #18
        Conv2D(2048, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #19
        Conv2D(2048, kernel_size=(3, 3), padding='same', data_format='channels_last'),
        BatchNormalization(),
        ReLU(),
        Dropout(0.3),
        #pool
        # MaxPooling2D(pool_size=(2, 2), strides=2, data_format='channels_last'),


        GlobalAveragePooling2D(),
        # Flatten(),

        Dense(2048),
        ReLU(),
        Dropout(0.5),
        Dense(2048),
        ReLU(),
        Dropout(0.5),
        Dense(2048),
        ReLU(),
        Dropout(0.5),
    ]