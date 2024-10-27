import requests
from bs4 import BeautifulSoup
import os
from flask import Blueprint, app, current_app, flash, jsonify, redirect, render_template, request, session, url_for, abort
from flask_login import  current_user, login_required
from werkzeug.utils import secure_filename
from .models import DataPosts, MemoPosts, NetworkPosts, QuestionPosts, User, UserProfile, tradepost, Posts, CyberPosts, Save
from website import db


views = Blueprint('views', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@views.route('/', methods=['GET', 'POST'])

def home(): 
    name="Ayanda!"
    return render_template("home.html", Hello='Welcome to Lecture.AI ' + name )

@views.route('/nexus')
def nexus():
    return render_template("nexus.html")

@views.route('/profile')
@login_required
def profile():
     # Retrieve the user's data from the database using their session ID/email/username
    user = current_user
    # Render the profile template and pass the user object
    return render_template("profile.html", user=user)


@views.route('/set_theme', methods=['POST'])
def set_theme():
    data = request.get_json()
    session['theme'] = data['theme']
    return '', 204  # No content response

@views.route('/sectorC')
def sectorC():
    return render_template("sectorC.html")

@views.route('/sectorD')
def sectorD():
    return render_template("sectorD.html")

@views.route('/sectorE')
def sectorE():
    return render_template("sectorE.html")

@views.route('/sectorF')
def sectorF():
    return render_template("sectorF.html")

@views.route('/sectorG')
def sectorG():
    return render_template("sectorG.html")

@views.route('/r-trade')
def trade():
    trades = tradepost.query.all()  # Fetch all trades
    for trade in trades:
        print(f"Trade image: {trade.image}") 
    return render_template('r-trade.html', trades=trades)

@views.route('/create-trade', methods=['POST'])
@login_required
def create_trade():
    if request.method == 'POST':
        if not current_user.is_authenticated:  # Ensure the user is authenticated
            flash('You need to be logged in to create a trade!', category='error')
            return redirect(url_for('views.login'))
        
        image = request.files.get('image')
        description = request.form.get('caption')
      
        price = request.form.get('price')
        category = request.form.get('category')
 

        title = request.form.get('title')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            new_trade = tradepost(
                image=filename,
                description=description,
                title=title, 
                price=float(price) if type == 'Sell' else None,
                category=category,
                
                user_id=current_user.id  # Only access id if current_user is authenticated
            )

            db.session.add(new_trade)
            db.session.commit()
            flash('Trade post created successfully!', category='success')
            return redirect(url_for('views.trade'))

    return redirect(url_for('views.trade'))



@views.route('/blog')
def blog():
    urls = [
        "https://www.bbc.com/future/article/20230317-how-recycling-can-help-the-climate-and-other-facts",
        "https://www.who.int/news-room/fact-sheets/detail/electronic-waste-%28e-waste%29",
        "https://freelancian.co.za/what-can-i-recycle-to-make-money-in-south-africa/"  
    ]

    articles = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  

         
            soup = BeautifulSoup(response.text, 'html.parser')

            article_content = soup.find('article')  

            articles.append({
                'title': soup.title.string if soup.title else 'No Title',
                'html': str(article_content)
            })

        except requests.RequestException as e:
            print(f"Error fetching article from {url}: {e}")
            articles.append({
                'title': 'Error Loading Article',
                'html': "<p>Error loading article</p>"
            })

    return render_template('blog.html', articles=articles)


@views.route('/videos')
def videos():
    video_list = [
        {'title': 'Artificial Intelligence Integrated in Recycling!', 'url': 'https://www.youtube.com/embed/On5WUCUNmfc'}, 
        {'title': 'Make Money Through Waste!', 'url': 'https://www.youtube.com/embed/cQqhKzcHnAg'},  
        {'title': 'AI Making Our Lives Easier!', 'url': 'https://www.youtube.com/embed/KPVSTjfcdng'}
    ]

    return render_template("videos.html", videos=video_list)



@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/certificate')
def certificate():
    url = "https://environmentgo.com/free-online-recycling-courses/#:~:text=Free%20Online%20Recycling%20Courses%201%201.%20Advanced%20Diploma,Electronics%20for%20Recycling%20in%20a%20Circular%20Economy%20"

    try:
        response = requests.get(url)
        response.raise_for_status()  

        
        soup = BeautifulSoup(response.text, 'html.parser')

      
        content = soup.find('main')  

     
        content_html = str(content)

    except requests.RequestException as e:
        print(f"Error fetching certificate data: {e}")
        content_html = "<p>Error loading content</p>"

    return render_template('certificate.html', content_html=content_html)


@views.route('/help')
def help():
    return render_template("help.html")

@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

@views.route('/terms')
def terms():
    return render_template("terms.html")



@views.route('/login')
def login():
    return render_template("login.html")



@views.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")

@views.route('/create-profile', methods=['GET', 'POST'])
@login_required
def createProfile():
    
    
    if request.method == 'POST':
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        bio = request.form.get('bio')
        location = request.form.get('location')
        workplace = request.form.get('workplace')
        education = request.form.get('education')
        highlights = request.form.get('highlights')
        linkedin = request.form.get('linkedin')
        facebook = request.form.get('facebook')
        instagram = request.form.get('instagram')
        media_type = request.form.get('mediaType')
        category_prefix = request.form.get('categoryPrefix')


        cover_photo = request.files.get('coverPhoto')
        media_uploads = request.files.getlist('mediaUpload')
        
        cover_photo_filename = None
        media_upload_filenames = []
        
        if cover_photo and allowed_file(cover_photo.filename):
            cover_photo_filename = secure_filename(cover_photo.filename)
            cover_photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cover_photo_filename))
        
        for media_upload in media_uploads:
         if media_upload and allowed_file(media_upload.filename):
            filename = secure_filename(media_upload.filename)
            media_upload.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            media_upload_filenames.append(filename)
            
        
        profile = UserProfile(
            firstname=firstname,
            lastname=lastname,
            bio=bio,
            location=location,
            workplace=workplace,
            education=education,
            highlights=highlights,
            linkedin=linkedin,
            facebook=facebook,
            instagram=instagram,
            cover_photo=cover_photo_filename,
            media_upload=','.join(media_upload_filenames),
            media_type='image' if media_uploads and media_uploads[0].content_type.startswith('image') else 'video', 
            user_id=current_user.id
        )

        db.session.add(profile)
        db.session.commit()
        flash('Profile created successfully!', category='success')
        return redirect(url_for('views.cans'))

    return render_template('create-profile.html')


