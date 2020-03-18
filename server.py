from flask import Flask, jsonify, make_response
from HDUCoursesAPI.db_sqlite import DBSqlite

db = DBSqlite()
tb = 'course2019-20202'
app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to use HDU Courses API"

@app.route('/teacher/<name>')
def teacher(name):
    result = db.fetchcolume(tb, 'TEACHER', name)
    return make_response(jsonify(result))


@app.route('/teachers')
def teachers():
    pass

@app.route('/weekday/<data>')
def weekday(data):
    result = db.fetchcolume(tb, 'TIME', data)
    return make_response(jsonify(result))

if __name__ == "__main__":
    app.run(debug=True)
