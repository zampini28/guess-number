import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

def load_training_data():
    dataset, labels = zip(*[
        (data['grid'], data['label'])
        for filename in os.listdir('dataset') if filename.endswith('.npy')
        for data in [np.load(os.path.join('dataset', filename), allow_pickle=True).item()]
    ])

    return np.array(dataset), np.array(labels)

def preprocess_data(x):
    return (x.astype('float32') / 1.0).reshape(x.shape[0], -1)

def create_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(128, 'relu'),
        layers.Dense(64, 'relu'),
        layers.Dense(10, 'softmax'),
    ])

    model.compile('adam', 'sparse_categorical_crossentropy', None, ['accuracy'])

    return model

if __name__ == '__main__':
    input('press any key to continue...')
    x, y = load_training_data()

    x = preprocess_data(x)

    model = create_model(x.shape[1:])
    model.fit(x, y, 32, 10)

    model.save('number_recognition_model.keras')