@views.route('/cans')
def cans():
    profiles = UserProfile.query.all()
    return render_template("cans.html", profiles=profiles)

@views.route('/update-profile/<int:profile_id>', methods=['GET', 'POST'])
@login_required
def update(profile_id):
    profile = UserProfile.query.get_or_404(profile_id)

    if request.method == 'POST':
        profile.firstname = request.form.get('firstName')
        profile.lastname = request.form.get('lastName')
        profile.bio = request.form.get('bio')
        profile.location = request.form.get('location')
        profile.workplace = request.form.get('workplace')
        profile.education = request.form.get('education')
        profile.highlights = request.form.get('highlights')
        profile.linkedin = request.form.get('linkedin')
        profile.facebook = request.form.get('facebook')
        profile.instagram = request.form.get('instagram')

        # Handle cover photo upload
        cover_photo = request.files.get('coverPhoto')
        if cover_photo and allowed_file(cover_photo.filename):
            cover_photo_filename = secure_filename(cover_photo.filename)
            cover_photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cover_photo_filename))
            profile.cover_photo = cover_photo_filename

        # Handle media uploads
        media_uploads = request.files.getlist('mediaUpload')
        media_filenames = []

        for media in media_uploads:
            if media and allowed_file(media.filename):
                filename = secure_filename(media.filename)
                media.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                media_filenames.append(filename)

        if media_filenames:
            profile.media_upload = ','.join(media_filenames)

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.update', profile_id=profile.id))

    return render_template('update-profile.html', profile=profile)



    

@views.route('/Paper_Cardboard')
def Paper_Cardboard():
    return render_template("Paper_Cardboard.html")

@views.route('/plastic')
def plastic():
    return render_template("plastic.html")

@views.route('/Metal_Info')
def MetalInfo():
    return render_template("Metal_Info.html")

