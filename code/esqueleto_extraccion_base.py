"""
Provides a simple extraction example

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

from pymongo import Connection
import datetime

# Date range
start = datetime.datetime(2011, 5, 16, 0, 0, 0)
end = datetime.datetime(2011, 5, 16, 23, 59, 59)

condition = {'created_at': {'$gte': start, '$lt':end}}
for item in coll.find(condition).sort([("created_at", True)]):
    # Do something
    print item