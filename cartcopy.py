from flask import Flask, render_template, request, redirect, session
from collections import defaultdict
import json 
app = Flask(__name__)
app.secret_key = 'hfawef920343a0fsdoogs'

products = [
    {'id': 1, 'name': 'Pepperoni Pizza', 'price': 8.99},
    {'id': 2, 'name': 'Vegan Californian Pizza', 'price': 13.99},
    {'id': 3, 'name': 'Margeritha Pizza', 'price': 9.99},
    {'id': 4, 'name': 'Ham Pizza', 'price': 11.99},
    {'id': 5, 'name': 'Tonno Pizza', 'price': 12.99},
    {'id': 6, 'name': 'Chicken Pizza', 'price': 12.99},
    {'id': 7, 'name': 'BBQ Grill Pizza', 'price': 13.99},
    {'id': 8, 'name': 'Maxicano Pizza', 'price': 13.99},
    {'id': 9, 'name': 'Four Cheese Pizza', 'price': 13.99},
    {'id': 10, 'name': 'Hawaii Pizza', 'price': 9.99},
    {'id': 11, 'name': 'Vegan Pizza', 'price': 13.99},
    {'id': 12, 'name': 'Meatlover Pizza', 'price': 14.99},
    {'id': 13, 'name': 'Cappuccino', 'price': 1.95},
    {'id': 14, 'name': 'Americano', 'price': 1.95},
    {'id': 15, 'name': 'Latte', 'price': 2.45},
    {'id': 16, 'name': 'Coca Cola', 'price': 1.35},
    {'id': 17, 'name': 'Sprite Zero', 'price': 1.35}
]
item_quantities = {}
complete_orders = []
complete_mario = []
orders = {}
order_id_counter = 1

def generate_order_id():
    global order_id_counter
    order_id = order_id_counter
    order_id_counter += 1
    return order_id

@app.route('/')
def index():
    return render_template('final.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] =[]
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        session['cart'] = session['cart'] + [product]
        return '', 204
    else:
        return '', 404

@app.route('/view_cart')
def view_cart():
    cart = session.get('cart', [])
    item_quantities = defaultdict(int)
    for item in cart:
        item_key = (item['name'], item['price'])
        item_quantities[item_key] += 1
    return render_template('cart.html', item_quantities=item_quantities)

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    total = round(sum(item['price'] for item in cart), 2)
    item_quantities = defaultdict(int)
    for item in cart:
        item_key = (item['name'], item['price'])
        item_quantities[item_key] += 1
    return render_template('checkout.html', cart=cart, total=total, item_quantities=item_quantities)

@app.route('/process_order', methods=['POST'])
def process_order():
    cart = session.get('cart', [])
    item_quantities = defaultdict(int)
    for item in cart:
        item_key = (item['name'], item['price'])
        item_quantities[item_key] += 1
    if 'cart' in session:
        name = request.form.get('name')
        order_id = generate_order_id()
        order = {
            'order_id': order_id,
            'name': name,
            'cart': item_quantities.items()
        }
        orders[order_id] = order
        session['luigi']=session['cart']
        session['order_id'] = order_id
 
        file_path = 'orders.json'
        order['cart'] = list(order['cart'])
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        data.append(order)
        with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                complete_orders.append(order)
        session['cart'] = []
        return render_template('order_completed.html', order_id=order_id, name=name, item_quantities=item_quantities, complete_orders=complete_orders)
    else:
        return "Your cart is empty!"

@app.route('/luigi')
def luigi_orders():
    return render_template('luigi.html', complete_orders=complete_orders)

@app.route('/mark_order_complete/<int:order_id>', methods=['GET'])
def mark_order_complete(order_id):
    index_to_remove = None
    for i, order in enumerate(complete_orders):
        if order['order_id'] == order_id:
            index_to_remove = i
            break
    if index_to_remove is not None:
        completed_order = complete_orders.pop(index_to_remove)
        complete_mario.append(completed_order)
    return redirect('/luigi')

@app.route('/mario')
def mario_orders():
    return render_template('mario.html', complete_mario=complete_mario) 

if __name__ == '__main__': 
    app.run(debug=True)