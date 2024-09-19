from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('index.html', title='Menu')

@app.route('/train')
def train():
    return render_template('train.html', title='Train')

@app.route('/run')
def run():
    return render_template('run.html', title='Run')
