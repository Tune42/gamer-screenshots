from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os.path
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# generated key in python via secrets.token_hex(16)
# secret key serves as protection against modifying cookies and such
app.config['SECRET_KEY'] = '34b1d628cc7a4a647d3900624aa2bf91'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/richLUL.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link = db.Column(db.Text, nullable=False, default='static/richLUL.png')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

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

# runs server in debug mode if this app is ran in python
# instead of having to use 'flask run' command in terminal.
if __name__ == '__main__':
    app.run(debug=True)