from flask import Blueprint, render_template, redirect, url_for, request
from .auth import session
from .database import *
from werkzeug.security import check_password_hash

views = Blueprint('views', __name__)

# Routes for blueprint views
@views.route('/', methods=['GET','POST'])
def home():
    if('user' in session):
        username = session['user']['username']
        return render_template('index.html', username=username)
    else:
        return redirect( url_for('auth.login'))
    
@views.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        email = session['user']['email']
        username = session['user']['username']

        old_password = request.form['old-password']
        new_password = request.form['new-password']
        if  (check_password_hash( get_user_password(email), old_password) == False):
            data = {'status': 404}
            return data
        else:
            update_password(email, new_password)
            data = {'status': 200}
            return data
    else:
        if('user' in session):
            email = session['user']['email']
            username = session['user']['username']
            return render_template('profile.html', email = email, username = username)
        else:
            return redirect(url_for('auth.login'))    

@views.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        email = session['user']['email']
        ratings = request.form['ratings']
        reviews = request.form['p-review']
        add_review(email, ratings, reviews)
        return render_template('product.html', session_user = email, reviews = get_review(email))
    else:
        if('user' in session):
            email = session['user']['email']
            return render_template('product.html', session_user = email, reviews = get_review(email))
        else:
            return redirect(url_for('auth.login'))