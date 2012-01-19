"""
This script performances calls to Gephi server in order to 
create a graph in real time

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

from pymongo import Connection
import datetime
import re
import pycurl

def send(n_from, n_to):
    """
    Description: Send data to a gephi server
    """
    gephi_server_url = "http://localhost:8080/workspace0?operation=updateGraph"
    
    n1 = """{"an":{"%s":{"label":"%s"}}}"""  % (n_from , n_from)
    
    n2 = """{"an":{"%s":{"label":"%s"}}}"""  % (n_to , n_to)
    
    edge = """{"ae":{"%s%s":{"source":"%s","target":"%s","directed":true}}}
           """  % (n_from, n_to ,n_from, n_to)
           
    data = """%s\r %s\r %s\r""" % (n1 , n2 , edge)
    
    conn = pycurl.Curl()
    conn.setopt(pycurl.URL , gephi_server_url)
    conn.setopt(pycurl.POSTFIELDS , data)
    conn.perform()
    conn.close()
    
# Database configuration
conn = Connection('labs', 27017)
db = conn.twitter 
coll = db.nolesvotes

# Search conditions
start = datetime.datetime(2011, 5, 16, 18, 0, 0)
end = datetime.datetime(2011, 5, 16, 18, 59, 59)
cond = {'retweeted_status': {'$exists': True} , 
                'created_at': {'$gte': start, '$lt':end}}

# Perform search
for item in coll.find(cond).sort([("created_at", True)]):
    send(str(item['retweeted_status']['user']['screen_name']), str(item['user']['screen_name']))                        

