import pickle
from os import listdir, getcwd


class WinPredictor():

    MODELS_PATH = getcwd().replace('\\', '/')+'/static/models/'

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

        # Find the most recent model
        file_names = listdir(self.MODELS_PATH)
        most_recent = file_names[-1]

        # print(most_recent)

        with open(self.MODELS_PATH+most_recent, 'rb') as f:
            model = pickle.load(f)
        # print(model)
        self.model = model

    def predict(self, timelines):
        # Split into X and Y and remove unnecessary columns
        X = timelines.drop(
            ['red_kills', 'red_deaths', 'winner', 'match_id'], axis=1)
        y = timelines['winner']

        predictions = self.model.predict(X)
        all_probs = self.model.predict_proba(X)

        # Max index of max probability
        ix = all_probs.argmax(1)

        max_probs = []
        for row, i in enumerate(ix):
            max_probs.append(all_probs[row][i])

        # return as (prediction, probability, actual)
        return {'pred': predictions, 'prob': max_probs, 'actual': y}
