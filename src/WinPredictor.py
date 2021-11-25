import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegressionCV, SGDClassifier
import pickle
from datetime import datetime
from os import listdir, getcwd

# Use model.predict_proba(X_test)


class WinPredictor():

    MODELS_PATH = getcwd().replace('\\', '/')+'/models'

    def load_saved_model(self):
        """
        Loads the most recent saved model in folder \models
        """
        directory_items = listdir(self.MODELS_PATH)

        if len(directory_items) <= 0:
            print("No past items found!\nPlease train a model first.")
            return None

        # Check if all are files of type
        filenames = []
        for item in directory_items:
            if item.split('.')[1] == 'pkl':
                filenames.append(item)

        # Find most recent model if there are any
        most_recent_i = -1
        most_recent_date = None
        for i, filename in enumerate(filenames):
            date_raw = filename.split("_")[0]
            date = datetime.fromisoformat(date_raw)
            if most_recent_date == None:
                most_recent_date = date
                most_recent_i = i
            elif most_recent_date < date:
                most_recent_date = date
                most_recent_i = i

        # Load the most recent file.

        return
