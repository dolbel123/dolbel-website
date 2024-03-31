from website import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    cart_items = db.relationship('Cart', backref=db.backref('user', lazy=True))
    orders = db.relationship('Order', backref=db.backref('user', lazy=True))
    auctions = db.relationship('Auction', backref=db.backref('seller', lazy=True))

  
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def __str__(self):
        return f'<User {self.id}>'

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=13), nullable=False, unique=True)
    description = db.Column(db.String(length=1324), nullable=False, unique=True)
    product_detail = db.Column(db.String(1000), nullable=False)
    in_stock = db.Column(db.Integer(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    product_picture = db.Column(db.String(1000), nullable=False)
   

    cart_items = db.relationship('Cart', backref=db.backref('item', lazy=True))
    orders = db.relationship('Order', backref=db.backref('item', lazy=True))
    auctions = db.relationship('Auction', backref=db.backref('seller-item', lazy=True))

    def __repr__(self):
        return f'<Item {self.name}>'
    
    def __str__(self):
        return f'<Item {self.name}>'

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    user_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_link = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __str__(self):
        return f'<Cart {self.id}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)

    user_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_link = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __str__(self):
        return f'<Order {self.id}>'
    

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_picture = db.Column(db.String(1000), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    current_bid = db.Column(db.Float, default=0.0)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='auction')
    bids = db.relationship('Bid', backref='auction')

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('auction', uselist=False))

    

    def __str__(self):
        return f'<Auction {self.id}>'






class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_picture = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # FK
    user_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    auction_link = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)

    def __str__(self):
        return f'<Review {self.id}>'


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_date = db.Column(db.DateTime, default=datetime.utcnow)
    # FK
    user_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    auction_link = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)

    def __str__(self):
        return f'<Bid {self.id}>'