

import requests
def getProxies():
    """
    Fetches elite proxy servers from free-proxy-list.net.

    Returns:
        List of elite proxy servers in the format 'ip_address:port'.
    """
    r = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("tbody")
    proxies = []
    for row in table.find_all("tr"):
        columns = row.find_all("td")
        if columns[4].text.strip() == "elite proxy":
            proxy = f"{columns[0].text}:{columns[1].text}"
            proxies.append(proxy)
    return proxies