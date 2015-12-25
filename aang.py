from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from news_data_model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://jlanaajgscrrlo:wXwt2_X1sKZwZ91Y8tFRbC" \
                                        "BfrL@ec2-107-22-184-127.compute-1.amazonaws.com:5432/da1cenu2lbulpo"
db = SQLAlchemy(app)

# app = Flask(__name__)


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


@app.route('/')
@app.route('/Index')
def hello_world():
    news = NewsModel('http://test.com/gweg')
    db.session.add(news)
    db.session.commit()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


