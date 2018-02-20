import requests
import base64
import csv
import numpy

import listmanip as lm

# try python 2, otherwise python 3
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

from datetime import datetime, date, timedelta

# import configuration class
from config import SPORTS_FEEDS_CONSTANTS as SF 

class Sports_Feeds_Scraper():
	def __init__(self, season, feed_type):
		if season not in SF.SEASONS:
			print("Error: Season doesn't exist. Setting to 2016-2017 regular.")
			self.season = "2016-2017-regular"
		else:
			self.season = season
			print("Setting season to " + season)

		if feed_type not in SF.ENDING_URLS:
			print("Feed type not found in ENDING_URLS. Setting to overall.")
			self.feed_type = "overall"
		else:
			self.feed_type = feed_type
			print("Setting season to " + feed_type)

	# WARNING: The following functions with a leading underscoreare meant to be 
    # internal to the class, so please refrain from changing this function unless 
    # you really know what you're doing.

	# returns a 2d list using the csv content from 
	# mysportsfeeds
	# the first empty column counts in the indexing
	# the first row is discounted, as it's just headers

	@staticmethod
	def _process_csv_to_2d(csv_content, desired_cols):
		csv_file = StringIO(csv_content)
		csv_reader = csv.reader(csv_file)

		row = 0;
		col = 0;
		result = []
		headers = []
		selected_headers = []
		for row_item in csv_reader:
			if row > 0:
				col = 0
				row_to_insert = []
				for col_item in row_item:
					if col in desired_cols:
						row_to_insert.append(col_item)
					col = col + 1
				result.append(row_to_insert)
			else:
				for header in row_item:
					headers.append(header)
					if col in desired_cols:
						selected_headers.append(header)
			row = row + 1

		return result, headers

	@staticmethod
	def _create_header(username, password):
		header_string = "Basic " + base64.b64encode("{}:{}".format(username, password).encode("utf-8")).decode("ascii")
		return { "Authorization": header_string }
	
	# returns a list of game results, where the each list item is:
	# [away team abbr, home team abbr, whether away team won]
	def _get_game_outcomes_for_season(self):
		current_date = datetime.strptime(str(SF.START_DATES[self.season]), "%Y%m%d").date()
		current_date = current_date + timedelta(SF.SEASON_TIMEDELTA)
		raw_matrix = []

		# save current object state
		original_feed_type = self.feed_type
		self.feed_type = "scoreboard"

		for i in range(SF.SEASON_DURATION):
			params = { "fordate": current_date.strftime("%Y%m%d") }
			content = self._get_content(params)

			current_raw_games, headers = self._process_csv_to_2d(content, SF.SB_DESIRED_COLS)
			for game in current_raw_games:
				away_team_abbr = game[SF.SB_AWAY_TEAM_ABBR_INDEX]
				home_team_abbr = game[SF.SB_HOME_TEAM_ABBR_INDEX]
				result = int(game[SF.SB_AWAY_TEAM_SCORE_INDEX] > game[SF.SB_HOME_TEAM_SCORE_INDEX])

				game_to_append = [away_team_abbr, home_team_abbr, result]
				raw_matrix.append(game_to_append)

			current_date = current_date + timedelta(1)

		# restore original type
		self.feed_type = original_feed_type

		return raw_matrix


	def _get_content(self, _params):
		open_file = open(SF.USERNAME_PASSWORD_FILENAME, 'rb')
		read_rows = csv.reader(open_file)
		username_password = []
		for row in read_rows:
			del username_password[:]
			for word in row:
				username_password.append(word)

		username = username_password[0]
		password = username_password[1]

		resp_code = 429 # this is the throttled code
		while (resp_code == 429):
			try:
				response = requests.get(
					url = SF._form_url(self.season, self.feed_type),
					params = _params,
					headers= self._create_header(username, password)
				)
				resp_code = response.status_code	
			except requests.exceptions.RequestException:
				print("Failure to GET data.")

			if (resp_code == 429):
				print("We have been throttled, received response 429. Going to put the program in an infinite loop for 300 seconds...")
				begin_time = datetime.now()
				current_time = datetime.now()
				while ((current_time - begin_time).total_seconds() > 300):
					current_time = datetime.now()

		# should have some addtional error-checking, but
		# just return content for now
		return response.content

	# returns a list of game results, where the each list item is:
	# [away team abbr, home team abbr, whether away team won]
	def _get_game_outcomes_for_season(self):
		current_date = datetime.strptime(str(SF.START_DATES[self.season]), "%Y%m%d").date()
		current_date = current_date + timedelta(SF.SEASON_TIMEDELTA)
		raw_matrix = []

		# save current object state
		original_feed_type = self.feed_type
		self.feed_type = "scoreboard"

		for i in range(SF.SEASON_DURATION):
			params = { "fordate": current_date.strftime("%Y%m%d") }
			content = self._get_content(params)

			current_raw_games, headers = self._process_csv_to_2d(content, SF.SB_DESIRED_COLS)
			for game in current_raw_games:
				away_team_abbr = game[SF.SB_AWAY_TEAM_ABBR_INDEX]
				home_team_abbr = game[SF.SB_HOME_TEAM_ABBR_INDEX]
				result = int(game[SF.SB_AWAY_TEAM_SCORE_INDEX] > game[SF.SB_HOME_TEAM_SCORE_INDEX])

				game_to_append = [away_team_abbr, home_team_abbr, result]
				raw_matrix.append(game_to_append)

			current_date = current_date + timedelta(1)

		# restore original type
		self.feed_type = original_feed_type

		return raw_matrix

	# returns a hashmap of data for teams
	# the keys are the team abbreviations
	def get_team_data_hash(self, desired_cols):		
		teams, headers = process_csv_to_2d(content, OVR_DESIRED_COLS)
	
		data_hash = {}
	
		# initialize with w/l ratio and points/points against ratio
		for team in teams:
			#win_loss = float(team[OVR_WINS])/float(team[OVR_LOSSES])
			pts_pts_against = float(team[OVR_POINTS])/float(team[OVR_POINTS_AGAINST])
			data_hash[team[OVR_TEAM_ABBR]] = [pts_pts_against]
	
		return data_hash

s = Sports_Feeds_Scraper("2016-2017-regular", "overall")
c = s._get_content({})
print(c)
print(numpy.array(s._get_game_outcomes_for_season()))
