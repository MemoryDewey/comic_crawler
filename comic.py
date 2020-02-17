import requests
import json
from lxml import etree
import execjs
import re
import os
import time
import random
from urllib import request
import http

# request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36',
    'Referer': 'https://www.177mh.net',
}

# 图片下载request headers
image_headers = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.177mh.net',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

# 漫画网址
PREFIX = 'https://www.177mh.net'
# 获取图片前缀接口
IMAGE_HREF = 'https://css.gdbyhtl.net/img_v1/cn_svr.aspx'

# 代理IP
# https://www.xicidaili.com/nn/
proxy = [
    {'http': '115.211.227.2:9999'},
    {'http': '1.196.177.25:9999'},
    {'http': '36.25.40.69:9999'},
    {'http': '59.60.209.168:9999'},
    {'http': '49.89.85.23:9999'},
]


# 获取图片章节
def get_chapter(url):
    response = requests.get(url, headers=headers)
    try:
        html = etree.HTML(response.content)
        chapters = html.xpath('//div[@class="ar_list_coc"]/ul/li/a')
        item = []
        for chapter in chapters:
            temp = {'title': chapter.xpath('@title')[0],
                    'href': PREFIX + chapter.xpath('@href')[0],
                    'coid': chapter.xpath('@href')[0].split('/')[2][:-5]
                    }
            item.append(temp)
        # 爬取的章节为倒序，倒置一下数组为正序
        item.reverse()
        with open('./details.json', mode='w', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False))
    except Exception as e:
        raise e


# 获取图片下载前缀
def get_image_prefix(params):
    response = requests.get(IMAGE_HREF, headers=headers, params=params)
    text = response.text
    # http/https 前缀
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url = re.findall(pattern, text)
    return url[0]


# 获取漫画
def get_comic(_chapter, _cid):
    global data
    if os.path.exists('./downloads/%s' % _chapter['title']):
        print('%s had downloaded' % _chapter['title'])
    else:
        print('start downloading %s' % _chapter['title'])
        response = requests.get(_chapter['href'], headers=headers)
        coid = _chapter['coid']
        try:
            html = etree.HTML(response.content)
            # 解析并执行JS
            script_content = html.xpath('//script[1]/text()')[0]
            parse_str = script_content.replace('function(p,a,c,k,e,d)', 'function fun(p, a, c, k, e, d)')
            parse_str = parse_str.replace('eval(', '')[:-2]
            fun = """
                 function run(){
                                let result = %s;
                                return result;
                            }
                """ % parse_str
            parse_str = execjs.compile(fun).call('run')
            fun = """
                function run(){
                                %s;
                                return {"z":atsvr,"page":msg,"s":img_s};
                            }
                """ % parse_str
            parse_str = execjs.compile(fun).call('run')
            url_params = {'z': parse_str['z'], 's': parse_str['s'], 'cid': _cid, 'coid': coid}
            image_prefix = get_image_prefix(url_params)
            page_str = parse_str['page']
            pages = page_str.split('|')
            if not os.path.exists('./downloads/%s' % _chapter['title']):
                os.makedirs('./downloads/%s' % _chapter['title'])
                for index, url in enumerate(pages):
                    image = image_prefix + url + '.webp'
                    random_proxy = proxy[random.randint(0, len(proxy) - 1)]
                    proxy_support = request.ProxyHandler(random_proxy)
                    print("proxy ip is %s" % random_proxy)
                    opener = request.build_opener(proxy_support)
                    request.install_opener(opener)
                    req = request.Request(image, headers=image_headers)
                    res = request.urlopen(req)
                    try:
                        data = res.read()
                    except http.client.IncompleteRead as e:
                        data = e.partial
                    with open('./downloads/%s/%s.jpg' % (_chapter['title'], index), 'wb') as fp:
                        fp.write(data)
                    # 程序随机休眠0.5s到1s
                    seconds = random.uniform(0.5, 1)
                    time.sleep(seconds)
                    print('%s - %d - save image from %s' % (_chapter['title'], index, image))
            print('download %s  complete' % _chapter['title'])
        except Exception as e:
            raise e


if __name__ == '__main__':
    # 网站漫画ID
    cid = "240268"
    chapters = None
    get_chapter('https://www.177mh.net/colist_%s.html' % cid)
    f = open('./details.json', 'r', encoding='UTF-8')
    chapters = json.load(f)
    for chapter in chapters:
        get_comic(chapter, cid)
    print('done')
