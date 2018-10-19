import requests

def parseDoiResponse( response ):
         m={'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
         doi, url, year, month, publisher, author, title, journal = "", "", "", "", "", "", "", ""
         parts = response.split(",")
         for x in parts:
              p = x.split("=")
              if p[0].strip() == "doi":
                   doi = p[1].strip()
              if p[0].strip() == "url":
                   url = p[1].strip()
              if p[0].strip() == "publisher":
                   publisher = p[1].strip()
              if p[0].strip() == "author":
                   author = p[1].strip()
              if p[0].strip == "title":
                   title = p[1].strip()
              if p[0].strip == "journal":
                   journal = p[1].strip()
              if p[0].strip() == "year":
                   year = p[1].strip()
              if p[0].strip() == "month":
                   month = p[1].strip()
                   month = month[1:-1] # remove { and } as in {sep}
                   month = m[month.lower()]
         return doi, url, year, month, publisher, author, title, journal

class Preprint:

        def __init__ (self):
                self.doi = ""
                self.identifiersLink = ""
                self.citationLink = ""
                self.preprintProvider = ""
                self.identifier = ""
                self.html_link = ""
                self.download_link = ""
                self.authors = []
                self.title = ""

                self.date_last_transitioned = ""
                self.date_modified = ""
                self.description = ""
                self.date_published = ""
                self.preprint_doi_created = ""

                self.peer_review_url = ""
                self.peer_review_publisher = ""
                self.peer_review_author = ""
                self.peer_review_title = ""
                self.peer_review_journal = ""
                self.peer_review_doi = ""
                self.peer_review_publish_date = ""

                # use a set instead of a list for efficiency
                # we're going to add only unique keywords and set update is faster
                self.keywords = set()

        def getKeywords( self ):
                return self.keywords
        
        def getDatePublished( self ):
                return self.date_published
        
        def setScalars( self, id, html_link, download_link ):

                self.identifier = id
                self.html_link = html_link
                self.download_link = download_link

        def printValues( self ):

                print( )
                print( "Preprint Service: ", self.preprintProvider )
                print( "Identifier Link: ", self.identifiersLink )
                print( "Citation Link: ", self.citationLink )
                print( "DOI: ", self.doi )
                print( "Identifier: ", self.identifier )
                print( "Download URL: ", self.download_link )
                print( "This preprint's homepage: ", self.html_link )
                print( "Date Last Transitioned: ", self.date_last_transitioned ) 
                print( "Date Modified: ", self.date_modified ) 
                print( "Abstract: ", self.description ) 
                print( "Date Published:", self.date_published ) 
                print( "Preprint DOI Created: ", self.preprint_doi_created ) 
                if ( self.peer_review_doi != "" ):
                     print( "Peer Review DOI: ", self.peer_review_doi )
                     print( "Peer Review Publication Date: ", self.peer_review_publish_date )
                for keyword in self.keywords:
                        print( "Keyword: ", keyword )

        def parseLinkData( self, linkJSON ):

                if 'doi' in linkJSON:
                     self.peer_review_doi = linkJSON['doi']
                     headers = {"accept": "application/x-bibtex"}
                     r = requests.get(self.peer_review_doi, headers = headers)
                     doi, url, year, month, publisher, author, title, journal = parseDoiResponse( r.text )
                     if ( month != "" ): # not all doi's return a month
                       if ( month < 10 ):
                          month = '0' + str(month)
                       else:
                          month = str(month)
                     self.peer_review_publish_date = str(year) + '-' + month
                     self.peer_review_url = url
                     self.peer_review_publisher = publisher
                     self.peer_review_author = author
                     self.peer_review_title = title
                     self.peer_review_journal = journal

        def parseIdentifierData( self, idJSON ):

                if ( idJSON['attributes']['category'] == 'doi' ):
                        self.doi = 'https://dx.doi.org/' + idJSON['attributes']['value']

        def parseAttrData( self, attr ):

                self.date_last_transitioned = attr['date_last_transitioned']
                self.date_modified = attr['date_modified']
                self.description = attr['description']
                self.date_published = attr['date_published']
                self.preprint_doi_created = attr['preprint_doi_created'] 
                n = len( attr['subjects'] )
                for i in range(n):
                        keyword = attr['subjects'][i]
                        n2 = len( keyword )
                        for j in range(n2):
                                # API returns the full keyword taxonomy, 
                                # i.e Physical Sciences and Mathematics -> Earth Sciences -> Geology
                                # We don't need to capture this each time
                                # If we already have Physical Sciences and Mathematics -> Earth Sciences then just grab Geology
                                if keyword[j]['text'] not in self.keywords:  # faster than `keyword not in {list}`
                                        self.keywords.add( keyword[j]['text'] )


        def parseRelData( self, rel ):
                        
                self.identifiersLink = rel['identifiers']['links']['related']['href'] # DOI and other identifiers
                self.citationLink = rel['citation']['links']['related']['href'] # citation details
                #self.preprintProvider = rel['provider']['data']['id'] # preprint server the paper came from

                # Other data that is returned, but not captured/used at the moment
                ##
                #print( rel['files'] ) # list of storage providers enabled
                #print( rel['actions'] )
                #print( rel['primary_file'] ) # details about files and folders 
                #print( rel['contributors'] ) # who can make changes to the preprint
                #print( rel['license'] ) # license details
