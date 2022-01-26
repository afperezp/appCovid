from django.shortcuts import render

# Create your views here.

import pyrebase

config = {
    'apiKey': "AIzaSyByJhZKkc9G0B-MrOOsnuDxIgUUELIEKyM",
  'authDomain': "covid19-e6bf1.firebaseapp.com",
  'databaseURL': "https://covid19-e6bf1-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "covid19-e6bf1",
  'storageBucket': "covid19-e6bf1.appspot.com",
  'messagingSenderId': "96661594726",
  'appId': "1:96661594726:web:d1dcb138c79bf3f4f1c3a7",
  'measurementId': "G-4QXVFPQ3PM"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def index(request):

    AstraZenecaCount = database.child("CovidApp").child('ConteoVacunas').child('Astra Zeneca').get().val()
    JanssenCount = database.child("CovidApp").child('ConteoVacunas').child('Janssen').get().val()
    ModernaCount = database.child("CovidApp").child('ConteoVacunas').child('Moderna').get().val()
    PfizerCount = database.child("CovidApp").child('ConteoVacunas').child('Pfizer').get().val()

    context = {
        'AstraZenecaCount':AstraZenecaCount, 
        'JanssenCount':JanssenCount, 
        'ModernaCount':ModernaCount, 
        'PfizerCount':PfizerCount, 
    }
    return render(request, 'index.html', context)


def scanQR(request):

    
    return render(request, "scanView", {})