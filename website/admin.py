




from flask import Blueprint, render_template, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm
from website import db 
from website.models import Item, Order
from werkzeug.utils import secure_filename]
ppplplp

admin = Blueprint('admin', __name__)

@admin.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_shop_item():
    if current_user.id == 1:  
        form = ShopItemsForm()

        if form.validate_on_submit():
            product_picture = form.product_picture.data
            file_path = f"./media/{secure_filename(product_picture.filename)}"
            product_picture.save(file_path)

            product = Item(
                name=form.name.data,
                price=form.price.data,
                barcode=form.barcode.data,
                description=form.description.data,
                product_detail=form.product_detail.data,
                in_stock=form.in_stock.data,
                product_picture=file_path  
            )
            
            db.session.add(product)
            db.session.commit()
            flash(f'{form.name.data} added successfully')
            
            return redirect(url_for('admin.add_shop_item'))

        return render_template('add-shop-items.html', form=form)
    
    return render_template('404.html')

@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
         items = Item.query.order_by(Item.date_added).all()
         return render_template('shop_items.html', items=items)
    return render_template('404.html')




@admin.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.id == 1:
        item = Item.query.get_or_404(id)
        form = ShopItemsForm(obj=item)

        try:
            if form.validate_on_submit():
                # Update the existing item with the form data
                item.name = form.name.data
                item.price = form.price.data
                item.barcode = form.barcode.data
                item.description = form.description.data
                item.product_detail = form.product_detail.data
                item.in_stock = form.in_stock.data

                # Handle updating the product picture if a new one is provided
                if form.product_picture.data:
                    product_picture = form.product_picture.data
                    file_path = f"./media/{secure_filename(product_picture.filename)}"
                    product_picture.save(file_path)
                    item.product_picture = file_path

                # Commit the changes to the database
                db.session.commit()

                flash('Product updated successfully', 'success')
                return redirect(url_for('admin.shop_items'))
        except Exception as e:
            print('product not updated', e)
            flash('Product details not updated!!')

        return render_template('edit-product.html', form=form, item=item)
    
    return render_template('404.html')




@admin.route('/delete-product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    if current_user.id == 1:
        item = Item.query.get_or_404(id)

        try:
            # Delete the item from the database
            db.session.delete(item)
            db.session.commit()
            flash('Product deleted successfully', 'success')
        except Exception as e:
            print('Error deleting product:', e)
            flash('Error deleting product', 'danger')

        return redirect(url_for('admin.shop_items'))

    return render_template('404.html')


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/view-orders')
@login_required
def view_order():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_order.html', orders=orders)
    
    return render_template('404.html')


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        order = Order.query.get_or_404(order_id)  # Fetch the order from your database using the provided order_id
        form = OrderForm()

        if form.validate_on_submit():
            # Update the order status in your database based on form data
            order.status = form.status.data
            db.session.commit()

            flash('Order status updated successfully', 'success')
            return redirect(url_for('admin.view_order'))

        return render_template('update_order.html', form=form, order=order)
    return render_template('404.html')




@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin_dashboard.html')
    return render_template('404.html')

