import random

from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
from seleniumwire import webdriver  # Import from seleniumwire
from webdriver_manager.chrome import ChromeDriverManager

# Proxy settings
proxy_host = 'rotating.proxyempire.io'
proxy_port = "9000"
proxy_username = "2RaXFoVTw0YID3Mi"
proxy_password = "mobile;;;;"


def initialize_driver():
    # Configure Chrome options
    options = Options()
    # options.add_argument(
    #     "--headless"
    # )  # Uncomment this line if you want to run in headless mode
    # Randomize window size
    width = random.randint(800, 1920)
    height = random.randint(600, 1080)
    window_size = f"{width},{height}"
    options.add_argument(f"--window-size={window_size}")
    # Print the selected window size
    print(f"Window Size: {window_size}")
    proxy_string = f"{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
    options.add_argument(f'--proxy-server=http://{proxy_string}')
    options.add_argument("--disable-third-party-cookies")
    options.add_argument('ignore-certificate-errors')
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    # Generate a random user agent
    user_agent = UserAgent().random
    options.add_argument(f"--user-agent={user_agent}")
    # Print the selected user agent
    print(f"User Agent: {user_agent}")
    # Configure Selenium Wire options for proxy authentication
    selenium_wire_options = {
        # 'proxy': {
        #     # 'http': f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
        #     # 'https': f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
        #     'no_proxy': 'localhost,127.0.0.1'
        # }
    }

    # Automatically download and set up ChromeDriver
    chromedriver_path = ChromeDriverManager().install()
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=selenium_wire_options)

    # driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=selenium_wire_options)
    return driver
