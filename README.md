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



### API 文档
https://winglim.github.io/