from flask import Flask, jsonify, make_response, request, redirect
from HDUCoursesAPI.db_sqlite import DBSqlite
from HDUCoursesAPI.db_json import DBJson
from HDUCoursesAPI.utils import db2dict, count2dict
from HDUCoursesAPI.course_spider import SpiderThread
import random
import time

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

exporting_threads = {}
@app.route('/spider')
def spider():
    global exporting_threads
    year = request.args.get('year')
    term = request.args.get('term')
    if year == None or term == None:
        return make_response(jsonify({
            'status': 'failed',
            'msg': 'please input year and term'
        }))
    thread_id = random.randint(0, 10000)
    exporting_threads[thread_id] = SpiderThread(year, term)
    exporting_threads[thread_id].start()
    return make_response(jsonify({
        'status': 'running',
        'thread_id': thread_id
    }))


@app.route('/status/<int:thread_id>')
def spider_status(thread_id):
    global exporting_threads
    if exporting_threads[thread_id].spider.end_time == 0:
        end_time = time.time()
    return make_response(jsonify({
        'status': exporting_threads[thread_id].spider.status,
        'page_count': exporting_threads[thread_id].spider.page_count,
        'total_time': end_time - exporting_threads[thread_id].spider.start_time
    }))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
