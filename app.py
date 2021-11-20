from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('base.html')


@app.route('/predict')
def predictions_page():
    return render_template('predictions.html')
