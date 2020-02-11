from ProiectPa import db  ,  login_manager
from datetime import datetime
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    custom = db.relationship('CustomPizza', backref='author', lazy=True)
    urole=db.Column(db.String(20),nullable=False)
    def __repr__(self):
        return f"{self.username}"
    def get_urole(self):
        return self.urole
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float,nullable=False)
    table=db.Column(db.Integer,nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    staff_id=db.Column(db.Integer,nullable=True)
    over = db.Column(db.Integer, default='0')
    def __init__(self,details,price,table,user_id,over,staff_id=0):
        self.details=details
        self.price=price
        self.table=table
        self.user_id=user_id
        self.staff_id=staff_id
        self.over = over
     
class Pizza(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text,unique=True,nullable=False)
    details=db.Column(db.Text,nullable=False)
    weight=db.Column(db.Float , nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40) , nullable=False, default='default.jpg')
class Pastas(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text,unique=True,nullable=False)
    details=db.Column(db.Text,nullable=False)
    weight=db.Column(db.Float , nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40) , nullable=False, default='default.jpg')
class Salads(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text,unique=True,nullable=False)
    details=db.Column(db.Text,nullable=False)
    weight=db.Column(db.Float , nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40) , nullable=False, default='default.jpg')
class Sauce(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text,unique=True,nullable=False)
    weight=db.Column(db.Float , nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40) , nullable=False, default='default.jpg')
class Drinks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text,unique=True,nullable=False)
    weight=db.Column(db.Float , nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40) , nullable=False, default='default.jpg')
class Ingredients(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),unique=True)
    price = db.Column(db.Float,nullable=False)
class CustomPizza(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text,nullable=False)
    details=db.Column(db.Text,nullable=False)
    client_id=db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)




