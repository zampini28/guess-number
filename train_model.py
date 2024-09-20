import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

def load_training_data():
    dataset, labels = zip(*[
        (data['grid'], data['label'])
        for filename in os.listdir('dataset') if filename.endswith('.npy')
        for data in [np.load(os.path.json('dataset', filename), allow_pickle=True).item()]
    ])

    return np.array(dataset), np.array(labels)

def preprocess_data(x):
    return (x.astype('float32') / 1.0).reshape(x.shape[0], -1)

def create_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(128, 'relu'),
        layers.Dense(64, 'relu'),
        layers.Dense(9, 'softmax'),
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

print('hello world')
if __name__ == '__main__':
    print('calling load_training_data...')
    x, y = load_training_data()
    print('load_training_data has turned:')
    print(f'x: {type(x)}')
    print(x)
    print(f'y: {type(y)}')
    print(y)

    input('press any key to continue...')

    print('calling preprocess_data on x...')
    x = preprocess_data(x)
    print('preprocess_data has turned:')
    print(f'x: {type(x)}')
    print(x)

    input('press any key to continue...')

    print('calling create_model on x...')
    print('sending...')
    print(x.shape[1:])
    model = create_model(x.shape[1:])
    print('create_model has turned:')
    print(f'model: {type(model)}')
    print(model)

    input('press any key to continue...')
