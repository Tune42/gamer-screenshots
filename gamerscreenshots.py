from flask import Flask, render_template, url_for, flash, redirect
import sqlite3
import os.path
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# generated key in python via secrets.token_hex(16)
# secret key serves as protection against modifying cookies and such
app.config['SECRET_KEY'] = '34b1d628cc7a4a647d3900624aa2bf91'

#dummy data, used in home route and pulling from the db
posts = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "gamerscreenshots.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('SELECT * FROM posts')
results = c.fetchall()
for entry in results:
    posts.append({
        'Author': entry[0],
        'Title': entry[1],
        'Comments': entry[2],
        'Date': entry[3],
        'Link': entry[4]
    })
conn.close()

#home route
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

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