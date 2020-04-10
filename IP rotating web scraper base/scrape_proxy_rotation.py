from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

ua = UserAgent()  # From here we generate a random user agent
proxies = []  # Will contain proxies [ip, port]

# Main function
def main():
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    print(len(proxies))
    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    for n in range(1, 500):
        req = Request('http://icanhazip.com')
        req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        target = Request('ADDRESS HERE')
        target.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

        try:
            # my_ip = urlopen(req).read().decode('utf8')
            # print('#' + str(n) + ': ' + my_ip)

            # target_contents = urlopen(target).read().decode('utf8')
            # print('#' + str(n) + ': ' + target_contents)

            proxy_string = proxy['ip'] + ':' + proxy['port']
            print('#' + str(n) + ' attempted IP: ' + proxy_string)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % proxy_string)
            chrome = webdriver.Chrome(options=chrome_options, executable_path=r'CHROMEDRIVER PATH')
            chrome.get("ADDRESS HERE")
            print("fetch completed")
            time.sleep(3)
            chrome.close()

            proxy_index = random_proxy()
            proxy = proxies[proxy_index]
        except:  # If error, delete this proxy and find another one
            del proxies[proxy_index]
            print('#' + str(n) + ': ' + 'Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
    return random.randint(0, len(proxies) - 1)

if __name__ == '__main__':
    main()
