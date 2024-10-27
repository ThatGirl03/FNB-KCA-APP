from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase App
cred = credentials.Certificate("path/to/your/firebase/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class Note:
    def __init__(self, id, data, date, user_id):
        self.id = id
        self.data = data
        self.date = date or datetime.utcnow()
        self.user_id = user_id

    def save(self):
        db.collection('notes').document(self.id).set({
            'data': self.data,
            'date': self.date,
            'user_id': self.user_id
        })

class User(UserMixin):
    def __init__(self, id, firstname, lastname, email, password, profile_id=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.profile_id = profile_id

    def save(self):
        db.collection('users').document(self.id).set({
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password,
            'profile_id': self.profile_id
        })

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)


class UserProfile:
    def __init__(self, id, firstname, lastname, bio, location, workplace, education, highlights,
                 linkedin, facebook, instagram, cover_photo, media_upload, media_type, user_id):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.bio = bio
        self.location = location
        self.workplace = workplace
        self.education = education
        self.highlights = highlights
        self.linkedin = linkedin
        self.facebook = facebook
        self.instagram = instagram
        self.cover_photo = cover_photo
        self.media_upload = media_upload
        self.media_type = media_type
        self.user_id = user_id

    def save(self):
        db.collection('user_profiles').document(self.id).set({
            'firstname': self.firstname,
            'lastname': self.lastname,
            'bio': self.bio,
            'location': self.location,
            'workplace': self.workplace,
            'education': self.education,
            'highlights': self.highlights,
            'linkedin': self.linkedin,
            'facebook': self.facebook,
            'instagram': self.instagram,
            'cover_photo': self.cover_photo,
            'media_upload': self.media_upload,
            'media_type': self.media_type,
            'user_id': self.user_id
        })


class TradePost:
    def __init__(self, id, title, description, price, image, category, user_id):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.image = image
        self.category = category
        self.user_id = user_id

    def save(self):
        db.collection('trade_posts').document(self.id).set({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'category': self.category,
            'user_id': self.user_id
        })


class Admin(UserMixin):
    def __init__(self, id, name, staff, contact_email, password):
        self.id = id
        self.name = name
        self.staff = staff
        self.contact_email = contact_email
        self.password = generate_password_hash(password)

    def save(self):
        db.collection('admins').document(self.id).set({
            'name': self.name,
            'staff': self.staff,
            'contact_email': self.contact_email,
            'password': self.password
        })


class Posts:
    def __init__(self, id, image, pdf, date_created=None):
        self.id = id
        self.image = image
        self.pdf = pdf
        self.date_created = date_created or datetime.utcnow()

    def save(self):
        db.collection('posts').document(self.id).set({
            'image': self.image,
            'pdf': self.pdf,
            'date_created': self.date_created
        })


class Save:
    def __init__(self, id, device_name, image, price, created_at=None):
        self.id = id
        self.device_name = device_name
        self.image = image
        self.price = price
        self.created_at = created_at or datetime.utcnow()

    def save(self):
        db.collection('saves').document(self.id).set({
            'device_name': self.device_name,
            'image': self.image,
            'price': self.price,
            'created_at': self.created_at
        })


class CyberPosts:
    def __init__(self, id, image, pdf, date_created=None):
        self.id = id
        self.image = image
        self.pdf = pdf
        self.date_created = date_created or datetime.utcnow()

    def save(self):
        db.collection('cyber_posts').document(self.id).set({
            'image': self.image,
            'pdf': self.pdf,
            'date_created': self.date_created
        })


class DataPosts:
    def __init__(self, id, image, pdf, date_created=None):
        self.id = id
        self.image = image
        self.pdf = pdf
        self.date_created = date_created or datetime.utcnow()

    def save(self):
        db.collection('data_posts').document(self.id).set({
            'image': self.image,
            'pdf': self.pdf,
            'date_created': self.date_created
        })


class NetworkPosts:
    def __init__(self, id, image, pdf, date_created=None):
        self.id = id
        self.image = image
        self.pdf = pdf
        self.date_created = date_created or datetime.utcnow()

    def save(self):
        db.collection('network_posts').document(self.id).set({
            'image': self.image,
            'pdf': self.pdf,
            'date_created': self.date_created
        })


class QuestionPosts:
    def __init__(self, id, image, pdf, date_created=None):
        self.id = id
        self.image = image
        self.pdf = pdf
        self.date_created = date_created or datetime.utcnow()

    def save(self):
        db.collection('question_posts').document(self.id).set({
            'image': self.image,
            'pdf': self.pdf,
            'date_created': self.date_created
        })


class MemoPosts:
    def __init__(self, id, image, pdf, date_created=None):
        self.id = id
        self.image = image
        self.pdf = pdf
        self.date_created = date_created or datetime.utcnow()

    def save(self):
        db.collection('memo_posts').document(self.id).set({
            'image': self.image,
            'pdf': self.pdf,
            'date_created': self.date_created
        })
