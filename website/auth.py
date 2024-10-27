from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from firebase_admin import firestore

from website.models import User

# Initialize Firestore client
db = firestore.client()

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_ref = db.collection('users').document(email).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            if check_password_hash(user_data['password'], password):
                flash('Welcome to Easy Link!', category='success')
                user = User(email=user_data['email'], firstname=user_data['firstname'], lastname=user_data['lastname'], password=user_data['password'])  # Create a User object
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not all([email, lastname, firstname, password1, password2]):
            flash('All fields are required!', category='error')
            return redirect(url_for('auth.sign_up'))

        user_ref = db.collection('users').document(email).get()
        if user_ref.exists:
            flash('Email address already in use. Please use a different email.', category='error')
            return redirect(url_for('auth.sign_up'))

        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('auth.sign_up'))

        # Create a new user in Firestore
        new_user = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'password': generate_password_hash(password1, method='pbkdf2:sha256')  # Hash the password
        }
        db.collection('users').document(email).set(new_user)  # Store the user document in Firestore

        flash('Account created!', category='success')
        login_user(User(email=email, firstname=firstname, lastname=lastname, password=new_user['password']), remember=True)  # Create User object
        return redirect(url_for('auth.login'))

    return render_template("sign-up.html", user=current_user)
