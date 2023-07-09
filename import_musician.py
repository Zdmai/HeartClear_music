from pymysql import connect
import pymysql
import requests
from bs4 import BeautifulSoup

#  建立链接
conn = connect(host='localhost', port=3306, db='heartclearmusic', user='root', password='zzz', charset='utf8')
# 获取游标
cur = conn.cursor()
# cur.execute("select* from musics")
# result=cur.fetchone()
# print(result)


# 打开文件，读取所有文件存成列表

# hd="http://music.163.com/artist?id="
#
# headers = {
#     'User-Agent':
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# }
with open('musician.txt', "r",encoding='utf8') as file:
    # 可以选择readline或者read的方式,但下面的代码要有所变化
    # data_list = file.readlines()
    # 遍历列表
    error=0
    total=0
    for line in file:
        total+=1
        # print(line)

        # print(id)
        # print(musician_name)
        # print(url)


        try:
            ls = line.replace('\n', '').split(';')
            id = ls[1]
            # print(data[0].find_all('img')[0]['src'])
            musician_name = ls[0]
            # sql="INSERT INTO `test77`.`musicians` (`id`, `music_name`, `music_picture`) VALUES (%s, %s, %s);"
            sql="insert into musician(id,name)values (%s,%s);"
            row_count = cur.execute(sql, (id, musician_name))
            print(id)
            conn.commit()

        except:
            print("错误+1","重复的id:",id)
            error+=1

        # sql = "INSERT INTO `test77`.`musicians` (`id`, `music_name`, `music_picture`) VALUES (%s, %s, %s);"
        # row_count = cur.execute(sql, (int(id), musician_name, musician_url))
        # # row_count = cur.execute(sql, (1,"1","1"))
        # print(id)
        # conn.commit()
# 统一提交
conn.commit()
# 关闭游标　
cur.close()
# 关闭连接
conn.close()
print("共:",total)
print("错误：",error)