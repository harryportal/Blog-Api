from blogapi import api
from flask_restful import Resource
from flask import request



class Register(Resource):
    def post(self):
        user_data = request.get_json()

