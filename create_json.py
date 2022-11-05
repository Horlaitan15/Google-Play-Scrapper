from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Booking(webdriver.Firefox):
    def __init__(self):
        super(Booking, self).__init__()

    # This is the first function that will get the booking.com homepage.
    def get_links(self, link):
        self.maximize_window()
        self.get(link)
        self.implicitly_wait(10)
        SCROLL_PAUSE_TIME = 1
        # Get the end of the page.
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down the bottom of the page.
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        url_list = []
        try:
            urls = self.find_elements(by=By.CSS_SELECTOR, value="div[role='listitem'] div div a")
        except:
            urls = self.find_elements(by=By.CSS_SELECTOR, value="div[role='listitem'] div div div a")
        for url in urls:
            url_list.append(url.get_attribute('href'))

        with open("urls.txt", 'w') as f:
            f.writelines(str(url_list))

        print("Done Scraping:", link)
        print(f"EXtracted {len(url_list)} links from {link}")

        self.close()

if __name__ == "__main__":
    url = input("Enter Google Play URL: ")
    scrape = Booking()
    scrape.get_booking_first_page(url)
