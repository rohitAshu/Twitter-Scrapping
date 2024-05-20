import random
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from .env


def twitterLogin_auth(driver):
    """
       Perform Twitter login authentication.
       Returns:NoSuchElementException
           tuple: A tuple containing a boolean indicating success or failure of the login attempt,
                  and a string with a message indicating the outcome.
                  :rtype: object
       """
    driver.get('https://twitter.com/i/flow/login')
    sleep(3)
    try:
        username = driver.find_element(By.XPATH, "//input[@name='text']")
        username.send_keys("d41972")
        print("Username element found and value sent successfully.")
        pass
    except NoSuchElementException:
        return False, "username Profile_name = serializers.CharField(required=True)lement not found"
    try:
        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        next_button.click()
        print("next_button element found and Next Clicked Successfully")
        sleep(6)
        pass
    except NoSuchElementException:
        return False, "next_button Element not found"
    try:
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys("syMpEntabLuTeRICNERYlaRmi")
        print("Password element found and Password filled Successfully")
    except NoSuchElementException:
        return False, "password Element not found"
    try:
        log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
        log_in.click()
        print("log_in elecment is found  Log in clicked Successfully")
    except NoSuchElementException:
        return False, "log_in Element not found"
    return True, "Twitter Login Successfully"
