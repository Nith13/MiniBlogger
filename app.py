# app.py (Flask backend)

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'key'

# Dummy data for users and posts
users = {'user1': {'email': 'nith@christ.com', 'password': generate_password_hash('password')}}
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            return render_template('register.html', message='Username already exists')

        users[username] = {'email': email, 'password': generate_password_hash(password)}
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts.append({'author': session['username'], 'title': title, 'content': content, 'likes': 0, 'dislikes': 0})
        return redirect(url_for('index'))

    return render_template('create_post.html')

if __name__ == '__main__':
    app.run(debug=True)
