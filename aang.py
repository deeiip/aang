from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from news_data_model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://jlanaajgscrrlo:wXwt2_X1sKZwZ91Y8tFRbC" \
                                        "BfrL@ec2-107-22-184-127.compute-1.amazonaws.com:5432/da1cenu2lbulpo"
db = SQLAlchemy(app)

# app = Flask(__name__)


@app.route('/')
@app.route('/Index')
def hello_world():
    news = NewsModel('http://test.com/gweg')
    db.session.add(news)
    db.session.commit()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


