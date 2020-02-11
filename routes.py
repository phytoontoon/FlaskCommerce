import os
import secrets
from PIL import Image
from flask import render_template , url_for , flash , redirect , request , jsonify , json 
from ProiectPa import app , db ,bcrypt , ma
from flask_admin.contrib.sqla import ModelView
from ProiectPa.models import Post , Pizza, Ingredients,User, Salads, Sauce , Drinks , Pastas
from functools import wraps
from flask_login import login_user, current_user, logout_user, login_required
from ProiectPa.forms import RegistrationForm, LoginForm , UpdateAccountForm ,IngredientsForm, PizzaForm , SaladsForm, SauceForm , DrinksForm, PastaForm

class Comanda(ma.Schema):
  class Meta:
    fields = ('id', 'details', 'price', 'table', 'date_posted','user_id','staff_id','over')

comenzi = Comanda(many=True)
@app.route('/')
@app.route('/home')
def home():
    Ing=Ingredients.query.all()
    Piz=Pizza.query.all()
    Sal=Salads.query.all()
    Sau=Sauce.query.all()
    Drin=Drinks.query.all()
    Past=Pastas.query.all()
    return render_template('todo.html',Sauces=Sau,Ingredients=Ing,Pizza=Piz,Salads=Sal,Drinks=Drin,Pastas=Past)
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture2(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (256, 256)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/order' , methods=['POST'])
def PostOrder():
    details = request.json['details']
    price = request.json['price']
    table = request.json['table']
    user_id=request.json['user_id']
    over=request.json['over']
    new_post = Post(details,price,table,user_id,over)
    db.session.add(new_post)
    db.session.commit()
    return '201'


@app.route('/orders' , methods=['GET'])
def GetOrders():
    posts=Post.query.all()  
    result=comenzi.dump(posts)
        
    return jsonify(result)



@app.route('/order/<id>' , methods=['PUT'])
def UpdateOrder(id):
    order=Post.query.get(id)
    order.staff_id=request.json['staff_id']
    order.over=request.json['over']
    db.session.commit()
    return '201'


@app.route('/order<id>', methods=['DELETE'])
def DeleteOrder(id):
    db.session.delete(Product.query.get(id))
    db.session.commit()
    return '201'

@app.route('/register', methods=['POST','GET'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data , email=form.email.data,password=hashed_password,urole='user')
        db.session.add(user)
        db.session.commit()
        ##flash(f'Cont creat cu succes!')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register' ,form=form)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

    
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    id=current_user.get_id
    x=Post.query.all()
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form,coms=x,id=id)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin/pizza", methods=['POST','GET'])
def adminpizza():
    form=PizzaForm()
   ## SaForm=SaladsForm()
    ## InForm=IngredientsForm()
    ## PaForm=PaForm()
    ## DiForm=DiForm()
    ## SuForm=SauceForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            text = picture_file
            txt= url_for('static', filename='profile_pics/' + text)
            print(txt)
            pizza=Pizza(name=form.name.data,details=form.ingredients.data,weight=form.weight.data,price=form.price.data,image=txt)
            db.session.add(pizza)
            db.session.commit()
    return render_template('pizzaadmin.html',form=form)

@app.route("/admin/Salads", methods=['POST','GET'])
def adminsalads():
    
    form=SaladsForm()
    ## InForm=IngredientsForm()
    ## PaForm=PaForm()
    ## DiForm=DiForm()
    ## SuForm=SauceForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            text = picture_file
            txt= url_for('static', filename='profile_pics/' + text)
            print(txt)
            salad=Salads(name=form.name.data,details=form.ingredients.data,weight=form.weight.data,price=form.price.data,image=txt)
            db.session.add(salad)
            db.session.commit()
    return render_template('saladadmin.html',form=form)

@app.route("/admin/Ingredients", methods=['POST','GET'])
def admining():
  
    form=IngredientsForm()
    ## PaForm=PaForm()
    ## DiForm=DiForm()
    ## SuForm=SauceForm()
    if form.validate_on_submit():
       
      
        Ing=Ingredients(name=form.name.data,price=form.price.data)
        db.session.add(Ing)
        db.session.commit()
    return render_template('admining.html',form=form)
        
@app.route("/admin/Paste", methods=['POST','GET'])
def adminpaste():
  
    
    form=PastaForm()
    ## DiForm=DiForm()
    ## SuForm=SauceForm()
    if form.validate_on_submit() :
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            text = picture_file
            txt= url_for('static', filename='profile_pics/' + text)
            print(txt)
            past=Pastas(name=form.name.data,details=form.ingredients.data,weight=form.weight.data,price=form.price.data,image=txt)
            db.session.add(past)
            db.session.commit()
    return render_template('adminpastas.html',form=form)

@app.route("/admin/sauce", methods=['POST','GET'])
def adminsauce():
    form=SauceForm()
    if form.validate_on_submit() :
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            text = picture_file
            txt= url_for('static', filename='profile_pics/' + text)
            print(txt)
            sau=Sauce(name=form.name.data,weight=form.weight.data,price=form.price.data,image=txt)
            db.session.add(sau)
            db.session.commit()
    return render_template('adminsauce.html',form=form)

@app.route("/admin/drinks", methods=['POST','GET'])
def admindrinks():
    form=DrinksForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            text = picture_file
            txt= url_for('static', filename='profile_pics/' + text)
            print(txt)
            dr=Drinks(name=form.name.data,weight=form.weight.data,price=form.price.data,image=txt)
            db.session.add(dr)
            db.session.commit()
    return render_template('admindrinks.html',form=form)

@app.route("/admin/comenzi")
def tabasyc():
    return render_template('comasync.html')

@app.route("/comenzi")
def staffcom():
    return render_template('comstaff.html')

@app.route("/admin/register", methods=['POST','GET'])
def staffregister():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data , email=form.email.data,password=hashed_password,urole='staff')
        db.session.add(user)
        db.session.commit()
        ##flash(f'Cont creat cu succes!')
        return redirect(url_for('home'))
    return render_template('regstaff.html',title='Register' ,form=form)
