#!/usr/bin/env python"
# coding: utf-8
# author: 芋圆
import requests, argparse, sys, re
from requests.packages import urllib3
from urllib.parse import urlparse
import warnings
from concurrent.futures import ThreadPoolExecutor
import queue
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
url_list=[]
threads=[]
q1 = queue.Queue()

def parse_args():
    parser = argparse.ArgumentParser(epilog=None)
    parser.add_argument("-u", "--url", help="The website")
    parser.add_argument("-f", "--file", help="The file contains url or js")
    parser.add_argument("-w", "--web", help="web. ",action="store_true")
    parser.add_argument("-s", "--screenweb", help="screenweb ", action="store_true")
    return parser.parse_args()

def extract_URL(JS):
    pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
    pattern = re.compile(pattern_raw, re.VERBOSE)
    result = re.finditer(pattern, str(JS))
    if result == None:
        return None
    js_url = []
    return [match.group().strip('"').strip("'") for match in result
            if match.group() not in js_url]




def Extract_html(URL):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    }
    try:
        raw = requests.get(URL, headers=header, timeout=5, verify=False)
        if raw.status_code == 200:
            raw = raw.content.decode("utf-8", "ignore")
            return raw
        else:
            return None
    except:
        return None

def process_url(URL, re_URL):  #源码当中的js提取并访问
    black_url = ["javascript:"]  # Add some keyword for filter url.
    URL_raw = urlparse(URL)
    ab_URL = URL_raw.netloc
    host_URL = URL_raw.scheme
    if re_URL[0:2] == "//":
        result = host_URL + ":" + re_URL
    elif re_URL[0:4] == "http":
        result = re_URL
    elif re_URL[0:2] != "//" and re_URL not in black_url:
        if re_URL[0:1] == "/":
            result = host_URL + "://" + ab_URL + re_URL
        else:
            if re_URL[0:1] == ".":
                if re_URL[0:2] == "..":
                    result = host_URL + "://" + ab_URL + re_URL[2:]
                else:
                    result = host_URL + "://" + ab_URL + re_URL[1:]
            else:
                result = host_URL + "://" + ab_URL + "/" + re_URL
    else:
        result = URL
    return result
def find_by_file(file_path, js=False):
    with open(file_path, "r") as fobject:
        links = fobject.read().split("\n")
    if links == []: return None
    print("ALL Find " + str(len(links)) + " links")
    urls = []
    i = len(links)
    for link in links:
        if js == False:
            temp_urls = find_by_url(link)
        else:
            temp_urls = find_by_url(link, js=True)
        if temp_urls == None: continue
        print(str(i) + " Find " + str(len(temp_urls)) + " URL in " + link)
        for temp_url in temp_urls:
            if temp_url not in urls:
                urls.append(temp_url)
        i -= 1
    return urls



def find_by_url(url, js=False):
    if js == False:
        try:
            print("url:" + url)
        except:
            print("Please specify a URL")
        print('获取接口信息中')
        html_raw = Extract_html(url)
        if html_raw == None:
            print("Fail to access " + url)
            return None
        #print(html_raw)
        html = BeautifulSoup(html_raw, "html.parser")
        html_scripts = html.findAll("script")
        #print(html_scripts)
        script_array = {}
        script_temp = ""
        for html_script in html_scripts:
            script_src = html_script.get("src")
            #print(script_src)
            if script_src == None:
                script_temp += html_script.get_text() + "\n"
            else:
                purl = process_url(url, script_src)
                script_array[purl] = Extract_html(purl)
                #print(script_array[purl])
        if url[-1] != '/':
            url = url + '/'
        script_array[url] = script_temp
        # script_array.append(script_temp)
        allurls = []

        # 遍历js文件，获取js文件中接口信息
        for script in script_array:
            #print(script)
            temp_urls = extract_URL(script_array[script])
            if len(temp_urls) == 0: continue
            for temp_url in temp_urls:
                temp_url = temp_url.strip('../')
                # print(temp_url)
                url_vul = process_url(script, temp_url)
                # print(url_vul)
                temp1 = urlparse(url)
                temp2 = urlparse(url_vul)

                # 获取到的接口信息中去除jpg、png、css、vue等
                if '.exe' not in temp2.path and '.png' not in temp2.path and '.jpg' not in temp2.path and '.vue' not in temp2.path and '.css' not in temp2.path and '@' not in temp2.path and '.svg' not in temp2.path:

                    allurls.append(url_vul)


        pattern = r"(?P<ip>\d+\.\d+\.\d+\.\d+)"  # 定义匹配 IP 地址的正则表达式
        match = re.search(pattern, url)  # 在 URL 中查找匹配正则表达式的部分
        if match:
            url = match.group("ip")  # 获取匹配到的 IP 地址部分
        else:
            print("No match found.")
        allurls = [x for x in allurls if url in x]
        allurls = list(dict.fromkeys(allurls))
        print("接口数量:" + str(len(allurls)))
        print(allurls)
        filename = "result.txt"
        with open(filename, 'a') as f:
            for item in allurls:
                f.write("%s\n" % item)
        return allurls

async def fetch(session,url):
    async with session.get(url,verify_ssl=False) as response:
        html = await response.text()
        lex=str(len(html))
        status=str(response.status)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = str(soup.title.string)
        except AttributeError:
            title = 'No title found'
        print('WebTitle:' +url + '    code:' + status + '    title:' + title+'   len:'+lex)
        with open('web.txt', 'a+') as f:
            f.write('WebTitle:' +url + '    code:' + status + '    title:' + title+'   len:'+lex+'\n')
        return html
async def main():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    async with aiohttp.ClientSession() as session:
        for ip in open("result.txt"):
            ip=ip.strip('\n')
            url_list.append(ip)
        tasks=[asyncio.create_task(fetch(session,url)) for url in url_list]
        done,pending = await asyncio.wait(tasks)

def jsfind():
    list=[]
    for url in open('web.txt'):
        url.strip('\n')
        str = url
        list1 = str.split('    ',1)      #采用默认分隔符进行分割
        if list1[1] in list:
                list.append(list1[1])
        else:
            with open(r'webscreen.txt', 'a+') as f:
                f.write(str)
                f.close()
            list.append(list1[1])

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    urllib3.disable_warnings()
    args = parse_args()
    print(args.url)
    if args.url != None:
        urls = find_by_url(args.url)
    if args.file != None:
        urls = find_by_file(args.file)
    if args.web == True:
        asyncio.run(main())
        if args.screenweb == True:
            jsfind()

