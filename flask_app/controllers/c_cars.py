from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.controllers.c_users import purchase
from flask_app.models.m_car import Car
from flask_app.models.m_user import User


#Ruta Add car
@app.route('/car/new', methods=["POST"])
def createCar ():
    if not Car.validate_car(request.form):
        return redirect('/new')
    data = {
        "model" : request.form["model"],
        "maker" : request.form["maker"],
        "description" : request.form["description"],
        "price" : request.form["price"],
        "year" : request.form["year"],
        "user_id" : session["user_id"]
    }
    Car.addCar(data)
    return redirect('/dashboard')

# #mostrar Cars
@app.route('/car/<int:id>')
def car_display(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }

    # count = Car.count_likes(data),
    return render_template("car_display.html", car=Car.get_one(data), user=User.get_by_id(user_data), poster = Car.get_user_name_post(data), purchase = Car.get_if_purchased(data))

# #ruta para GET de editar/update
@app.route('/edit/car/<int:id>')
def get_car_edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_car.html", edit = Car.get_one(data), user=User.get_by_id(user_data))

# #ruta para editar/update
@app.route('/update/car', methods=['POST'])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/new')
    data = {
        "model" : request.form["model"],
        "maker" : request.form["maker"],
        "description" : request.form["description"],
        "price" : request.form["price"],
        "year" : request.form["year"],
        "user_id" : session["user_id"],

        #id del Car - hidden en el formulario
        "id": request.form["id"]
    }
    Car.update(data)
    return redirect('/dashboard')

# #eliminar Cars
@app.route('/delete/car/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Car.delete(data)
    return redirect('/dashboard')