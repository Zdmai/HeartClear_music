#包含简介，歌单标签，  歌曲的名字，歌手名，专辑名，歌曲id(可以通过id来下载歌曲和歌词）
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
        # print(l)
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
        song_txt = song_soup.find_all('script', type='application/ld+json')
        dic = eval(song_txt[0].text)
        # print(dic)#字典
        s = dic['description']
        start = s.find('简介：') end = s.find('更多相关热门精选歌单推荐尽在网易云音乐')
        # print(description)#简介和标签
        description = s[start:end]

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

                for l in singer:
                    # print(l)
                    # print(l.select('a')[0].string)
                    if '歌手' in str(l):
                        singer_name.append(str(l.select('.s-fc7')[0].string))
                    elif '专辑' in str(l):
                        album_name = l.select('.s-fc7')[0].string
                # print('\t','歌手：',singer_name,end='')
                # print('\t','专辑：',album_name)
                print("\t歌名：{:40}，id:{:<15},歌手：{:<20},专辑：{}".format(str(songname), id[0], str(singer_name),
                                                                          album_name))












