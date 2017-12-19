import sys
import utils
from Preprint import Preprint
from api_token import osf_token

# List to hold all our preprints
preprints = []

# URLs for OSF API

# API URL to list all preprint providers
api_url_providers = "https://api.osf.io/v2/preprint_providers"

# API URL to search/download preprints, NOTE: this is currently hard-coded to search EarthArXiv
api_url_search = "https://api.osf.io/v2/preprints/?filter[provider]=eartharxiv"

# Set up the headers to be sent as part of every API request
# osf_token is unique to each user and needs to be obtained from OSF site, it's imported from api_token.py
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(osf_token)}

# Send a request to the search API, this example just asks for all preprints at EarthArXiv
response = utils.queryAPI(api_url_search, headers)

# Check the response status code, 200 indicates everything worked as expected
if response.status_code == 200:

	# Extract the JSON data from the response
	json_object = utils.getJSON( response ) 

	# Total number of preprints in the results
	total_preprints = json_object['links']['meta']['total']

	# Parse all the preprints in the response (the current 'page' of results)
	utils.parsePreprints( preprints, json_object, headers )

	# The API returns 10 preprints per "page". We need to look at the Links
	# data to see if there are additional pages. 
	next = json_object['links']['next']

	# Send a request to the search API, this time for the next page
	while( next != None ):
		nextResponse = utils.queryAPI(next, headers)
		json_object = utils.getJSON( nextResponse ) 
		utils.parsePreprints( preprints, json_object, headers )
		next = json_object['links']['next']

else:

	# Something went wrong with the API call/response
	print( "Error connecting to API, HTTP status code is: ", response.status_code )

# Test to make sure everything is working properly. Print out the current values we have for the preprint
#preprint.printValues()

# Download the preprint
#print("Downloading preprint to: ", sys.argv[1])
#utils.download( download_link, sys.argv[1])
