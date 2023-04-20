from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sys


# 개발 환경
# from config import config_dev as config
# 배포 환경
from kk_editor.config import config_prod as config


# 모델 클래스 정의
db = SQLAlchemy()

global app
def create_app():
    global app
    # Flask application 생성
    app = Flask(__name__)

    # DB 설정 파일 입력
    app.config.from_object(config)
    # ORM
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    from kk_editor.models import Article
    # 데이터베이스에 테이블이 존재하지 않을 때만 테이블 생성
    from models import Article
    with app.app_context():
        db.create_all()

    ################# API url 매핑 #################
    # blueprint
    @app.route('/')
    def hello_editor():
        return 'Hello kk-editor!'
    # blueprint 등록
    from apis import v1
    app.register_blueprint(v1.bp)

    # rest api
    from apis import api
    api.init_app(app)

    return app
