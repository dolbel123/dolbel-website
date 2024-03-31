from sqlalchemy.exc import SQLAlchemyError  # Import the SQLAlchemyError exception
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from website.models import Item, Cart, Order, Auction
from flask_login import login_required, current_user
from website import db
from intasend import APIService
from werkzeug.utils import secure_filename
from .forms import AuctionForm
from datetime import datetime
views = Blueprint('views', __name__)


API_PUBLISHABLE_KEY = 'ISPubKey_test_67eb8fd0-d2e0-408f-9675-ec4e9ad18602'
API_TOKEN = 'ISSecretKey_test_f8154bce-546a-44b4-a123-2ade0c21f2cf'

@views.route('/')
def market():
    
    
    # Calculate the cart count for the logged-in user
    cart = Cart.query.filter_by(user_link=current_user.id).all() if current_user.is_authenticated else []
    cart_count = len(cart)

    items = Item.query.all()

    return render_template('market.html', items=items, cart=cart, cart_count=cart_count)


 


@views.route('/add-to-cart/<int:item_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(item_id):
    item = Item.query.get_or_404(item_id)

    # Check if the item is already in the user's cart
    existing_item = Cart.query.filter_by(item_link=item.id, user_link=current_user.id).first()

    try:
        if existing_item:
            # If the item exists, increase the quantity
            existing_item.quantity += 1
            flash('Quantity increased in your cart', 'success')
            cart_item = existing_item  # Assign the existing item to cart_item
        else:
            # Add the item to the user's cart with quantity 1
            cart_item = Cart(quantity=1, user_link=current_user.id, item_link=item.id)
            db.session.add(cart_item)
            flash('Item added to your cart', 'success')

        db.session.commit()
        flash(f'{cart_item.item.name} added to cart', 'success')
        return redirect(request.referrer)

    except SQLAlchemyError as e:  # Use SQLAlchemyError
        db.session.rollback()  # Rollback changes if an exception occurs
        print('Error adding item to cart:', e)
        flash(f'Error: {e}', 'danger')
        return redirect(request.referrer)
    





    

from flask import render_template

@views.route('/cart')
@login_required
def cart():
    user_cart = Cart.query.filter_by(user_link=current_user.id).all()
    total_fee = calculate_total_fee(user_cart)  # You need to implement this function
    shipping_cost = calculate_shipping_cost()  # You need to implement this function

    return render_template('cart.html', user_cart=user_cart, total_fee=total_fee, shipping_cost=shipping_cost)


def calculate_total_fee(cart):
    total_fee = sum(item.quantity * item.item.price for item in cart)
    return total_fee

def calculate_shipping_cost():
    # Implement your shipping cost calculation logic here
    shipping_cost = 5  # Replace with your actual calculation
    return shipping_cost

@views.route('/update_quantity/<int:item_id>/<action>', methods=['POST'])
@login_required
def update_quantity(item_id, action):
    cart_item = Cart.query.filter_by(item_link=item_id, user_link=current_user.id).first()

    if cart_item:
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'reduce':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                # If quantity is already 1, you might want to remove the item from the cart
                db.session.delete(cart_item)
                flash(f'{cart_item.item.name} removed from cart', 'success')

        db.session.commit()
        flash('Cart updated successfully', 'success')

    return redirect(url_for('views.cart'))

@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(user_link=current_user.id).all()

    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.item.price * item.quantity  # Fix the typo here, change "-" to "+"

            # Convert total amount to Pounds (GBP)
            

            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
            create_order_response = service.collect.mpesa_stk_push(
                phone_number=2547377067499,
                email=current_user.email_address,
                amount= total + 5,
                narrative='Dolbel Order Summary'
            )

            for item in customer_cart:
                new_order = Order()
                
                new_order.quantity = item.quantity
                new_order.price = item.item.price
                new_order.status = create_order_response['invoice']['state'].capitalize()
                new_order.payment_id = create_order_response['id']

                new_order.item_link = item.item_link
                new_order.user_link = item.user_link

                db.session.add(new_order)

                item_in_db = Item.query.get(item.item_link)
                item_in_db.in_stock -= item.quantity

            for item in customer_cart:
                db.session.delete(item)
                # Commenting out the line below as it seems incorrect
                # db.session.delete(item)

            db.session.commit()

            flash('Dolbel Order Completed')
            return redirect('/orders')
        except Exception as e:
            print(e)
            print("The Item does not exist")
            flash('Order not placed')
            return redirect('/')
    else:
        flash('Your cart is empty')
        return redirect('/')



@views.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_link=current_user.id).all()
    return render_template('orders.html', orders=orders)



@views.route('/auction', methods=['GET', 'POST'])
@login_required
def auction():
    
    
    # Calculate the cart count for the logged-in user
    cart = Cart.query.filter_by(user_link=current_user.id).all() if current_user.is_authenticated else []
    cart_count = len(cart)

  

    auctions = Auction.query.all()
    return render_template('auction.html', cart=cart, auctions=auctions)



@views.route('/list-item', methods=['GET', 'POST'])
@login_required
def list_item():
    form = AuctionForm()

    if form.validate_on_submit():
        product_picture = form.product_picture.data
        file_path = f"./media/{secure_filename(product_picture.filename)}"
        product_picture.save(file_path)

        try:
            # Convert start_time and end_time to datetime objects
            start_time = datetime.strptime(form.start_time.data, '%Y-%m-%d')
            end_time = datetime.strptime(form.end_time.data, '%Y-%m-%d')

            # Rest of your code...

            new_auction = Auction(
                product_picture=file_path,
                item_name=form.item_name.data,
                description=form.description.data,
                start_time=start_time,
                end_time=end_time,
                current_bid=form.current_bid.data,
                seller_id=current_user.id,
                item_id=form.item_id.data  # Replace 'some_item_id' with the actual ID of the item
            )

            db.session.add(new_auction)
            db.session.commit()

            flash(f'Item "{form.item_name.data}" listed successfully', 'success')
            return redirect(url_for('views.auction'))

        except Exception as e:
            print(e)
            db.session.rollback()  # Rollback changes if an exception occurs
            flash(f'Error: {e}', 'danger')
            return redirect(request.referrer)

    return render_template('list-item.html', form=form)

@views.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Item.query.get_or_404(product_id)  # Fetch the product from the database
    print(product.product_picture) 
    return render_template('product-details.html', product=product)
