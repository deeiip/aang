from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/Index')
def hello_world():
    return render_template('index.html')
    #return html_minify(rendered_html)


if __name__ == '__main__':
    app.run(debug=True)
