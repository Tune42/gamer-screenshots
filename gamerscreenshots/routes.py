from flask import render_template, url_for, flash, redirect
from gamerscreenshots import app
from gamerscreenshots.forms import RegistrationForm, LoginForm
from gamerscreenshots.models import User, Post

#home route
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

#about route
@app.route("/about")
def about():
    return render_template('about.html', title='About')

#registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # success, below, is the bootstrap class banner
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

#login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)