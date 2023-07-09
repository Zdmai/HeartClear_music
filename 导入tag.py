from pymysql import connect
import pymysql

#  建立链接
conn = connect(host='localhost', port=3306, db='heartclearmusic', user='root', password='zzz', charset='utf8')
# 获取游标
cur = conn.cursor()
# cur.execute("select* from musics")
# result=cur.fetchone()
# print(result)


# 打开文件，读取所有文件存成列表
with open('tag.txt', "r",encoding='utf8') as file:
    # 可以选择readline或者read的方式,但下面的代码要有所变化
    # data_list = file.readlines()
    # 遍历列表
    error=0
    total=0
    for line in file:
        # print(line)
        total+=1
        try:
            ls = line.replace('\n', '').split(';')
            id = ls[0]
            tag=ls[2]
            # INSERT INTO `test77`.`musics` (`id`, `music_name`, `music_picture`, `lyric`, `album_name`, `musician_id`) VALUES (1, '晴天', '无', '晴天', '周杰伦', '1')
            sql = "INSERT INTO `heartclearmusic`.`tag` (`tag_name`, `music_id`) VALUES (%s,%s);"
            # print(sql)
            # 参数化方式传参

            row_count = cur.execute(sql, (tag, id))
            # 显示操作结果
            conn.commit()
        except:
            error+=1
# 统一提交
conn.commit()
# 关闭游标　
cur.close()
# 关闭连接
conn.close()
print("共：",total)
print("重复：",error)