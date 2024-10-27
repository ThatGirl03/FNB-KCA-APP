import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from flask_login import LoginManager, current_user
from website.models import User

# Initialize Firestore and Firebase
cred = credentials.Certificate('firebase_key.json')  # Ensure this path is correct
firebase_admin.initialize_app(cred)
db = firestore.client()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gdfwdfeygfe vgduqdfehtdfe'
    
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'}

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'admin_auth.login'  # Redirects to login if unauthorized
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        # Fetch the user from Firestore
        user_ref = db.collection('users').document(email).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            return User(user_id=user_data['id'], email=user_data['email'], first_name=user_data['first_name'], last_name=user_data['last_name'])
        return None

    # Register blueprints
    from .views import views
    from .admin_auth import admin_auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin_auth, url_prefix='/')

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app
