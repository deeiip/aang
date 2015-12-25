from flask import Flask, redirect, request
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

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


class Comments(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    about = db.Column(db.String(50))
    comment = db.Column(db.String(268))
    comm_by = db.Column(db.String(50))

    def __init__(self, about, by, comment):
        self.about = about
        self.comm_by = by
        self.comment = comment


@app.route('/')
@app.route('/Index')
def home_page():
    # news = NewsModel('http://test.com/gweg6rufhgfvfdbhd')
    # db.session.add(news)
    # db.session.commit()
    about = request.args.get('subject')
    if about is None:
        return redirect("/start", code=302)
    newss = db.session.query(NewsModel).filter_by(url='http://test.com/gweg')
    print(newss)
    for nm in newss:
        print(nm.url)
        print(nm.about)
    return render_template('index.html')


@app.route('/start')
def start_page():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


