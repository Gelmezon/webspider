#!/usr/bin/env python
# encoding: utf-8
import requests
import time
from lxml import etree
from bs4 import BeautifulSoup
import re
import sys
import csv
import codecs
reload(sys)
sys.setdefaultencoding('utf8')

io=["科技","文学","文化","流行","生活","经管"]
hds= [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
for opinion in io:
  filename = "F:\\" + opinion + ".csv."
  f = open(filename, "w")
  f.write(codecs.BOM_UTF8)
  write = csv.writer(f)
  write.writerow(["书名", "作者", "出版信息", "评分"])
  for i in range(0,300):

    try:
     time.sleep(5)
     url="https://book.douban.com/tag/"+opinion+"?start="+str(i*80)+"&type=T"


     douban= requests.get(url,hds[(i+3)%3]).text;

     soup=BeautifulSoup(douban,"lxml")

     list_soup = soup.find_all('li', {'class': 'subject-item'})
     if(len(list_soup)==0):
        break

     for list in list_soup:
      page=str(list)
      patten = 'title="(.*?)"\W'
      p=re.compile(patten)
      title= p.findall(page)
      ls=list.find_all('div',{"class":"pub"})
      fen=list.find_all('span',{"class":"rating_nums"})
      writer=((ls[0].string.strip()).split("/"))[0]
      if((float(fen[0].string))>8):
       write.writerow([title[0], writer, ls[0].string.strip(), fen[0].string])
       print  title[0]+"----"+ ls[0].string.strip()+"-----"+fen[0].string
     else:
      continue
    except:
     if(len(list_soup)>10):
        continue
     else:
           print "当前页数" + str(i + 1)
           f.close()
           break