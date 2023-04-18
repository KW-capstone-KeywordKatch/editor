from flask import Flask

import core.crawler.main

# blueprint
from . api import v1

def create_app():
    # Flask application 생성
    app = Flask(__name__)
    print(__name__)

    @app.route('/')
    def hello_editor():
        return 'Hello editor!'

    @app.route('/crawl')
    def start_crawl():
        core.crawler.main.start_crawl()


    app.register_blueprint(v1.bp)

    return app
