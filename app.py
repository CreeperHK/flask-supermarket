from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo
from werkzeug.security import generate_password_hash as hash, check_password_hash as check_hash
import datetime
import pytz
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.secret_key = 'chu'

# MongoDB Connection
connectType = 'azure'

if connectType == 'Atlas':
    myclient = pymongo.MongoClient("")
    mongo = myclient["db"]

if connectType == 'azure':
    myclient = pymongo.MongoClient("")
    mongo = myclient["supermarket"]

if connectType == 'localhost':
    myclient = pymongo.MongoClient("")
    mongo = myclient["flask_test"]

@app.route('/')
def index():
    session.pop('username', None)
    session.pop('admin', None)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.user.find_one({'username': username})  # Select `username` from user

        # Admin login
        if username.endswith('-a'):
            admin_username = username.rstrip('-a').strip()  # Remove '-a' for admin login
            admin_user = mongo.admin.find_one({'username': admin_username})  # Select `username` from admin

            if admin_user:
                if check_hash(admin_user['password'], password):
                    session['username'] = admin_username 
                    session['admin'] = admin_username
                    session.permanent = True
                    return redirect(url_for('admin'))
                else:
                    flash('Invalid admin username or password')
            else:
                flash('Invalid user rank')

        # Non-admin login
        elif user and check_hash(user['password'], password):
            session['username'] = username  # Save username to session
            return redirect(url_for('welcome'))
        else:   
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash(password)

        # Check if the username exists
        existing_user = mongo.user.find_one({'username': username})  # Select `username` from user
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            # Stop user for register
        
        # Check if end with -a
        if username.endswith('-a'):
            flash('illegal Username. Please choose a different one.')
            return redirect(url_for('register')) 
            # Stop user for register           

        # Check done with no error
        mongo.user.insert_one({'username': username, 'password': hashed_password})  # Insert username, password into user
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
        # register done, send to login

    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' in session and 'admin' in session:
        return render_template('admin.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/admin_item')
def admin_item():
    if 'username' in session and 'admin' in session:
        items = mongo.item.find().sort([('show', -1), ('id', 1)])
        return render_template('admin_item.html', items=items)
    return redirect(url_for('login'))

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if 'username' in session and 'admin' in session:
            new_item = {
                'show': request.form.get('show', False) == 'on',
                'id': request.form['id'],
                'image': request.form['image'],
                'name': request.form['name'],
                'description': request.form['description'],
                'price': float(request.form['price'])
            }
            mongo.item.insert_one(new_item)
            return redirect(url_for('admin_item'))
    return render_template('add_item.html')

