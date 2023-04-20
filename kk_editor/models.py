from kk_editor import db

class Article(db.Model):
    # 스키마 변경 허용
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), unique=False, nullable=False)
    company = db.Column(db.String(20), unique=False, nullable=False)
    title = db.Column(db.String(240), unique=False, nullable=False)
    content = db.Column(db.String(5000), unique=False, nullable=False)
    image = db.Column(db.String(240), unique=False, nullable=True)
    link = db.Column(db.String(240), unique=True, nullable=False)

    def __init__(self, time, company, title, content, image, link):
        self.time = time
        self.company = company
        self.title = title
        self.content = content
        self.image = image
        self.link = link


class Keywords(db.Model):
    # {keyword: [article id 리스트]}
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(32), unique=True, nullable=False)
    # 키워드가 등장한 횟수(클수록 많은 기사에서 등장함)
    rank = db.Column(db.Integer, unique=False, nullable=False)
    # "1 3 5 11 19" 형태의 문자열
    articles = db.Column(db.String(1024), unique=False, nullable=False)

    def __init__(self, keyword: str, rank: int, articles: str):
        self.keyword = keyword
        self.rank = rank
        self.articles = articles
