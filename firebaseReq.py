from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import pytz

timezone = pytz.timezone('Asia/Seoul')
cred = credentials.Certificate('firestore_admin.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
userCollection = db.collection('user')

def willAccept(uid):
    try:
        
        userData = userCollection.document(uid).get().to_dict()
        countPerDay = userData.get('countPerDay')
        if countPerDay >= 5:
            return 'Enough credit today'

        currentReq = userData.get('currentReq')
        if datetime.now().timestamp()-currentReq.timestamp()<7200:
            return 'Too early to make request'
        else :
            return 'True'
    except :
        return 'Failed to load data from firebase'


def success(uid) :
    try :
        userData = userCollection.document(uid)
        userData.update({"credit":firestore.Increment(30),"currentReq": datetime.now(timezone),'countPerDay':firestore.Increment(1)})
        return True
    except :
        print('[Error] : updating user data has failed')
        return False

def resetCount():
    try:
        docs = userCollection.get()
        print('reset started')
        for userData in docs:
            doc_ref = userCollection.document(userData.id)
            doc_ref.update({'countPerDay':0})
    except:
        print('[Error] : Reset count per day has failed')

