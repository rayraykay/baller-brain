import requests
import base64
import csv
import numpy

import listmanip as lm

from StringIO import StringIO
from datetime import datetime, date, timedelta

USERNAME_PASSWORD_FILENAME 		= "username_password.txt"

# parameters for nba
REG_SEASON_DURATION				= 31	# 7 months, so roughly 31*7
REG_SEASON_TIMEDELTA			= 0

REG_START_DATE_2016_2017		= 20161025

SB_AWAY_TEAM_ABBR_INDEX			= 0
SB_HOME_TEAM_ABBR_INDEX			= 1
SB_AWAY_TEAM_SCORE_INDEX		= 2
SB_HOME_TEAM_SCORE_INDEX		= 3
SB_DESIRED_COLS					= [15, 19, 23, 24]

OVR_TEAM_ABBR					= 0
OVR_WINS						= 1
OVR_LOSSES						= 2
OVR_POINTS						= 3
OVR_POINTS_AGAINST				= 4
OVR_DESIRED_COLS				= [2] + range(7,11)

# debug constants
DEBUG_GET_URL_LIST				= [
	"https://api.mysportsfeeds.com/v1.2/pull/nba/2016-2017-regular/overall_team_standings.csv?teamstats=W,L,PTS,PTSA",
	"https://api.mysportsfeeds.com/v1.2/pull/nba/2016-2017-regular/scoreboard.csv?", 
]
DEBUG_GET_URL					= DEBUG_GET_URL_LIST[1] 
DEBUG_DESIRED_COLS				= OVR_DESIRED_COLS

def create_header(username, password):
	header_string = "Basic " + base64.b64encode("{}:{}".format(username, password).encode("utf-8")).decode("ascii")
	return { "Authorization": header_string }

# returns a 2d list
# the first empty column counts in the indexing
# the first row is discounted, as it's just headers
def process_csv_to_2d(csv_content, desired_cols):
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

def get_content(_url, _params):
	open_file = open(USERNAME_PASSWORD_FILENAME, 'rb')
	read_rows = csv.reader(open_file)
	username_password = []
	for row in read_rows:
		del username_password[:]
		for word in row:
			username_password.append(word)	

	username = username_password[0]
	password = username_password[1]

	try:
		response = requests.get(
			url = _url,		
			params = _params,
			headers=create_header(username, password)
		)
	except requests.exceptions.RequestException:
		print("Failure to GET data.")
	
	# should have some addtional error-checking, but 
	# just return content for now
	return response.content

def feature_matrix():
	raw_matrix = debug_get_scoreboard_for_year()
	data_hash = get_team_data_hash()
	for i in range(len(raw_matrix)):
		home_team_data = data_hash[raw_matrix[i][1]]
		away_team_data = data_hash[raw_matrix[i][0]]
		result = [raw_matrix[i][2]]
		raw_matrix[i] = home_team_data + away_team_data + result
		print(raw_matrix[i])
	return raw_matrix

# returns a hashmap of data for teams
# the keys are the team abbreviations
def get_team_data_hash():
	content = get_content(DEBUG_GET_URL_LIST[0], {})
	teams, headers = process_csv_to_2d(content, OVR_DESIRED_COLS)

	data_hash = {}

	#initialize with w/l ratio and points/points against ratio
	for team in teams:
		#win_loss = float(team[OVR_WINS])/float(team[OVR_LOSSES])
		pts_pts_against = float(team[OVR_POINTS])/float(team[OVR_POINTS_AGAINST])
		data_hash[team[OVR_TEAM_ABBR]] = [pts_pts_against]

	return data_hash

# returns a list of game results, where the each list item is:
# [away team abbr, home team abbr, whether away team won]
def debug_get_scoreboard_for_year():
	"Getting the scoreboard for the year..."
	current_date = datetime.strptime(str(REG_START_DATE_2016_2017), "%Y%m%d").date()
	current_date = current_date + timedelta(REG_SEASON_TIMEDELTA)
	raw_matrix = []	
	
	for i in range(REG_SEASON_DURATION):
		params = { "fordate": current_date.strftime("%Y%m%d") }
		content = get_content(DEBUG_GET_URL_LIST[1], params)
	
		current_raw_games, headers = process_csv_to_2d(content, SB_DESIRED_COLS)
		for game in current_raw_games:
			away_team_abbr = game[SB_AWAY_TEAM_ABBR_INDEX]
			home_team_abbr = game[SB_HOME_TEAM_ABBR_INDEX]
			result = int(game[SB_AWAY_TEAM_SCORE_INDEX] > game[SB_HOME_TEAM_SCORE_INDEX])
			
			game_to_append = [away_team_abbr, home_team_abbr, result]
			raw_matrix.append(game_to_append)
			
		current_date = current_date + timedelta(1)

	return raw_matrix

def debug_print_content(content):
	print(content)

	raw_array, headers = process_csv_to_2d(content, DEBUG_DESIRED_COLS)

	# display headers nicely
	print("Displaying headers...")
	for i in range(len(headers)):
		print("Header " + str(i) + ": " + str(headers[i]))

	# display selected matrix
	selected_headers = lm.selected_items(headers, DEBUG_DESIRED_COLS) 
	print(selected_headers)
	data = numpy.array(raw_array)
	print(data)

