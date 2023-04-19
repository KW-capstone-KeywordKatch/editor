from kk_editor import db

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
