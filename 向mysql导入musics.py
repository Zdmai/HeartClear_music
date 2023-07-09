#导入歌曲
import re
from pymysql import connect
import pymysql

#  建立链接

###配置文件
conn = connect(host='localhost', port=3306, db='heartclearmusic', user='root', password='zzz', charset='utf8')
# 获取游标
cur = conn.cursor()



# 打开文件，读取所有文件存成列表

###提供music文件
with open('music.txt', "r",encoding='utf8') as file:

    error=0
    total=0
    for line in file:
        # print(line)
        total+=1
        # try:
        ls = line.replace('\n', '').split(';')
        id = ls[0]
        music_name = ls[1]
        music_picture = ls[2]
        # print(len(music_picture))

        try:
        ####提供歌词的存储路径
            lyric = open('./static/mp3/' + id + '.txt', 'r', encoding='utf8').read()
            # print(lyric)
            album_name = ls[4]

            musician_id = ','.join(eval(ls[5]))
            # print(musician_id)
            # print(ls)




        #sql="insert into music(id,music_name,lyric,album_name,picture,musician_id)values (%s,%s,%s,%s,%s,%s);"

            sql="INSERT INTO heartclearmusic.music (id, music_name, lyric, album_name, picture, musician_id) VALUES (%s, %s, %s, %s, %s, %s)"
        # print(sql)
        # 参数化方式传参

        # row_count = cur.execute(sql, (id, music_name, music_picture, lyric, album_name, musician_id))

            row_count = cur.execute(sql,(id,music_name,lyric,album_name,music_picture,musician_id))

        # 显示操作结果
            conn.commit()
        except:
            error+=1
            print(album_name, "长度：", len(album_name))
            print(id)



    # except:
    #     error+=1
# 统一提交
conn.commit()
# 关闭游标　
cur.close()
# 关闭连接
conn.close()
print("总共：",total)
print("错误",error)