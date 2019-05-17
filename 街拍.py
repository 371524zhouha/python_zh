import requests,re
from hashlib import md5
from urllib.parse import urlencode

def get_page_index(offset,keyword): # 获取页面的HTML
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36/'}
    #
    data={'keyword':keyword,}
    try:
        url='https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset='+str(offset*20)+'&format=json&'+urlencode(data)+'&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis'

        response=requests.get(url,headers=headers)
        if response.status_code== 200:
            # print(response.text)
            return response.text
    except requests.ConnectionError:
        print('请求失败')
        return None

def get_images_url(html):
    # pattern=re.compile(
        # '"image_url":"(.*?)"',re.S)
    url_=re.compile(
        '"url":"h(.*?)"}',re.S)
    # items=re.findall(pattern,html)
    items = re.findall(url_, html)
    # print(len(items))
    return items

def save_image(offset,keyword,j):
    items=get_images_url(get_page_index(offset,keyword))
    n=j
    for image in items:
        n=n+1
        print('h'+image)
        r = requests.get('h'+image)
        path = 'F:/python_work/1/' + str(n) + '.jpg'
        print(path)
        # url = image + '.jpg'
        # path = "F:\python_work\1\.jpg" #设置图片文件路径，前提是必须要有abc这个文件夹
        # r = requests.request('get', url)  # 获取网页
        print(r.status_code)
        with open(path, 'wb') as f:  # 打开写入到path路径里-二进制文件，返回的句柄名为f
            f.write(r.content)  # 往f里写入r对象的二进制文件
        f.close()
        print(n)
# save_image(0,'街拍')
for i in range(5):
    save_image(i,'街拍',i*100)