import firebase_admin
from firebase_admin import credentials, firestore
import firebase_admin.auth

# Path to your Firebase Admin SDK key file
cred = credentials.Certificate('firebase-admin-sdk-key.json')

# Initialize Firebase
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# # Simple Test: Add a user
# def add_user(user_id, name, currency):
#     user_ref = db.collection('users').document(user_id)
#     user_ref.set({
#         'name': name,
#         'currency': currency
#     })
#
# # Test adding a user
# add_user('user123', 'Alice', 1000)
# print('User added successfully!')

# Sign-Up Function
def sign_up(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f'Successfully created user {user.uid}')
    except firebase_admin.auth.EmailAlreadyExistsError:
        print('This email is already in use!')

# Login Function
def login(email, password):
    try:
        # Sign in with email and password
        user = auth.get_user_by_email(email)
        print(f'Logged in successfully: {user.uid}')
        return user
    except firebase_admin.auth.UserNotFoundError:
        print('No user found with this email!')
        return None
