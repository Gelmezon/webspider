#!/usr/bin/env python
# encoding: utf-8
import requests
import re
import pandas
import time
from bs4 import BeautifulSoup
import MySQLdb
import lxml
import sys
reload(sys)
sys.setdefaultencoding('utf8')

db=MySQLdb.connect(host='localhost' , user='root' , passwd='mysql' , db='pythonTest' , charset="utf8")
cursor=db.cursor()
try:
    sqlcreate="CREATE TABLE `nanjing` (`houseid`  int(24) NOT NULL AUTO_INCREMENT, `房子描述`  varchar(200) NOT NULL ,`平米单价`  int(50)  ,`房子总价(万)`  int(20)  ,`地址`  varchar(200)  ,`住宅大小(平米)`  int(50)  ,`房间结构`  varchar(200)  ,`房子朝向`  varchar(20)  ,PRIMARY KEY (`houseid`));"
    cursor.execute(sqlcreate)
    db.commit()
except:
    print "表单已经存在,清除表单....."
    sqlcreate="delete  from nanjing "
    cursor.execute(sqlcreate)
    db.commit()


hds= [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

for pageNum in range(1,200):
  try:
   time.sleep(2.5)
   url = "https://nj.lianjia.com/ershoufang/pg"+str(pageNum)
   fangzi = requests.get(url, hds[pageNum%3]).text
   soup = BeautifulSoup(fangzi, "lxml")
   list_soup = soup.find_all("li", {"class": "clear"})
   for page in list_soup:
      titleDiv=page.find_all("div",{"class":"title"})[0].find_all("a")[0]
      priceSpan= page.find_all("div",{"class":"unitPrice"})[0].find_all("span")[0]
      addressA=page.find_all("div",{"class":"positionInfo"})[0].find_all("a")[0]
      houseInfoDiv=page.find_all("div",{"class":"houseInfo"})[0]
      totalspan=page.find_all("div",{"class":"totalPrice"})[0].find_all("span")[0]
      title=titleDiv.string.strip()
      price=priceSpan.string.strip()
      address=addressA.string.strip()
      houseInfo=str(houseInfoDiv).split("|")
      Tprice=str(totalspan.string.strip())
      print  price+"---------"+address+"--------"+title+"------"+Tprice+"万"+"------"+houseInfo[1]+"--------"+houseInfo[2]+"-----------"+houseInfo[3]
      patten="\d{4,7}"
      patten1="\d{2,5}"
      patten2="\d{2,5}"
      priceInt= int(re.findall(patten,str(price))[0])
      TpriceInt=int(re.findall(patten1,str(Tprice))[0])
      houseaireint=int(re.findall(patten2,str(houseInfo[2]))[0])
      sql="insert into nanjing VALUES (NULL ,'%s','%d','%d','%s','%d','%s','%s')"%(str(title),priceInt,TpriceInt,str(address),houseaireint,str(houseInfo[1]),str(houseInfo[3]))
      try:
        cursor.execute(sql)
        db.commit()
      except Exception ,e:
          print repr(e)
          print "输入数据发生错误"
          db.rollback()
  except:
      print "抓取数据失败"
      continue
db.close()

