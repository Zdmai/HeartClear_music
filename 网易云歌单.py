#包含简介，歌单标签，  歌曲的名字，歌手名，专辑名，歌曲id(可以通过id来下载歌曲和歌词）

#7.2.20改，解决只爬取，显示的介绍的不足，能够爬取隐藏简介
import requests
from bs4 import BeautifulSoup
import re

#song_url='http://music.163.com/song/media/outer/url?id='#下载歌曲的接口
#song_word_url='http://music.163.com/api/song/lyric?id={num_id}&lv=-1&kv=-1&tv=-1'下载歌词的接口

hd='http://music.163.com'

#url='http://music.163.com/playlist?id=94284266'
url='http://music.163.com/discover/playlist'#歌单


# headers={
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# }

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
}

fw=open('音乐.txt','w',encoding='utf-8')#结果文件
fw_musician=open("歌手.txt",'w',encoding='utf-8')
fw_tag=open("标签.txt",'w',encoding="utf-8")

for i in range(0,500,35):

    url=f'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset={i}'
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    soup = BeautifulSoup(html_data, 'html.parser')

    # print(soup)
    # quit()

    ls = soup.select('.m-cvrlst.f-cb li')

    # print(ls[0])#歌单列表

    for l in ls:

        img = l.select('.j-flag')[0]['src']



        data = l.select('.tit')[0]
        # print(type(data))
        title = data['title']

        playlist_id = data['href']
        playlist_url = hd + playlist_id
        # print(title,playlist_id)

        # print(playlist_url)#歌单地址
        song_response = requests.get(url=playlist_url, headers=headers)
        song_soup = BeautifulSoup(song_response.text, 'html.parser')
        # print(song_soup)
        # quit()

        #修改，这是简单介绍
        # song_txt = song_soup.find_all('script', type='application/ld+json')
        # dic = eval(song_txt[0].text)
        # # print(dic)#字典
        # s = dic['description']
        # start = s.find('简介：')
        # end = s.find('更多相关热门精选歌单推荐尽在网易云音乐')
        # # print(description)#简介和标签
        # description = s[start:end]
        description_txt=song_soup.select('.intr.f-brk')
        if len(description_txt)>1:
            description_txt=song_soup.select('.intr.f-brk.f-hide')
        #print(description_txt[0].text)
        description=description_txt[0].text
        # print(type(description))
        # print(description)


        song_label = song_soup.select('.tags.f-cb')


        # print(song_label)

        labels = song_label[0].find_all('i')
        # print(labels)

        label = []

        for lab in labels:
            label.append(lab.text)
        # print(label)#歌单label标签
        print('歌单：', title)
        print(description)
        print('标签：', label)
        song_list = song_soup.select('.f-hide li')
        for song_data in song_list:
            # print(song_data)
            songname = song_data.text

            id = re.findall('.*?id=(.*)', song_data.find_all('a')[0]['href'])

            song_url = hd + song_data.find_all('a')[0]['href']
            # print(song_url,id)
            if len(id) != 0:
                # print('\t',title,id[0],end='')

                song_response = requests.get(url=song_url, headers=headers)
                song_html = BeautifulSoup(song_response.text, 'html.parser')
                # print(song_html)
                singer = song_html.select('.des.s-fc4')
                # <p class="des s-fc4">歌手：<span title="羽肿"><a class="s-fc7" href="/artist?id=12094419">羽肿</a></span></p>
                # print(singer)

                singer_name = []
                singer_id=[]

                for l in singer:
                    # print(l)
                    # print(l.select('a')[0].string)
                    if '歌手' in str(l):
                        singer_name.append(str(l.select('.s-fc7')[0].string))
                        # print(l.select('.s-fc7')[0]['href'])
                        singerid=re.findall('.*?id=(.*)', l.select('.s-fc7')[0]['href'])
                        singer_id.append(singerid[0])#歌手id列表



                    elif '专辑' in str(l):
                        album_name = l.select('.s-fc7')[0].string
                        album_id=re.findall('.*?id=(.*)', l.select('.s-fc7')[0]['href'])[0]
                        # print(album_id)

                # print('\t','歌手：',singer_name,end='')
                # print('\t','专辑：',album_name)
                # print("\t歌名：{:40}，id:{:<15},歌手：{:<20},专辑：{}".format(str(songname), id[0], str(singer_name),
                #                                                           album_name))
                song_url = f'http://music.163.com/song?id={id[0]}'
                song_response = requests.get(url=song_url, headers=headers).text
                # print(song_response)
                song_soup = BeautifulSoup(song_response, 'html.parser')
                # print(song_soup)
                img_data = song_soup.select('.u-cover.u-cover-6.f-fl')
                img_url = img_data[0].select('.j-img')[0]['data-src']

                # print("\t歌名：{:40}，id:{:<15},歌手：{:<20},专辑：{},".format(str(songname), id[0], str(singer_name),
                #                                                           album_name))
                print(f"id:{id[0]},歌名：{str(songname)},图片链接：{img_url},专辑名：{str(album_name)}")

                #歌曲id:id[0]
                #音乐名：str(songname)
                #图片链接：img_url
                #歌词：
                #专辑名：str(album_name)    专辑id:album_id
                #歌手：singer_name     歌手id:singer_id
                #标签：label



                result_list=[]
                result_list.append(id[0])  # id
                result_list.append(str(songname))#歌名

                #result_list.append(str(singer_name))#歌手
                result_list.append(img_url)
                result_list.append(str(album_name))#专辑
                result_list.append('1')

                result_list.append('\n')

                # fw.write(str(songname)+','+id[0]+','+str(singer_name)+','+str(album_name)+'\n')
                # fw.write(str(result_list)+'\n')

                fw.write(id[0]+';'+str(songname)+';'+img_url+';'+'歌词'+';'+str(album_name)+';'+str(singer_id)+'\n')
                fw_tag.write(id[0]+str(songname)+str(label))
                for i,j in zip(singer_name,singer_id):
                    fw_musician.write(i+j)

fw.close()
fw_musician.close()
fw_tag.close()












