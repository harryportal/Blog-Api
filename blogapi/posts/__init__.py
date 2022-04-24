from flask_restful import Resource
from blogapi import api

class NewPost(Resource):
    def get(self):
