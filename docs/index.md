## 根据筛选条件查找
```url
curl --location --request GET \
    'https://api.limxw.com/courses/query?title=高等数学&weekday=周四'
```


## 返回样例
```json
[
    {
        "academic": "理学院",
        "class_id": "(2020-2021-2)-A071432s-41823-1",
        "credit": 5,
        "location": [
            "第12教研楼108"
        ],
        "method": "学校组织",
        "other": [
            "20320111",
            "20320112"
        ],
        "property": "学科必修",
        "status": "已开",
        "teacher": "韩斌",
        "time_info": [
            {
                "weekday": "周四",
                "start": "15:15",
                "end": "16:50",
                "location": "第12教研楼108"
            },
            {
                "weekday": "周五",
                "start": "10:00",
                "end": "12:25",
                "location": "第12教研楼108"
            }
        ],
        "title": "高等数学A2",
        "week_info": {
            "start": 1,
            "end": 16,
            "flag": 0
        }
    }
]
```


## 可选参数

| 参数名 | 类型 | 默认值 | 说明   |
| -------- | ------ |----|-------- |
| limit | INT    | 10 |输出数量 |
| page  | INT    | 0  |分页     |
| status   | String |    |开课状态 |
| title    | String |    |课程名称 |
| credit   | INT    |    |学分   |
| method   | String |    |考查方式 |
| property | String |    |课程性质 |
| teacher  | String |    |老师名字 |
| class_id | String |    |课程代号 |
| time     | String |    |上课时间 |
| weekday  | String |    |上课日期 |
| location | String |    |上课地点 |
| academic | String |    |开课学院 |
| other    | String |    |合班信息 |
