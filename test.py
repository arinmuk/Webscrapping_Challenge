
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import textwrap
import pymongo
import datetime as datetime
#import requests
from splinter import Browser
#from bs4 import BeautifulSoup
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
executable_path = {"executable_path": "chromedriver"}
browser=Browser("chrome", **executable_path, headless=False)


#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
def scrape():
        mars_data={}
        conn = 'mongodb://localhost:27017'
        client = pymongo.MongoClient(conn)
        db = client.mars_data
        mars_scrape_col = db.mars_scrape.find()
        mars_data["scrape_time"]=str(datetime.datetime.now())
        url1='https://mars.nasa.gov/news/'
        browser.visit(url1)
        browser.is_element_present_by_id("grid_gallery module list_view", 1)
        html = browser.html
        news_soup = BeautifulSoup(html, "html.parser")
        print(news_soup.prettify())
        results1 = news_soup.find_all('div', class_="content_title")
        #results = soup.find_all('section', class_="grid_gallery module list_view")
        results1
        news_headlines=[]
        for newst in results1:
            news_headlines.append(newst.text)
            #print(newst.text)
        news_headlines
        print(news_headlines[0])
        mars_data["news_title"] = news_headlines[0]
        results = news_soup.find_all('div', class_="image_and_description_container")
        results
        title=[]
        description=[]
        for result in results:
            # Error handling
            try:
                # Identify and return title of listing
                #desc = result.find('div', class_="rollover_description_inner").text
                desc = result.find('div', class_="rollover_description_inner").text
                # Identify and return price of listing
                title.append(result.a["href"])
                description.append(desc)

                # Print results only if title, price, and link are available
            
            except AttributeError as e:
                print(e)
        #print(title[0])
        print(description[0])
        print(news_headlines[0])
        news_headlines

        mars_data["news_det"] = description[0]




        ##*************************************
        url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        part_urlstr='https://www.jpl.nasa.gov'
        response = requests.get(url2)
        soup2 = BeautifulSoup(response.text, 'html.parser')
        #img_res= soup2.find_all('a', class_="fancybox")
        img_res= soup2.find_all('li', class_="slide")
        img_res
        #img_res= soup2.find_all('div', class_="img")
        #img_res
        pic=[]
        for data in img_res:
            #print(data.a["data-fancybox-href"])
            try:
                pic.append(data.a["data-fancybox-href"])
            except:
                print("done")
        picture_url='https://www.jpl.nasa.gov' + pic[0]
        print(picture_url) 
        mars_data["picture_url"]=picture_url
        url3='https://twitter.com/marswxreport?lang=en'
        part_urlstr='https://twitter.com/marswxreport?lang=en'
        response = requests.get(url3)
        soup3 = BeautifulSoup(response.text, 'html.parser')
        mars_wea= soup3.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        mwea=[]
        for wea_res in mars_wea:
            
            #print(wea_res.text)
            #print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            #if(search_string in wea_res.text ):
                #weather_data=wea_res.text
            mwea.append(wea_res.text)
        weather_mars=mwea[0]    
        str_remove=weather_mars.find('pi')
        #str_len=len(weather_data)
        #cutoff= str_len-str_len
        #print(str_remove)
        #print(str_len)
        #print(cutoff)
        weather_data = weather_mars[:str_remove]
        print(weather_data)
        mars_data["weather"]=weather_data
        url4='https://space-facts.com/mars/'
        table= pd.read_html(url4)
        df = table[0]

        #df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons','Orbit Distance', 'Orbit Period', 'Surface Temperature ', 'First Record','Recorded By']
        df=df.rename(columns={0:'description',1:'value'})
        df=df.set_index('description')
        #print(list(df.columns))
        #df.head(9)
        html_table = df.to_html()
        #html_table
        mars_data["fact_html"]=html_table
        url5='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        suburl5='https://astrogeology.usgs.gov'
        response = requests.get(url5)
        soup5 = BeautifulSoup(response.text, 'html.parser')
        hemis_pic= soup5.find_all('a', class_="itemLink product-item")
        hemisphere_image_urls=[]
        dict_build={}
        for results in hemis_pic:
                dict_build={}
                txt_fix=results.text
                rmv_string=txt_fix.find("Enhance")
                picture_title=txt_fix[:rmv_string]
                dict_build["title"]=picture_title
                
                #print(dict_build)
                hemisphere_image_urls.append(dict_build)
                url7=suburl5+results["href"]
                response = requests.get(url7)
                soup7 = BeautifulSoup(response.text, 'html.parser')
                #print(soup7.prettify())
                grab_pic= soup7.find_all('img', class_="wide-image")
                #grab_pic
                for pic in grab_pic:
                    #print(pic["src"])
                    imgtext=pic["src"]
                dict_build["img_url"]=suburl5+imgtext
        if hemisphere_image_urls==[]:
                hemisphere_image_urls = [
                            {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
                            {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
                            {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
                            {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
                            ]
        hemisphere_image_urls        
        mars_data['hemisphere']=hemisphere_image_urls
        db.mars_scrape.update({},mars_data,upsert=True)
        return mars_data

scrape()