from os import getcwd, listdir
from pathlib import Path
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from src.RawDataWrangler import RawDataWrangler
from src.RawDataFormatter import RawDataFormatter
from src.DataValidator import DataValidator
from src.WinPredictor import WinPredictor
import copy
import config

app = Flask(__name__)
raw_data_wrangler = RawDataWrangler(API_KEY=config.API_KEY)
raw_data_formatter = RawDataFormatter(summoner_name="Sasheemy")
data_validator = DataValidator()
win_predictor = WinPredictor()

win_predictor.load_saved_model()


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
            raw_data_wrangler.player = player
            return redirect(url_for("predictions_page", summoner_name=summoner_name, region=region))

    # If invalid, reload page with message that the name is invalid
    kparams = {"summoner_name": summoner_name,
               "region": region}
    return render_template('processing.html', **kparams)


@app.route('/predict', methods=["GET", "POST"])
def predictions_page():
    # Get the summoner name from args
    summoner_name = str(request.args.get("summoner_name"))
    region = str(request.args.get("region"))

    # download player timeline data (Raw Data Wrangler)
    raw_timelines = raw_data_wrangler.get_raw_match_timelines(
        summoner_name, region, count=3, start=0)

    # Then format the data (Raw Data Formatter)
    timelines = raw_data_formatter.format_timeline_data(raw_timelines)

    match_ids = timelines['match_id'].values

    # Then validate (Data Validator) TODO

    # apply model(s) and get predictions (Win Predictor)
    results = win_predictor.predict(timelines)

    print(results)

    # Then download pertinent player data (Raw Data Wrangler for match data)
    raw_recent_matches = raw_data_wrangler.get_three_recent_matches(
        match_ids, region)

    # Format matches
    recent_matches = raw_data_formatter.format_match_data(raw_recent_matches)

    # Create a singular prediction
    GREEN = "rgba(51, 170, 51, .4)"
    RED = "rgba(255, 0, 0, .4)"

    pred = {'modelPrediction': 'green',
            'percentage': -100,
            'actual': 'purple',
            'color': GREEN,
            'Blue': {'Names': None,
                     'Champions': None,
                     'CS': 0,
                     'Gold': 0,
                     'XP': 0,
                     'Turrets': 0,
                     'Inhibs': 0,
                     'Fire_Dragons': 0,
                     'Water_Dragons': 0,
                     'Earth_Dragons': 0,
                     'Air_Dragons': 0,
                     'Heralds': 0},
            'Red': {'Names': None,
                    'Champions': None,
                    'CS': 0,
                    'Gold': 0,
                    'XP': 0,
                    'Turrets': 0,
                    'Inhibs': 0,
                    'Fire_Dragons': 0,
                    'Water_Dragons': 0,
                    'Earth_Dragons': 0,
                    'Air_Dragons': 0,
                    'Heralds': 0}}

    # Package data to send to predictions page
    predictions = [copy.deepcopy(pred), copy.deepcopy(pred), pred]

    for i, match_id in enumerate(match_ids):
        prediction = predictions[i]
        # Determine which team requested player is on. (Check summoner name)
        player_team = recent_matches[(recent_matches['match_id'] == match_id) & (
            recent_matches['summoner_name'].apply(lambda x: x.lower()) == summoner_name.lower())]['team'].values[0]

        # Add Percentage based on team
        if player_team == results['pred'][i]:
            prediction['percentage'] = "{:.2f}".format(100*results['prob'][i])
        else:
            prediction['percentage'] = "{:.2f}".format(
                100 * (1 - results['prob'][i]))

        winning_team = timelines[timelines['match_id']
                                 == match_id]['winner'].values[0]
        # Add color based on percentage
        if results['pred'][i] == winning_team:
            prediction['color'] = GREEN
        else:
            prediction['color'] = RED

        # Add predicted
        prediction['modelPrediction'] = results['pred'][i]

        # Add actual
        prediction['actual'] = results['actual'][i]

        # Add blue team values
        for team in ['Blue', 'Red']:

            for k in prediction[team]:
                if k == 'Names' or k == 'Champions':
                    continue

                if k == 'Turrets':
                    prediction[team][k] = timelines[timelines['match_id']
                                                    == match_id][team.lower()+'_'+k.lower()+"_destroyed"].values[0]
                    continue

                if k == 'Inhibs':
                    prediction[team][k] = timelines[timelines['match_id']
                                                    == match_id][team.lower()+"_inhibitors_destroyed"].values[0]
                    continue

                if k == 'Heralds':
                    prediction[team][k] = timelines[timelines['match_id']
                                                    == match_id][team.lower()+"_rift_heralds"].values[0]
                    continue

                prediction[team][k] = timelines[timelines['match_id']
                                                == match_id][team.lower()+'_'+k.lower()].values[0]

        # Add blue names
        prediction['Blue']['Names'] = recent_matches[(recent_matches['match_id'] == match_id) & (
            recent_matches['team'] == 'blue')]['summoner_name'].values

        # Blue champions
        blue_champions = recent_matches[(recent_matches['match_id'] == match_id) & (
            recent_matches['team'] == 'blue')]['champion_name'].apply(lambda x: 'images/'+x+'_0.jpg').values
        prediction['Blue']['Champions'] = blue_champions

        # Red team names
        prediction['Red']['Names'] = recent_matches[(recent_matches['match_id'] == match_id) & (
            recent_matches['team'] == 'red')]['summoner_name'].values

        # Red champions
        red_champions = recent_matches[(recent_matches['match_id'] == match_id) & (
            recent_matches['team'] == 'red')]['champion_name'].apply(lambda x: 'images/'+x+'_0.jpg').values
        prediction['Red']['Champions'] = red_champions

    # Render predictions page
    return render_template('predictions.html', preds=predictions)
