from selenium import webdriver
import random
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import concurrent.futures


def getProxies():
    """
    Fetches elite proxy servers from free-proxy-list.net.

    Returns:
        List of elite proxy servers in the format 'ip_address:port'.
    """
    try:
        r = requests.get("https://free-proxy-list.net/")
        r.raise_for_status()  # Raise HTTPError for bad status codes
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("tbody")
        proxies = []
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if columns[4].text.strip() == "elite proxy":
                proxy = f"{columns[0].text}:{columns[1].text}"
                proxies.append(proxy)
        return proxies
    except requests.RequestException as e:
        print("Error fetching proxies:", e)
        return []


def testProxy(proxy):
    """
    Tests the provided proxy by making a request to https://httpbin.org/ip.

    Args:
        proxy (str): The proxy server in the format 'ip_address:port'.

    Returns:
        str or None: The proxy server if it is working, otherwise returns None.
    """
    try:
        r = requests.get(
            "https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5
        )
        r.raise_for_status()  # Raises HTTPError if the response status code is >= 400
        return proxy
    except requests.exceptions.RequestException:
        return None


def rotateProxy(working_proxies):
    """
    Rotates to a random working proxy from the list and makes a request to http://httpbin.org/ip.

    Args:
        working_proxies (list): List of working proxy servers in the format 'ip_address:port'.

    Returns:
        None
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
    driver.get("http://httpbin.org/ip")
    print(driver.find_element(By.TAG_NAME, "body").text)
    driver.quit()

def initialize_driver():
    """
    Initialize a Chrome WebDriver with rotating proxies and a random user agent.

    Returns:
        webdriver.Chrome: A Chrome WebDriver instance.
    """
    proxies = getProxies()
    working_proxies = []
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(testProxy, proxies)
            working_proxies = [result for result in results if result is not None]

        num_working_proxies = len(working_proxies)
        print(f"Found {num_working_proxies} working proxies.")
        rotateProxy(working_proxies)

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
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-third-party-cookies")
    default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    user_agent = random.choice(user_agents) if user_agents else default_user_agent
    options.add_argument(f"--user-agent={user_agent}")
    driver = webdriver.Chrome(options=options)
    return driver





