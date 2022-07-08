from selenium import webdriver
import pandas as pd
import os

def crawl():
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    d = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    
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