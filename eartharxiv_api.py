import sys
import utils
from Preprint import Preprint
from api_token import osf_token

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

	# Count how many elements (preprints) we have in the response
	num_elements = len(json_object['data'])

	# Loop over all the response preprints, NOTE: in this example we're just testing the first
	# preprint. As the code gets developed more, we'll loop over num_elements and examine
	# all of the responses
	for i in range(1):
	
		# Response is comprised of Relationships, Links, and Attributes
		# Here we seperate them out of the response
		rel = json_object['data'][i]['relationships']
		links = json_object['data'][i]['links']
		attr = json_object['data'][i]['attributes']
		
		# Also need to extract scalar values like id and construct the download link
		id = json_object['data'][i]['id']
		download_link = "https://eartharxiv.org/" + id + "/download"
		
		# Create a Preprint object to store all the information on this preprint
		preprint = Preprint()

		# The Relationships data has links to more information
		# Use our helper function to extract those links and put them in our preprint object
		preprint.extractRelData( rel )

		# Add the id and download_link values to our object
		preprint.setScalars( id, download_link )

		# Now that we have the identifiers link, send it back to the API
		# to get the Identifier JSON and extract the actual DOI identifier
		response2 = utils.queryAPI( preprint.identifiersLink, headers )
		if response2.status_code == 200:
			json_object2 = utils.getJSON( response2 )
			utils.parseIdentifier( json_object2, preprint )
		else:
			print( "Error, HTTP status code is: ", response2.status_code )

	# The API returns 10 preprints per "page". We need to look at the Links
	# data to see if there are additional pages. TO DO: extend this section
	n = len(json_object['links'])
	
else:

	# Something went wrong with the API call/response
	print( "Error, HTTP status code is: ", response.status_code )

# Test to make sure everything is working properly. Print out the current values we have for the preprint
preprint.printValues()

# Download the preprint
print("Downloading preprint to: ", sys.argv[1])
utils.download( download_link, sys.argv[1])
