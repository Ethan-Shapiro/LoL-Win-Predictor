from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from src.RawDataWrangler import RawDataWrangler
from src.RawDataFormatter import RawDataFormatter
from src.DataValidator import DataValidator
from src.WinPredictor import WinPredictor

app = Flask(__name__)
raw_data_wrangler = RawDataWrangler(API_KEY="YOURKEY")
raw_data_formatter = RawDataFormatter(summoner_name="Sasheemy")
data_validator = DataValidator()
win_predictor = WinPredictor()


@app.route('/')
def home_page():
    return render_template('base.html')


@app.route('/query', methods=["GET", "POST"])
def processing_page():
    if request.method == "POST":
        summoner_name = request.form.get("summoner_name")
        region = request.form.get("region")
        # Validate summoner name
        player = raw_data_wrangler.validate_summoner_name(
            summoner_name=summoner_name, region=region)

        # If valid, load the predictions page
        if player != False:
            return redirect(url_for("predictions_page", summoner_name=summoner_name))

    # If invalid, reload page with message that the name is invalid
    kparams = {"summoner_name": summoner_name,
               "region": region}
    return render_template('processing.html', **kparams)


@app.route('/predict', methods=["GET", "POST"])
def predictions_page():
    # Get the summoner name from args
    summoner_name = request.args.get("summoner_name")
    region = request.args.get("region")

    # download player timeline data (Raw Data Wrangler)
    raw_timelines = raw_data_wrangler.get_raw_match_timelines(
        summoner_name, region, count=3, start=0)

    # Then format the data (Raw Data Formatter)
    raw_formatted = raw_data_formatter.format_data(raw_timelines)

    # Then validate (Data Validator)

    # apply model(s) and get predictions (Win Predictor)

    # Then download pertinent player data (Raw Data Wrangler for match data)
    # Package data to send to predictions page
    predictions = [{'percentage': 98.65,
                    'color': "rgba(51, 170, 51, .4)",
                    'Ally': {'Names': ['X', 'Y', 'Z', 'A', 'B']},
                    'Enemy': {'Names': ['X', 'Y', 'Z', 'A', 'B']}},
                   {'percentage': 98.65,
                    'color': "rgba(51, 170, 51, .4)",
                    'Ally': {'Names': ['X', 'Y', 'Z', 'A', 'B']},
                    'Enemy': {'Names': ['X', 'Y', 'Z', 'A', 'B']}}]

    # Render predictions page
    return render_template('predictions.html')
