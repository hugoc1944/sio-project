from flask import Blueprint, render_template, redirect, url_for, request
from .auth import session
from .database import *

views = Blueprint('views', __name__)

# Routes for blueprint views
@views.route('/', methods=['GET','POST'])
def home():
    if('user' in session):
        username = session['user']['username']
        return render_template('index.html', username=username)
    else:
        return redirect( url_for('auth.login'))