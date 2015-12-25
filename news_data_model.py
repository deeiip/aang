from aang import db


class NewsModel(db.Model):
    url = db.Column(db.String(200), primary_key=True)
    about = db.Column(db.String(50))
    entities = db.Column(db.Text)
    concepts = db.Column(db.Text)
    sentiment = db.Column(db.Text)
    author = db.Column(db.String(150))
    title = db.Column(db.String(400))

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Url %r>' % self.url


