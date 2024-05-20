from selenium import webdriver
import random
import requests
import ipaddress

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import concurrent.futures


def get_proxies():
    """
    Retrieves a list of proxy server IPs from a file.

    Returns:
        list: A list of proxy server IPs.
    """
    proxies = []
    for _ in range(10):
        proxies.append(generate_ipv4())

    return proxies


def test_proxy(proxy):
    """
    Tests the provided proxy by making a request to https://httpbin.org/ip.

    Args:
        proxy (str): The proxy server in the format 'ip_address:port'.

    Returns:
        str or None: The proxy server if it is working, otherwise returns None.
    """
    try:
        # This will create an IPv4 or IPv6 object if the address is valid
        ip_obj = ipaddress.ip_address(proxy)
        return ip_obj
    except ValueError:
        return None


def rotate_proxy(working_proxies):
    """
    Rotates to a random working proxy from the list and makes a request to http://httpbin.org/ip.

    Args:
        working_proxies (list): List of working proxy servers in the format 'ip_address:port'.

    Returns:
        None
        :param working_proxies:
        :return:
    """
    if not working_proxies:
        print("No working proxies found.")
        return
    random_proxy = random.choice(working_proxies)
    print(f"Rotating to proxy: {random_proxy}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--proxy-server={random_proxy}")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )
    driver.get('https://httpbin.org/ip')
    print(driver.find_element(By.TAG_NAME, "body").text)
    driver.quit()


def initialize_driver():
    """
    Initialize a Chrome WebDriver with rotating proxies and a random user agent.

    Returns:
        webdriver.Chrome: A Chrome WebDriver instance.
    """
    proxies = get_proxies()
    # return  proxies
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(test_proxy, proxies)
            working_proxies = [result for result in results if result is not None]

        num_working_proxies = len(working_proxies)
        print(f"Found {num_working_proxies} working proxies.")
        rotate_proxy(working_proxies)

    except Exception as e:
        print("An error occurred during proxy testing:", e)
    try:
        with open('user_agents.txt', 'r') as file:
            user_agents = file.readlines()
    except Exception as e:
        print("Error reading user_agents.txt:", e)
    user_agents = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Uncomment this line if you want to run in headless mode
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-third-party-cookies')
    default_user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.212 Safari/537.36')
    user_agent = random.choice(user_agents) if user_agents else default_user_agent
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    return driver


def generate_ipv4():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))
