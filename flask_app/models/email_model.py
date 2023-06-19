from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:

    DB = "email_validation_db"

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#! Not catching all duplicates?
#if the following remains true to the end then the data is valid
    @staticmethod
    def validate_email(new_email):
        is_valid = True
        # test whether email submitted is an actual email
        if not EMAIL_REGEX.match(new_email['email']): 
            flash ("Email is not valid!")
            is_valid = False
        # test to verify the email doesn't already exist in the db
        query = """
        SELECT * 
        FROM emails
        WHERE email = %(email)s;
        """    
        results = connectToMySQL('email_validation_db').query_db(query,new_email)
        # use to check if working...
        print(results)

        if results:
            flash("Email already exists!")
            is_valid = False

        return is_valid

    # method to save & add new email (return email id)
    @classmethod
    def save_submission(cls, data):
        query = """INSERT INTO emails (email)
        VALUES (%(email)s) ;
        """

        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    #method to view a list of all emails
    @classmethod
    def get_all(cls):
        query = """
        SELECT * 
        FROM emails;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        # use to check if working...
        print(results)

        emails = []

        for email in results:
            emails.append( cls(email))
        return emails