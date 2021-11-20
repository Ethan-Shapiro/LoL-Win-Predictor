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

    def format_data(self, raw_timelines: list) -> pd.DataFrame:

        if raw_timelines is None:
            return

        timelines_formatted = {}

        i = 0
        for timeline in raw_timelines:
            i += 1
            # Don't use games less than 15 minutes long
            # Length will be 16 because the i = 15 frame holds
            # The data from min 14-15
            if len(timeline['info']['frames']) < 16:
                continue

            # Determine each player's team first
            player_teams = self.determine_teams(
                timeline['info']['frames'][0]['participantFrames'])

            # Participants only need to be processed once at the 15 minute mark

            player_data = self.process_participants(
                timeline['info']['frames'][15]['participantFrames'], player_teams)
            # print(player_data)

            # send the frames for event data to be processed
            event_data = self.process_events(
                timeline['info']['frames'], player_teams)
            # print(event_data)

            # Combines the above data into a dictionary of lists
            game_dict = {**player_data, **event_data}

            # Get winning team
            last_frame_i = len(timeline['info']['frames']) - 1
            win_event_index = len(
                timeline['info']['frames'][last_frame_i]['events']) - 1
            winner_raw = timeline['info']['frames'][last_frame_i]['events'][win_event_index]['winningTeam']
            BLUE_TEAM_ID = 100
            RED_TEAM_ID = 200

            if winner_raw == BLUE_TEAM_ID:
                winner = 'blue'
            elif winner_raw == RED_TEAM_ID:
                winner = 'red'
            else:
                continue

            # Add timeline's date.
            try:
                last_event_i = len(
                    timeline['info']['frames'][last_frame_i]['events']) - 1
                unix_date = timeline['info']['frames'][last_frame_i]['events'][last_event_i]['realTimestamp']

            except KeyError:
                unix_date = None
                print(f"Error at {i}")

            # Add date and winner to game_dict
            game_dict['unix_date'] = unix_date
            game_dict['winner'] = winner

            # Add game_dict to complete_dict
            for k, v in game_dict.items():
                if k not in timelines_formatted:
                    timelines_formatted[k] = [v]
                else:
                    timelines_formatted[k].append(v)
        return pd.DataFrame.from_dict(timelines_formatted)

    def process_participants(self, participants: list, player_team_map: dict) -> dict:
        """
        A method that formats the participant info and returns it by team.
        """
        blue_keys = ['blue_gold', 'blue_cs', 'blue_jg', 'blue_xp']

        red_keys = [x.replace('blue', 'red') for x in blue_keys]

        blank_keys = ['_gold', '_cs', '_xp', '_jg']

        all_keys = blue_keys + red_keys

        team_data = {k: 0 for k in all_keys}
        for id in participants:
            # Add appropriate values depending on team
            team = player_team_map[id]

            # Add Gold
            team_data[team+blank_keys[0]] += participants[id]['totalGold']

            # Add minions killed (Creep Score)
            team_data[team+blank_keys[1]] += participants[id]['minionsKilled']

            # Add experience (xp)
            team_data[team+blank_keys[2]] += participants[id]['xp']

            # Add jungle minions killed
            team_data[team+blank_keys[3]
                      ] += participants[id]['jungleMinionsKilled']
        return team_data

    def process_events(self, frames: list, player_team_map: dict) -> dict:
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

        blank_events = ['_wards_placed', '_wards_destroyed',
                        '_air_dragons', '_fire_dragons', '_earth_dragons',
                        '_ocean_dragons', '_turrets_destroyed',
                        '_rift_heralds', '_inhibitors_destroyed',
                        '_kills', '_assists', '_deaths']

        blue_events = ['blue'+x for x in blank_events]

        red_events = ['red'+x for x in blank_events]

        # Intiailize events dictionary
        all_keys = blue_events + red_events
        team_events = {k: 0 for k in all_keys}

        fifteen_min_to_ms = 900000

        for i, frame in enumerate(frames):

            if i > 16:
                break

            # Loop through frame data
            for data in frame['events']:

                # Ensure timestamp is within bounds
                # If not, all next frames are out of bounds as well
                if data['timestamp'] > fifteen_min_to_ms:
                    break

                # Check for killing anything & killerId is legitament
                if 'killerId' not in data and data['type'] != 'WARD_PLACED':
                    continue

                # Check killerId is legitament
                if 'killerId' in data:
                    if data['killerId'] < 1 or data['killerId'] > 10:
                        continue

                # Check creatorId is legitament
                if data['type'] == 'WARD_PLACED':
                    if data['creatorId'] <= 0:
                        continue

                action_type = data['type']

                # Kills, Deaths, and Assists
                if action_type == 'CHAMPION_KILL':

                    # Add Kill to Killer's team
                    killer_team = player_team_map[str(data['killerId'])]
                    team_events[killer_team+'_kills'] += 1

                    # Add Assists to Killer's team
                    if 'assistingParticipantIds' in data:
                        team_events[killer_team +
                                    '_assists'] += len(data['assistingParticipantIds'])

                    # Add death to other team
                    victim_team = player_team_map[str(data['victimId'])]
                    team_events[victim_team+'_deaths'] += 1

                # Wards
                if action_type == 'WARD_KILL':

                    # Add ward destroyed to team
                    killer_team = player_team_map[str(data['killerId'])]
                    team_events[killer_team+'_wards_destroyed'] += 1

                if action_type == 'WARD_PLACED':

                    # Add ward placed to team
                    creator_team = player_team_map[str(data['creatorId'])]
                    team_events[creator_team+'_wards_placed'] += 1

                # Epic Monsters
                if action_type == 'ELITE_MONSTER_KILL':

                    killer_team = player_team_map[str(data['killerId'])]

                    # Rift Herald
                    if data['monsterType'] == 'RIFTHERALD':
                        team_events[killer_team+'_rift_heralds'] += 1

                    # Dragons
                    if data['monsterType'] == 'DRAGON':

                        # Fire Dragons
                        if data['monsterSubType'] == 'FIRE_DRAGON':
                            team_events[killer_team+'_fire_dragons'] += 1

                        # Ocean Dragons
                        if data['monsterSubType'] == 'OCEAN_DRAGON':
                            team_events[killer_team+'_ocean_dragons'] += 1

                        # Air Dragons
                        if data['monsterSubType'] == 'AIR_DRAGON':
                            team_events[killer_team+'_air_dragons'] += 1

                        # Earth Dragons
                        if data['monsterSubType'] == 'EARTH_DRAGON':
                            team_events[killer_team+'_earth_dragons'] += 1
                # Buildings
                if action_type == 'BUILDING_KILL':
                    killer_team = player_team_map[str(data['killerId'])]

                    # Turrets
                    if data['buildingType'] == 'TOWER_BUILDING':
                        team_events[killer_team+'_turrets_destroyed'] += 1

                    # Inhibitors
                    if data['buildingType'] == 'INHIBITOR_BUILDING':
                        team_events[killer_team+'_inhibitors_destroyed'] += 1
        return team_events

    def determine_teams(self, players):
        """
        A method that returns the team ID of a player given their position
        at the start of the game.
        Parameter(s):
            position (x, y): Position of player
        """

        player_team_map = {}
        # Team 100 starts within 1000 units of the origin in both axis
        blue_team_starting_threshhold = 1000
        for p_id in players:
            position = players[p_id]['position']
            if position['x'] < blue_team_starting_threshhold and position['y'] < blue_team_starting_threshhold:
                player_team_map[p_id] = 'blue'
            else:
                player_team_map[p_id] = 'red'
        return player_team_map


# raw_data_wrangler = RawDataWrangler.RawDataWrangler('na1', 'Sasheemy')
# raw_timelines = raw_data_wrangler.get_raw_match_timelines(count=1)
# raw_data_formatter = RawDataFormatter('Sasheemy')
# raw_data = raw_data_formatter.format_data(raw_timelines)
