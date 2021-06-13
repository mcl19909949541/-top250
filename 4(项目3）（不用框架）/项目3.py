# coding = utf-8
# author = 孟辰林 2020303090

'''
项目三：采集豆瓣电影TOP250
要求：
1.采集地址:https://movie.douban.com/top250
2.采集数据为：电影名称、导演、评分、介绍、电影海报图及地址。
3.将采集到的数据存储到mysql数据库、json文件、csv文件
4.可自动采集所有数据页(选做)
5.图片需要单独下载到指定文件夹。(选做)
'''

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import os
import requests
import csv
import json
import pymysql

def main():
    # 初始网址
    baseurl = "https://movie.douban.com/top250?start="
    #获取信息
    datalist = getData(baseurl)

    #测试打印
    for data in datalist:
        print(data)

    #下载图片
    download(datalist)

    #保存到mysql
    #save_mysql(datalist)

    #保存到json
    #save_json(datalist)

    #保存到csv
    #save_csv(datalist)


# 影片图片链接规则
findImgSic = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 让换行符包含在字符串中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到概况
findIng = re.compile(r'"inq">(.*)</span>')
# 找到导演
findBd = re.compile(r'导演(.*?)\xa0', re.S)


# 爬取网址
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取网页的函数10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取的网页信息

        # 逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找字符串
            data = []  # 保存一部电影的所有信息
            item = str(item)
            # print(item)

            # Link = re.findall(findLink, item)[0]  # 查找影片链接
            # data.append(Link)

            # 1.匹配电影名
            titles = re.findall(findTitle, item)

            ctitle = titles[0]
            data.append(ctitle)


            # 2.导演
            bd = re.findall(findBd, item)

            data.append(bd)

            #3.评分
            rating = re.findall(findRating, item)[0]#评分
            data.append(rating)

            #4，介绍
            inq = re.findall(findIng, item)
            if len(inq) != 0:
                inq = inq[0].replace(",", "")
                data.append(inq)
            else:
                data.append("  ")

            #5.图片地址
            imgSrc = re.findall(findImgSic, item)[0]
            data.append(imgSrc)  # 匹配添加图片地址

            datalist.append(data)  # 把处理好的一部电影信息存储

    # print(datalist)
    return datalist


#请求网页
def askURL(url):
    head = {          #伪装URL
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:  #异常处理
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#下载图片
def download(datalist):
    # 下载图片
    # 创建一个文件夹
    if not os.path.exists('./pictures'):
        os.mkdir('./pictures')

    for i in range(0,250):
        img_name = datalist[i][0] + '.jpg'
        img_path = 'pictures/' + img_name
        img_data = requests.get(url=datalist[i][4]).content
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
        print("successful")

#保存到mysql
def save_mysql(datalist):
    db = pymysql.connect(host="localhost", port=3306, user="root", password="mcl72732002",
                         db="movies")  # 现在本地配置mysql，此为修改后的密码
    cursor = db.cursor()  #获取 cursor 来操作数据库
    cursor.execute("DROP TABLE IF EXISTS movies")
    sql = "create table movies(name varchar(1000) ,director varchar(1000) ,rating varchar(1000) ,appraise varchar(1000) ,links varchar(500))"  # 创建表格，注意此处要定义主键
    #sql = """create table movie (name char(20) ,director verchar(20),rating char(20),appraise char(20),links verchar(20))"""
    cursor.execute(sql)
    # 数据库插入
    cur = db.cursor()  # 创建游标对象
    sql = 'insert into movies(name,director,rating,appraise,links) value (%s,%s,%s,%s,%s)'
    for data in datalist:
        valu = (data[0], data[1], data[2],data[3],data[4])
        cur.execute(sql, valu)
        db.commit()
        #print("successful")

    return
#保存到json
def save_json(datalist):
    with open('movies_json.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(datalist, indent=2, ensure_ascii=False))
    return

#保存到csv
def save_csv(datalist):
    csvFile = open("./movies_csv.csv","w+",encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(("电影名","导演","评分","介绍","图片地址"))
        for data in datalist:
            writer.writerow((data[0],data[1],data[2],data[3],data[4]))
    finally:
        csvFile.close()
    return

if __name__ == "__main__":
    main()
    print("爬取完毕！")
