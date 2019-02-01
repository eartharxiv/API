import sys
import utils
from Preprint import Preprint
from callOsfApi import callOsfApi

# command line inputs
# full path and filename of output summary file 
summaryFile = sys.argv[1]

# print out status messages as we go along (True or False)
verbose = sys.argv[2]

# start date - YYYY-MM-DD we should start the index from
startDate = sys.argv[3]

# preprint provider
provider = 'eartharxiv'

# get the papers
preprints = callOsfApi(provider, startDate, verbose)

# open log files for writing 
l = open(summaryFile, 'w')

# loop over all the papers we found
n = len(preprints)
line = "Preprints submitted this month: " + str(n)
print( line, file=l )
print( " ", file=l )
count = 1
for preprint in preprints:

   # status update
   if verbose: print("Working on preprint", count, "of", n)
   count += 1

   # make sure we get valid data from the API
   # if we can't get a published date then use the last modified date
   if preprint.date_published is None:
     preprint.date_published = preprint.date_modified
   parts = preprint.date_published.split("T")
   date = "Date Received: " + parts[0].strip()

   k = "Topic Areas: "
   a = "Authors: "
   link = "Link to paper: https://eartharxiv.org/" + preprint.identifier 
   print( preprint.title, file=l )
   print( date, file=l )
   print( link, file=l )
   
   for keyword in preprint.keywords:
      k += keyword + ", "
   for author in preprint.authors:
      a += author + ", "
   k = k[:-1]
   a = a[:-1]
   print( a, file=l ) 
   print( k, file=l )
   print( " ", file=l )

# close the log files   
l.close()

# print out the results
print("Total number of preprints returned:", len(preprints))
