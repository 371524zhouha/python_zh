import requests,os,math,json,threading,time
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor
from hanzishouzimu import main1

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}



def get_city_list(citys):
    '''得到城市的首字母组合'''
    city_lists = []
    for city in citys:
        city_lists.append(main1(city))
    return city_lists

def get_city_page_url(city):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    url='https://{}.lianjia.com/ershoufang/'.format(city)
    try:
        response=requests.get(url,headers=headers)
        doc=pq(response.text)
        number_max=int(doc(".resultDes .total span").text())
        page_max=math.ceil(float(number_max/30))
        print(page_max)
        if page_max>2:page_max=2
        url_pages=[]
        for i in range(page_max):
            url_page=url+'pg'+str(i+1)+'/'
            url_pages.append(url_page)
        return url_pages
    except:
        print('获得各城市各页的url数值有错误，请检查')

details= list()

def get_valid_ip():
    url = "http://localhost:5555/random"
    try:
        ip = requests.get(url).text
        return ip
    except:
        print("请先运行代理池")

def get_house_url(url_page):
    global details
    """获得一个城市，前100页中房子的URL"""
    house_urls = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

    response=requests.get(url_page,headers=headers)
    doc=pq(response.text)
    # print(doc)
    try:
        urls=doc('.clear .noresultRecommend').items()
        # print(urls)
        i=0
        for url in urls:
            i+=1
            if i>30:
                break
            # print(url.attr('href'))
            house_urls.append(url.attr('href'))
        print(len(house_urls))
        return house_urls
    except:
        print('获取网页中：',url_page,':::单个房间的url出错,请检查')


lock = threading.Lock()
def get_house_detail(res):
    global details
    house_urls=res.result()
    for house_url in house_urls:
       try:
           response = requests.get(house_url, headers=headers, timeout=3)
           doc = pq(response.text)
           detail = {}
           detail["title"] = doc('.content .title .main').text()
           detail["prince"] = doc('.unitPriceValue').text()
           detail["area"] = doc('.houseInfo .area .mainInfo').text()
           detail["built_time"] = doc('.houseInfo .area .subInfo').text()
           print(detail)
           details.append(detail)
       except:
            print("获取详情页出错,换ip重试")
            proxies = {
               "http": "http://" + get_valid_ip(),
                }
            try:
                response = requests.get(house_url, headers=headers, proxies=proxies)
                doc = pq(response.text)
                detail = {}
                detail["title"] = doc('.content .title .main').text()
                detail["prince"] = doc('.unitPriceValue').text()
                detail["area"] = doc('.houseInfo .area .mainInfo').text()
                detail["built_time"] = doc('.houseInfo .area .subInfo').text()
                print(detail)
                details.append(detail)
            except:
                    print(house_url,':获取详细信息失败;换个ip试一试')

def save_data(data,filename):
    with open(filename+".json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    citys = ['北京', '天津']
    citys_zimu = get_city_list(citys)
    for city in citys_zimu:
        url_pages=get_city_page_url(city)
        p = ThreadPoolExecutor(30)
        print(url_pages)
        for page_url in url_pages:
            p.submit(get_house_url, page_url).add_done_callback(get_house_detail)
        p.shutdown()
        save_data(details, city)
        details.clear()

if __name__ == '__main__':
    old_time=time.time()
    main()
    new_time=time.time()
    print('每个城市60个数据，一共花费的时间是：',new_time-old_time)

