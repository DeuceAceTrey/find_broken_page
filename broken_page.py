import undetected_chromedriver.v2 as webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    if(__name__ == '__main__'):
        url = 'https://infinityyachts.com/search/'
        print(url)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options,use_subprocess = True)
        driver.delete_all_cookies()

        print("*---Moving into website---*")

        driver.get(url)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(15)
        print("---Loading all boat pages---")
        boat_links = []
        while(True):
            try:
                driver.find_element(By.ID,"load-more-boats").click()
            except:
                break
            sleep(10)

        print("---Loading complete---")
        boat_links = driver.find_elements("xpath","//a[text()='View Yacht']")
        i = 0
        hrefs = []
        broken_pages = []
        for link in boat_links:
            hrefs.append(link.get_attribute('href'))

        df = pd.DataFrame({'urls' : hrefs})
        writer = pd.ExcelWriter('links.xlsx',engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Sheet1')
        writer.save()
        broken_pages = []
        for href in hrefs:    
            try:
                print("Checking page " + href)
                driver.get(href)
                sleep(2)
                text = driver.find_element('xpath','//h4[text()="Gallery"]').text
                print(text + "FOUND")
            except:
                broken_pages.append(href)
                print("##**** Broken page found : " +href)
        
        print("***Broken pages found : ")
        for bp in broken_pages:
            print(bp)
        df = pd.DataFrame({'urls' : broken_pages})
        writer = pd.ExcelWriter('broken_pages.xlsx',engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Sheet1')
        writer.save()


main()