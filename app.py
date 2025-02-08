import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase Admin SDK key file
cred = credentials.Certificate('firebase-admin-sdk-key.json')

# Initialize Firebase
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Simple Test: Add a user
def add_user(user_id, name, currency):
    user_ref = db.collection('users').document(user_id)
    user_ref.set({
        'name': name,
        'currency': currency
    })

# Test adding a user
add_user('user123', 'Alice', 1000)
print('User added successfully!')
