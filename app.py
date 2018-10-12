import pprint

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/buy', methods=['POST'])
def buy():
    pprint.pprint(request.form)
    return ''


if __name__ == '__main__':
    app.run()
