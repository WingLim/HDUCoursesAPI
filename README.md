# HDU Courses API
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

默认端口号为 `8000`

```python
python server.py
```

### API 文档
https://winglim.github.io/HDUCoursesAPI

### 导入数据到数据库

```bash
mongoimport -d courses -c course2020-20212 \
  --uri mongodb://username:password@localhost \
  --authenticationDatabase admin \
  --jsonArray courses_course2020_20212.json
```

## 使用 Docker 部署

`winglim/hducourses` 镜像为 API 服务

可配置的环境变量如下:

- `MONGODB_URL` - 连接到 `mongodb` 数据库的地址

`winglim/hducoursesdb` 镜像会导入课程数据到 `mongodb` - 默认值 [`mongodb://localhost`](https://github.com/WingLim/HDUCoursesAPI/blob/1cd017e62ed89d194ba34409278302121e3b45cf/HDUCoursesAPI/config.py#L6)

可配置的环境变量如下:

- `USERNAME` - 用户名 - 默认值 `root`
- `PASSWORD` - 密码 - 默认值 `root`
- `HOSTNAME` - 位于同一网络下的 `mongodb` 的主机别名 - 默认值 `mongodb`

[`docker-compose.yml`](https://github.com/WingLim/HDUCoursesAPI/blob/master/docker-compose.yml)
```yaml
version: '3'
services:
    courses:
        image: winglim/hducourses
        environment:
            MONGODB_URL: mongodb://mongoadmin:secret@mongodb

    mongodb:
        image: mongo
        environment:
            MONGO_INITDB_ROOT_USERNAME: mongoadmin
            MONGO_INITDB_ROOT_PASSWORD: secret
            MONGO_INITDB_DATABASE: courses

    mongo_seed:
        image: winglim/hducoursesdb
        environment:
            USERNAME: mongoadmin
            PASSWORD: secret
        depends_on:
            - mongodb

```

