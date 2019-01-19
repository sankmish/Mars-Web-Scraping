from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
import time

mars_scrape = {}

def scrape():
    url = "https://mars.nasa.gov/news"

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    slide = soup.find('li', class_="slide")
    news_title = slide.find('h3').text
    news_p = slide.find('div', class_="article_teaser_body").text

    mars_scrape['news_title'] = news_title
    mars_scrape['news_p'] = news_p

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(5)

    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find_all('div',class_="download_tiff")
    featured_image_url = 'https:' + image[1].a['href']

    mars_scrape['featured_image_url'] = featured_image_url

    url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html= browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('p', class_="tweet-text").text

    mars_scrape['mars_weather'] = mars_weather

    url= "http://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[0]

    df.set_index(0)
    df.columns = ['description','value']
    mars_facts = df.to_html(index=False)
    mars_facts.replace('\n', '')

    mars_scrape['mars_facts'] = mars_facts

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis","Valles"]
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = bs(html, 'html.parser')
        urls = soup.find('div', class_="downloads").find_all('li')
        img_url = urls[0].a['href']
        title = soup.find('title').text.split(' Enhanced')[0]
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
        browser.click_link_by_partial_text('Back')

    mars_scrape['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()
    
    return mars_scrape