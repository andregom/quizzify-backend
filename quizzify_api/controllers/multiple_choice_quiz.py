import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import request, jsonify
from flask_restx import Resource
from http import HTTPStatus

from quizzify_api.server.instance import server

app, api = server.app, server.api


@api.route('/quiz/<type>/<id>', methods=['GET'])
class QuizController(Resource):

    def get(self, type, id):
        # try:
            return self.get_question(type, id, query = request.get_json())
        # except Exception as error:
        #     print(error)
        #     return HTTPStatus.INTERNAL_SERVER_ERROR

    
    @staticmethod
    def get_question(type, id, query):
        from ..quizzify_core.quiz_generation.quiz_assembler import mount_quiz_from
        context = query.get('context', '')
        quiz = mount_quiz_from(context)
        return jsonify(quiz)
