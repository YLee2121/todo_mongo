from flask import Flask, jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256
from app import db

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True 
        session['user'] = user 
        return jsonify(user), 200

    def signup(self):

        # create the user object
        user = {
            "_id": uuid.uuid4().hex, 
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }

        # encrypt password  
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # check for existing email address
        if db.user.find_one({"email": user['email']}):
            return jsonify( {"error": " Email address already in used"} ), 400
        
        # db update
        if db.user.insert_one(user):
            return self.start_session(user)

        return jsonify({"error":"Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        
        user = db.user.find_one({
            "email": request.form.get('email')
        })


        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify( {"error": "Invalid Login"}), 401