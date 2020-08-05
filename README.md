Requirements and Background
-------------

In order to access the API you will need an API Token. Tokens are unique to each user and should not be shared. As such, no token is included in this repository. To get your token, first login to the <a href="https://osf.io">OSF site</a>. Once logged in, click on your name in the top right corner and select "Settings". In the Settings menu that now appears on the left, select "Personal Access Tokens". The "New Token" button will generate a new token specific to your account.

Once you have the token, create a file named api_token.py with one line in it:
```python
osf_token = "BLAH"
```
where BLAH should be replaced with your token. The code will import api_token.py and reference osf_token when making calls to the API.

To Run
---------
clone the repository
then run:
python downloadAndIndexPreprints.py preprint_download_dir True 2019-01-01 preprintlog.txt

Overview
---------
This code creates two log files, downloads available preprints, and creates a text file for each preprint containing the preprint abstract. One log file contains metadata on available preprints, such as authors, keywords, title, publication date, etc. The other log file contains metadata on peer-reviewed papers associated with preprints. This log file contains similar metadata as that of the preprints: e.g. authors, title, publication date, journal, etc. The EarthArXiv preprint identifier is used in both log files and provides a means a linking preprints to their peer-reviewed papers.

Semi-colon is used as the seperator in each of the log files. Paper titles often have commas in them and using semi-colons to seperate columns allows us to preserve the titles. Preprint log has the form:

identifier; preprint provider; preprint doi; peer review doi; preprint publication date; peer review publication date; title; author list; keyword list

Peer-review log has the form:

preprint identifier; preprint provider; peer review doi; peer review date published; peer review journal; peer review title; peer review author list; peer review publisher; peer review url 

[![DOI](https://zenodo.org/badge/113208059.svg)](https://zenodo.org/badge/latestdoi/113208059)

