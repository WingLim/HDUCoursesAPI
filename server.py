from flask import Flask, jsonify, make_response
from HDUCoursesAPI.db_sqlite import DBSqlite
from HDUCoursesAPI.utils import db2dict, count2dict

db = DBSqlite()
tb = 'course2019-20202'
app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to use HDU Courses API"

@app.route('/teacher/<name>')
def teacher(name):
    r = db.fetchcolumn(tb, 'TEACHER', name)
    result = db2dict(r)
    return make_response(jsonify(result))


@app.route('/teachers')
def teachers():
    r = db.fetchcount(tb, 'TEACHER')
    result = count2dict(r)
    return make_response(jsonify(result))

@app.route('/weekday/<data>')
def weekday(data):
    r = db.fetchcolumn(tb, 'TIME', data)
    result = db2dict(r)
    return make_response(jsonify(result))

if __name__ == "__main__":
    app.run(debug=True)
