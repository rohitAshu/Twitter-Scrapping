import random
from django.conf import settings
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver as wiredriver
from webdriver_manager.chrome import ChromeDriverManager

class InitializeDriver:
    @staticmethod
    def _setup_options():
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Uncomment this line if you want to run in headless mode
        # Randomize window size
        width = random.randint(800, 1920)
        height = random.randint(600, 1080)
        window_size = f"{width},{height}"
        options.add_argument(f"--window-size={window_size}")
        print(f"Window Size: {window_size}")
        options.add_argument("--disable-third-party-cookies")
        # Generate a random user agent
        user_agent = UserAgent().random
        options.add_argument(f"--user-agent={user_agent}")
        print(f"User Agent: {user_agent}")
        return options

    def initialize_paid_proxy(self):
        options = self._setup_options()
        proxy_host = settings.PROXY_HOST
        proxy_port = settings.PROXY_PORT
        proxy_username = settings.PROXY_USERNAME
        proxy_password = settings.PROXY_PASSWORD
        selenium_wire_options = {
            'proxy': {
                'http': f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
                'https': f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chromedriver_path = ChromeDriverManager().install()
        service = Service(chromedriver_path)
        driver = wiredriver.Chrome(service=service, options=options, seleniumwire_options=selenium_wire_options)
        print('Paid proxy is Working')
        return driver

    def initialize_free_proxy(self):
        options = self._setup_options()
        chromedriver_path = ChromeDriverManager().install()
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print('Free proxy is Working')
        return driver
