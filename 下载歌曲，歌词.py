import requests
from bs4 import  BeautifulSoup
import json
import re
import os

# song_url = f"http://music.163.com/song/media/outer/url?id={num_id}.mp3"
# songwords_url = f"http://music.163.com/api/song/lyric?id={num_id}&lv=-1&kv=-1&tv=-1"

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
filename='music//歌曲//'
if not os.path.exists(filename):
    os.mkdir(filename)

fr=open('music.txt','r',encoding='utf-8')
for line in fr:
    ls=line.split(';')
    #print(ls)
    num_id=ls[0]

    music_url = f"http://music.163.com/song/media/outer/url?id={num_id}.mp3"
    songwords_url = f"http://music.163.com/api/song/lyric?id={num_id}&lv=-1&kv=-1&tv=-1"
    # song_url=f'http://music.163.com/song?id={num_id}'

    title=ls[1]
    # title=ls[0]
    # musician=ls[3]
    music_content = requests.get(url=music_url, headers=headers).content
    res = requests.get(url=songwords_url, headers=headers).text
    json_obj = json.loads(res)
    lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lrc_text = re.sub(reg, '', lyric).strip()
    lrc_text = 'musician:' + str(musician) + '\n' + 'song_name:' + title + lrc_text
    print(title)
    with open(filename + num_id + ".mp3", 'wb') as f:
        f.write(music_content)
    with open(filename+num_id+".txt",'w',encoding='utf-8') as w:
        w.write(lrc_text)

    # song_response=requests.get(url=song_url,headers=headers).text
    # # print(song_response)
    # song_soup=BeautifulSoup(song_response,'html.parser')
    # # print(song_soup)
    # img_data=song_soup.select('.u-cover.u-cover-6.f-fl')
    # img_url=img_data[0].select('.j-img')[0]['data-src']
    #
    # print(img_url)
    # print(title)










