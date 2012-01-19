"""
This script creates a simple RT network but filter by one hastag

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

from pymongo import Connection
import datetime
import re

# Database configuration
conn = Connection('labs', 27017)
db = conn.twitter 
coll = db.nolesvotes

# Search conditions
start = datetime.datetime(2011, 5, 16, 18, 0, 0)
end = datetime.datetime(2011, 5, 16, 18, 59, 59)
cond = {'retweeted_status': {'$exists': True} , 
                'created_at': {'$gte': start, '$lt':end}}

# Variable to save the network structure
network = ''
# Perform search
for item in coll.find(cond).sort([("created_at", True)]):
    target_hashtags = ['democraciarealya']
    hash_find = False
    for item_hash in item['entities']['hashtags']:
        if item_hash['text'].lower() in target_hashtags:
            hash_find = True
    if hash_find:
        network += '\t%s -> %s\n' % (item['retweeted_status']['user']['screen_name'], 
                                    item['user']['screen_name'])

# Save data into a file
file_out = file('/tmp/retweet_network_hash.dot' , 'w')
file_out.write('digraph G{\n%s}' % network)
file_out.close()