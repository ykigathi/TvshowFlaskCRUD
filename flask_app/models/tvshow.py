from flask import flash
from flask_app.config.mysql_connection import connectToMySQL
from datetime import datetime

class Tvshow:

    db= 'belt_exam_db'

    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.title = data["title"]
        self.network = data["network"]
        self.description = data["description"]
        self.release_date = data["release_date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tvshows;"
        results = connectToMySQL(cls.db).query_db(query)
        tvshows=[]
        for r in results:
            tvshows.append( cls(r) )
        return tvshows
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tvshows WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod    
    def insert(cls, data):
        query = "INSERT INTO tvshows (user_id, title, network, description, release_date, created_at, updated_at) VALUES (%(user_id)s, %(title)s, %(network)s,%(description)s, %(release_date)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):         
        # now = datetime.now()
        # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # formatted_date = data['release_date'].strftime('%Y-%m-%d')
        query = "UPDATE tvshows SET title=%(title)s, network=%(network)s, description=%(description)s, release_date=%(release_date)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tvshows WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    #tvshows validations
    def validate_tvshow(data):
        is_valid = True
        if len(data['title']) < 2:
            is_valid = False
            flash('You must add a Title name.')
        #validate Network 
        if len(data['network']) < 2:
            flash('Your Tv Show must have a Network name.')
            is_valid = False
        #validate Description 
        if len(data['description']) < 2:
            flash('Your Tv Show must have a good description.')
            is_valid = False
        #validate Date released
        if len(data['release_date']) < 8:
            is_valid = False
            flash("Add a release date.")
        return is_valid
        

    