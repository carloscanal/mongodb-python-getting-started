from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

import sys
import os
import pymongo

# Create your views here.
def index(request):

    ### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

    # uri = 'mongodb://heroku_crrxdwnw:b6m00vrrmnqggnbm536s4hq44b@ds037185.mlab.com:37185/heroku_crrxdwnw?retryWrites=false' 

    # uri = 'mongodb+srv://canal:astur9@cluster0-vodgj.mongodb.net/test?retryWrites=true&w=majority'

    uri = os.environ['MONGODB_URI'] + '?retryWrites=false'  # si no da error

    print("MONGODB_URI= %s" %(uri), flush=True)

    client = pymongo.MongoClient(uri)

    db = client.get_default_database()
    
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.

    greetings = db['greetings']

    # First qwe insert a new document in the collection og greetings

    greetings.insert({'dateCreated' : datetime.now().strftime("%d/%m/%Y %H:%M:%S") })

    # Finally we run a query
                     
    cursor = greetings.find().sort('dateCreated', -1)

    for greeting in cursor:
       print ('Greetins from %s' % (greeting['dateCreated']))
    
    number = cursor.count()
    
    print('%d greetings have been found' % (number), flush=True)
    
    ### Since this is an example, we'll clean up after ourselves.

    ### db.drop_collection('songs')

    ### Only close the connection when your app is terminating

    client.close()
    
    return render(request, "index.html", {"greetings": list(cursor.rewind()), "number": number})
