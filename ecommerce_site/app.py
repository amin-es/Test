from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key
# It's good practice to make this a more complex and randomly generated key for production
# For example: import os; app.config['SECRET_KEY'] = os.urandom(24)

# Product catalog
products = [
    {
        'id': 1,
        'name': 'Laptop',
        'price': 1200.00,
        'image': 'uploads/laptop.jpg',
        'description': 'A high-performance laptop suitable for all your needs.'
    },
    {
        'id': 2,
        'name': 'Smartphone',
        'price': 800.00,
        'image': 'uploads/smartphone.jpg',
        'description': 'A latest model smartphone with advanced features.'
    },
    {
        'id': 3,
        'name': 'Headphones',
        'price': 150.00,
        'image': 'uploads/headphones.jpg',
        'description': 'Noise-cancelling headphones for an immersive audio experience.'
    },
    {
        'id': 4,
        'name': 'Smartwatch',
        'price': 250.00,
        'image': 'uploads/smartwatch.jpg',
        'description': 'Stay connected and track your fitness with this smartwatch.'
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return 'Product not found', 404

@app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET']) # Allow GET for simplicity in links
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    # Find the product from our catalog
    product_to_add = next((p for p in products if p['id'] == product_id), None)
    if not product_to_add:
        return 'Product not found', 404 # Or redirect with a message

    item_in_cart = next((item for item in session['cart'] if item['id'] == product_id), None)

    if item_in_cart:
        item_in_cart['quantity'] += 1
    else:
        session['cart'].append({
            'id': product_to_add['id'],
            'name': product_to_add['name'],
            'price': product_to_add['price'],
            'quantity': 1
        })
    session.modified = True # Make sure the session is saved
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Your cart is empty. Add some products before checking out.', 'info')
        return redirect(url_for('index'))

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        # Simulate order processing
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')

        print("--- ORDER RECEIVED (TEST MODE) ---")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Address: {address}")
        print("Cart Items:")
        for item in cart_items:
            print(f"  - {item['name']} (Qty: {item['quantity']})")
        print(f"Total: ${total_price:.2f}")
        print("------------------------------------")

        session.pop('cart', None) # Clear the cart
        flash('Order placed successfully! (TEST MODE)', 'success')
        return redirect(url_for('index'))

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
