from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import xml.etree.ElementTree as ET

# Set up Chrome WebDriver
def scrape_twitter_data(Profile_name):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    # options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-third-party-cookies")


    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

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

    people = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span")
    people.click()
    sleep(5)
    print("Clicked on people Successfully !!")

    profile = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
    profile.click()
    sleep(5)
    print("Went on profile Man ")

    Usertags = []
    Timestamps = []
    Tweets = []
    Replys = []
    Retweets = []
    articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')

    while True:
        for article in articles:
            user_tag = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]").text
            Usertags.append(user_tag)
            print("done 1", user_tag)

            timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
            Timestamps.append(timestamp)
            print("done 2", timestamp)

            tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
            Tweets.append(tweet)
            print("done 3", tweet)

            reply = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
            Replys.append(reply)
            print("done 4", reply)

            retweet = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
            Retweets.append(retweet)
            print("done 5", retweet)

            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
            Tweets2 = list(set(Tweets))
            if len(Tweets2) > 5:
                break
        break

    # Create XML structure
    root = ET.Element("TwitterData")
    for i in range(len(Usertags)):
        tweet_elem = ET.SubElement(root, "Tweet")
        ET.SubElement(tweet_elem, "Name").text = Profile_name
        ET.SubElement(tweet_elem, "UserTag").text = Usertags[i]
        ET.SubElement(tweet_elem, "Timestamp").text = Timestamps[i]
        ET.SubElement(tweet_elem, "TweetContent").text = Tweets[i]
        ET.SubElement(tweet_elem, "Reply").text = Replys[i]
        ET.SubElement(tweet_elem, "Retweet").text = Retweets[i]

    # Create XML file
    tree = ET.ElementTree(root)
    tree.write("twitter_data.xml")

    driver.quit()
    return True

if __name__ == "__main__":
    Profile_name = input("Enter a reputed person's name: ")
    sleep(10)
    Profile = scrape_twitter_data(Profile_name)
    if Profile:
        print("Profile scraped and saved to twitter_data.xml successfully!")
    else:
        print("No Profile found or unable to scrape.")



# Narendra Modi