@views.route('/GlassInfo')
def GlassInfo():
    return render_template("GlassInfo.html")

@views.route('/Electronics_Info')
def electronics():
    return render_template("Electronics_Info.html")


@views.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Proceed with saving the file or any other processing
        flash('File allowed and processed successfully!')
        return redirect(url_for('views.index'))
    else:
        flash('File not allowed')
        return redirect(request.url)
    

@views.route('/delete-profile', methods=['POST'])
@login_required
def delete_profile():
    data = request.get_json()  
    profile_id = data.get('profile_id') 
    
  
    profile = UserProfile.query.get_or_404(profile_id)
    
    
    db.session.delete(profile)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Profile deleted successfully!'})

@views.route('/pick-profile')
def pick_profile():
    return render_template('pick_profile_home.html', hide_navbar_items=True)



@views.route('/indivual-profile')
def individual_profile():
    return render_template('individual_home.html')

@views.route('/admin-profile')
def admin_profile():
    return render_template('pick_profile_home.html')


ADMIN_PASSWORD = 'admin123'
ADMIN_EMAIL = 'admin@easylink.ac.za'
@views.route('/admin_home')
def admin_home():
    # Ensure only logged-in admin can access this page
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_auth.adm_login'))
    
    return render_template('admin_home.html')

# Update login route to set session
@views.route('/adm_login', methods=['GET', 'POST'])
def adm_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the input matches hardcoded admin details
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True  # Set session variable
            flash('Login successful!', 'success')
            return redirect(url_for('views.admin_home'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('admin_auth.adm_login'))

    return render_template('adm_login.html')


   
@views.route('/some_protected_page')
def some_protected_page():
    if 'admin_logged_in' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('admin_auth.adm_login'))

    return render_template('protected_page.html')


@views.route('/org-trade')
def org_trade():
    return render_template('org_trade.html')

@views.route('/requests')
def admin_request():
    return render_template('requests.html')

@views.route('/admin_base', methods=['GET', 'POST'])
def admin_base():
    return render_template('admin_home.html')





@views.route('/admin_kids')
def admin_kids():
    return render_template('admin_kids.html')

@views.route('/admin_individuals')
def admin_individuals():
    return render_template('admin_individuals.html')

@views.route('/request-trades')
def request_trades():
    return render_template('request_trades.html')

@views.route('/Request_Blog')
def request_blog():
    return render_template('request_blog.html')

@views.route('/Request_Videos')
def request_video():
    return render_template('request_videos.html')

@views.route('/ict')
def ict():
    return render_template('ict.html')

@views.route('/iot')
def iot():
    return render_template('iot.html')

@views.route('/code')
def code():
    return render_template('code.html')

@views.route('/networks')
def networks():
    return render_template('networks.html')

@views.route('/udemy')
def udemy():
    return render_template('udemy.html')

@views.route('/math')
def math():
    return render_template('math.html')






@views.route('/manage_telkom')
def manage_telkom():
    return render_template('manage_telkom.html')

@views.route('/manage_microsoft')
def manage_microsoft():
    return render_template('manage_microsoft.html')

@views.route('/manage_cisco')
def manage_cisco():
    return render_template('manage_cisco.html')

@views.route('/manage_google')
def manage_google():
    return render_template('manage_google.html')

@views.route('/manage_learners')
def manage_learners():
    return render_template('manage_learners.html')

@views.route('/numbers')
def numbers():
    return render_template('numbers.html')

@views.route('/manage_sectorC')
def manage_sectorC():
    return render_template('manage_sectorC.html')

@views.route('/manage_sectorD')
def manage_sectorD():
    return render_template('manage_sectorD.html')

@views.route('/manage_sectorE')
def manage_sectorE():
    return render_template('manage_sectorE.html')

@views.route('/manage_sectorF')
def manage_sectorF():
    return render_template('manage_sectorF.html')

@views.route('/manage_sectorG')
def manage_sectorG():
    return render_template('manage_sectorG.html')

#SECTORA
@views.route('/manage_sectorA', methods=['GET', 'POST'])
def manage_sectorA():
    if request.method == 'POST':
        image_file = request.files['image']
        pdf_link = request.form['pdf']

        # Save the uploaded image
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # Save the post in the database
        new_post = Posts(image=image_file.filename, pdf=pdf_link)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('views.manage_sectorA'))

    # Query all posts from the database
    posts = Posts.query.all()

    return render_template('manage_sectorA.html', posts=posts)

