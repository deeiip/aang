from flask import Flask, redirect, request, render_template, Response
from flask.ext.sqlalchemy import SQLAlchemy
import json
from alchemi_rest import *
import sys
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://jlanaajgscrrlo:wXwt2_X1sKZwZ91Y8tFRbC" \
                                        "BfrL@ec2-107-22-184-127.compute-1.amazonaws.com:5432/da1cenu2lbulpo"
db = SQLAlchemy(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
# app = Flask(__name__)


class NewsModel(db.Model):
    url = db.Column(db.String(200), primary_key=True)
    about = db.Column(db.String(50))
    entities = db.Column(db.Text)
    concepts = db.Column(db.Text)
    sentiment = db.Column(db.Text)
    author = db.Column(db.String(150))
    title = db.Column(db.String(400))
    attrs = ['url','about','entities',
                      'concepts','sentiment','author','title']

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Url %r>' % self.url


class Comments(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    about = db.Column(db.String(50))
    comment = db.Column(db.String(268))
    comm_by = db.Column(db.String(50))
    attrs = ['id','about','comment', 'comm_by']

    def __init__(self, about, by, comment):
        self.about = about
        self.comm_by = by
        self.comment = comment


def create_json_from_model(model):
    temp_dict = {}
    for item in model.attrs:
        current = getattr(model, item)
        temp_dict[item] = current
        # print(getattr(model, item))
    # for item in dir(model):
    #     if not item.startswith('__'):
    #         print(item)
    #         print(getattr(model, item))
    return json.dumps(temp_dict)


@app.route('/')
@app.route('/Index')
def home_page():
    # news = NewsModel('http://test.com/gweg6rufhgfvfdbhd')
    # db.session.add(news)
    # db.session.commit()
    about = request.args.get('subject')
    if about is None:
        return redirect("/start", code=302)
    # newss = db.session.query(NewsModel).filter_by(url='http://test.com/gweg')
    # print(newss)
    # for nm in newss:
        # chk = create_json_from_model(nm)
    return render_template('index.html')


@app.route('/start')
def start_page():
    return render_template('login.html')


@app.route('/data')
def ajax_all_data():
    about = request.args.get('subject')

    if about is None:
        return "Invalid Ajax query"
    else:
        # create_db_entry('TCS')
        about = about.lower()
        ret = '['
        result = db.session.query(NewsModel).filter_by(about=about)
        count = 0
        for item in result:
            ret += create_json_from_model(item) + ','
            count += 1
        if count != 0:
            ret = ret[:-1]
        ret += ']'
    return Response(ret, mimetype='text/json')

@app.route('/media_data')
def media_det_ajax():
    about = request.args.get('subject')
    src = request.args.get('channel')
    if (about is None) or (src is None):
        return "Invalid Ajax Query"
    else:
        about = about.lower()
        ret = '['
        result = db.session.query(NewsModel).filter(NewsModel.url.contains(src)).filter_by(about=about)
        count = 0
        for item in result:
            ret += create_json_from_model(item) + ','
            count += 1
        if count != 0:
            ret = ret[:-1]
        ret += ']'
    return Response(ret, mimetype='text/json')


@app.route('/author_data')
def author_data():
    about = request.args.get('subject')
    author = request.args.get('author')
    if (about is None) or (author is None):
        return "Invaid Ajax Query"
    else:
        about = about.lower()
        # author = author.lower()
        result = db.session.query(NewsModel).filter(NewsModel.author.contains(author)).filter_by(about=about)
        count = 0
        ret = '['
        for item in result:
            ret += create_json_from_model(item) + ','
            count += 1
        if count != 0:
            ret = ret[:-1]
        ret += ']'
    return Response(ret, mimetype='text/json')


@app.route('/author')
def author():
    src = request.args.get('author')
    return render_template('author_glance.html', detail_by=src)


@app.route('/media')
def media_house_involvement():
    src = request.args.get('channel')
    return render_template('media_glance.html', detail_by = src)


@app.errorhandler(404)
def page_not_found(e):
    # create_db_entry('tcs')
    return render_template('404.html', error_code='404', message='We could not find the page you were looking for.')\
        , 404


@app.errorhandler(500)
def application_error(e):

    return render_template('404.html', error_code='500', message='App encountered an unexpected'
                                                                 ' error. Rest assured, we will do our part')\
        , 500


@app.route('/create_data')
def create_data():
    about = request.args.get('subject')
    try:
        create_db_entry(about, False)
        return "success"
    except Exception:
        return "fail"


def create_db_entry(name, from_file=True):
    name = name.lower()
    reqst = Request(API_KEY, name)
    newses = reqst.request(from_file)
    for news in newses:
        news_model = NewsModel(news.url)
        news_model.about = name
        news_model.author = news.author
        news_model.title = news.title
        news_model.sentiment = json.dumps(news.sentiment.__dict__)
        enstr = '['
        for entity in news.entities:
            enstr += json.dumps(entity.__dict__)
            enstr += ','
        if len(news.entities) != 0:
            enstr = enstr[:-1]
        enstr += ']'
        news_model.entities = enstr
        constr = '['
        for conc in news.concept:
            constr += json.dumps(conc.__dict__)
            constr += ','
        if len(news.concept) != 0:
            constr = constr[:-1]
        constr += ']'
        news_model.concepts = constr
        db.session.merge(news_model)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)


