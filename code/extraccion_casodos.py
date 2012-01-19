"""
Provides a mutual information approach in order to represent a simple
graph with variables dependences

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

from pymongo import Connection
import datetime
import math

def add_coocurrence(cooccurrences, hashtag_one, hashtag_two):
    """
    """
    # Check if key is in dict
    if hashtag_one not in cooccurrences:
        cooccurrences[hashtag_one] = {}
    # Check if key is in dict
    if hashtag_two not in cooccurrences[hashtag_one]:
        cooccurrences[hashtag_one][hashtag_two] = 0
    # Increment coocurrence between hashtags
    cooccurrences[hashtag_one][hashtag_two] += 1
    
    
def increment_frecuency(frecuency, hashtag):
    """
    """
    # Check if key is in dict
    if hashtag not in frecuency.keys():
        frecuency[hashtag] = 1
    else:
        # Increment frecuency
        frecuency[hashtag] += 1
        
        
# Database configuration
conn = Connection('labs', 27017)
db = conn.twitter 
coll = db.nolesvotes

# Search conditions
start = datetime.datetime(2011, 5, 17, 15, 0, 0)
end = datetime.datetime(2011, 5, 17, 15, 15, 59)
cond = {'created_at': {'$gte': start, '$lt':end}}

# Variable to save the network structure
cooccurrences = {}
frecuency = {}

# Threshold to drop edges
mi_threshold = 0.0

# Perform search
n = 0
for  tweet in coll.find(cond).sort([("created_at", True)]):
    # Check if this tweet has hastag
    if 'entities' in  tweet.keys():
        len_hastags = len(tweet['entities']['hashtags'])
        # Coocurrences start with two items
        if len_hastags > 1:
            n += 1
            i = 0
            while i < len_hastags - 1:
                j = i + 1
                while j < len_hastags - 1:
                    # Get coocurrence
                    hashtag_one =  tweet['entities']['hashtags'][i]['text'].lower().encode('utf-8')
                    hashtag_two =  tweet['entities']['hashtags'][j]['text'].lower().encode('utf-8')
                    if hashtag_one != hashtag_two:
                        # Incement global frecuency
                        increment_frecuency(frecuency, hashtag_one)
                        increment_frecuency(frecuency, hashtag_two)
                        # Add coocurrence
                        add_coocurrence(cooccurrences, hashtag_one, hashtag_two)
                    j += 1
                i += 1
    

# Save data into a file
file_out = file('/tmp/hastag_coocurrence2.tsv' , 'w')

len_keys = len(frecuency)
i = 0
while i < len_keys - 1:
    j = i + 1
    while j < len_keys - 1:
        aux = 0
        # Check first order coocurrences
        if frecuency.keys()[i] in cooccurrences.keys():
            if frecuency.keys()[j] in cooccurrences[frecuency.keys()[i]]:
                aux += cooccurrences[frecuency.keys()[i]][frecuency.keys()[j]]
        if frecuency.keys()[j] in cooccurrences.keys():
            if frecuency.keys()[i] in cooccurrences[frecuency.keys()[j]]:
                aux += cooccurrences[frecuency.keys()[j]][frecuency.keys()[i]]
        if aux != 0:
            px = float(frecuency[frecuency.keys()[i]]) / n
            py = float(frecuency[frecuency.keys()[j]]) / n
            pxy = float(aux) / n
            mi = - pxy * (math.log(pxy/(px*py), 2))
            print '(%s , %s)' % (frecuency.keys()[i], frecuency.keys()[j])
            print 'p(x,y)=%.3f p(x)=%.3f p(y)=%.3f MI:%.3f\n' % (pxy, px, py, mi)
            if mi > mi_threshold:
                # We apply some transformations to visualize in graphstream
                file_out.write('%s\t%s\tnull\t%s\t%s\tnull\t%s\n' % (
                                    frecuency.keys()[i], 
                                    float(frecuency[frecuency.keys()[i]]) * 2,
                                    frecuency.keys()[j], 
                                    float(frecuency[frecuency.keys()[j]]) * 2,
                                    mi * 80))
        j += 1
    i += 1
file_out.close()