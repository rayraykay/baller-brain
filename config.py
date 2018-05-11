class SPORTS_FEEDS_CONSTANTS():
	###
	# CONSTANTS FOR INDIVIDUAL DATA FEEDS (please refer to the API docs on the sports feeds website
	# to see what kinds of data feeds there are)
	###

	# Some clarifications:
	# - ENDING_URL: Each data feed requires an ending URL. The specific syntax can be found on the API docs.i
	# - IMPORTANT: Make sure all feeds are in .csv format, or else you'll crash the program!
	# - DESIRED_COLS: When using this data feed, you need to specify desired columns of data from the matrix returned from the feed's API.
	# For example, for scoreboard stats, columns 15, 19, 23, and 24 specify team abbreivations and their scores for a given
	# game. This variable should be in list form with integers.
	# - INDICES: The indices after the desired columns correspond to columns in the final data matrix once the undesired columns are
	# filtered out.

	ENDING_URLS = { "overall":			"overall_team_standings.csv?teamstats=W,L,PTS,PTSA", 
					"scoreboard":		"scoreboard.csv?", 
	}

	# CONSTANTS FOR SCOREBOARD STATS

	SB_DESIRED_COLS					= [15, 19, 23, 24]
	SB_AWAY_TEAM_ABBR_INDEX			= 0
	SB_HOME_TEAM_ABBR_INDEX			= 1
	SB_AWAY_TEAM_SCORE_INDEX		= 2
	SB_HOME_TEAM_SCORE_INDEX		= 3

	# CONSTANTS FOR OVERALL TEAM STATS

	OVR_DESIRED_COLS				= [2] + list(range(7,11))
	OVR_TEAM_ABBR					= 0
	OVR_WINS						= 1
	OVR_LOSSES						= 2
	OVR_POINTS						= 3
	OVR_POINTS_AGAINST				= 4

	###
	# GENERAL CONSTANTS FOR SPORTSFEEDS
	###

	USERNAME_PASSWORD_FILENAME 		= "username_password.txt"

	SEASON_DURATION	    			= 10	    # 7 months, so roughly 31*7
	SEASON_TIMEDELTA	    		= 0         # you can set this to request starting at a start date delayed by REG_SEASON_TIMEDELTA days
		                                        # ex. if this is set to 10, and if you request data for the 2017-18 season, then the data 
		                                        # will start on 20171028 instead

	SEASONS                         = [
		                                "2015-2016-regular",
		                                "2016-playoff",
		                                "2016-2017-regular",
		                                "2017-playoff",
		                                "2017-2018-regular",
		                              ]

	URL_START                       = "https://api.mysportsfeeds.com/v1.2/pull/nba/"

	START_DATES                     = { "2015-2016-regular": 20151028, 
										"2016-playoff":		 20160416, 
										"2016-2017-regular": 20161025, 
										"2017-playoff":		 20170415, 
										"2017-2018-regular": 20171018
										}

	REG_START_DATE_2015_2016        = 20151028
	REG_START_DATE_2016_2017		= 20161025
	REG_START_DATE_2017_2018        = 20171018


	# CONSTANTS FOR DEBUG FUNCTIONS

	DEBUG_GET_URL_LIST				= [
		    "https://api.mysportsfeeds.com/v1.2/pull/nba/2016-2017-regular/overall_team_standings.csv?teamstats=W,L,PTS,PTSA",
		    "https://api.mysportsfeeds.com/v1.2/pull/nba/2016-2017-regular/scoreboard.csv?",
	]
	DEBUG_GET_URL					= DEBUG_GET_URL_LIST[1]
	DEBUG_DESIRED_COLS				= OVR_DESIRED_COLS

	@classmethod
	def _form_url(cls, season, feed_type):
		if season in cls.SEASONS and feed_type in cls.ENDING_URLS:
			return cls.URL_START + season + "/" + cls.ENDING_URLS[feed_type]
		else:
			print("Error: input parameters not found in config.py, return empty string")
			return ""

class MACHINE_LEARNING_CONSTANTS():
    _p = 3 # placeholder