@app.route('/edit_item/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'username' in session and 'admin' in session:
        if request.method == 'POST':
            updated_item = {
                'show': request.form.get('show', False) == 'on',
                'id': request.form['id'],
                'image': request.form['image'],
                'name': request.form['name'],
                'description': request.form['description'],
                'price': float(request.form['price'])
            }
            mongo.item.update_one({'id': item_id}, {'$set': updated_item})
            return redirect(url_for('admin_item'))
        
        item = mongo.item.find_one({'id': item_id})
        return render_template('edit_item.html', item=item)
    return redirect(url_for('login'))

@app.route('/delete_item/<item_id>', methods=['POST'])
def delete_item(item_id):
    if 'username' in session and 'admin' in session:
        mongo.item.delete_one({'id': item_id})
        return redirect(url_for('admin_item'))
    return redirect(url_for('login'))

@app.route('/order')
def order():
    if 'username' in session:
        items = mongo.item.find({'show': True}).sort('id', 1)
        return render_template('order.html', items=items)
    return redirect(url_for('login'))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if 'username' in session:
        username = session['username']
        order_data = {
            'username': username,
            'items': [],
            'total_price': 0,
            'time': datetime.datetime.now(),
            'state':'Processing'
        }
        quantities = []

        # request.form.items() shows like = [('quantity[1]', '0'), ('quantity[2]', '4'), ('quantity[3]', '0')]
        for key, value in request.form.items():
            if key.startswith('quantity['):
                item_id = key.split('[')[1][:-1]
                quantity = int(value)
                quantities.append([item_id, quantity]) # Add to list for Insert to DB

        # Start to add order
        for item_id, quantity in quantities:
            if quantity > 0:
                item = mongo.item.find_one({'id': item_id})
                if item:
                    item_price = item['price']
                    order_data['items'].append({'id': item_id, 'quantity': quantity})
                    order_data['total_price'] += item_price * quantity
                else:
                    print(f"Item with id {item_id} not found.")

        if order_data['items']:
            mongo.order.insert_one(order_data) # Insert (order_data) INTO order

        return redirect(url_for('show_order'))
    return redirect(url_for('login'))

@app.route('/show_order')
def show_order():
    if 'username' in session:
        username = session['username']
        state_priority = {
            'Completed': 1,
            'Shipping': 2,
            'Confirmed': 3,
            'Processing': 4
        }
        orders_data = list(mongo.order.find({'username': username}))
        items_dict = {str(item['id']): item['name'] for item in mongo.item.find()}

        orders_data.sort(key=lambda order: state_priority.get(order['state'], 5))

        # Rename the item.id into item.name for showing
        for order in orders_data:
            for item in order['items']:
                item_id = str(item['id'])
                item_name = items_dict.get(item_id, "Forget to put the item name in 'item', you idiot")
                item['name'] = item_name  # Add item name to the item object

    return render_template('show_order.html', orders=orders_data)

@app.route('/admin_order')
def admin_order():
    if 'username' in session and 'admin' in session:
        orders_data = list(mongo.order.find())
        items_dict = {str(item['id']): item['name'] for item in mongo.item.find()}

        # Rename the item.id into item.name for showing
        for order in orders_data:
            for item in order['items']:
                item_id = str(item['id'])
                item_name = items_dict.get(item_id, "Forget to put the item name in 'item', you idiot")
                item['name'] = item_name  # Add item name to the item object

        return render_template('admin_order.html', orders=orders_data)
    return redirect(url_for('login'))

@app.route('/update_order_state/<order_id>', methods=['POST'])
def update_order_state(order_id):
    if 'username' in session and 'admin' in session:
        new_state = request.form['new_state'] 
        mongo.order.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'state': new_state}} 
        )
        return redirect(url_for('admin_order'))
    return redirect(url_for('login'))

@app.route('/filter_orders', methods=['GET'])
def filter_orders():
    if 'username' in session and 'admin' in session:
        selected_state = request.args.get('state')

        items_dict = {str(item['id']): item['name'] for item in mongo.item.find()}
        if selected_state == "All":
            orders = list(mongo.order.find())
            for order in orders:
                for item in order['items']:
                    item_id = str(item['id'])
                    item_name = items_dict.get(item_id, "Forget to put the item name in 'item', you idiot")
                    item['name'] = item_name

        elif selected_state:
            orders = list(mongo.order.find({'state': selected_state}))
            for order in orders:
                for item in order['items']:
                    item_id = str(item['id'])
                    item_name = items_dict.get(item_id, "Forget to put the item name in 'item', you idiot")
                    item['name'] = item_name
        else:
            orders = list(mongo.order.find())
            for order in orders:
                for item in order['items']:
                    item_id = str(item['id'])
                    item_name = items_dict.get(item_id, "Forget to put the item name in 'item', you idiot")
                    item['name'] = item_name

        return render_template('admin_order.html', orders=orders)
    return redirect(url_for('login'))

@app.route('/delete_order/<order_id>', methods=['POST'])
def delete_order(order_id):
    if 'username' in session and 'admin' in session:
        mongo.order.delete_one({'_id': ObjectId(order_id)})
        return redirect(url_for('admin_order'))  # Redirect to the order list page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)