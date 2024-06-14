import random
import ipaddress
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent
import undetected_chromedriver as uc

def print_proxy_location(proxy_ip):
    """
    Prints the location information of the given proxy IP address.

    Parameters:
        proxy_ip (str): The IP address of the proxy.

    Returns:
        None

    Example:
        >>> print_proxy_location('203.0.113.1')
        # Output might vary depending on the actual location data retrieved.
        # Proxy IP Location: Country= United States , Region= California , City= San Francisco
    """
    # url = f"https://ip-api.com/{proxy_ip}/json"
    url = f"http://ipinfo.io/{proxy_ip}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(
            "Proxy IP Location: Country=",
            data.get("country"),
            ", Region=",
            data.get("region"),
            ", City=",
            data.get("city"),
        )
    else:
        print("Failed to retrieve location information for the proxy IP.")


def get_proxies():
    """
    Retrieves a list of proxy server IPs from a file.

    Returns:
        list: A list of proxy server IPs.
    """
    proxies = []
    for _ in range(10):
        proxies.append(".".join(str(random.randint(0, 255)) for _ in range(4)))
    print("proxies get_proxies : ", proxies)
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

    # driver = webdriver.Chrome(
    #     service=ChromeService(ChromeDriverManager().install()),
    #     options=options,
    # )
    driver = uc.Chrome(
        headless=True, use_subprocess=False
    )  # this is untective chrome driver
    # driver = uc.Chrome(use_subprocess=False)  # this is untective chrome driver
    driver.get("https://httpbin.org/ip")
    print(
        "-----------hhtpd://httpbin.org/ip"
    )
    print(driver.find_element(By.TAG_NAME, "body").text)
    driver.quit()


def initialize_driver():
    """
    Initializes a Selenium WebDriver with Chrome options including proxy,
    window size, and user agent.

    Returns:
        WebDriver: The initialized WebDriver object.

    Notes:
        This function utilizes a list of proxies obtained from `get_proxies()`
        function and selects one randomly.
        It then validates the selected proxy using `validate_proxies()` function.
        The WebDriver is configured with the selected proxy, randomized window size,
        and a random user agent.
        For headless operation, uncomment the line adding '--headless' argument.

    Example:
        >>> driver = initialize_driver()
        # This initializes a WebDriver with randomized window size, user agent, and a
        randomly selected validated proxy.
    """
    options = webdriver.ChromeOptions()
    print(f"Here is number of {len(get_proxies())} proxies.")
    validated_proxies = validate_proxies(get_proxies())
    print("Validated Proxies:", validated_proxies)
    random_proxy_ip = random.choice(validated_proxies)
    print("this proxy ip is used:", random_proxy_ip)
    # Proxy Functionality
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http = random_proxy_ip
    prox.httpProxy = random_proxy_ip
    prox.ssl_proxy = random_proxy_ip
    # zxcxz = print_proxy_location(random_proxy_ip)
    # return zxcxz
    options.add_argument(
        "--headless"
    )  # Uncomment this line if you want to run in headless mode
    # Randomize window size
    width = random.randint(800, 1920)
    height = random.randint(600, 1080)
    window_size = f"{width},{height}"
    options.add_argument(f"--window-size={window_size}")
    # Print the selected window size
    print(f"Window Size: {window_size}")

    options.add_argument("--disable-third-party-cookies")
    # Generate a random user agent
    user_agent = UserAgent().random
    options.add_argument(f"--user-agent={user_agent}")
    # Print the selected user agent
    print(f"User Agent: {user_agent}")
    driver = webdriver.Chrome(options=options)
    return driver


def generate_ipv4():
    """
    Generates a random IPv4 address.

    Returns:
        str: A string representing a random IPv4 address.

    Example:
        >>> ip_address = generate_ipv4()

        >>> print(ip_address)
        # Output may vary, e.g., '192.168.0.1'
    """
    print("-----------------------------------" * 88)
    return ".".join(str(random.randint(0, 255)) for _ in range(4))
