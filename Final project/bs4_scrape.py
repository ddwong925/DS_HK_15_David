import urllib2
import requests
from bs4 import BeautifulSoup
 
# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('wunder-data.txt', 'w')

# set cookie as showmetar = 1
r = requests.Session()
metar = r.get('http://www.wunderground.com/cgi-bin/findweather/getForecast?setpref=SHOWMETAR&value=1')

# Iterate through year, month, and day
for y in range(2000, 2001):
  for m in range(5, 13):
    for d in range(1, 32):
 
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
      #elif (m in [1,3,5,7,8,10,12] and d >31):
        #continue
 

      # Open wunderground.com url
      url = "http://www.wunderground.com/history/airport/VHHH/"+str(y)+ "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
      page = r.get(url)
      
 
      # Get temperature from page
      soup = BeautifulSoup(page.text, "lxml")

      HistoryTable = soup.find('table', id='obsTable')
# spans = HistoryTable.find_all(attrs={'class':'no-metars'})

      col = []
      for row in HistoryTable.findAll("th")
        col.append(row.text.strip())

      for row in HistoryTable.findAll("tr")[1::2]:
        col = row.findAll("td")
      
        Time = col[0].string.strip()
        Temp = col[1].text.strip()
        

        Dew_point = col[2].text.strip()
        Humidity = col[3].text.strip()
        Pressure = col[4].text.strip()
        Visibility = col[5].text.strip()
        Wind_Dir = col[6].text.strip()
        Wind_Speed = col[7].text.strip()
        Gust_Speed = col[8].text.strip()
        Precip = col[9].text.strip()
        Events = col[10].text.strip()
        Conditions = col[11].text.strip()

      for row in HistoryTable.findAll("tr")[2::2]:
        col = row.findAll("td")
        Metar = col[1].text.strip()
 
      # Format month for timestamp
        if len(str(m)) < 2:
          mStamp = '0' + str(m)
        else:
          mStamp = str(m)
   
        # Format day for timestamp
        if len(str(d)) < 2:
          dStamp = '0' + str(d)
        else:
          dStamp = str(d)
   
        # Build timestamp
        timestamp = str(y) + mStamp + dStamp
        print timestamp
	  
	  # Write timestamp and temperature to file
        f.write((timestamp + "," +
          Time + "," +
          Temp + "," +
          Dew_point + "," +
          Humidity + "," +
          Pressure + "," +
          Visibility + "," +
          Wind_Dir + "," +
          Gust_Speed + "," +
          Precip + "," +
          Events + "," +
          Conditions + "," +
          Metar + "," +
          "\n").encode("utf-8-sig"))
# Done getting data! Close file.
f.close()
