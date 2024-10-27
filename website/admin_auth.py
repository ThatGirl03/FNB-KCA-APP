import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

admin_auth = Blueprint('admin_auth', __name__)

@admin_auth.route('/adm_login', methods=['GET', 'POST'])
def adm_login():
    if request.method == 'POST':
        contact_email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.get(contact_email)

        if admin:
            if check_password_hash(admin.password, password):
                flash('Welcome to Admin Dashboard!', category='success')
                login_user(admin, remember=True)
                return redirect(url_for('admin_home.admin_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("adm_login.html", admin=current_user)

@admin_auth.route('/adm-logout')
@login_required
def adm_logout():
    logout_user()
    return redirect(url_for('admin_auth.adm_login'))

@admin_auth.route('/admin_sign-up', methods=['GET', 'POST'])
def adm_sign_up():
    if request.method == 'POST':
        contact_email = request.form.get('contact_email')
        admin_name = request.form.get('staff_name')
        staff = request.form.get('staff')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = Admin.get(contact_email)

        if existing_user:
            flash('Email address already in use. Please use a different email.', category='error')
            return redirect(url_for('admin_auth.adm_sign_up'))

        # Check if staff number already exists
        existing_registration = Admin.get(staff)
        if existing_registration:
            flash('Staff number already in use. Please use a different staff number.', category='error')
            return redirect(url_for('admin_auth.adm_sign_up'))

        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('admin_auth.adm_sign_up'))

        # Create new admin
        Admin.create(staff=staff, name=admin_name, contact_email=contact_email, password=password1)
        flash('Account created!', category='success')
        return redirect(url_for('admin_auth.adm_login'))

    return render_template("admin_sign-up.html", admin=current_user)

@admin_auth.route('/admin_home', methods=['GET'])
@login_required
def admin_home():
    # Fetch all admins from Firestore (optional, depending on your needs)
    all_admins = db.collection('admins').stream()
    admins = [admin.to_dict() for admin in all_admins]
    return render_template('admin_home.html', admins=admins)
