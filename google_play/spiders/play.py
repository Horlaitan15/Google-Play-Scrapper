import scrapy
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyfiglet


def get_url(url, api_key):
    if len(api_key) != 0:
        payload = {'api_key': api_key, 'url': url, 'autoparse': 'true', 'country_code': 'in'}

        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    else:
        proxy_url = url

        assert isinstance(proxy_url, object)
    return proxy_url


def url_list():
    with open('urls.txt', 'r') as f:
        url = f.readlines()
    return list(eval((url[0])))


class ApiSpider(scrapy.Spider):
    name = 'play'

    def __init__(self, *args, **kwargs):
        super(
            ApiSpider, self
        ).__init__(*args, **kwargs)
        self.font = pyfiglet.figlet_format("Google Play Scraper", font='doh', width=200)
        print(self.font)
        self.key = []
        self.url = []

    # allowed_domains = ['x']
    # start_urls = ['http://httpbin.org/ip']

    allowed_domains = ['api.scraperapi.com', 'play.google.com']

    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
                       'RETRY_TIMES': 5}

    def start_requests(self):

        yield scrapy.Request(get_url(url_list()[0], api_key=''), callback=self.parse, meta={'pos': 0})

        # def get_links(link):
        #     driver = webdriver.Chrome()
        #     driver.maximize_window()
        #     driver.get(link)
        #     driver.implicitly_wait(10)
        #     SCROLL_PAUSE_TIME = 1
        #     # Get the end of the page.
        #     last_height = driver.execute_script("return document.body.scrollHeight")
        #     while True:
        #         # Scroll down the bottom of the page.
        #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #         time.sleep(SCROLL_PAUSE_TIME)
        #         new_height = driver.execute_script("return document.body.scrollHeight")
        #         if new_height == last_height:
        #             break
        #         last_height = new_height
        #     url_list = []
        #     try:
        #         try:
        #             urls = driver.find_elements(by=By.CSS_SELECTOR, value="div[role='listitem'] div div a")
        #         except AttributeError:
        #             urls = driver.find_elements(by=By.CSS_SELECTOR, value="div[role='listitem'] div div div a")
        #     except Exception as e:
        #         print('Failed')
        #     for url in urls:
        #         url_list.append(url.get_attribute('href'))

        #     with open("url.txt", 'w') as f:
        #         f.writelines(str(url_list))

        #     driver.close()

        # url = '&'.join(list(parameters['url']))
        # key = parameters['key']
        # print("---"*100)
        # print(url)
        # try:
        #     get_links(url)
        # except Exception as e:
        #     print(f"Failed: {e}")
        
        

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.select_one("h1[itemprop='name'] span").text
        try:
            company_name = soup.select_one(".Vbfug > a:nth-child(1) > span:nth-child(1)").text
        except AttributeError:
            company_name = "No name"
        try:
            developer_email = soup.select_one("div.VVmwY:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(2)").text
        except AttributeError:
            developer_email = 'No email'
        try:
            developer_website = soup.select_one("div.VVmwY:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(2)").text
        except AttributeError:
            developer_website = "No website found"
        try:
            developer_address = soup.select_one("div.VVmwY:nth-child(3) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(2)").text
        except AttributeError:
            developer_address = "No specified address"
        try:
            video = soup.select_one(".oiEt0d > source:nth-child(1)")['src']
        except:
            video = "No video attached"
        print(video)

        item = {'app_name': name, 'company_name': company_name, 'developer_email': developer_email, 'developer_website': developer_website, 'developer_address': developer_address, 'attached_video': video}

        yield item

        pos = 0
        for url in url_list()[1:]:
            print("--------"*30)
            print(item)
            print("Crawling: ", url)
            print("Finished crawling: ", url)
            print('\n')
            pos += 1

            yield scrapy.Request(get_url(url, ''), callback=self.parse, meta={'pos': pos})
