from flask import render_template, send_file, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
# from flask_share import Share
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
import qrcode
import io
import shortuuid
import string
import random
from urllib.parse import urlparse


from .models import Url, User
from . import app, db, mail, cache


def shorten_url(long_url):
    # Generate a random short URL key
    letters = string.ascii_letters + string.digits
    short_key = ''.join(random.choice(letters) for _ in range(6))
    
    # Store the short URL in a database
    # Here, we'll return it
    return short_key

# Helper function to generate the QR code
def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_code_image = qr.make_image(fill_color="black", back_color="white")
    return qr_code_image



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email.lower()).first()
        print(user)
        
        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Password incorrect. Please try again.')
        else:
            flash('Email is not registered yet.')
    return render_template('login.html')

# creating a logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            flash('Email already exists.')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.')
        elif password != confirm_password:
            flash('Passwords don\'t match.')
        else:
            new_user = User(email=email.lower(), username=username, password_hash=generate_password_hash(password))
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
            flash('Account created successfully.')
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        title = request.form['title']
        custom_url = request.form['custom_url'] or None
        if custom_url:
            existing_url = Url.query.filter_by(short_url=custom_url).first()
            if existing_url:
                flash ('That custom URL already exists. Please try another one!')
                return redirect(url_for('home'))
            o = urlparse(request.base_url)
            short_url = f"{o.hostname}/{custom_url}"
            url_code = custom_url
            custom_url=custom_url
        elif long_url[:4] != 'http':
            long_url = 'http://' + long_url
        else:
            o = urlparse(request.base_url)
            url_code = shortuuid.uuid()[:6]
            short_url = f"{o.hostname}/{url_code}"
        url = Url(long_url=long_url, short_url=short_url, custom_url=custom_url, url_code = url_code, title=title, user_id=current_user.id)
        url.save()
        return redirect(url_for('dashboard', url_id =url.id))

    urls = Url.query.order_by(Url.created_at.desc()).limit(10).all()
    return render_template('index.html', urls=urls)

@app.route('/<url_code>')
@cache.cached(timeout=50)
def redirect_url(url_code):
    url = Url.query.filter_by(url_code=url_code).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.long_url)
    return 'URL not found.'


@app.route("/dashboard/<int:url_id>/")
@login_required
@cache.cached(timeout=50)
def dashboard(url_id):
    url = Url.query.filter_by(id=url_id).first()
    host = request.host_url

    # Generate the QR code image
    qr_code_image = generate_qr_code(url.long_url)

    # Save the image to a temporary file
    temp_file_path = 'C:\\Users\\hp\\Documents\\flask-project\\darrkzero-scissor-api\\darrkzero\\static\\temp_qrcode.png'
    qr_code_image.save(temp_file_path)

    # Send the file as a response
            
    # return send_file(temp_file_path, mimetype='image/png', as_attachment=True)
    return render_template('dashboard.html', url=url, host=host, temp_file_path=temp_file_path)


@app.route('/history')
@login_required
@cache.cached(timeout=50)
def link_history():
    urls = Url.query.filter_by(user_id=current_user.id).order_by(Url.created_at.desc()).all()
    host = request.host_url
    return render_template('history.html', urls=urls, host=host)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    url = Url.query.get_or_404(id)
    db.session.delete(url)
    db.session.commit()
    return redirect(url_for('home'))
    

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_url(id):
    url = Url.query.get_or_404(id)
    if url:
        if request.method == 'POST':
            custom_url = request.form['custom_url']
            if custom_url:
                existing_url = Url.query.filter_by(custom_url=custom_url).first()
                if existing_url:
                    flash ('That custom URL already exists. Please try another one.')
                    return redirect(url_for('edit_url', id=id))
                o = urlparse(request.base_url)
                short_url = f"{o.hostname}/{custom_url}"
                url.custom_url = custom_url
                url.short_url = short_url
                url.url_code = custom_url
            db.session.commit()
            return redirect(url_for('dashboard', url_id=url.id))
        return render_template('edit.html', url=url)
    return 'URL not found.'

# about route 
@app.route('/about')
def about():

    return render_template('about.html')

