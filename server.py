from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from HDUCoursesAPI.db_sqlite import DBSqlite
from HDUCoursesAPI.utils import make_json

app = FastAPI()

origins = [
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

db = DBSqlite()
tb = 'course2020-20212'


class Query(BaseModel):
    status: Optional[int] = None
    title: Optional[str] = None
    credit: Optional[int] = None
    method: Optional[str] = None
    property: Optional[str] = None
    teacher: Optional[str] = None
    class_id: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    academic: Optional[str] = None
    other: Optional[str] = None


@app.get("/courses/query")
def query(
        req: Request,
        status: Optional[int] = None,
        title: Optional[str] = None,
        credit: Optional[int] = None,
        method: Optional[str] = None,
        property: Optional[str] = None,
        teacher: Optional[str] = None,
        class_id: Optional[str] = None,
        time: Optional[str] = None,
        location: Optional[str] = None,
        academic: Optional[str] = None,
        other: Optional[str] = None,
        limit: int = 10
):
    filters = Query(**req.query_params).dict(exclude_unset=True)
    r = db.fetch(tb, filters, limit=limit)
    return make_json(r)


@app.get('/courses/{column}/{data}')
def one_column(
        req: Request,
        column: str,
        data: str,
        limit: int = 10,
        status: Optional[int] = None,
        title: Optional[str] = None,
        credit: Optional[int] = None,
        method: Optional[str] = None,
        property: Optional[str] = None,
        teacher: Optional[str] = None,
        class_id: Optional[str] = None,
        time: Optional[str] = None,
        location: Optional[str] = None,
        academic: Optional[str] = None,
        other: Optional[str] = None,
):
    filters = Query(**req.query_params).dict(exclude_unset=True)
    r = db.fetch(tb, filters, column, data, limit)
    return make_json(r)
