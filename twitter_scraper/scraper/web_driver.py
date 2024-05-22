import ipaddress
import random
from fake_useragent import UserAgent
from selenium import webdriver


def get_proxies():
    """
    Retrieves a list of proxy server IPs from a file.

    Returns:
        list: A list of proxy server IPs.
    """
    proxies = []
    for _ in range(10):
        proxies.append('.'.join(str(random.randint(0, 255)) for _ in range(4)))
    return proxies


def validate_proxies(proxies):
    """
    Validate a list of proxy server IPs.

    Parameters:
        proxies (list): A list of proxy server IPs to validate.

    Returns:
        list: A list of validated proxy server IPs.
    """
    validated_proxies = []
    for proxy in proxies:
        if validate_proxy(proxy):
            validated_proxies.append(proxy)
    return validated_proxies


def validate_proxy(proxy):
    """
    Validate a proxy server IP.

    Parameters:
        proxy (str): The proxy server IP to validate.

    Returns:
        bool: True if the proxy is valid, False otherwise.
    """
    try:
        # This will create an IPv4 or IPv6 object if the address is valid
        ip_obj = ipaddress.ip_address(proxy)
        return ip_obj.version == 4
    except ValueError:
        return False


def initialize_driver():
    """
    Initialize a Chrome WebDriver with proxy settings and additional options.
    Returns:
        webdriver.Chrome: A Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    print(f"Here is number of  {len(get_proxies())}  proxies.")
    validated_proxies = validate_proxies(get_proxies())
    print("Validated Proxies:", validated_proxies)
    random_proxy_ip = random.choice(validated_proxies)
    print("this proxy ip is used:", random_proxy_ip)
    options.add_argument('--headless')  # Uncomment this line if you want to run in headless mode
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-third-party-cookies')
    options.add_argument(f'--user-agent={UserAgent().random}')
    driver = webdriver.Chrome(options=options)
    return driver


def generate_ipv4():
    """
    Generate a random IPv4 address.

    Returns:
        str: A string representing a random IPv4 address in the format 'x.x.x.x',
             where each 'x' is an integer between 0 and 255.
    """
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))