@views.route('/manage_nexus', methods=['GET', 'POST'])
def manage_nexus():
    if request.method == 'POST':
        device_name = request.form['device_name']
        image_file = request.files['image']
        price = request.form['price']

        # Save the uploaded image
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # Save the post in the database
        new_post = Save(device_name=device_name, image=image_file.filename, price=price)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('views.manage_nexus'))

    # Query all posts from the database
    posts = Save.query.all()

    return render_template('manage_nexus.html', posts=posts)


@views.route('/sectorA') #gvbhbhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
def sectorA():
   posts = Posts.query.order_by(Posts.date_created.desc()).all() 
   return render_template("sectorA.html", posts=posts)


@views.route('/delete/<int:post_id>', methods=['POST'])  #gggggggggggggggggggggggggggggggggggggggggggggggg
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    # Remove the post's image file from the file system if needed
    if post.image:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], post.image))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('views.manage_sectorA'))


@views.route('/edit/<int:post_id>', methods=['GET', 'POST']) #eeeeeeeeeeeeeeeeeeee
def edit_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':
        # Update the post with new data
        post.pdf = request.form['pdf']
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image = filename
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('views.manage_sectorA'))
    return render_template('edit_post.html', post=post)

@views.route('/kca')
def kca():
    return render_template('kca.html')

@views.route('/components')
def components():
    return render_template('components.html')


@views.route('/accounting')
def accounting():
    return render_template('accounting.html')

@views.route('/robotics')
def robotics():
    return render_template('robotics.html')

@views.route('/arduino_projects')
def arduino_projects():
    return render_template('arduino_projects.html')

@views.route('/physics')
def physics():
    return render_template('physics.html')



@views.route('/science')
def science():
    return render_template('science.html')

@views.route('/engineer')
def engineer():
    return render_template('engineer.html')

@views.route('/nex')
def nex():
    return render_template('nex.html')

@views.route('/computers')
def computers():
    return render_template('computers.html')

@views.route('/save')
def save():
    return render_template('save.html')

#CYBERSECURITY

# Route to manage cybersecurity (handle file uploads and show posts)
@views.route('/manage_cybersecurity', methods=['GET', 'POST'])
def manage_cybersecurity():
    if request.method == 'POST':
        image_file = request.files['image']
        pdf_link = request.form['pdf']

        # Save the uploaded image to the specified folder
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
        image_file.save(image_path)

        # Save the new post in the database
        new_post = CyberPosts(image=image_file.filename, pdf=pdf_link)
        db.session.add(new_post)
        db.session.commit()

        flash('New cybersecurity post created!', 'success')
        return redirect(url_for('views.manage_cybersecurity'))

    # Query all cybersecurity posts from the database
    posts = CyberPosts.query.all()
    return render_template('manage_cybersecurity.html', posts=posts)


@views.route('/agric')
def agric():
    posts = CyberPosts.query.order_by(CyberPosts.date_created.desc()).all()
    return render_template("agric.html", posts=posts)


@views.route('/delete_agric/<int:post_id>', methods=['POST'])
def delete_agric_post(post_id):
    post = CyberPosts.query.get_or_404(post_id)

    # If the post has an image, remove the image file from the file system
    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()

    flash('Agric post deleted successfully!', 'success')
    return redirect(url_for('views.manage_agric'))

# Route to edit a specific cybersecurity post by ID
@views.route('/edit_agric/<int:post_id>', methods=['GET', 'POST'])
def edit_agric_post(post_id):
    post = CyberPosts.query.get_or_404(post_id)

    if request.method == 'POST':
        # Update the post with new PDF and image data
        post.pdf = request.form['pdf']

        # Check if an image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save the new image
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image = filename

        db.session.commit()
        flash('Agric post updated successfully!', 'success')
        return redirect(url_for('views.manage_agric'))

    return render_template('edit_agric_post.html', post=post)

#DATA

