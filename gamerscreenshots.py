from flask import Flask, render_template, url_for
app = Flask(__name__)

#dummy data, used in home route
posts = [
    {
        'author': 'Tune42',
        'title': 'First Post',
        'content': 'First post content',
        'date_posted': 'April 29, 2020'
    },
    {
        'author': 'adb9210',
        'title': 'Second Post',
        'content': 'Second post content',
        'date_posted': 'April 29, 2020'
    }
]

#root page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

#about page
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# runs server in debug mode if this app is ran in python
# instead of having to use 'flask run' command in terminal.
if __name__ == '__main__':
    app.run(debug=True)