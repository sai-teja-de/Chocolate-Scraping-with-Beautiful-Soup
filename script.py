#Importing Libaries
import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#requesting 
layout = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html')

#scraping data with BeautifulSoup
soup= BeautifulSoup(layout.content,'html.parser')
#print(soup)

#getting all ratings into a list
list = soup.find_all(attrs={'class':'Rating'})
ratings=[]
for i in range(1,len(list)):
  x=list[i].get_text()
  ratings.append(float(x))

#ploting a histogram to know the ratings distribution
plt.hist(ratings)
plt.show()
plt.clf()

#getting all company names
tags = soup.select('.Company')
#print(tags)
company=[]
for i in range(1,len(tags)):
  y=tags[i].get_text()
  company.append(y)
#print(company)
#defining a dictionary of 2 list
d={'Company':company,'Ratings':ratings}

#converting dict to dataframe
df=pd.DataFrame.from_dict(d)
#print(df.head(10))

#Which companies produce the best rated bars
mean = df.groupby('Company').Ratings.mean().nlargest(10)
#print(mean)

#getting the percentage of Cocoa
coc=soup.select('.CocoaPercent')
cocoa_percents=[]
for td in coc[1:]:
  per=float(td.get_text().strip('%'))
  cocoa_percents.append(per)
#print(cocoa_percents)

#adding a col to df
df['CocoaPercentage']=cocoa_percents

#ploting a scatter plot to know the correlation btw cocoapercentage and ratings
plt.scatter(df.CocoaPercentage, df.Ratings)
z = np.polyfit(df.CocoaPercentage, df.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercentage, line_function(df.CocoaPercentage), "r--")
plt.show()

#getting origin and location details
origin = soup.select('.BroadBeanOrigin')
cocoa_grown=[]
for td in origin[1:]:
  cocoa_grown.append(td.get_text())

com_loc = soup.select('.CompanyLocation')
company_loc=[]
for td in com_loc[1:]:
  company_loc.append(td.get_text())
#adding these cols to df
df['Company_location']=company_loc
df['Cocoa_origin']=cocoa_grown

#Where are the best cocoa beans grown?
Best_cb = df.groupby('Cocoa_origin').Ratings.mean().nlargest(10)
print(Best_cb)
#Which companies produce best cocoa bars
Country_best=df.groupby('Company_location').Ratings.mean().nlargest(10)
print(Country_best)
