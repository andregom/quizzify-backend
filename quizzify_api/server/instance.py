from flask import Flask
from flask_restx import Api
from flask_cors import CORS


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.api = Api(self.app,
                       version='1.0',
                       title='Quizzify API',
                       description='Quizzify application REST API',
                       doc='/docs'
                       )

    def run(self, ):
        self.app.run(
            debug=True
        )


server = Server()
