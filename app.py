from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime
import os
from threading import Thread

app = Flask(__name__)

os.makedirs('dataset', exist_ok=True)

def save_data(grid_state, selected_number):
    grid = np.array(grid_state).reshape((20, 20))

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
    filename = f'dataset/training_data_{timestamp}.npy'

    np.save(filename, {'grid': grid, 'label': selected_number})

@app.route('/')
def menu():
    return render_template('index.html', title='Menu')

@app.route('/train')
def train():
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    return render_template('train.html', title='Train', timestamp=timestamp)

@app.route('/run')
def run():
    return render_template('run.html', title='Run')

@app.route('/endpoint', methods=['POST'])
def endpoint():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'no data provided'}), 400

    grid_state = data.get('gridState')
    selected_number = data.get('selectedNumber')

    if not isinstance(grid_state, list):
        return jsonify({'error': 'gridState must be a list'}), 400

    if not isinstance(selected_number, int) or selected_number not in range(1, 9):
        return jsonify({'error': 'selectedNumber must be an integer between 1 and 9'}), 400

    if all(i == 0 for i in grid_state):
        return jsonify({'error': 'gridState must not be all zeros'}), 400

    Thread(target=save_data, args=(grid_state, selected_number)).start()

    return jsonify({'message': 'data received successfully'}), 201
