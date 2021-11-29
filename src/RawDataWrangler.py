from riotwatcher import LolWatcher, ApiError
import time


class RawDataWrangler():

    def __init__(self, API_KEY: str):
        """
        Intializes a RawDataWrangler Object with an initial value for region
        and summoner_name.
        """
        self._lol_watcher = LolWatcher(API_KEY)
        self.player = None

    def validate_summoner_name(self, summoner_name, region):
        """
        A function that validates a summoner name exists in the league of legends region.
        """
        try:
            player = self._lol_watcher.summoner.by_name(
                region=region, summoner_name=summoner_name)
            return player
        except ApiError as e:
            return False

    def get_summoner_match_ids(self, summoner_name: str, region: str, count=100, start=0) -> set:
        """
        Attempts to query the match ids for the  summoner_name in the region. 
        Returns a set of match ids if successful.
        If query fails, returns a string with error message.
        If query succeeds but there are no matches, returns an empty set.
        """
        MAX_MATCHES = 100
        if count > MAX_MATCHES:
            count = MAX_MATCHES
        if count < 0:
            count = 0

        if self.player == False:
            print(
                f'No Summoner name {summoner_name} found in region {region}.')
            print(f'Possible invalid API key as well.')
            return None

        # Regions for match information are combined by locations

        def region_to_match_region(region: str):
            AMERICAS = ['na1', 'br1', 'la1', 'la2', 'oc1']
            ASIA = ['jp1', 'kr']
            EUROPE = ['eun1', 'euw1', 'tr1', 'ru']
            MATCH_REGION_MAP = {'AMERICAS': AMERICAS,
                                'ASIA': ASIA,
                                'EUROPE': EUROPE}
            for k, v in MATCH_REGION_MAP.items():
                if region in v:
                    return k
            return None

        # Get match ids of each match for both ranked and normal matches from the past 90 days.
        # If no matches are found, the set will be empty

        seconds_in_90_days = 86_400*90

        SEASON_2021_END = 1636984237

        try:
            raw_ranked_matches = self._lol_watcher.match.matchlist_by_puuid(region=region_to_match_region(region),
                                                                            end_time=SEASON_2021_END,
                                                                            puuid=self.player['puuid'],
                                                                            type='ranked',
                                                                            start=start,
                                                                            count=count)
        except ApiError:
            print(f'No matches found for {region} found in region {region}.')
            return None

        return set(raw_ranked_matches)

    def test_match_ids(self):
        return set(['NA1_4079641497', 'NA1_4058548214', 'NA1_4063957371', 'NA1_4098778351', 'NA1_4065437986',
                    'NA1_4060628939', 'NA1_4077631173', 'NA1_4082625326', 'NA1_4080583576', 'NA1_4060833887', 'NA1_4069677834',
                    'NA1_4085494880', 'NA1_4069599479', 'NA1_4060772904', 'NA1_4087781804', 'NA1_4075199495', 'NA1_4051361426', 'NA1_4074441749',
                    'NA1_4059979980', 'NA1_4057955324', 'NA1_4080486962', 'NA1_4072127595', 'NA1_4057990128', 'NA1_4051355605', 'NA1_4077860954',
                    'NA1_4060713305', 'NA1_4052670743', 'NA1_4054872174', 'NA1_4052747854', 'NA1_4068975121', 'NA1_4074355386', 'NA1_4056965836',
                    'NA1_4052663250', 'NA1_4061906347', 'NA1_4088225098', 'NA1_4065368158', 'NA1_4068893964', 'NA1_4057977402', 'NA1_4061852198',
                    'NA1_4057843968', 'NA1_4074231475', 'NA1_4052630272', 'NA1_4074188564', 'NA1_4080540735', 'NA1_4056009165', 'NA1_4088577342',
                    'NA1_4077122518', 'NA1_4075250999', 'NA1_4074448620', 'NA1_4074224521', 'NA1_4054076690', 'NA1_4054340872', 'NA1_4079787745',
                    'NA1_4069316718', 'NA1_4068990127', 'NA1_4057144817', 'NA1_4056616603', 'NA1_4075768264', 'NA1_4082276199', 'NA1_4051289608',
                    'NA1_4087492483', 'NA1_4063017974', 'NA1_4086326457', 'NA1_4061542073', 'NA1_4085487011', 'NA1_4090343659', 'NA1_4087439725',
                    'NA1_4086166050', 'NA1_4073914657', 'NA1_4069363955', 'NA1_4092468225', 'NA1_4069673990', 'NA1_4070631254', 'NA1_4054946649',
                    'NA1_4053667133', 'NA1_4074298422', 'NA1_4056618948', 'NA1_4057119924', 'NA1_4052685492', 'NA1_4096884980', 'NA1_4076202469',
                    'NA1_4056064098', 'NA1_4085522475', 'NA1_4086169692', 'NA1_4086340936', 'NA1_4053693172', 'NA1_4060688754', 'NA1_4076076117',
                    'NA1_4063954016', 'NA1_4064186416', 'NA1_4067301996', 'NA1_4056205513', 'NA1_4069342002', 'NA1_4051389305', 'NA1_4078671233',
                    'NA1_4078175008', 'NA1_4058044192', 'NA1_4054940769', 'NA1_4082607565', 'NA1_4061827761'])

    def get_raw_match_timelines(self, summoner_name: str, region: str, match_id=None, count=100, start=0):
        """
        A method that uses the list of match ids and gathers the data sequentially.
        With the Riot development key, I'm only able to create 100 queries every 2 min
        and 20 queries every 1 second.
        So I will query 19 queries and then pause for a second to not hit the limit.
        """

        match_region = self.region_to_match_region(region)
        if match_id != None:
            return [self._lol_watcher.match.timeline_by_match(
                    region=match_region, match_id=match_id)]

        timeline_info = []
        for i in range(start, count, 100):
            match_ids = self.get_summoner_match_ids(
                summoner_name=summoner_name, region=region, count=count, start=i)
            # match_ids = self.test_match_ids()
            if not match_ids:
                return None

            for j, id in enumerate(match_ids):
                timeline = self._lol_watcher.match.timeline_by_match(
                    region=match_region, match_id=id)
                timeline_info.append(timeline)
                # Sleep to make sure no more than 20 requests per second
                if j % 20 == 0:
                    time.sleep(0.5)
            print(f'got timelines {start}-{i+100}')
            # Riot watcher handles rate, but this would pause for 2 minutes otherwise
            # if count > 100 and len(timeline_info) < count:
            #     print("sleeping for 2")
            #     time.sleep(120)
            # If the len of match_ids is less than the max count, there will be no more
            # matches to get. So return what we have.
            if len(match_ids) < 100:
                print("No more matches to get.")
                break
        return timeline_info

    def get_three_recent_matches(self, match_ids: list, region):
        """
        A method that returns the 3 most recent matches for a given summoner name in the region.
        """

        match_region = self.region_to_match_region(region)

        match_info = []
        for i, id in enumerate(match_ids):
            match = self._lol_watcher.match.by_id(
                region=match_region, match_id=id)
            match_info.append(match)

        return match_info

    def region_to_match_region(self, region: str):
        AMERICAS = ['na1', 'br1', 'la1', 'la2', 'oc1']
        ASIA = ['jp1', 'kr']
        EUROPE = ['eun1', 'euw1', 'tr1', 'ru']
        MATCH_REGION_MAP = {'AMERICAS': AMERICAS,
                            'ASIA': ASIA,
                            'EUROPE': EUROPE}
        for k, v in MATCH_REGION_MAP.items():
            if region in v:
                return k
        return None

    def validate_region(self, region: str):
        assert type(region) == str, 'Region should be string'
        DEFAULT_REGION = 'na1'
        valid_regions = ['na1', 'br1', 'la1', 'la2', 'oc1',
                         'jp1', 'kr', 'eun1', 'euw1', 'tr1', 'ru']
        if region not in valid_regions:
            print(f"Invalid region! Region set to {DEFAULT_REGION}")
            self._region = DEFAULT_REGION
            return False
        self._region = region
        return True


# raw_data_wrangler = RawDataWrangler('blank')
# raw_data_wrangler.get_raw_match_data()[0]['info'].keys()
# matches = raw_data_wrangler.get_three_recent_matches("Sasheemy", "na1")
