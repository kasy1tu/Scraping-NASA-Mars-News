#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os 
import requests

def scrape_all():

# URL of page to be scraped 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    latest_title, latest_body = mars_news(browser)
    
    data = {
        "latest_title": latest_title,
        "latest_body": latest_body,
        "featured_image": featured_image,
        "facts": mars_fact,
        "hemispheres": hemisphere}
    
    browser.quit()
    return data
    
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        slides = soup.find_all('li', class_='slide')
        title = slides[0].find('div', class_ = 'content_title')
        latest_title = title.text.strip()
        body = slides[0].find('div', class_= 'article_teaser_body')
        latest_body = body.text.strip()
    except:
        return None, None 

    return latest_title, latest_body


def featured_image(browser):
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    images = soup.find_all('img', class_="headerimage fade-in")

    pic_src = []
    for image in images:
        pic = image['src']
        pic_src.append(pic)
        print(pic)

    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{pic}'
    
    return None 

def mars_fact():
    df = pd.read_html("https://space-facts.com/mars/")[0]
    df.columns=["Description", "Mars"]
    df.set_index("Description", inplace=True)
    df.to_html()
    return None

def hemisphere():
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)


    hemisphere_image_url = []

    # Get a list of all hemisphere
    links = browser.find_by_css("a.product-item h3")

    for index in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[index].click()
        
        try:
            sample_element = browser.links.find_by_text("Sample").first
            title = browser.find_by_css("h2.title").text
            link = sample_element["href"]

            hemisphere["title"] = title
            hemisphere["link"] = link

            hemisphere_image_url.append(hemisphere)
            browser.back()
        except:
            return hemisphere_image_url

