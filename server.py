from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from HDUCoursesAPI.db_mongo import DBMongo
import uvicorn

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

tb = 'course2020-20212'
db = DBMongo('mongodb://localhost', 'courses', tb)


class QueryModel(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    credit: Optional[int] = None
    method: Optional[str] = None
    property: Optional[str] = None
    teacher: Optional[str] = None
    class_id: Optional[str] = None
    time: Optional[str] = None
    weekday: Optional[str] = None
    location: Optional[str] = None
    academic: Optional[str] = None
    other: Optional[str] = None


@app.get("/courses/query")
def query(
        params: QueryModel = Depends(),
        limit: int = 10,
        page: int = 0
):
    filters = params.dict(exclude_unset=True, exclude_none=True)
    r = db.find(filters, limit=limit, page=page)
    return r


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
