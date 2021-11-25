from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('base.html')


@app.route('/predict')
def predictions_page():
    predictions = [{'percentage': 98.65,
                    'color': "rgba(51, 170, 51, .4)",
                    'Ally': {'Names': ['X', 'Y', 'Z', 'A', 'B']},
                    'Enemy': {'Names': ['X', 'Y', 'Z', 'A', 'B']}},
                   {'percentage': 98.65,
                    'color': "rgba(51, 170, 51, .4)",
                    'Ally': {'Names': ['X', 'Y', 'Z', 'A', 'B']},
                    'Enemy': {'Names': ['X', 'Y', 'Z', 'A', 'B']}}]
    return render_template('predictions.html', preds=predictions)
