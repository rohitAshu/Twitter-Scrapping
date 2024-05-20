from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from django.http import JsonResponse
import json

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-third-party-cookies")

driver = webdriver.Chrome(options=options)
driver.get("https://twitter.com/i/flow/login")

sleep(3)
username = driver.find_element(By.XPATH, "//input[@name='text']")
username.send_keys("ExoticaLtd")
print("Username filled Successfully")

next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
next_button.click()
print("Next Clicked Successfully")

sleep(6)
password = driver.find_element(By.XPATH, "//input[@name='password']")
password.send_keys("S5Us3/)pT$.H#yy")

print("Password filled Successfully")

log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
log_in.click()
print("Log in clicked Successfully")

sleep(10)

explore_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div/div[2]/span")
explore_btn.click()
sleep(5)
tradding_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span")
tradding_btn.click()
sleep(5)

trending_elements = []
testid_value = "cellInnerDiv"
elements = driver.find_elements(By.XPATH, f'//*[@data-testid="{testid_value}"]')

trending_topics = []

for element in elements:
    text = element.text.split('\n')
    if len(text) >= 4:
        item = {
            "id": text[0].strip(),
            "category": text[2].split(' · ')[0].strip(),
            "type": text[2].split(' · ')[1].strip() if ' · ' in text[2] else "Trending",
            "trending": text[3].strip(),
            "posts": text[4].strip() if len(text) > 4 else "N/A"
        }
        trending_topics.append(item)

# Convert to JSON format
json_output = json.dumps(trending_topics, indent=4)

print(json_output)







