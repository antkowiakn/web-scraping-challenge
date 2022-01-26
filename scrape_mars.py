from cgitb import html
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_everything():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    #run everything to scrape all functions and then store in a dictionary
    data={
        "news_title": news_title,
        'news_paragraph' : news_paragraph,
        'image': image,
        'mars_facts': mars_facts
    }

    browser.quit()
    return data

def mars_news(browser):
    
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title=soup.find_all('div', class_='content_title')[0].text
    news_paragraph=soup.find_all('div', class_='article_teaser_body')[0].text


    return news_title, news_paragraph

def image(browser):
    url='https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    image_soup=BeautifulSoup(html, "html.parser")
    image=image_soup.find('img', class_='headerimage fade-in').get('src')
    featured_image_url= f'https://spaceimages-mars.com/{image}'
    return featured_image_url

def mars_facts(browser):
    facts_url='https://galaxyfacts-mars.com/'
    table=pd.read_html(facts_url)
    mars_fact_table=table[0]
    mars_fact_table.columns=["Description","Mars", "Earth"]
    mars_fact_table.set_index('Description', inplace=True)
    return mars_fact_table.to_html(classes="table table=striped")



if __name__=="__main__":
    print(scrape_everything())
