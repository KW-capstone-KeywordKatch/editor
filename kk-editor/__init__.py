from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# blueprint
from .api import v1

# 모델 클래스 정의
db = SQLAlchemy()
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), unique=False, nullable=False)
    company = db.Column(db.String(20), unique=False, nullable=False)
    title = db.Column(db.String(240), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    image = db.Column(db.String(240), unique=False, nullable=True)

    def __init__(self, time, company, title, content, image):
        self.time = time
        self.company = company
        self.title = title
        self.content = content
        self.image = image


def create_app():
    # Flask application 생성
    app = Flask(__name__)
    print(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:hyungun990821@editor.cmtcak3iutyr.ap-northeast-2.rds.amazonaws.com:3306/editor'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # 데이터베이스에 테이블이 존재하지 않을 때만 테이블 생성
        db.create_all()

    @app.route('/')
    def hello_editor():
        return 'Hello editor!'

    @app.route('/crawl')
    def start_crawl():
        import core.crawler.main
        count, spend_time = core.crawler.main.start_crawl(db, Article)
        return f"{count}개 저장 완료.  걸린 시간: {spend_time}"


    app.register_blueprint(v1.bp)

    return app
