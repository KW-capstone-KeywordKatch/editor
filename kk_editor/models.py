from kk_editor import db

class Article(db.Model):
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