from flask import Flask
from flask_restplus import Api

class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                        version = '1.0',
                        title = 'API pix gerencianet',
                        description = 'API para gerar qr code para pagamento via pix',
                        doc = '/docs'
                      )

    def run(self):
        self.app.run(
            debug=True,
        )

server = Server()