from flask import Flask, render_template, url_for
import sqlite3
app = Flask(__name__)

#dummy data, used in home route and pulling from the db
posts = []
conn = sqlite3.connect('gamerscreenshots.db')
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