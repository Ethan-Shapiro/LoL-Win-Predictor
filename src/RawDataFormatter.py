import pandas as pd
import RawDataWrangler


class RawDataFormatter():
    """
    A class that formats the raw match data from RiotWatcher into an understandable
    pandas data frame.
    """

    def __init__(self, summoner_name):
        self._data = {}
        self._summoner_name = summoner_name

    def format_data(self, raw_timelines: list) -> dict:
        for timeline in raw_timelines:

            # Participants only need to be processed once at the 15 minute mark
            player_teams = self.determine_teams(
                timeline['info']['frames'][0]['participantFrames'])

            players_15_min = timeline['info']['frames'][16]['participantFrames']

            player_data = self.process_participants(players_15_min)

            # send the frames for event data to be processed
            event_data = self.process_events(timeline)

            # Combines the above data into a dictionary of lists

    def process_participants(self, participants: list, player_team_map: dict) -> dict:
        """
        A method that formats the participant info and returns it by team.
        """
        blue_keys = ['blue_gold', 'blue_cs', 'blue_jg', 'blue_xp']

        red_keys = [x.replace('blue', 'red') for x in blue_keys]

        all_keys = blue_keys + red_keys

        team_data = {k: 0 for k in all_keys}
        for id in participants:
            # Add appropriate values depending on team
            if player_team_map[id] == self.BLUE_TEAM_ID:
                keys = blue_keys
            else:
                keys = red_keys

            # Add Gold
            team_data[keys[0]] += participants[id]['totalGold']

            # Add minions killed (Creep Score)
            team_data[keys[0]] += participants[id]['minionsKilled']

            # Add Jungle minions killed
            team_data[keys[0]] += participants[id]['jungleMinionsKilled']

            # Add experience (xp)
            team_data[keys[0]] += participants[id]['xp']

            # Add kills
            team_data[keys[0]] += participants[id]['jungleMinionsKilled']

    def process_events(self, frames: list) -> dict:
        """
        Processes the event data for each team and returns it.
        """
        # For wards, check type = 'WARD_PLACED'
        # For wards, check type = 'WARD_KILL'
        # TeamId 100 = Blue
        # TeamId 200 = Red

        # For dragons and heralds type = ELITE_MONSTER_KILL
        # Check monsterType for herald, dragon, baron, or elder
        # Dragon monsterSubType = AIR_DRAGON, FIRE_DRAGON, EARTH_DRAGON, OCEAN_DRAGON
        # Baron monsterType = 'BARON_NASHOR'
        # Herald monsterType = RIFTHERALD

        # tower destroyed type = 'BUILDING_KILL'
        # buildingType = 'TOWER_BUILDING'
        # Plates type = TURRET_PLATE_DESTROYED

        # Inhibitor kill type = 'BUILDING_KILL'
        # Building Type = 'INHIBITOR_BUILDING'

        blue_events = ['blue_wards_placed', 'blue_wards_destroyed',
                       'blue_air_dragons', 'blue_fire_dragons', 'blue_earth_dragons',
                       'blue_ocean_dragons', 'blue_turret_plates', 'blue_turrets_destroyed',
                       'blue_rift_heralds', 'blue_barons', 'blue_inhibitors',
                       'blue_kills', 'blue_assists', 'blue_deaths']

        red_events = [x.replace('blue', 'red') for x in blue_events]

        all_keys = blue_events + red_events

        team_events = {k: 0 for k in all_keys}

        for frame in frames:

            # Loop through frame data
            for data in frame:

                # Check for killing anything
                if 'killerId' not in data:
                    continue

                kill_type = data['type']

                # Add for Kills, Deaths, and Assists
                if kill_type == 'CHAMPION_KILL':

                    # Add Kills to killer team
                    team_events['']

    def determine_team(self, position):
        """
        A method that returns the team ID of a player given their position
        at the start of the game.
        Parameter(s): 
            position (x, y): Position of player
        """
        BLUE_TEAM_ID = 100
        RED_TEAM_ID = 200
        # Team 100 starts within 1000 units of the origin in both axis
        team_100_starting_threshold = 1000
        if position[0] < team_100_starting_threshold and position[1] < team_100_starting_threshold:
            return 100
        return 200


raw_data_wrangler = RawDataWrangler.RawDataWrangler('na1', 'Sasheemy')
raw_data = raw_data_wrangler.get_raw_match_data()

raw_data[-1]['info']['participants'][0].keys()

raw_data[-1]['metadata']
