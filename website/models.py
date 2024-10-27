from firebase_admin import firestore
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = firestore.client()  # Initialize Firestore client

class Note:
    def __init__(self, user_id, data):
        self.data = data
        self.date = firestore.SERVER_TIMESTAMP  # Firestore will handle the timestamp
        self.user_id = user_id

    @staticmethod
    def create(user_id, data):
        note_ref = db.collection('notes').add({
            'data': data,
            'date': firestore.SERVER_TIMESTAMP,
            'user_id': user_id
        })
        return note_ref.id  # Return the ID of the created note

class User(UserMixin):
    def __init__(self, email, first_name, last_name, password=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    @staticmethod
    def create(email, first_name, last_name, password):
        user_ref = db.collection('users').document(email)
        user_ref.set({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': generate_password_hash(password)  # Hash the password
        })

    @staticmethod
    def get(email):
        user_ref = db.collection('users').document(email).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            return User(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password']
            )
        return None

class UserProfile:
    def __init__(self, user_id, firstname, lastname, bio, location, workplace, education, highlights):
        self.firstname = firstname
        self.lastname = lastname
        self.bio = bio
        self.location = location
        self.workplace = workplace
        self.education = education
        self.highlights = highlights
        self.user_id = user_id

    @staticmethod
    def create(user_id, firstname, lastname, bio, location, workplace, education, highlights):
        profile_ref = db.collection('user_profiles').document(user_id)
        profile_ref.set({
            'firstname': firstname,
            'lastname': lastname,
            'bio': bio,
            'location': location,
            'workplace': workplace,
            'education': education,
            'highlights': highlights
        })

    @staticmethod
    def get(user_id):
        profile_ref = db.collection('user_profiles').document(user_id).get()
        if profile_ref.exists:
            return profile_ref.to_dict()
        return None

class TradePost:
    def __init__(self, title, description, price, category, user_id):
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.user_id = user_id

    @staticmethod
    def create(title, description, price, category, user_id):
        post_ref = db.collection('trade_posts').add({
            'title': title,
            'description': description,
            'price': price,
            'category': category,
            'user_id': user_id,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id

class Admin(UserMixin):
    def __init__(self, staff, name, contact_email, password=None):
        self.staff = staff
        self.name = name
        self.contact_email = contact_email
        self.password = password

    @staticmethod
    def create(staff, name, contact_email, password):
        admin_ref = db.collection('admins').document(contact_email)
        admin_ref.set({
            'name': name,
            'staff': staff,
            'contact_email': contact_email,
            'password': generate_password_hash(password)  # Hash the password
        })

class Post:
    def __init__(self, image, pdf):
        self.image = image
        self.pdf = pdf

    @staticmethod
    def create(image, pdf):
        post_ref = db.collection('posts').add({
            'image': image,
            'pdf': pdf,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id

class Save:
    def __init__(self, device_name, image, price):
        self.device_name = device_name
        self.image = image
        self.price = price

    @staticmethod
    def create(device_name, image, price):
        save_ref = db.collection('saves').add({
            'device_name': device_name,
            'image': image,
            'price': price,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        return save_ref.id

class CyberPosts:
    def __init__(self, image, pdf):
        self.image = image
        self.pdf = pdf

    @staticmethod
    def create(image, pdf):
        post_ref = db.collection('cyber_posts').add({
            'image': image,
            'pdf': pdf,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id

class DataPosts:
    def __init__(self, image, pdf):
        self.image = image
        self.pdf = pdf

    @staticmethod
    def create(image, pdf):
        post_ref = db.collection('data_posts').add({
            'image': image,
            'pdf': pdf,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id

class NetworkPosts:
    def __init__(self, image, pdf):
        self.image = image
        self.pdf = pdf

    @staticmethod
    def create(image, pdf):
        post_ref = db.collection('network_posts').add({
            'image': image,
            'pdf': pdf,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id

class QuestionPosts:
    def __init__(self, image, pdf):
        self.image = image
        self.pdf = pdf

    @staticmethod
    def create(image, pdf):
        post_ref = db.collection('question_posts').add({
            'image': image,
            'pdf': pdf,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id

class MemoPosts:
    def __init__(self, image, pdf):
        self.image = image
        self.pdf = pdf

    @staticmethod
    def create(image, pdf):
        post_ref = db.collection('memo_posts').add({
            'image': image,
            'pdf': pdf,
            'date_created': firestore.SERVER_TIMESTAMP
        })
        return post_ref.id
