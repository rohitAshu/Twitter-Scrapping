from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from time import sleep
import json
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
    # Add more User-Agent strings as needed
]


# Set up Chrome WebDriver
def scrape_twitter_data(Profile_name):
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.3112.50 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-third-party-cookies")
    random_user_agent = random.choice(user_agents)
    options.add_argument(f"--user-agent={random_user_agent}")

    # options.add_argument('--disable-web-security')
    # options.add_argument('--disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure')

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

    sleep(16)

    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")

    search_box.send_keys(Profile_name)
    search_box.send_keys(Keys.ENTER)
    print("Entered the subject and clicked Successfully !!")
    sleep(3)

    people = driver.find_element(By.XPATH,
                                 "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span")
    people.click()
    sleep(5)
    print("Clicked on people Successfully !!")

    profile = driver.find_element(By.XPATH,
                                  "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
    profile.click()
    sleep(5)
    print("Went on profile Man ")

    data = []
    articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')

    while True:
        for article in articles:
            user_tag = driver.find_element(By.XPATH,
                                           "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]").text
            print("done 1", user_tag)

            timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
            print("done 2", timestamp)

            tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
            print("done 3", tweet)

            # reply = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
            # reply = driver.find_element(By.XPATH, ".//div[@data-testid='reply']").text
            reply = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
            print("done 4", reply)

            retweet = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
            print("done 5", retweet)

            data.append({
                "Name": Profile_name,
                "UserTag": user_tag,
                "Timestamp": timestamp,
                "TweetContent": tweet,
                "Reply": reply,
                "Retweet": retweet
            })

            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
            if len(data) > 5:
                break
        break

    # Save data to JSON file
    with open(f"{Profile_name}.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    driver.quit()
    return True


if __name__ == "__main__":
    Profile_name = input("Enter a reputed person's name: ")
    sleep(10)
    Profile = scrape_twitter_data(Profile_name)
    if Profile:
        print("Profile scraped and saved to twitter_data.json successfully!")
    else:
        print("No Profile found or unable to scrape.")

# Narendra Modi
