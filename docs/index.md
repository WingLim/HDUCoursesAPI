## 根据筛选条件查找
```url
GET https://api.limxw.com/courses/query?academic=机械工程&time=周三&location=7教&teacher=彭章明&credit=3
```


## 返回样例
```json
[
    {
        status: "已开",
        title: "液压与气动(甲)",
        credit: "3",
        method: "学校组织",
        property: "专业选修",
        teacher: "彭章明",
        class_id: "(2019-2020-1)-B0103630-41263-1",
        start_end: "01-15",
        time: "周一第3,4节{第1-15周};周三第1,2节{第1-15周|单周}",
        location: "第7教研楼北322;第7教研楼北322",
        academic: "机械工程学院",
        other: "17010111,17010112,17010113,17010114"
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
