import requests
from bs4 import BeautifulSoup
import re

#song_url='http://music.163.com/song/media/outer/url?id='#下载歌曲的接口
#song_word_url='http://music.163.com/api/song/lyric?id={num_id}&lv=-1&kv=-1&tv=-1'下载歌词的接口

hd='http://music.163.com'

#url='http://music.163.com/playlist?id=94284266'
url='http://music.163.com/discover/playlist'#歌单




headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
}

# fw=open('音乐.txt','a',encoding='utf-8')#结果文件
# fw_musician=open("歌手.txt",'a',encoding='utf-8')
# fw_tag=open("标签.txt",'a',encoding="utf-8")
fw=open('music.txt','w',encoding='utf-8')#结果文件
fw_musician=open("musician.txt",'w',encoding='utf-8')
fw_tag=open("tag.txt",'w',encoding="utf-8")


for i in range(0,500,35):#歌单大页面
    num=i
    number=0
    url=f'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset={i}'
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    soup = BeautifulSoup(html_data, 'html.parser')

    ls = soup.select('.m-cvrlst.f-cb li')

    # print(ls)#歌单列表，大歌单


    for l in ls:
        # print(l)
        # quit()
        number+=1
        img = l.select('.j-flag')[0]['src']

        # data = l.select('.tit')[0]
        # # print(type(data))
        # title = data['title']
        data=l.select('.msk')[0]
        title=data['title']

        playlist_id = data['href']
        playlist_url = hd + playlist_id#单个歌单的url

        # print(title,playlist_id)
        #
        # print(playlist_url)#歌单地址

        song_response = requests.get(url=playlist_url, headers=headers)
        song_soup = BeautifulSoup(song_response.text, 'html.parser')
        #print(song_soup)
        descriptino_txt=song_soup.select('#album-desc-more')

        print(f"第{num}页,第{number}个歌单")
        print("歌单：",title, playlist_url)
        print(descriptino_txt[0].text)

        song_label = song_soup.select('.tags.f-cb')
        labels = song_label[0].find_all('i')
        # print(labels)

        label = []

        for lab in labels:
            label.append(lab.text)
        print("标签：",label)

        song_list = song_soup.select('.f-hide li')#歌单的歌曲列表
        for song_data in song_list:
            try:
                # print(song_data)
                songname = song_data.text
                # print(songname)
                id = re.findall('.*?id=(.*)', song_data.find_all('a')[0]['href'])
                song_url = hd + song_data.find_all('a')[0]['href']

                # print(song_url,id)
                if len(id) != 0:
                    # print('\t',title,id[0],end='')

                    song_response = requests.get(url=song_url, headers=headers)
                    song_html = BeautifulSoup(song_response.text, 'html.parser')
                    # print(song_html)
                    singer = song_html.select('.des.s-fc4')
                    # print(singer)
                    singer_name = []
                    singer_id = []

                    for l in singer:
                        # print(l)
                        # print(l.select('a')[0].string)
                        if '歌手' in str(l):
                            singer_name.append(str(l.select('.s-fc7')[0].string))
                            # print(l.select('.s-fc7')[0]['href'])
                            # print(l.select('.s-fc7')[0].get('href',default=0))
                            if l.select('.s-fc7')[0].get('href', default=0) == 0:
                                singerid = 0
                            else:
                                singerid = re.findall('.*?id=(.*)', l.select('.s-fc7')[0].get('href', default=0))[0]

                            # print(singerid)

                            singer_id.append(singerid)  # 歌手id列表
                        elif '专辑' in str(l):
                            album_name = l.select('.s-fc7')[0].string

                            if l.select('.s-fc7')[0].get('href', default=0) == 0:
                                album_id = 0
                            else:

                                album_id = re.findall('.*?id=(.*)', l.select('.s-fc7')[0].get('href', default=0))[0]
                                # print(album_id)

                    song_url = f'http://music.163.com/song?id={id[0]}'
                    song_response = requests.get(url=song_url, headers=headers).text
                    # print(song_response)
                    song_soup = BeautifulSoup(song_response, 'html.parser')
                    # print(song_soup)
                    img_data = song_soup.select('.u-cover.u-cover-6.f-fl')
                    img_url = img_data[0].select('.j-img')[0]['data-src']

                    # print("\t歌名：{:40}，id:{:<15},歌手：{:<20},专辑：{},".format(str(songname), id[0], str(singer_name),
                    #                                                           album_name))

                    # 歌曲id:id[0]
                    # 音乐名：str(songname)
                    # 图片链接：img_url
                    # 歌词：
                    # 专辑名：str(album_name)    专辑id:album_id
                    # 歌手：singer_name     歌手id:singer_id
                    # 标签：label

                    #print('\t', f"id:{id[0]},歌名：{str(songname)},图片链接：{img_url},专辑名：{str(album_name)}")
                    fw.write(id[0] + ';' + str(songname) + ';' + img_url + ';' + '歌词' + ';' + str(album_name) + ';' + str(singer_id) + '\n')
                    fw_tag.write(id[0] +';'+ str(songname)+';' + str(label)+'\n')
                    for i, j in zip(singer_name, singer_id):
                        fw_musician.write(str(i)+';' + str(j)+'\n')
                    print('\t', f"id:{id[0]},歌名：{str(songname)},图片链接：{img_url},专辑名：{str(album_name)}")
            except:
                continue

fw.close()
fw_musician.close()
fw_tag.close()



