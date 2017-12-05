Requirements and Background
-------------

In order to access the API you will need an API Token. Tokens are unique to each user and should not be shared. As such, no token is included in this repository. To get your token, first login to the <a href="https://osf.io>OSF site</a>. Once logged in, click on your name in the top right corner and select "Settings". In the Settings menu that now appears on the left, select "Personal Access Tokens". The "New Token" button will generate a new token specific to your account.

Once you have the token, create a file named api_token.py with one line in it:
osf_token = "BLAH"
where BLAH should be replaced with your token. The code will import api_token.py and reference osf_token when making calls to the API.

TO DO
---------

Please note, this code is currently very preliminary and only used for testing. It does not (yet) extract all values returned from the API. Development will continue over the next few weeks and the code may be updated often. 
