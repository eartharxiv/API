import sys
import utils
import datetime
from Preprint import Preprint
from api_token import osf_token

def countKeywords(keywords, hydro, seis, week):
        if ("Hydrology" in keywords):
                if week in hydro:
                        hydro[week] += 1
                else: hydro[week] = 1
        if ("Geophysics and Seismology" in keywords):
                if week in seis:
                        seis[week] += 1
                else: seis[week] = 1
                
def printResults(d):
        keylist = sorted(d.keys())
        for key in keylist: print(key,d[key])

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

s2017 = {}
s2018 = {}
hydrology2017 = {}
hydrology2018 = {}
seismology2017 = {}
seismology2018 = {}

# Loop over all the preprints we found
for preprint in preprints:
        date = preprint.getDatePublished()
        keywords = preprint.getKeywords()
        if (date != None):
                parts = date.split("T")
                parts = parts[0].split("-")
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                week = datetime.date(year,month,day).isocalendar()[1]
                if year == 2017:
                        if week in s2017:
                                s2017[week] = s2017[week]+1
                        else: s2017[week] = 1
                        countKeywords(keywords, hydrology2017, seismology2017, week)
                if year == 2018:
                        if week in s2018:
                                s2018[week] = s2018[week]+1
                        else: s2018[week] = 1
                        countKeywords(keywords, hydrology2018, seismology2018, week)

print("Weekly submissions")
printResults(s2017)
printResults(s2018)
print("Hydrology submissions")
printResults(hydrology2017)
printResults(hydrology2018)
print("Seismology submissions")
printResults(seismology2017)
printResults(seismology2018)
