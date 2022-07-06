from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd

def crawl():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    d = webdriver.Chrome('C:/chromedriver.exe', chrome_options=options)

    d.get('https://playeternalreturn.com/stats?hl=ko-KR')
    d.implicitly_wait(3)
    x = d.find_element_by_tag_name('iframe')
    d.switch_to.frame(x)
    x = d.find_element_by_tag_name('iframe')
    d.switch_to.frame(x)
    d.page_source

    df = pd.read_html(d.page_source)[0]

    #df[0].to_csv('data.csv', encoding='cp949', index=False)
    d.quit()
    return df