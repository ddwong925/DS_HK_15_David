#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib2
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
 
# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('HK_weather00.txt', 'w')

# set cookie as showmetar = 1
r = requests.Session()
#metar = r.get('http://www.wunderground.com/cgi-bin/findweather/getForecast?setpref=SHOWMETAR&value=1')

# Iterate through year, month, and day
for y in range(2017, 2018):
  for m in range(12, 13):
    for d in range(1,8):
    
      # Check if leap year
      if y%400 == 0:
        leap = True
      elif y%100 == 0:
        leap = False
      elif y%4 == 0:
        leap = True
      else:
        leap = False

      # Check if already gone through month
      if (m == 2 and leap and d > 29):
        print "its first"
        continue
      elif (m == 2 and d > 28):
        print 'its second'
        continue
      elif (m in [4, 6, 9, 11] and d > 30):
        print 'its third'
        continue

      
      if len(str(d)) < 2:
        dd = "0" + str(d)
      else:
        dd = str(d)
      if len(str(m)) < 2:
        mm = "0" + str(m)
      else:
        mm = str(m)
      
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6/0); WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
      # Open wunderground.com url
      # url = "http://www.wunderground.com/history/airport/VHHH/"+str(y)+ "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
      url = "http://www.hko.gov.hk/cgi-bin/hko/yes.pl?year="+ str(y) +"&month=" + str(mm) +"&day=" +str(dd) +"&language=english&B1=Confirm"
      page = r.get(url,headers = headers)
      
      # Get temperature from page
      soup = BeautifulSoup(page.text,'lxml')

      # print soup.find('pre').text
      try:
        text = str(soup.find('pre').text)


        timestamp = str(y)+'-'+str(mm)+'-'+str(dd)
        print timestamp

        max_temp_text = re.search('MAX.*[0123456789.]+',text, re.IGNORECASE).group(0)
        max_temp = re.findall('[0123456789.]+',max_temp_text)
        print max_temp
        min_temp_text = re.search('MIN.*[0123456789.]+',text, re.IGNORECASE).group(0)
        min_temp = re.findall('[0123456789.]+',min_temp_text)
        print min_temp
        grass_temp_text = re.search('GRASS.*[0123456789.]+',text, re.IGNORECASE).group(0)
        grass_temp = re.findall('[0123456789.]+',grass_temp_text)
        print grass_temp
        min_hum_text = re.search('REL.*[0123456789.]+.*-',text, re.IGNORECASE).group(0)
        min_hum = re.findall('[0123456789.]+',min_hum_text)
        print min_hum
        max_hum_text = re.search('-.*[0123456789.]+.*PER',text, re.IGNORECASE).group(0)
        max_hum = re.findall('[0123456789.]+',max_hum_text)
        print max_hum
        rainfall_text = re.search('RAIN.*\n',text, re.IGNORECASE).group(0)
        rainfall = re.findall('[0123456789.]+|TRACE|trace|Trace',rainfall_text)
        print rainfall
        sun_text = re.search('DURA.*[0123456789.]+',text, re.IGNORECASE).group(0)
        sun = re.findall('[0123456789.]+',sun_text)
        print sun
        
        # try:
        #   sea_temp_text = re.search('SEA.*[0123456789.]+',text, re.IGNORECASE).group(0)
        #   sea_temp = re.findall('[0123456789.]+',sea_temp_text)
        #   print sea_temp_text
        #   print sea_temp
        # except:
        #   sea_temp = np.nan
        #   continue
        #   pass
        
        uv_text = re.search('UV INDEX.*\n.*INTEN', text, re.IGNORECASE).group(0)
        uv = re.findall('[0123456789.]+',uv_text)
        print uv
      
      except:
        text = np.nan

      


      f.write((timestamp + "," +
        max_temp[0] + "," +
        min_temp[0] + "," +
        grass_temp[0] + "," +
        max_hum[0] + "," +
        min_hum[0] + "," +
        rainfall[0] + "," +
        sun[0] + "," +
        # sea_temp[0] + "," +
        uv[0] + "," +
        "\n").encode("utf-8-sig"))
# Done getting data! Close file.
f.close()


#spans = HistoryTable.find_all(attrs={'class':'no-metars'})
      # col=[]
      # for row in HistoryTable.findAll("th"):
      #   col.append(row.text.strip())

      # for row in HistoryTable.findAll("tr")[1::2]:
      #   col = row.findAll("td")
      
      #   Time = col[0].string.strip()
      #   print Time

      

