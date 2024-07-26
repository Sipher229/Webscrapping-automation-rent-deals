from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

load_dotenv()

FORM = os.getenv('FORM')

markup = requests.get('https://appbrewery.github.io/Zillow-Clone/').text

soup = BeautifulSoup(markup, features='html.parser')

address_list = soup.findAll(name='address')
address_list = [address.getText().strip() for address in address_list]
links = soup.findAll(name='a', class_="StyledPropertyCardDataArea-anchor")
links = [link.get('href') for link in links]
prices = soup.findAll(name='span', class_='PropertyCardWrapper__StyledPriceLine')
prices = [price.getText().strip() for price in prices]

data = []

for i in range(len(address_list)):
    data_item = {'address': address_list[i], 'price': prices[i], 'link': links[i]}
    data.append(data_item)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(FORM)

for data_packet in data:
    address_input = driver.find_element(By.CSS_SELECTOR, '.KHxj8b')
    link_input = driver.find_elements(By.CSS_SELECTOR, '.KHxj8b')[1]
    price_input = driver.find_element(By.CSS_SELECTOR, '.whsOnd')
    submit_button = driver.find_element(By.CSS_SELECTOR, '.l4V7wb')

    address_input.click()
    address_input.send_keys(data_packet['address'])

    price_input.click()
    price_input.send_keys(data_packet['price'])

    link_input.click()
    link_input.send_keys(data_packet['link'])

    submit_button.click()
    time.sleep(2)
    submit_other_response = driver.find_element(By.CSS_SELECTOR, '.c2gzEf a')
    submit_other_response.click()
    time.sleep(2)




