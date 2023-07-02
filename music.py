import requests
from bs4 import BeautifulSoup
import re

#song_url='http://music.163.com/song/media/outer/url?id='
#song_word_url='http://music.163.com/api/song/lyric?id={num_id}&lv=-1&kv=-1&tv=-1'



#url='http://music.163.com/playlist?id=94284266'
#url='http://music.163.com/discover/playlist'
url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='


# headers={
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# }

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
}

for i in range(0, 666, 35):
    response=requests.get(url=url + f'{i}',headers=headers)
    print(url + f'{i}')
    html_data=response.text
    soup=BeautifulSoup(html_data, 'html.parser')
    #print(soup)
    ls=soup.select('.dec a')

    #lis=soup.select('')

    ht='http://music.163.com'
    song_url='http://music.163.com/song?id='
    for l in ls:
        project=l['title']
        link=ht+l['href']
        #print(title,link)
        print(project)

    #ul='http://music.163.com/playlist?id=2143660964'

    # html=requests.get(url=ul,headers=headers).text
    # song_soup=BeautifulSoup(html,'html.parser')
    # song_list=song_soup.select('.f-hide li a')
    # #print(song_list)
    # for l in song_list:
    #     print(l['href'],l.string)
        ul=link
        html = requests.get(url=ul, headers=headers).text
        song_soup = BeautifulSoup(html, 'html.parser')
        song_list = song_soup.select('.f-hide li a')
        #print(song_list)
        for l in song_list:
            #print(l['href'])
            id=re.findall('.*?id=(.*)',l['href'])
            title=l.string
            if len(id)!=0:
                #print('\t',title,id[0],end='')
                song=song_url+id[0]
                song_response=requests.get(url=song,headers=headers)
                song_html=BeautifulSoup(song_response.text,'html.parser')
                #print(song_html)
                singer=song_html.select('.des.s-fc4')
                #<p class="des s-fc4">歌手：<span title="羽肿"><a class="s-fc7" href="/artist?id=12094419">羽肿</a></span></p>
                #print(singer)
                singer_name=[]

                for l in singer:
                    #print(l)
                    #print(l.select('a')[0].string)
                    if '歌手' in str(l):
                        singer_name.append(str(l.select('.s-fc7')[0].string))
                    elif '专辑' in str(l):
                        album_name=l.select('.s-fc7')[0].string
                #print('\t','歌手：',singer_name,end='')
                #print('\t','专辑：',album_name)
                print("歌名：{:40}，id:{:<15},歌手：{:<20},专辑：{}".format(str(title),id[0],str(singer_name),album_name))










