"""
Simple trending topic extraction in real time (Madrid)

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

import requests
import json

__author__ = "Paradigma Labs 2012"

url = 'https://api.twitter.com/1/trends/766273.json'
content = requests.get(url).content
data = json.loads(content)

for tt in data[0]['trends']:
    name = tt['name']
    search_url = tt['url']
    print "%s  -->  %s" % (name, search_url)