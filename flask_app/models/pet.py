from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pet:
    def __init__(self,data):
        self.id = data['id']
        self.pet_type =  data['pet_type']
        self.name = data['name']
        self.breed = data['breed']
        self.age = data['age']
        self.diet = data['diet']
        self.date_made = data['date_made']
        self.conditions = data['conditions']
        self.vaccinations = data['vaccinations']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.image = data['image']

    @classmethod
    def save(cls, data):
        if 'image' not in data:
            data['image'] = None
        query = "INSERT INTO pets (pet_type, name, breed, age, diet, date_made, conditions, vaccinations, user_id, image) VALUES (%(pet_type)s,%(name)s,%(breed)s,%(age)s,%(diet)s,%(date_made)s,%(conditions)s,%(vaccinations)s,%(user_id)s,%(image)s);"
        return connectToMySQL('woofy').query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM pets WHERE user_id = %(id)s;"
        results =  connectToMySQL('woofy').query_db(query, data)
        all_pets = []
        if not results:
            return []
        for row in results:
            print(row)
            all_pets.append( cls(row) )
            
        return all_pets
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM pets WHERE id = %(id)s;"
        results = connectToMySQL('woofy').query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE pets SET pet_type=%(pet_type)s, name=%(name)s, breed=%(breed)s, age=%(age)s, diet=%(diet)s, date_made=%(date_made)s, conditions=%(conditions)s, vaccinations=%(vaccinations)s,updated_at=NOW(), image=%(image)s WHERE id = %(id)s;"
        return connectToMySQL('woofy').query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM pets WHERE id = %(id)s;"
        return connectToMySQL('woofy').query_db(query,data)

    @staticmethod
    def validate_pet(pet):
        is_valid = True
        if len(pet['pet_type']) < 1:
            is_valid = False
            flash("Pet type must be entered","pet")
        if len(pet['name']) < 1:
            is_valid = False
            flash("Name must be entered","pet")
        if len(pet['breed']) < 3:
            is_valid = False
            flash("Breed must be entered","pet")
        if len(pet['age']) == 0:
            is_valid = False
            flash("Pet age must be entered","pet")
        if len(pet['diet']) < 3:
            is_valid = False
            flash("Food Diet must be entered","pet")
        if pet['date_made'] == "":
            is_valid = False
            flash("Please enter a date","pet")
        return is_valid