# Route to manage data (handle file uploads and show posts)
@views.route('/manage_data', methods=['GET', 'POST'])
def manage_data():
    if request.method == 'POST':
        image_file = request.files['image']
        pdf_link = request.form['pdf']

        # Save the uploaded image to the specified folder
        if image_file:  # Check if an image file was uploaded
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(image_path)
            image_filename = image_file.filename
        else:
            image_filename = None  # Handle the case where no image is uploaded

        # Save the new post in the database
        new_post = DataPosts(image=image_filename, pdf=pdf_link)
        db.session.add(new_post)
        db.session.commit()

        flash('New Data Science post created!', 'success')
        return redirect(url_for('views.manage_data'))

    # Query all data posts from the database
    posts = DataPosts.query.all()
    return render_template('manage_data.html', posts=posts)

# Route to view all data posts
@views.route('/entrepreneurship')
def daentrepreneurshipta():
    posts = DataPosts.query.order_by(DataPosts.date_created.desc()).all()
    return render_template("entrepreneurship.html", posts=posts)

# Route to delete a specific data post by ID
@views.route('/delete_data/<int:post_id>', methods=['POST'])
def delete_data_post(post_id):
    post = DataPosts.query.get_or_404(post_id)

    # If the post has an image, remove the image file from the file system
    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()

    flash('Data Science post deleted successfully!', 'success')
    return redirect(url_for('views.manage_data'))

# Route to edit a specific data post by ID
@views.route('/edit_data/<int:post_id>', methods=['GET', 'POST'])
def edit_data_post(post_id):
    post = DataPosts.query.get_or_404(post_id)

    if request.method == 'POST':
        # Update the post with new PDF and image data
        post.pdf = request.form['pdf']

        # Check if an image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save the new image
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image = filename
            # If no new image is uploaded, keep the existing image

        db.session.commit()
        flash('Data Science post updated successfully!', 'success')
        return redirect(url_for('views.manage_data'))

    return render_template('edit_data_post.html', post=post)


#SECTORB
# Route to manage sector posts (handle file uploads and show posts)
@views.route('/manage_sectorB', methods=['GET', 'POST'])
def manage_sectorB():
    if request.method == 'POST':
        image_file = request.files['image']
        pdf_link = request.form['pdf']

        # Save the uploaded image to the specified folder
        if image_file:  # Check if an image file was uploaded
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(image_path)
            image_filename = image_file.filename
        else:
            image_filename = None  # Handle the case where no image is uploaded

        # Save the new post in the database
        new_post = NetworkPosts(image=image_filename, pdf=pdf_link)  # Adjust to your model for  sector B posts
        db.session.add(new_post)
        db.session.commit()

        flash('New Sector Bpost created!', 'success')
        return redirect(url_for('views.manage_sectorB'))

    # Query all sectorB posts from the database
    posts = NetworkPosts.query.all()  # Adjust to your model for sectorB posts
    return render_template('manage_sectorB.html', posts=posts)

# Route to view all sectorB posts
@views.route('/sectorB')
def sectorB():
    posts = NetworkPosts.query.order_by(NetworkPosts.date_created.desc()).all()  # Adjust to your model for sectorB posts
    return render_template("sectorB.html", posts=posts)

# Route to delete a specific sectorB post by ID
@views.route('/delete_network/<int:post_id>', methods=['POST'])
def delete_sectorB_post(post_id):
    post = NetworkPosts.query.get_or_404(post_id)

    # If the post has an image, remove the image file from the file system
    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()

    flash('Sector B post deleted successfully!', 'success')
    return redirect(url_for('views.manage_sectorB'))

# Route to edit a specific sectorB post by ID
@views.route('/edit_sectorB/<int:post_id>', methods=['GET', 'POST'])
def edit_sectorB_post(post_id):
    post = NetworkPosts.query.get_or_404(post_id)

    if request.method == 'POST':
        # Update the post with new PDF and image data
        post.pdf = request.form['pdf']

        # Check if an image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save the new image
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image = filename
            # If no new image is uploaded, keep the existing image

        db.session.commit()
        flash('Sector B post updated successfully!', 'success')
        return redirect(url_for('views.manage_sectorB'))

    return render_template('edit_sector_post.html', post=post)  # Ensure you have this template created


