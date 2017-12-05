class Preprint:
    
	doi = ""
	identifiersLink = ""
	citationLink = ""
	preprintProvider = ""
	identifier = ""
	download_link = ""

	def setScalars( self, id, download_link ):

		self.identifier = id
		self.download_link = download_link

	def printValues( self ):

		print( self.identifiersLink )
		print( self.citationLink )
		print( self.preprintProvider )
		print( "DOI: ", self.doi )
		print( "Identifier: ", self.identifier )
		print( "Download URL: ", self.download_link )

	def parseIdentifierData( self, idJSON ):

		if ( idJSON['attributes']['category'] == 'doi' ):
			self.doi = idJSON['attributes']['value']

	def extractRelData( self, rel ):
		        
		self.identifiersLink = rel['identifiers']['links']['related']['href'] # DOI and other identifiers
		self.citationLink = rel['citation']['links']['related']['href'] # citation details
		self.preprintProvider = rel['provider']['data']['id'] # preprint server the paper came from

		# Other data that is returned, but not captured/used at the moment
		##
        #print( rel['files'] ) # list of storage providers enabled
        #print( rel['actions'] )
		#print( rel['primary_file'] ) # details about files and folders 
		#print( rel['contributors'] ) # who can make changes to the preprint
		#print( rel['license'] ) # license details
