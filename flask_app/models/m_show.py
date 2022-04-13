from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Show:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.description = data["description"]
        self.release_date = data["release_date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
    
    #Add Show method
    @classmethod
    def addShow(cls, data):
        query = "INSERT INTO shows (title, network, description, release_date, created_at, updated_at , user_id) VALUES(%(title)s, %(network)s, %(description)s, %(release_date)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL("users_tv").query_db(query,data)
    

    #Get All shows method
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        resultado = connectToMySQL("users_tv").query_db(query)
        all_shows=[]
        for show in resultado:
            all_shows.append(cls(show))
        return all_shows
    
    #Get one show
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        resultado = connectToMySQL("users_tv").query_db(query, data)
        return cls(resultado[0])

    #Update Show
    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title=%(title)s, network=%(network)s, description=%(description)s, release_date=%(release_date)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL("users_tv").query_db(query,data)
    
    #validate Show
    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            is_valid = False
            flash("El nombre del show debe tener al menos 3 carácteres","show")
        if len(show['network']) < 3:
            is_valid = False
            flash("El nombre del network deben tener al menos 3 carácteres","show")
        if len(show['description']) < 10:
            is_valid = False
            flash("La descripción debe tener al menos 3 carácteres","show")
        if show['release_date'] == "":
            is_valid = False
            flash("Por favor ingresa una fecha","show")
        return is_valid
    
    #Delete Show
    # @classmethod
    # def delete(cls,data):
    #     query = "DELETE FROM shows WHERE id = %(id)s;"
    #     print("---DELETE---")
    #     print("show id", data)
    #     return connectToMySQL("users_tv").query_db(query,data)
    
    #count likes
    @classmethod
    def count_likes(cls,data):
        query = "SELECT COUNT(shows.id) FROM users LEFT JOIN liked_by ON users.id = liked_by.user_id LEFT JOIN shows ON shows.id = liked_by.show_id WHERE shows.id = %(id)s;"
        resultado = connectToMySQL("users_tv").query_db(query, data)
        print("-----TEST COUNT------")
        print (resultado)
        return resultado
    
    #Get name user who posted
    @classmethod
    def get_user_name_post(cls, data):
        query = "SELECT users.first_name, users.last_name FROM shows LEFT JOIN users ON user_id = users.id WHERE shows.id = %(id)s;"
        resultado = connectToMySQL("users_tv").query_db(query, data)
        print("-------GET USER TEST --------")
        print(resultado)
        return resultado
        