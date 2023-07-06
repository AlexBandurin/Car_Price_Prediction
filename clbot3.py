from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
import time
from time import sleep
import requests
import random
from random import randint
from selenium.webdriver.common.by import By
import re
import math

data = []
links = []
page_soups = []
car_details = []
cars = []
soups = []
car_dicts = []
rc = np.random.randint(10,20,[40])/15
rc2 = np.random.randint(40,100,[40])/55
dfs = pd.DataFrame()

order = ['Vehicle info','Vehicle info 2','Price','Cylinders','City','Condition','Odometer','Paint Color','Time',\
          'Title Status','Drive','Fuel','Transmission', 'Description', 'Type', 'Size','Lat','Long','Date','pID']

items = ["condition:","cylinders:","drive:","odometer:","paint color:","title status:","transmission:","fuel:","type:", "size:"]

def list_to_dict(rlist):
    return dict(map(lambda s : map(str.strip, s.split(':')), rlist))

class clbot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_num_pages(self):
        self.driver.get(link_root + "0~0") 
        sleep(1.2)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        page_info = soup.find('span', class_="cl-page-number").text
        posts_per_page_start = page_info.find('-') + 2
        posts_per_page_end = page_info.find('of') - 1
        num_of_posts_index = page_info.find('of') + len('of') + 1
        #print(posts_per_page_start, '---', posts_per_page_end)
        posts_per_page = int(page_info[posts_per_page_start:posts_per_page_end])
        #print(posts_per_page)
        num_of_posts = int(page_info[num_of_posts_index:].replace(',',''))
        pages = math.ceil(num_of_posts/posts_per_page)

        return pages

    def get_links(self):
        global links
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # posts = soup.find_all('a', class_= 'titlestring')
        
        # for i in posts:
        #     l = i.get('href')
        #     links.append(l)

        page_links = [element.get('href') for element in soup.select('.cl-search-result.cl-search-view-mode-list a.cl-app-anchor.text-only.posting-title')]
        #print(page_links)
        links += page_links
        return links

def parsing(links):
    cnt = 0
    global dfs
    descriptions = []
    
    for c,link in enumerate(links):  
            description = []
            cnt += 1
            if cnt % 20 == 0:
                print('count # -> ',cnt)
            if c!=0 and c % 250 == 0:
                print('sleeping')
                sleep(7)
                print('resuming')
            try:
                clean = []
                car_details = []
                # make HTTP requests
                each_page = requests.get(link)
                break_out_flag1 = False
                break_out_flag2 = False
                # The sleep function can help you to avoid the server to be overloaded with too many requests in a very short period of time.
                sleep(random.choice(rc))

                # store the BeautifulSoup object in a variable
                page_soup = BeautifulSoup(each_page.content, 'html.parser')
                soups.append(page_soup)
                url = link.strip()
                start = url.find("//") + len("//")
                end = url.find(".")
                city_name = url[start:end]
                # append city name
                car_details.append('City: ' + city_name.title())
                # append date
                car_details.append('Date: ' + page_soup.find('time', class_="date timeago").text.strip()[:-6])
                # append time
                car_details.append('Time: ' + page_soup.find('time', class_="date timeago").text.strip().replace(':',';')[-5:])
                # append lattitude
                geos = page_soup.findAll("div", {"class": "mapbox"})
                lat = geos[0].contents[1].get('data-latitude')
                car_details.append("Lat: " + lat.strip())
                # append longitude
                long = geos[0].contents[1].get('data-longitude')
                car_details.append("Long: " + long.strip())
                # append price
                car_details.append("Price: " + page_soup.find('span', class_="price").text.replace(',','').replace('$',''))

                # append posting descriptions
                for i in np.arange(2,500,2):
                    try:
                        section = page_soup.find(attrs={'id' : 'postingbody'}).contents[i]
                        if section is not None and isinstance(section, str):
                            section = section.strip()
                            description.append(re.sub("[^0-9a-zA-Z!\"#$%&'()*+,./;<=>?@[\\]^_`{|}~]", " ", section))
                            description.append(' ')

                    except IndexError:
                        break          
                car_details.append("Description: " + ''.join(description))  

                for c,i in enumerate(page_soup.find_all('span', recursive=True)):  
                    symbol_tracker1 = False
                    symbol_tracker2 = False
                    for j in items:
                        if (j.lower() in i.text.lower()):
                            car_details.append(i.text.title())

                    if c == 20:
                    #if (16 > c > 13) and ('tesla' in i.text.lower()):
                        #print(i.text)
                        vehicle_info = i.text
                        for i in vehicle_info:
                            if i == ':' or i == '' or i == '':
                                symbol_tracker1 = True
                                car_details.append("Vehicle info: ~")
                                
                        if symbol_tracker1 == False:
                            car_details.append("Vehicle info: " + re.sub("[^0-9a-zA-Z]+", " ", vehicle_info).title())

                    if c == 14:
                    #if (22 > c > 15) and ('tesla' in i.text.lower()):
                        #print(i.text)
                        vehicle_info2 = i.text
                        for i in vehicle_info2:
                            if i == ':' or i == '' or i == '':
                                symbol_tracker2 = True
                                car_details.append("Vehicle info 2: ~")
                            
                        if symbol_tracker2 == False:
                            car_details.append("Vehicle info 2: " + re.sub("[^0-9a-zA-Z]+", " ", vehicle_info2).title())

                car_details.append('pID:' + link.strip().replace('html','').replace('.','').split('/')[-1])
                car_dicts.append(list_to_dict(car_details))  

            except: 
                #print('exception found')
                pass
            
    #print(len(car_dicts))
    for item in car_dicts:
        df = pd.DataFrame.from_dict(item,orient='index').transpose()
        # concatenate each new df from the loop into the parent df
        dfs = pd.concat([dfs,df], axis=0, ignore_index=True, sort=True)
        # save to a csv file

# Execution:
        
bot = clbot()
sleep(1)

#link_root = "https://chicago.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://newyork.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://losangeles.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://dallas.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://phoenix.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://seattle.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://sfbay.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://miami.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://sandiego.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://portland.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://denver.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #20
#link_root = "https://minneapolis.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://tampa.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://sacramento.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #20
#link_root = "https://inlandempire.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://newjersey.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #20
#link_root = "https://detroit.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://longisland.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://charlotte.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://nh.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://fortmyers.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://denver.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://boston.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"
#link_root = "https://orangecounty.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~0~0"
#link_root = "https://atlanta.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #21
#link_root = "https://houston.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #20
#link_root = "https://austin.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~" #20
#link_root = "https://detroit.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~0~0" #21
link_root = "https://lasvegas.craigslist.org/search/cta?bundleDuplicates=1&purveyor=owner#search=1~list~"

pages = bot.get_num_pages()
#pages = 1
sleep(0.7)

#collect post url's for every page
for page_number in range(pages):
    bot.driver.get(link_root + str(page_number) + "~0")
    sleep(random.choice(rc2))
    bot.get_links()
    sleep(random.choice(rc2))    
bot.driver.quit()    
sleep(2)
print(len(links))
sleep(1)
#parse page contents and save df to csv
parsing(links)
#print(dfs.columns)
dfs = dfs.loc[:,order]\
    
dfs.to_csv('car_data-LasVegas_.csv',index = False)
