from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.m_user import User
from flask_app.models.m_show import Show
from flask_app.models.m_car import Car
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

#ruta principales
@app.route( '/', methods=['GET'] )
def inicio():
    return render_template( "index.html" )

#REGISTRAR USUARIOS
@app.route('/register', methods=['POST'])
def register():
    #validación
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    #Datos de session
    id = User.addUser(data)
    session['user_id'] = id

    return redirect('/dashboard')

#RUTA LOGIN
@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

#Ruta DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    car_data = {

    }
    # , shows=Show.get_all(), likes = User.get_likes(data), otroLike = User.check_likes(data)
    return render_template("dashboard.html",user=User.get_by_id(data), cars = Car.get_all(), poster = Car.get_user_name_seller(data), purchased = Car.get_if_purchased(data))

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#Ruta GET AÑADIR CArros
@app.route('/new')
def newCar():
    data ={
        'id': session['user_id']
    }
    return render_template("newCar.html", user=User.get_by_id(data))

#lpurchase a car
@app.route('/purchase', methods=['POST'])
def purchase():
    data = {
        'user_id': session['user_id'],
        'car_id': request.form['car_id']
    }
    User.purchase(data)
    print(data)
    return redirect('/dashboard')





#like a show
@app.route('/like', methods=['POST'])
def like():
    data = {
        'user_id': session['user_id'],
        'show_id': request.form['show_id']
    }
    User.like(data)
    print(data)
    return redirect('/dashboard')

#UNLIKE a show
@app.route('/unlike', methods=['POST'])
def unlike():
    data = {
        'user_id': session['user_id'],
        'show_id': int(request.form['show_id_u'])
    }
    User.unlike(data)
    print(data)
    return redirect('/dashboard')
