# HDU Course API
杭电某一学年某一学期全部课程的 API 接口，包含爬取课程的爬虫

## 使用

### 爬取课程信息

```python
python main.py
```
生成课程的 `json` 文件和 `courses.db` sqlite 数据库在 `data` 目录下

想要获取其他学年和学期，修改 `main.py` 中的

```python
self.year = '2019-2020'
self.term = '2'
```



### API 服务

默认端口号为 `3000`

```python
python server.py
```



### 可用 API

#### 查看所有老师数量和名字

https://api.limxw.com/teachers



**下列 API 均可通过可选参数进行筛选**

#### 根据老师名查找

https://api.limxw.com/teacher/{$老师名}

样例：

https://api.limxw.com/teacher/杨子飞



#### 根据课程名查找

https://api.limxw.com/title/{$课程名}

样例：

https://api.limxw.com/title/高等数学



#### 根据时间查找

https://api.limxw.com/time/{$时间}

样例：

https://api.limxw.com/title/周三



#### 根据课程属性查找

https://api.limxw.com/property/{$属性}

样例：

https://api.limxw.com/title/通识必修



https://api.limxw.com/courses/query?academic=机械工程&time=周三&local=7教&teacher=彭章明&credit=3

返回：
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
        local: "第7教研楼北322;第7教研楼北322",
        academic: "机械工程学院",
        other: "17010111,17010112,17010113,17010114"
    }
]
```

可选参数如下：

| 参数名 | 类型 | 默认值 | 说明   |
| -------- | ------ |----|-------- |
| limit | INT    | 10 |输出数量 |
| status   | String |    |开课状态 |
| title    | String |    |课程名称 |
| credit   | INT    |    |学分   |
| method   | String |    |考查方式 |
| property | String |    |课程性质 |
| teacher  | String |    |老师名字 |
| class_id | String |    |课程代号 |
| time     | String |    |上课时间 |
| local    | String |    |上课地点 |
| academic | String |    |开课学院 |
| other    | String |    |合班信息 |
