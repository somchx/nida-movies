from flask import render_template
from app import app
from app.api import get_movie_by_id, get_comments_by_movie_id

@app.route('/')
def landing():
    return render_template('index.html')

import bcrypt
from flask import request, render_template, redirect
from app import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = app.db["users"].find_one({"email": email})
        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            return redirect('/home')
        else:
            return redirect('/login')
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/setting/movie')
def setting_movie():
    return render_template('setting/setting_movie.html')

@app.route('/setting/user')
def setting_user():
    print("render")
    return render_template('setting/setting_user.html')

@app.route('/movie/detail/<id>')
def movie_detail_page(id):
    movie = get_movie_by_id(id)
    if not movie:
        return "Movie not found", 404
    comments = get_comments_by_movie_id(id)
    return render_template("movie_detail.html", movie=movie, comments=comments)



