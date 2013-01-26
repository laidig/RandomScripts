# Include the Dropbox SDK libraries
from dropbox import client, rest, session
from ConfigParser import SafeConfigParser
from itertools import product
from string import ascii_lowercase
from time import sleep
import json

import os, sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))
configfile = path + '/localconfig.ini'
parser = SafeConfigParser()
parser.read(configfile)

# Get your app key and secret from the Dropbox developer website
APP_KEY = parser.get('db','app_key')
APP_SECRET = parser.get('db','app_secret')

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
# get req token
request_token = sess.obtain_request_token()
url = sess.build_authorize_url(request_token)
print "url:", url
print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
raw_input()

# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)

with open ('out_grepped.txt','rb') as f:
	for line in f:
		delfile =json.loads(line)
		print delfile['path']
		revs = client.revisions(delfile['path'])
		for r in revs:
			print r
			if 'is_deleted' not in r:
				rev = r['rev']
				client.restore(delfile['path'],rev)
				break




