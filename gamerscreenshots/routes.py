from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from gamerscreenshots import app, db, bcrypt
from gamerscreenshots.forms import RegistrationForm, LoginForm
from gamerscreenshots.models import User, Post


@app.route("/")
@app.route("/home")
def home():
    posts = []
    users = {}
    for post in Post.query.order_by(Post.date_posted).all():
        posts.append(post)
    posts.reverse()
    for user in User.query.all():
        users[user.id] = (user.username, user.image_file)
    return render_template('home.html', posts=posts, users=users)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Already logged in!', 'success')
        return redirect(url_for('home'))
    form = RegistrationForm()  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # success, below, is the bootstrap class banner
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')