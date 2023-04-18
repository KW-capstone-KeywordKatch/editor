from flask import Flask

# blueprint
from . api import v1

def create_app():
    # Flask application 생성
    app = Flask(__name__)
    print(__name__)

    @app.route('/')
    def hello_editor():
        return 'Hello editor!'
    
    app.register_blueprint(v1.bp)

    return app
