from RawDataWrangler import RawDataWrangler
from RawDataFormatter import RawDataFormatter
from DataValidator import DataValidator
import pandas as pd

data_loc = 'data'


def create_dataset_from_raw(count, summoner_name, region):
    """
    Gets new data from Data Wrangler every two minutes up to count or no more data.
    """
    rdw = RawDataWrangler(region, summoner_name)
    rdf = RawDataFormatter(summoner_name)
    raw_data = rdw.get_raw_match_timelines(count=count, start=0)
    formatted_df = rdf.format_data(raw_data)
    return formatted_df


def save_df_to_pickle(df, summoner_name, rank):
    df.to_pickle(path=f'{data_loc}/{summoner_name}_{rank}.pkl')
    print(f"Successfully saved {summoner_name} to pickle.")


def read_df_from_pickle(summoner_name):
    df = pd.read_pickle(f'{data_loc}/{summoner_name}.pkl')
    return df


summoner_names = ['Sasheemy', 'gnomes4', 'WinnahWyatt', 'Duckz']

plat_players = ['Band 2wice', 'MuackaPuack', 'Sabie',
                'RebornSkullyman', 'ManGoated', 'Mugzzy', 'BeboBash', 'BigMan']
diamond_players = ['']
challenger_players = ['TL Armao', 'Doublelift', 'Pobelter', 'Revenge', 'Eyla']
pro_players = ['Biofrost', 'Peng Yiliang', 'FA Bjergsen', 'liveevil',
               'SentientAI', 'blaberfish2', 'goldenglue', 'Supersonics1']

region = 'na1'

for s in plat_players[3:]:
    df = create_dataset_from_raw(1000, s, region)
    print(df.shape)
    save_df_to_pickle(df, s, 'plat')

# df = create_dataset_from_raw(1000, 'Sasheemy', 'na1')
# print(df.shape)
#save_df_to_pickle(df, 'Sasheemy')

# test_df = pd.DataFrame.from_dict({"test": [1, 2, 3], "test2": [1, 2, 3]})
# save_df_to_pickle(test_df, 'asdfasd')
