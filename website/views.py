from flask import Blueprint, render_template, redirect, url_for, request
from .auth import session
from .database import *
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

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
            type = get_type(email)
            return render_template('profile.html', email = email, username = username, type = type)
        else:
            return redirect(url_for('auth.login'))    

@views.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        email = session['user']['email']
        ratings = request.form['ratings']
        reviews = request.form['p-review']
        add_review(email, ratings, reviews)
        return render_template('product.html', session_user = email, reviews = get_review())
    else:
        if('user' in session):
            email = session['user']['email']
            return render_template('product.html', session_user = email, reviews = get_review())
        else:
            return redirect(url_for('auth.login'))

@views.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        email = session['user']['email']
        ratings = request.form['ratings']
        reviews = request.form['p-review']
        add_review(email, ratings, reviews)
        return render_template('about.html', session_user = email)
    else:
        if('user' in session):
            email = session['user']['email']
            return render_template('about.html', session_user = email)
        else:
            return redirect(url_for('auth.login'))
        
@views.route('/search', methods=['GET'])
def products_search():
    lista_produtos = get_products()
    if ('user' in session):
        return render_template('products.html',lista=lista_produtos,user=session['user']["username"])
    else:
	    return redirect(url_for('auth.login'))

@views.route("/products", methods=['GET'])
def products():
    print(get_products())
    lista_produtos = get_products()
    if ('user' in session):
        return render_template('products.html',lista=lista_produtos,user=session['user']["username"])
    else:
        return redirect(url_for('auth.login'))
    
@views.route("/add_product", methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        stock = request.form['stock']
        categories = request.form['categories']

        upload_dir = os.path.join("website", "static", "images", "uploads")
        file = request.files['image']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        filename = file.filename
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        add_products(quantity, stock, description, name, file_path, price, categories)
        return render_template('add_product.html', user=session['user']["username"])
    else:
        if ('user' in session):
            return render_template('add_product.html',user=session['user']["username"])
        else:
            return redirect(url_for('auth.login'))