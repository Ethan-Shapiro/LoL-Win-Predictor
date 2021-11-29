import time
from RawDataWrangler import RawDataWrangler
from RawDataFormatter import RawDataFormatter
from DataValidator import DataValidator
import pandas as pd

data_loc = 'data'


def create_dataset_from_raw(count, summoner_name, region):
    """
    Gets new data from Data Wrangler every two minutes up to count or no more data.
    """
    rdw = RawDataWrangler('blank')
    rdf = RawDataFormatter(summoner_name)
    rdw.player = rdw.validate_summoner_name(summoner_name, region)
    raw_data = rdw.get_raw_match_timelines(
        summoner_name, region, count=count, start=0)
    formatted_df = rdf.format_timeline_data(raw_data)
    return formatted_df


def save_df_to_csv(df, summoner_name, rank):
    df.to_csv(f'{data_loc}/{rank}_{summoner_name}.csv', index=False)
    print(f"Successfully saved {summoner_name} to csv.")


def read_df_from_csv(summoner_name):
    df = pd.read_csv(f'{data_loc}/{summoner_name}.csv')
    return df


friend_names = ['Sasheemy', 'gnomes4', 'WinnahWyatt', 'Duckz']

# TODO Add Iron Players
iron_players = []
bronze_players = ['Ativva', '0SaN', 'TheOnlySRT', 'ChrisLeodon']
silver_players = ['jamesbong3', 'Adamik',
                  'Kei1245', 'Dark Cosmic 4', 'Torqids']
gold_players = ['ddnycee', 'Sadeki', 'NenoPanda', 'Huntottosaw', 'Qcpatron']
plat_players = ['Band 2wice', 'MuackaPuack', 'Sabie',
                'RebornSkullyman', 'ManGoated', 'Mugzzy', 'BeboBash', 'BigMan']
diamond_players = ['PayXtoXwin', 'gay rat',
                   'vincoin', 'Yassuo', 'congqiancongqian']
challenger_players = ['TL Armao', 'Doublelift', 'Pobelter', 'Revenge', 'Eyla']
pro_players = ['Biofrost', 'Peng Yiliang', 'FA Bjergsen', 'liveevil',
               'SentientAI', 'blaberfish2', 'goldenglue', 'Supersonics1']

region = 'na1'

all_players = diamond_players + plat_players + \
    gold_players + silver_players + bronze_players
# i = 0
# while i < len(all_players):
#     try:
#         df = create_dataset_from_raw(1000, all_players[i], region)
#         print(df.shape)
#         save_df_to_csv(df, all_players[i], 'pro')
#         i += 1
#     except:
#         # Wait for a minute before trying again
#         time.sleep(60)


# for s in bronze_players:
#     df = create_dataset_from_raw(1000, s, region)
#     print(df.shape)
#     save_df_to_csv(df, s, 'bronze')

df = create_dataset_from_raw(3, 'oWill', 'na1')
print(df.shape)
save_df_to_csv(df, 'oWill', 'UNSEENDATA')

# test_df = pd.DataFrame.from_dict({"test": [1, 2, 3], "test2": [1, 2, 3]})
# save_df_to_pickle(test_df, 'asdfasd')
