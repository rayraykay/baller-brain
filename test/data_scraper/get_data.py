import requests
import base64
import csv
import numpy

from StringIO import StringIO

USERNAME_PASSWORD_FILENAME 		= "username_password.txt"

# debug constants
DEBUG_GET_URL					= "https://api.mysportsfeeds.com/v1.2/pull/nba/2016-2017-regular/overall_team_standings.csv?teamstats=W,L,PTS,PTSA"
DEBUG_FOR_DATE					= "20180120"
DEBUG_DESIRED_COLS				= [2] + range(7, 10 + 1)

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
		row = row + 1

	return result, headers	

def get_test():
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
			url = DEBUG_GET_URL,		
			#params = { "fordate": DEBUG_FOR_DATE },
			headers=create_header(username, password)
		)
	except requests.exceptions.RequestException:
		print("Failure to GET data.")

	content = response.content
	print(content)
	
	raw_array, headers = process_csv_to_2d(content, DEBUG_DESIRED_COLS)
	print(headers)
	data = numpy.array(raw_array)
	print(data)
