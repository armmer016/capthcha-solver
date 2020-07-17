import requests
import re
import os
from PIL import Image
from io import BytesIO
from CAPTCHA_object_detection import *
import time
from colorama import Fore
from colorama import init
from time import process_time
try:
    import pkg_resources.py2_warn
except ImportError:
    pass
init()
ip = ""
proxyList = []
target = input("target == ")
session_id = input("session id == ")
proxy = input("proxy? y/n == ")
index = 0

def chomp(x):
    if x.endswith("\r\n"):
        return x[:-2]
    if x.endswith("\n") or x.endswith("\r") or x.endswith(" "):
        return x[:-1]
    return x

if ("y" in proxy):
    infile = open('proxylist.txt','r')
    ip = infile.readlines()
    proxyList = []
    for line in (ip):
        print(line)
        proxyList.append(chomp(line))
    infile.close()

if ("tor" in proxy):
    proxies = {
        "http": "socks5://127.0.0.1:9150",
    }


def getPicture(data):
    
    imageurl = ("http://playserver.co/index.php/VoteGetImage/"+str(data))
    print(imageurl)
    headers = {
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Referer": "http://playserver.in.th/index.php/Vote/prokud/MC-Surviver-19921",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie":"__utma=123569098.25167225.1590924307.1590924307.1590924307.1; __utmz=123569098.1590924307.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
        "Connection": "close"
         }
    if ("n" in proxy):
        rsp = requests.get(imageurl,headers=headers)
    else:
        rsp = requests.get(imageurl,headers=headers,proxies=proxies,verify=False)
        #rsp = requests.get(imageurl,headers=headers)
    #rsp.raise_for_status()
    content_type_received = rsp.headers['Content-Type']
    binarycontent = BytesIO(rsp.content)
    if content_type_received.startswith('image'): 
        i = Image.open(binarycontent)
        outfilename = os.path.join('myimg'+str(session_id)+'.jpg')
        with open(outfilename, 'wb') as f:
            print("write")
            f.write(rsp.content)
        rsp.close()


def getPostPIC():
    picID = ""
    headers = {
        "Accept": "*/*",
        "Content-Length": "0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Origin": "http://playserver.in.th",
        "Referer": "http://playserver.in.th/index.php/Vote/prokud/MC-Surviver-19921",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
         }
    url = "http://playserver.co/index.php/Vote/ajax_getpic/MC-Surviver-19921"
    if ("n" in proxy):
        r = requests.post(url, headers=headers)
    else:
        r = requests.post(url, headers=headers, proxies=proxies)
    checksum = r.text
    print(checksum)
    m = re.search('"checksum":"(.+?)"',checksum)
    if m:
        picID = m.group(1)

    return picID
    
def preSubmit(): 
    print("preSubmit...")
    picID = getPostPIC()
    getPicture(picID)
    text = Captcha_detection("myimg"+str(session_id)+".jpg")
    print("Result: "+str(text))
    data = ("server_id=19921&captcha="+text+"&gameid=xxxEAGLE-VOTE&checksum="+picID)
    return data
    
def submit(data1):
    print("submit")
    headers = {
        "Accept": "*/*",
        "Content-Length": "64",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://playserver.in.th",
        "Referer": "http://playserver.in.th/index.php/Vote/prokud/MC-Surviver-19921",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
         }
    
    url = "http://playserver.co/index.php/Vote/ajax_submitpic/MC-Surviver-19921"
    if ("n" in proxy):
        r = requests.post(url, headers=headers,  data=data1)
    else:
        r = requests.post(url, headers=headers,  data=data1 ,proxies=proxies)
    print(r.text)
    newFile = open('logSUBMIT.txt','w')
    newFile.write(r.text)
    return (r.text)

success = 0
attemp = 0

for x in range(int(target)):
    if ("y" in proxy):
        proxies = {
          "http": "http://"+proxyList[index],
        }
        print(proxyList[index])
    start2 = process_time()
    attemp += 1
    try:
        firstData = preSubmit()
        if len(firstData)>3:
            checksum = submit(firstData)
        else :
            print ("firstDATA ERROR")
    except Exception as e:
        print("ERROR : "+str(e))
        index += 1
        continue

    f = re.search('"success":false',checksum)
    s = re.search('"success":true',checksum)
    if f:
        x = int(success)-1
        print(Fore.RED+" failed"+Fore.WHITE)
    if s:
        success += 1
        print(Fore.GREEN+" success"+Fore.WHITE)    
    end2 = process_time()
    timer2 = int(end2)-int(start2)
    print(timer2)
    sleepTime = 60-int(timer2/2)
    print(str(session_id)+" sleeping..."+str(sleepTime)+"sec -> "+Fore.MAGENTA+" success: "+str(success)+" attemp: "+str(attemp)+Fore.WHITE)
    index += 1



