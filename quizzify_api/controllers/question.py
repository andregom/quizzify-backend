import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import request, jsonify
from flask_restx import Resource
from http import HTTPStatus

from quizzify_api.server.instance import server

from ..quizzify_core.question_generation.question_generator import generate_question

app, api = server.app, server.api


@api.route('/questions/<type>/<id>', methods=['GET'])
class QuestionsController(Resource):

    def get(self, type, id):
        try:
            return self.get_question(type, id, query = request.get_json())
        except Exception as error:
            print(error)
            return HTTPStatus.INTERNAL_SERVER_ERROR

    
    @staticmethod
    def get_question(type, id, query):
        context = query.get('context', '')
        answer = query.get('answer', '')
        question = generate_question(context, answer)
        return jsonify(question)
