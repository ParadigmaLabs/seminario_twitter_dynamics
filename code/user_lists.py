"""
Simple script to get user's memeberships

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

import requests
import json
import sys

__author__ = "Paradigma Labs 2012"

user_lists = []
max_pages = 5
next_cursor = -1

for i in range(0,max_pages):
    url = 'https://api.twitter.com/1/lists/memberships.json?screen_name=%s&cursor=%s' % (sys.argv[1], next_cursor)
    content = requests.get(url).content
    data = json.loads(content)
    next_cursor = data['next_cursor']

    for list_data in data['lists']:
        name = list_data['name']
        uri = list_data['uri']
        description = list_data['description']
        user_lists.append("%s (%s): %s" % (name, uri, description))

for l in user_lists:
    print l