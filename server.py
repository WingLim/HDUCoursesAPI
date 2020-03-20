from flask import Flask, jsonify, make_response, request, redirect
from HDUCoursesAPI.db_sqlite import DBSqlite
from HDUCoursesAPI.db_json import DBJson
from HDUCoursesAPI.utils import db2dict, count2dict

db = DBSqlite()
tb = 'course2019-20202'
app = Flask(__name__)

@app.route('/courses')
def index():
    return redirect('https://winglim.github.io/HDUCoursesAPI/')

@app.route('/courses/query')
def query():
    filters = request.args.to_dict()
    print(filters)
    tmp = request.args.get('limit')
    limit = (tmp if tmp != None else 10)
    r = db.fetch(tb, filters, limit=limit)
    d = db2dict(r)
    result = DBJson().cook_course_json(d)
    return make_response(jsonify(result))

@app.route('/courses/title/<data>')
@app.route('/courses/property/<data>')
@app.route('/courses/teacher/<data>')
@app.route('/courses/time/<data>')
def onecolume(data):
    filters = request.args.to_dict()
    column = request.path.split('/')[2]
    tmp = request.args.get('limit')
    limit = (tmp if tmp != None else 10)
    r = db.fetch(tb, filters, column, data, limit)
    result = db2dict(r)
    return make_response(jsonify(result))

@app.route('/courses/teachers')
def teachers():
    r = db.fetchcount(tb, 'TEACHER')
    result = count2dict(r)
    return make_response(jsonify(result))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
