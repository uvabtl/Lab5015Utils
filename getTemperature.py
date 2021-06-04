#!/usr/bin/python
import MySQLdb
import sys

if len(sys.argv) != 3:
    print("ERROR, usage: ./getTemperature.py date [YYYY-MM-DD] time [HH:MM:SS]")
    sys.exit()

date = sys.argv[1]
time = sys.argv[2]

# Open database connection
db = MySQLdb.connect("localhost","logger","raspberry","temperatures" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# esecuzione di una query
query = "SELECT * FROM temperaturedata WHERE dateandtime BETWEEN (\'"+date+" "+time+"\' - INTERVAL 1 MINUTE) AND \'"+date+" "+time+"\'"
cursor.execute(query)

# Lettura di una singola riga dei risultati della query
data = cursor.fetchone()

if data is None:
    raise ValueError("Could not read box temperature")
elif len(data) != 4:
    raise ValueError("Could not read box temperature")
else:
    print("temp: "+str(data[2]))

# disconnect from server
db.close()
