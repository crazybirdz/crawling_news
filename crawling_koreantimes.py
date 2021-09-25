from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
path = '/home/ec2-user/environment/selenium/chromedriver'

driver = webdriver.Chrome(executable_path=path,options=options)
# driver.implicitly_wait(8)

def extract_news_urls(src):
    urls = []
    driver.get(src)
    # time.sleep(10)
    news_list = driver.find_elements_by_class_name('list_article_area')
    for news_element in news_list:
        url = news_element.find_element_by_css_selector('div.list_article_headline.HD > a').get_attribute('href')
        urls.append(url)
    # driver.close()
    return urls

def extract_by_content(limit, urls):
    content = ''
    split_news = '\n' + '---------------------------End----------------------------' + '\n'

    for idx, url in enumerate(urls):
        if idx + 1 == limit:
            break
        driver.get(url)
        driver.implicitly_wait(5)
        # news_title_en = driver.find_element_by_css_selector('div.list_article_headline.HD > a').text
        # news_title_kr = driver.find_element_by_css_selector('div.list_articleHDK.HD_kor > a').text
        # title = news_title_en + '\n' + news_title_kr
        
        # driver.click()
        # time.sleep(3)
        
        title_en = driver.find_element_by_css_selector('div.view_headline.HD').text
        title_kr = driver.find_element_by_css_selector('div.view_headlineK.HD_kor').text
        title = title_en + '\n' + title_kr
        
        news_text = driver.find_element_by_id('startts').text
        
        first_enter = news_text.find('\n')
        text = title + news_text[first_enter:]
        
        content += text + split_news

    return content
    
def get_koreantimes(num):
    URL = 'http://www.koreatimes.co.kr/www/sublist_743.html'
    urls = extract_news_urls(URL)
    content = extract_by_content(num, urls)
    driver.quit()
    return content