import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    from . import annotation
    app.register_blueprint(annotation.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
