import random
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException



# List of user credentials
USER_CREDENTIALS = [
    {"username": "ExoticaLtd", "password": "S5Us3/)pT$.H#yy"},
    {"username": "kR4285512683720", "password": "Kr@200020"},
    {"username": "RakeshVerma", "password": "RakeshVerma@123"},
    # Add more user credentials as needed
]

def twitterLogin_auth(driver):
    """
       Perform Twitter login authentication.
       Returns:NoSuchElementException
           tuple: A tuple containing a boolean indicating success or failure of the login attempt,
                  and a string with a message indicating the outcome.
                  :rtype: object
       """
    # Select a random set of credentials
    credentials = random.choice(USER_CREDENTIALS)
    username_value = credentials['username']
    password_value = credentials['password']

    driver.get('https://twitter.com/i/flow/login')
    sleep(3)
    try:
        # username = driver.find_element(By.XPATH, "//input[@name='text']")
        # username.send_keys("ExoticaLtd")
        # print("Username element found and value sent successfully.")
        username = driver.find_element(By.XPATH, "//input[@name='text']")
        username.send_keys(username_value)
        print("Username element found and value sent successfully.")

        pass
    except NoSuchElementException:
        return False, "username E    Profile_name = serializers.CharField(required=True)lement not found"
    try:
        # next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        # next_button.click()
        # print("next_button element found and Next Clicked Successfully")
        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        next_button.click()
        print("Next button element found and clicked successfully.")
        sleep(6)
        pass
    except NoSuchElementException:
        return False, "next_button Element not found"
    try:
        # password = driver.find_element(By.XPATH, "//input[@name='password']")
        # password.send_keys("S5Us3/)pT$.H#yy")
        # print("Password element found and Password filled Successfully")
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys(password_value)
        print("Password element found and value sent successfully.")
    except NoSuchElementException:
        return False, "password Element not found"
    try:
        # log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
        # log_in.click()
        # print("log_in elecment is found  Log in clicked Successfully")
        log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
        log_in.click()
        print("Log in button found and clicked successfully.")
    except NoSuchElementException:
        return False, "log_in Element not found"
    return True, "Twitter Login Successfully"



