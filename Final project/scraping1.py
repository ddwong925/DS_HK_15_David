#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib2
import requests
from bs4 import BeautifulSoup
import pandas as pd


# proxies = {
#     'http': 'http://proxyap.inet.bloomberg.com:81',
#     'https': 'https://proxyap.inet.bloomberg.com:81'
#     }


# set cookie as showmetar = 1
r = requests.Session()
# path = 'C:\\cert\\BBrootNEW.cer'

metar = r.get('http://www.wunderground.com/cgi-bin/findweather/getForecast?setpref=SHOWMETAR&value=1')

mm_df = pd.DataFrame()

# Iterate through year, month, and day
for y in range(2000, 2001):
	for m in range(2, 3):
		for d in range(21,23):
 		
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
				continue
			elif (m == 2 and d > 28):
				continue
			elif (m in [4, 6, 9, 11] and d > 30):
				continue
			Datestamp = str(y)+'-'+str(m)+'-'+str(d)
			

			# Open wunderground.com url
			url = "http://www.wunderground.com/history/airport/VHHH/"+str(y)+ "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
			#url = "http://www.wunderground.com/history/airport/VHHH/2015/12/15/DailyHistory.html"
			page = r.get(url)

			# Get temperature from page
			soup = BeautifulSoup(page.text, "lxml")

			HistoryTable = soup.find('table', id='obsTable')
						
			labels = [] # all headers from wunderground
			columns = {} # all columns from all "tr"[1::2]
			columns2 = {} # all columns from all "tr"[2::2]
			master_df1 = pd.DataFrame()
			master_df2 = pd.DataFrame() # create a master df to store all the daily data
			master_df3 = pd.DataFrame()
			try:
				for label in HistoryTable.findAll("th"):
					labels.append(label.text.strip())
					
				for row in HistoryTable.findAll("tr")[1::2]:
					col = row.findAll("td")


					for i, v in enumerate(labels):
						data = []
						col_1 = col[i].text.strip()
						data.append(col_1)
						columns[labels[i]] = data
					df1 = pd.DataFrame([columns], columns=columns.keys())
					df1["Datestamp"] = Datestamp
					master_df1 = pd.concat([master_df1,df1])
					
						
				for row2 in HistoryTable.findAll("tr")[2::2]:
					data2 = []
					col2 = row2.findAll("td")

					col_2 = col2[1].text.strip()
					data2.append(col_2)

					columns2['Mlabels']=data2
					
					df2 = pd.DataFrame(columns2)
					
					master_df2 = pd.concat([master_df2,df2])
					
				
					# df1 = pd.DataFrame([columns], columns=columns.keys())
					# df1["Datastamp"] = Datestamp
				
				df3 = pd.concat([master_df1, master_df2], axis = 1)
				# -----------------------------------
				print "df3"
				print df3

				
				# master_df3 = pd.concat([master_df3,df3])
				# print "master_df3"
				# print master_df3
				# print "-----------------------------------------------"

				# mm_df = pd.concat([mm_df, master_df3])
				# print Datestamp
			except:
				print "No Data"			
				continue
				pass

			
				# print mm_df
		master_df3.to_csv ('Results.csv', encoding='utf-8-sig')
				# mm_df.to_csv ('Results.csv', encoding='utf-8-sig')
