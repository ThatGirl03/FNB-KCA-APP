import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from flask_login import LoginManager, current_user
import os

# Initialize Firebase
cred = credentials.Certificate('firebase_key.json')  # Ensure correct path
firebase_admin.initialize_app(cred)
db = firestore.client()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gdfwdfeygfe vgduqdfehtdfe'

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'}

    # Set up LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth
    from .admin_auth import admin_auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin_auth, url_prefix='/')

    # User loader for login management
    from .models import User  # Make sure this is updated to use Firebase
    @login_manager.user_loader
    def load_user(user_id):
        user_ref = db.collection('users').document(user_id).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            return User(id=user_id, **user_data)
        return None

    return app
