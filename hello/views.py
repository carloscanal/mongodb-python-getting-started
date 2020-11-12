from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

import sys
import os
import pymongo

# Create your views here.
def index(request):

    ### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

    # uri = 'mongodb://heroku_7k20dqtj:ld8e257gkq8qfiounmvi2543cb@ds249267.mlab.com:49267/heroku_7k20dqtj?retryWrites=false' 

    # uri = 'mongodb+srv://canal:canal@cluster0-vodgj.mongodb.net/test?retryWrites=true&w=majority'

    # uri = os.environ['MONGODB_URI'] # + '?retryWrites=false'  # si no da error
    
    uri = 'mongodb+srv://canal:canal@cluster0.vodgj.mongodb.net/appsNube?retryWrites=true&w=majority'

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
