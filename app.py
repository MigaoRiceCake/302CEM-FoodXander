from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from decimal import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskapp'
app.config['SECRET_KEY'] = "somethingsomethingsecretkey??"

db = SQLAlchemy(app)

class users(db.Model, UserMixin):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(128), nullable=False)
    
    orders = db.relationship('orders', backref='customer')
    
    def get_id(self):
        return (self.ID)

    def __repr__(self):
        return '<Username %r>' % self.username
    
class restaurants(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(128), nullable=False)

    menuitems = db.relationship('menuitems', backref='restaurant')
    orders = db.relationship('orders', backref='restaurant')


    def get_id(self):
        return (self.ID)

    def __repr__(self):
        return '<Name %r>' % self.name
    
# class drivers(db.Model):
#     ID = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(32), nullable=False)
#     phone = db.Column(db.Integer, nullable=False)

#     def get_id(self):
#            return (self.ID)

#     def __repr__(self):
#         return '<Name %r>' % self.name

class menuitems(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    restID = db.Column(db.Integer, db.ForeignKey('restaurants.ID'), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Numeric, nullable=False)

    def get_id(self):
        return (self.ID)

    def __repr__(self):
        return '<Name %r>' % self.name

class orders(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.ID'), nullable=False)
    restID = db.Column(db.Integer, db.ForeignKey('restaurants.ID'), nullable=False)
    items = db.Column(db.String(512), nullable=False)
    # driverID = db.Column(db.Integer, db.ForeignKey('drivers.ID'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum('pending', 'complete', 'cancelled'), nullable=False, server_default=('pending'))
    
    def get_id(self):
        return (self.ID)

class registerForm(FlaskForm):
    username = StringField(label=("Username"), validators=[InputRequired()])
    password = PasswordField(label=('Password'), validators=[InputRequired()])
    phone = StringField(label=('Phone Number (+852)'), validators=[InputRequired()])
    address = StringField(label=('Address'), validators=[InputRequired()])
    submit = SubmitField(label=('Register'))

class loginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

loginSys = LoginManager()
loginSys.init_app(app)
loginSys.login_view = 'login'

@loginSys.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()

    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        if user is None:
            user = users(username = form.username.data, password = form.password.data, phone = form.phone.data, address = form.address.data)
            db.session.add(user)
            db.session.commit()

            flash("Registration Successful!")
            form.username.data = ''
            form.password.data = ''
            form.phone.data = ''
            form.address.data = ''
            return redirect(url_for('login'))
        else:
            flash("Username already taken, please try again")
            form.username.data = ''
            form.password.data = ''

    return render_template('register.html', form = form)

@app.route('/home')
@login_required
def home():
    return render_template('landing.html')

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['GET','POST'])
def order():
    try:
        print(session['cart_item'])
        print(session['all_total_price'])
        
        n_order = orders(userID = int(current_user.ID), restID = 1, items = str(session['cart_item']), status = 'pending')
        db.session.add(n_order)
        db.session.commit()

        flash("Order Submitted!")

        session['cart_item'] = {}
        session['all_total_quantity'] = 0
        session['all_total_price'] = 0.00
        
        return redirect(url_for('.menu'))
    except Exception as e:
        print(e)

@app.route('/add', methods=['GET','POST'])
def add_to_cart():
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        # validate the received values
        if _quantity and _code and request.method == 'POST':
            row = menuitems.query.filter_by(ID=_code).first()
            itemDict = { str(row.ID) : {
                                    'name' : row.name,
                                    'code' : row.ID,
                                    'quantity' : int(_quantity),
                                    'price' : str(row.price),
                                    't_price': str(_quantity * row.price)
                                }
                }
            
            all_total_price = Decimal(0.0)
            all_total_quantity = 0
            
            # session.modified = True
            if 'cart_item' in session:
                if str(row.ID) in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if str(row.ID) == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = int(total_quantity)
                            session['cart_item'][key]['t_price'] = str(total_quantity * row.price)
                else:
                    session['cart_item'].update(itemDict)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][str(key)]['quantity'])
                    individual_price = Decimal(session['cart_item'][str(key)]['t_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemDict
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row.price
            
            session['all_total_quantity'] = all_total_quantity
            print(session['all_total_quantity'])
            session['all_total_price'] = all_total_price
            print(session['all_total_price'])
            
            return redirect(url_for('.menu'))
        else:			
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
        
@app.route('/empty')
def empty_cart():
    try:
        session['cart_item'] = {}
        session['all_total_quantity'] = 0
        session['all_total_price'] = 0.00
        return redirect(url_for('.menu'))
    except Exception as e:
        print(e)

@app.route('/remove_item/<int:code>')
def remove_item(code):
    try:
        all_total_price = Decimal(0.0)
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:				
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = Decimal(session['cart_item'][key]['t_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
		
        if all_total_quantity != 0:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return redirect(url_for('.menu'))
    except Exception as e:
        print(e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()

    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        if user:
            if str(form.password.data) == user.password:
                login_user(user)
                flash("Login Succesfull, Welcome {}".format(user.username))
                return redirect(url_for('home'))
            else:
                flash("Username and Password does not match")
        else:
            flash("User does not exist")
    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logout Succesfull")
    return redirect(url_for('index'))

@app.route('/settings/<int:ID>', methods=['GET', 'POST'])
@login_required
def settings(ID):
    form = registerForm()
    modUser = users.query.get_or_404(ID)
    form.username.data = modUser.username
    form.password.data = ''
    form.phone.data = modUser.phone
    form.address.data = modUser.address

    if request.method == "POST":
        modUser.username = request.form['username']
        modUser.password = request.form['password']
        modUser.phone = request.form['phone']
        modUser.address = request.form['address']

        try:
            db.session.commit()
            flash("Account Settings Appended Successfully!")
            return redirect(url_for('home'))

        except:
            flash("Error Appending Account Settings, Please Try Again!")
            return render_template("settings.html", form = form, modUser = modUser, ID = ID)
    else:
        return render_template("settings.html", form = form, modUser = modUser, ID = ID)

@app.route('/delete/<int:ID>')
@login_required
def delete(ID):
    if ID == current_user.ID:
        modUser = users.query.get_or_404(ID)

        try:
            db.session.delete(modUser)
            db.session.commit()
            flash("User Deleted Successfully!")

            return redirect(url_for('index'))

        except:
            flash("Error Deleting User, Please Try Again!")
            return redirect(url_for('settings', ID = current_user.ID))
    else:
        flash("Permission Denied: User Cannot Be Deleted!")
        return redirect(url_for('home'))
    
@app.route('/admin')
def admin():

    pendList = {}
    pendOrderList = orders.query.filter_by(status='pending')
    
    for row in pendOrderList:
        uID = row.userID
        user = users.query.get_or_404(uID)
        username = user.username
        items = json.loads(row.items.replace("'", '"'))
        
        total = Decimal(0.0)
        
        for item in items:
            total = total + Decimal(items[item]['t_price'])
        
        pendList.update({ str(row.ID): {
                                    'user' : str(username),
                                    'status' : str(row.status),
                                    'date' : str(row.date),
                                    'items' : items,
                                    'total': str(total)
                                }
                            })
        
    compList = {}
    compOrderList = orders.query.filter_by(status='complete')
    
    for row in compOrderList:
        uID = row.userID
        user = users.query.get_or_404(uID)
        username = user.username
        items = json.loads(row.items.replace("'", '"'))
        
        total = Decimal(0.0)
        
        for item in items:
            total = total + Decimal(items[item]['t_price'])
        
        compList.update({ str(row.ID): {
                                    'user' : str(username),
                                    'status' : str(row.status),
                                    'date' : str(row.date),
                                    'items' : items,
                                    'total': str(total)
                                }
                            })

    cancList = {}
    cancOrderList = orders.query.filter_by(status='cancelled')
    
    for row in cancOrderList:
        uID = row.userID
        user = users.query.get_or_404(uID)
        username = user.username
        items = json.loads(row.items.replace("'", '"'))
        
        total = Decimal(0.0)
        
        for item in items:
            total = total + Decimal(items[item]['t_price'])
        
        cancList.update({ str(row.ID): {
                                    'user' : str(username),
                                    'status' : str(row.status),
                                    'date' : str(row.date),
                                    'items' : items,
                                    'total': str(total)
                                }
                            })
    
    return render_template('admin.html', pendList = pendList, compList = compList, cancList = cancList)

@app.route('/pending_order/<int:code>')
def pending_order(code):
    try:
        target = orders.query.get_or_404(code)
        target.status = 'pending'
        db.session.commit()
        flash("Order Reverted")
        return redirect(url_for('.admin'))
    except Exception as e:
        print(e)

@app.route('/complete_order/<int:code>')
def complete_order(code):
    try:
        target = orders.query.get_or_404(code)
        target.status = 'complete'
        db.session.commit()
        flash("Order Complete")
        return redirect(url_for('.admin'))
    except Exception as e:
        print(e)
        
@app.route('/cancel_order/<int:code>')
def cancel_order(code):
    try:
        target = orders.query.get_or_404(code)
        target.status = 'cancelled'
        db.session.commit()
        flash("Order Cancelled")
        return redirect(url_for('.admin'))
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    app.run(debug=True)