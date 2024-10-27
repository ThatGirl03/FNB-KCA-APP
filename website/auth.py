from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from firebase_admin import firestore

from website.models import User

auth = Blueprint('auth', __name__)
db = firestore.client()

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
                user = User(id=email, **user_data)  # Adjust User model accordingly
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_ref = db.collection('users').document(email).get()
        if user_ref.exists:
            flash('Email already in use. Use a different email.', category='error')
            return redirect(url_for('auth.sign_up'))

        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('auth.sign_up'))

        # Add user to Firestore
        new_user = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": generate_password_hash(password1)
        }
        db.collection('users').document(email).set(new_user)
        flash('Account created!', category='success')
        login_user(User(id=email, **new_user), remember=True)
        return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)
