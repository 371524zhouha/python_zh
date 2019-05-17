import requests,re,os,asyncio,time
from urllib import request
from urllib.parse import urlencode
from pypinyin import lazy_pinyin
class ximalaya():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
    def pinyin(self,key):
        pin=lazy_pinyin(key)
        pin="".join(pin)  #Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串
        return pin

    def get_zhonglei_html(self,category,pin,page):
        data={
            'category':category,
            'subcategory': pin,
            'page':page,
        }
        htmls=[]
        url='https://www.ximalaya.com/revision/category/queryCategoryPageAlbums?category={}&subcategory={}&meta=&sort=0&page={}&perPage=30'.format(category,pin,page)
        # print(url)
        r=requests.get(url,headers=self.header)
        # print(r.text)
        pattern1=re.compile('"albumId":(.*?),',re.S)
        pattern2=re.compile('"title":"(.*?)",',re.S)
        part=re.findall(pattern1,r.text)
        titles=re.findall(pattern2,r.text)
        # print(titles,part)
        for i in range(len(titles)):
            url='https://www.ximalaya.com/revision/play/album?albumId={}&pageNum=1&sort=-1&pageSize=30'.format(part[i])
            # print("名字:",titles[i],"  url:",url)
            htmls.append({'专辑名称：':titles[i],'链接：':url})
        return htmls

    def download_music(self,html,zhuanjiming,gequming):
        # path=zhuanjiming
        # if os.path.exists(path):
        gequming=gequming.translate(str.maketrans('','','/'))
        path='F:/python_work/1/ximalaya/'+gequming+ '.m4a'
        request.urlretrieve(html,path)
        print(zhuanjiming,'===',gequming,'===下载成功')


    def download_music2(self,htmls,zhonglei):
        # path=zhuanjiming
        # if os.path.exists(path):
        for i in range(len(htmls)-1):
            html=htmls[i].get('歌曲链接：')
            gequming=htmls[i].get('歌曲名称：')
            zhuanjiming=htmls[i].get('专辑名称：')
            path1='F:/python_work/1/ximalaya/'+zhonglei
            if not os.path.exists(path1):os.mkdir(path1)
            path=path1+'/'+str(i)+ '.m4a'
            request.urlretrieve(html,path)
            print(zhuanjiming,'===',gequming,'===下载成功')
    async def download_music3(self,html,zhonglei):
        time.sleep(5)
        html=html.get('歌曲链接：')
        gequming=html.get('歌曲名称：')
        zhuanjiming=html.get('专辑名称：')
        path1='F:/python_work/1/ximalaya/'+zhonglei
        if not os.path.exists(path1):os.mkdir(path1)
        path=path1+'/'+str(i)+ '.m4a'
        request.urlretrieve(html,path)
        print(zhuanjiming,'===',gequming,'===下载成功')

    def get_yinpin(self,htmls):
        song_html=[]
        for i in range(len(htmls)-1):
            url=htmls[i].get('链接：')
            if url==None: continue
            r = requests.get(url, headers=self.header)
            pattern1 = re.compile('"src":"(.*?)"', re.S)
            song_names = re.compile('"trackName":"(.*?)",', re.S)
            part = re.findall(pattern1, r.text)
            song_titles = re.findall(song_names, r.text)
            for j in range(len(part)-1):
                # if j==1: continue
                # print(song_titles[j])
                song_html.append({
                    '专辑名称：': htmls[i].get('专辑名称：'),
                    '歌曲名称：': song_titles[j],
                    '歌曲链接：': part[j]})
                # self.download_music(part[j],htmls[i].get('专辑名称：'),str((i+1)*(j+1)))
        return song_html




htmls=ximalaya().get_zhonglei_html('yinyue','yaogun','2')
htms=ximalaya().get_yinpin(htmls)
# print(htms)
ximalaya().download_music3(htms,'yaogun')
# loop=asyncio.get_event_loop()
# tasks=[ximalaya().download_music3(html,'yaogun') for html in htms]
# loop.run_until_complete(asyncio.gather(*tasks))
