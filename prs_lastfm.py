from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from requests.exceptions import ConnectionError
from webdriver_manager.chrome import ChromeDriverManager
from urllib.error import URLError
import chromedriver_autoinstaller
import requests
import os


class lastfm_parser():
    def __init__(self, debug):
        ua = dict(DesiredCapabilities.CHROME)
        self.options = webdriver.ChromeOptions()
        if not debug:
            self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x935')
        self.ban_cymbols = ['#', '%', '&', '{', '}', '\\', '<', '>', '*',
                            '?', '/', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=']
        self.check_connection()
        
    def check_connection(self):
        try:
            chromedriver_autoinstaller.install(cwd=True)
            self.browser = webdriver.Chrome(options=self.options)
            self.browser.set_page_load_timeout(15)
            self.browser.get("https://www.google.com")
            self.connection = True
        except (ConnectionError, WebDriverException, URLError) as exc:
            # If ofline
            print(exc)
            with open('log.txt', 'w') as f:
                f.write(str(exc))
            self.connection = False
        return 1

    def get_track(self, track_name):
        url = "https://www.last.fm/ru/search?q=" + track_name
        try:
            self.browser.get(url)
        except TimeoutException:
            pass

        try:
            data = self.browser.find_element(
                By.XPATH, '//*[@id="mantle_skin"]/div[3]/div/div[1]/section[3]/table/tbody/tr[1]/td[5]/a').get_attribute('href')
            self.browser.get(data)
        except (NoSuchElementException, TimeoutException):
            return False
        try:
            artist_name = self.browser.find_element(
                By.XPATH, '//*[@id="mantle_skin"]/div[2]/div/div[2]/section/ol/li[1]/div/h3/a').text
            img_url = self.browser.find_element(
                By.XPATH, '//*[@id="mantle_skin"]/div[2]/div/div[2]/section/ol/li[1]/div/div/span/img').get_attribute('src')
            files = os.listdir('extra/imgs_recomended')
        except NoSuchElementException:
            return False

        for i in range(1, 4):
            artist_name = self.browser.find_element(
                By.XPATH, f'//*[@id="mantle_skin"]/div[2]/div/div[2]/section/ol/li[{i}]/div/h3/a').text
            img_url = self.browser.find_element(
                By.XPATH, f'//*[@id="mantle_skin"]/div[2]/div/div[2]/section/ol/li[{i}]/div/div/span/img').get_attribute('src')
            if artist_name + '.jpg' in files:
                continue
            break
        self.download_recomended((img_url, artist_name))
        return True

    def download_recomended(self, data):
        try:
            img = data[0]
            artist_name = data[1]
            image = requests.get(img)
            with open(f'extra/imgs_recomended/{self.delete_ban_cymbols(artist_name)}.jpg', 'wb') as f:
                f.write(image.content)
        except:
            pass

    def clear_page(self):
        self.browser.get('data:,')

    def delete_ban_cymbols(self, text):
        for c in self.ban_cymbols:
            text = text.replace(c, '')
        return text

    def quit_webdriver(self):
        self.browser.quit()
        return 1


if __name__ == '__main__':
    t1 = lastfm_parser(False)
    t1.get_track('Numb')
    input()

    'Cutting Crew - (I Just) Died In Your Arms (Official Music Video).jpg'