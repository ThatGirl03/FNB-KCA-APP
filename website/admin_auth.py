from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from firebase_admin import firestore

from website.models import Admin

admin_auth = Blueprint('admin_auth', __name__)
db = firestore.client()

@admin_auth.route('/adm_login', methods=['GET', 'POST'])
def adm_login():
    if request.method == 'POST':
        contact_email = request.form.get('email')
        password = request.form.get('password')

        admin_ref = db.collection('admins').document(contact_email).get()
        
        if admin_ref.exists:
            admin_data = admin_ref.to_dict()
            if check_password_hash(admin_data['password'], password):
                flash('Welcome to Admin Dashboard!', category='success')
                admin = Admin(id=contact_email, **admin_data)  # Assuming Admin is updated to work with Firestore
                login_user(admin, remember=True)
                return redirect(url_for('views.admin_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("adm_login.html", admin=current_user)


@admin_auth.route('/admin_sign-up', methods=['GET', 'POST'])
def adm_signUp():
    if request.method == 'POST':
        contact_email = request.form.get('contact_email')
        admin_name = request.form.get('admin_name')
        staff = request.form.get('staff')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if email is already in use
        admin_ref = db.collection('admins').document(contact_email).get()
        if admin_ref.exists:
            flash('Email address already in use. Please use a different email.', category='error')
            return redirect(url_for('admin_auth.adm_signUp'))

        # Password matching
        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('admin_auth.adm_signUp'))

        # Add admin to Firebase
        new_admin = {
            "name": admin_name,
            "staff": staff,
            "contact_email": contact_email,
            "password": generate_password_hash(password1)
        }
        db.collection('admins').document(contact_email).set(new_admin)
        flash('Admin account created!', category='success')
        login_user(Admin(id=contact_email, **new_admin), remember=True)
        return redirect(url_for('admin_auth.adm_login'))

    return render_template("admin_sign-up.html", admin=current_user)