#QUESTIONS
# Route to manage question posts (handle file uploads and show posts)
@views.route('/manage_questions', methods=['GET', 'POST'])
def manage_questions():
    if request.method == 'POST':
        image_file = request.files['image']
        pdf_link = request.form['pdf']

        # Save the uploaded image to the specified folder
        if image_file:  # Check if an image file was uploaded
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(image_path)
            image_filename = image_file.filename
        else:
            image_filename = None  # Handle the case where no image is uploaded

        # Save the new post in the database
        new_post = QuestionPosts(image=image_filename, pdf=pdf_link)  # Adjust to your model for question posts
        db.session.add(new_post)
        db.session.commit()

        flash('New Question post created!', 'success')
        return redirect(url_for('views.manage_questions'))

    # Query all question posts from the database
    posts = QuestionPosts.query.all()  # Adjust to your model for question posts
    return render_template('manage_questions.html', posts=posts)

# Route to view all question posts
@views.route('/questions')
def questions():
    posts = QuestionPosts.query.order_by(QuestionPosts.date_created.desc()).all()  # Adjust to your model for question posts
    return render_template("questions.html", posts=posts)

# Route to delete a specific question post by ID
@views.route('/delete_question/<int:post_id>', methods=['POST'])
def delete_question_post(post_id):
    post = QuestionPosts.query.get_or_404(post_id)

    # If the post has an image, remove the image file from the file system
    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()

    flash('Question post deleted successfully!', 'success')
    return redirect(url_for('views.manage_questions'))

# Route to edit a specific question post by ID
@views.route('/edit_question/<int:post_id>', methods=['GET', 'POST'])
def edit_question_post(post_id):
    post = QuestionPosts.query.get_or_404(post_id)

    if request.method == 'POST':
        # Update the post with new PDF and image data
        post.pdf = request.form['pdf']

        # Check if an image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save the new image
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image = filename
            # If no new image is uploaded, keep the existing image

        db.session.commit()
        flash('Question post updated successfully!', 'success')
        return redirect(url_for('views.manage_questions'))

    return render_template('edit_question_post.html', post=post)  # Ensure you have this template created


#MEMOS
# Route to manage memo posts (handle file uploads and show posts)
@views.route('/manage_memo', methods=['GET', 'POST'])
def manage_memo():
    if request.method == 'POST':
        image_file = request.files['image']
        pdf_link = request.form['pdf']

        # Save the uploaded image to the specified folder
        if image_file:  # Check if an image file was uploaded
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(image_path)
            image_filename = image_file.filename
        else:
            image_filename = None  # Handle the case where no image is uploaded

        # Save the new post in the database
        new_post = MemoPosts(image=image_filename, pdf=pdf_link)  # Adjust to your model for memo posts
        db.session.add(new_post)
        db.session.commit()

        flash('New Memo post created!', 'success')
        return redirect(url_for('views.manage_memo'))

    # Query all memo posts from the database
    posts = MemoPosts.query.all()  # Adjust to your model for memo posts
    return render_template('manage_memo.html', posts=posts)

# Route to view all memo posts
@views.route('/memo')
def memo():
    posts = MemoPosts.query.order_by(MemoPosts.date_created.desc()).all()  # Adjust to your model for memo posts
    return render_template("memo.html", posts=posts)

# Route to delete a specific memo post by ID
@views.route('/delete_memo/<int:post_id>', methods=['POST'])
def delete_memo_post(post_id):
    post = MemoPosts.query.get_or_404(post_id)

    # If the post has an image, remove the image file from the file system
    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()

    flash('Memo post deleted successfully!', 'success')
    return redirect(url_for('views.manage_memo'))

# Route to edit a specific memo post by ID
@views.route('/edit_memo/<int:post_id>', methods=['GET', 'POST'])
def edit_memo_post(post_id):
    post = MemoPosts.query.get_or_404(post_id)

    if request.method == 'POST':
        # Update the post with new PDF and image data
        post.pdf = request.form['pdf']

        # Check if an image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save the new image
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image = filename
            # If no new image is uploaded, keep the existing image

        db.session.commit()
        flash('Memo post updated successfully!', 'success')
        return redirect(url_for('views.manage_memo'))

    return render_template('edit_memo_post.html', post=post)  # Ensure you have this template created
