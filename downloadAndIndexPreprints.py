import sys
import utils
from Preprint import Preprint
from callOsfApi import callOsfApi

def preprintInLog(preprint, loggedPreprints):

   found = False
   index = 0
   for i in range( len(loggedPreprints) ):
     p = loggedPreprints[i]
     if preprint.identifier == p.identifier:
       found = True
       index = i
       break
   return found, index

# command line inputs
# downloadDir - directory to download papers to, also where logs are stored
downloadDir = sys.argv[1]
# print out status messages as we go along (True or False)
verbose = sys.argv[2]
# start date - YYYY-MM-DD we should start the index from
startDate = sys.argv[3]
# log file for the peer reviewed article data
peerReviewLog = sys.argv[4]

# seperator for log file
s1 = ';'

# the API returns all preprints that were created
# some papers may not be available for download
# due to moderation problems or retraction
# keep track of how many preprints we actually get
numPreprints = 0

# check that the download directory includes 
# the trailing /
lc = downloadDir[-1]
if (lc != '/'):
   downloadDir += '/'

# preprint provider
provider = 'eartharxiv'

# set up log files based on provider
log = downloadDir + provider + '.log'

# get the papers
preprints = callOsfApi(provider, startDate, verbose)

# open log files for writing 
l = open(log, 'w')
l2 = open(peerReviewLog, 'w')

# loop over all the papers we found
n = len(preprints)
count = 1
for preprint in preprints:

   # status update
   if verbose: print("Downloading preprint", count, "of", n)
   count += 1

   # try to download the file
   localFile = downloadDir + 'papers/' + preprint.identifier + '.pdf'
   localAbstract = downloadDir + 'abstracts/' + preprint.identifier + '.txt'
   error, message = utils.download( preprint.download_link, localFile )
   if ( not error ):

      # write the abstract to a file
      abstF = open(localAbstract, 'w')
      abstF.write( preprint.description )
      abstF.close()

      # increment our count by 1
      numPreprints += 1

      # does this preprint exist in the list of objects
      #found, index = preprintInLog( preprint, loggedPreprints )
      #if ( found  ):
      #  loggedPreprints[index] = preprint 
      #else:
      #  loggedPreprints.append( preprint ) 

      # write to the log file

      # remove the seperator from the title or else we'll have trouble reading back the logs
      title = preprint.title.replace(s1," ")

      # make sure we get valid data from the API
      if preprint.date_published is None:
        preprint.date_published = preprint.date_modified # if published date corrupted use the last modified date

      line = preprint.identifier + s1 + provider + s1 + preprint.doi + s1 + preprint.peer_review_doi + s1 + \
        preprint.date_published + s1
      line += preprint.peer_review_publish_date + s1 + title
      k = ""
      a = ""
      for keyword in preprint.keywords:
        k += keyword + ":"
      for author in preprint.authors:
        a += author + ":"
      k = k[:-1]
      a = a[:-1]
      line += s1 + a + s1 + k
      print( line, file=l ) 
      if ( preprint.peer_review_doi != "" ):
         line = preprint.identifier + s1 + provider + s1 + preprint.peer_review_doi + s1 + \
           preprint.peer_review_publish_date + s1 + \
           preprint.peer_review_journal + s1 + preprint.peer_review_title + s1 + \
           preprint.peer_review_author + s1 + preprint.peer_review_publisher + \
           s1 + preprint.peer_review_url
         print(line, file=l2)

# close the log files   
l.close()
l2.close()

# print out the results
print("Total number of preprints returned:", len(preprints))
print("Number of preprints downloaded:", numPreprints)
