import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import request
from flask_restx import Resource
from http import HTTPStatus

from quizzify_api.server.instance import server

app, api = server.app, server.api


@api.route('/questions/<type>/<id>', methods=['GET'])
class QuestionsController(Resource):

    def get(self, type, id):
        try:
            return self.get_question(type, id)
        except Exception as error:
            print(error)
            return HTTPStatus.INTERNAL_SERVER_ERROR

    
    @staticmethod
    def get_question(type, id):
        return 'How are you doing?'