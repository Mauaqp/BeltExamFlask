from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.m_show import Show
from flask_app.models.m_user import User


#Ruta AddShow
@app.route('/show/new', methods=["POST"])
def createRecipe ():
    if not Show.validate_show(request.form):
        return redirect('/new')
    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "description" : request.form["description"],
        "release_date" : request.form["release_date"],
        "user_id" : session["user_id"]
    }
    Show.addShow(data)
    return redirect('/dashboard')

#mostrar shows
@app.route('/show/<int:id>')
def show_display(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_display.html",show=Show.get_one(data),user=User.get_by_id(user_data), count = Show.count_likes(data), poster = Show.get_user_name_post(data))

#ruta para GET de editar/update
@app.route('/edit/show/<int:id>')
def get_show_edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_show.html",edit = Show.get_one(data), user=User.get_by_id(user_data))

#ruta para editar/update
@app.route('/update/show', methods=['POST'])
def update_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/new')
    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "description" : request.form["description"],
        "release_date" : request.form["release_date"],
        "user_id" : session["user_id"],
        #id del show - hidden en el formulario
        "id": request.form["id"]
    }
    Show.update(data)
    return redirect('/dashboard')

#eliminar shows
@app.route('/delete/show/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Show.delete(data)
    return redirect('/dashboard')