import json
import requests
import urllib.request

# Helper function to download a file from a URL
def download( url, localFile ):
	
	response = urllib.request.urlretrieve(url, localFile)

# Generic function to send a query to the API
def queryAPI( url, headers ):

	response = requests.get(url, headers=headers)
	return response

# Helper function to extract and decode JSON from API responses
def getJSON( response ):

	json_object = json.loads(response.content.decode('utf-8'))
	return json_object

# Helper function to parse JSON response and look for identifier data
def parseIdentifier ( jsonData, preprint ):

	num_elements = len( jsonData['data'] )
	for j in range( num_elements ):
		data = jsonData['data'][j]
		preprint.parseIdentifierData( data )
