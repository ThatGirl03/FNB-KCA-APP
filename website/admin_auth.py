from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db
from flask_login import login_user, login_required, logout_user, current_user



admin_auth = Blueprint('admin_home', __name__)
@admin_auth.route('/admin_home', methods=['GET'])
def admin_home():
    admin = admin.query.all()  # Fetch all organizations from the database
    return render_template('admin_home.html', admin=admin)


admin_auth = Blueprint('admin_auth',__name__)

@admin_auth.route('/adm_login', methods=['GET', 'POST'])
def adm_login():
    if request.method == 'POST':
        contact_email = request.form.get('email')
        password = request.form.get('password')

        Adm = Admin.query.filter_by(contact_email=contact_email).first()

        
        if Adm:
            if check_password_hash(Adm.password, password): 
                flash('Welcome to Admin Dashboard!', category='success')
                login_user(Adm, remember=True)
                return redirect(url_for('views.admin_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
                



    return render_template("adm_login.html", admin=current_user )


@admin_auth.route('/adm-logout')
@login_required
def adm_logout():
    logout_user()
    return redirect(url_for('admin_auth.adm_login'))
   




@admin_auth.route('/admin_sign-up', methods=['GET', 'POST'])
def adm_signUp():
    if request.method == 'POST':
        contact_email = request.form.get('contact_email')
        admin_name = request.form.get('staff_name')
        staff = request.form.get('staff')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = Admin.query.filter_by(contact_email=contact_email).first()

        if existing_user:
            flash('Email address already in use. Please use a different email.', category='error')
            return redirect(url_for('admin_auth.adm_signUp'))
        
          # Check if registration number already exists
        existing_registration = Admin.query.filter_by(staff=staff).first()
        if existing_registration:
            flash('Staff number already in use. Please use a different staff number.', category='error')
            return redirect(url_for('admin_auth.adm_signUp'))
        
        existing_staff = Admin.query.filter_by(name=admin_name).first()
        if existing_staff:
            flash('Staff number already in use. Please use a different staff number.', category='error')
            return redirect(url_for('admin_auth.adm_signUp'))

        # Continue with creating the user if email is unique
        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('admin_auth.adm_signUp'))

        new_admin = Admin(
            name=admin_name,
            staff=staff,
            contact_email=contact_email,
            password=generate_password_hash(password1, method='pbkdf2:sha256')  # <-- Hash the password
        )

        db.session.add(new_admin)
        db.session.commit()
        flash('Account created!', category='success')
        login_user(new_admin, remember=True)  # <-- Ensure 'new_organization' is used
        return redirect(url_for('admin_auth.adm_login'))

    return render_template("admin_sign-up.html", admin=current_user)


