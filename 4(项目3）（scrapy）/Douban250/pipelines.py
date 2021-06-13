import hashlib
import pymysql
import csv
import json
import os
import codecs
import scrapy
from scrapy.exceptions import DropItem


class Douban250Pipeline:
    def process_item(self, item, spider):
        return item

# 数据存储在csv文件里
class savefileTongscrapyPipeline(object):
    def __init__(self):
        self.file = open('movies_scv.csv', 'w+', newline='',encoding="utf-8")
        self.csvwriter = csv.writer(self.file)
        self.csvwriter.writerow([ '电影名','导演', '评分', '介绍','图片地址'])
    def process_item(self, item, spider):
        self.csvwriter.writerow([item['cover_url'], item['cintroduce'], item['name'], item['quote'],item['score']])
        return item
    def close_spider(self, spider):
        self.file.close()

# 保存为json文件
class JsonPipeline(object):
    def __init__(self):
        #文件的位置
        store_file = os.path.dirname(__file__) + '/spiders/movies_json.json'
        # 打开文件，设置编码为utf-8
        self.file = codecs.open(filename= store_file, mode= 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) +',\n'
        # 逐行写入
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

#数据保存到mysql
#连接数据库
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "host",
        passwd = "mcl72732002",
        charset = "utf8",
        use_unicode = False
    )
    return conn
class HellospiderPipeline(object):
    def process_item(self, item, spider):
        db = dbHandle()
        cursor = db.cursor()
        cursor.execute("USE tieba")
        cursor = db.cursor()  # 获取 cursor 来操作数据库
        cursor.execute("DROP TABLE IF EXISTS movies")
        sql = "create table movies(name varchar(1000) ,director varchar(1000) ,rating varchar(1000) ,appraise varchar(1000) ,links varchar(500))"  # 创建表格，注意此处要定义主键
        # sql = """create table movie (name char(20) ,director verchar(20),rating char(20),appraise char(20),links verchar(20))"""
        cursor.execute(sql)
        # 数据库插入
        cur = db.cursor()  # 创建游标对象
        sql = 'insert into movies(name,director,rating,appraise,links) value (%s,%s,%s,%s,%s)'
        for data in item:
            valu = (data[0], data[1], data[2], data[3], data[4])
            cur.execute(sql, valu)
            db.commit()
            # print("successful")
        return item

#保存图片
class Top250Pipeline(object):

    def get_media_requests(self, item, info):
        for image_url in item['cover_url']:
            yield scrapy.Request(image_url)

        # 自定义 文件路径 和 文件名
        def file_path(self, request, item, response=None, info=None):
            image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
            return f'pitcures/{item["name"]}.jpg'


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        #item['image_paths'] = image_paths
        return item