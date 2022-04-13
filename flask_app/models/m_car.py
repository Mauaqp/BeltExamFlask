from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    def __init__(self, data):
        self.id = data["id"]
        self.model = data["model"]
        self.maker = data["maker"]
        self.price = data["price"]
        self.description = data["description"]
        self.year = data["year"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
    
    #Add Show method
    @classmethod
    def addCar(cls, data):
        query = "INSERT INTO cars (model, maker, price, description, year, created_at, updated_at , user_id) VALUES(%(model)s, %(maker)s, %(price)s, %(description)s,%(year)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL("car_deals").query_db(query,data)
    

    #Get All cars method
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        resultado = connectToMySQL("car_deals").query_db(query)
        all_cars=[]
        for car in resultado:
            all_cars.append(cls(car))
        return all_cars
    
    #Get one show
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        resultado = connectToMySQL("car_deals").query_db(query, data)
        return cls(resultado[0])

    #Update CAr
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET model=%(model)s, maker=%(maker)s, description=%(description)s, price=%(price)s, year=%(year)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL("car_deals").query_db(query,data)
    
    #validate Show
    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car['model']) < 3:
            is_valid = False
            flash("El nombre del modelo debe tener al menos 3 carácteres","car")
        if len(car['maker']) < 3:
            is_valid = False
            flash("El nombre del maker deben tener al menos 3 carácteres","car")
        if len(car['description']) < 10:
            is_valid = False
            flash("La descripción debe tener al menos 3 carácteres","car")
        if len(car['price']) < 3:
            is_valid = False
            flash("El precio del carro debe ser realista","car")
        if car['year'] == "":
            is_valid = False
            flash("Por favor ingresa una fecha","car")
        return is_valid
    
    #Delete Show
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        print("---DELETE---")
        print("car id", data)
        return connectToMySQL("car_deals").query_db(query,data)

    #Get name del seller
    @classmethod
    def get_user_name_seller(cls, data):
        query = "SELECT users.first_name FROM users JOIN cars ON user_id = users.id WHERE cars.id = %(id)s;"
        resultado = connectToMySQL("car_deals").query_db(query, data)
        print("-------GET USER SELLER --------")
        print(resultado)
        return resultado

    # Get if was purchased
    @classmethod
    def get_if_purchased(cls, data):
        query = "SELECT car_id FROM purchased_by LEFT JOIN cars ON purchased_by.car_id = cars.id WHERE cars.id = %(id)s;"
        resultado = connectToMySQL("car_deals").query_db(query, data)
        print("-------GET PURCHASED TEST --------")
        print(resultado)
        return resultado

    #count likes
    @classmethod
    def count_likes(cls,data):
        query = "SELECT COUNT(shows.id) FROM users LEFT JOIN liked_by ON users.id = liked_by.user_id LEFT JOIN shows ON shows.id = liked_by.show_id WHERE shows.id = %(id)s;"
        resultado = connectToMySQL("car_deals").query_db(query, data)
        print("-----TEST COUNT------")
        print (resultado)
        return resultado
    
    #Get name user who posted
    @classmethod
    def get_user_name_post(cls, data):
        query = "SELECT users.first_name, users.last_name FROM cars LEFT JOIN users ON user_id = users.id WHERE cars.id = %(id)s;"
        resultado = connectToMySQL("car_deals").query_db(query, data)
        print("-------GET USER TEST --------")
        print(resultado)
        return resultado
        