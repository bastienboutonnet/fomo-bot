import urllib
import re
import json
import urllib2
from bs4 import BeautifulSoup

url = 'https://coinmarketcap.com/all/views/all/'
r = urllib.urlopen(url).read()
soup = BeautifulSoup(r, 'html.parser')
assets = soup.find_all("a", class_="currency-name-container")

asset_list = []
for i in range(len(assets)):
   asset_list.append(assets[i]['href'])

coins = []
for i in range(len(asset_list   )):
    coins.append(asset_list[i].split('/')[2])


reddits_urls = []
for i, coin in coins:
    # base_url = 'https://coinmarketcap.com/currencies/'+coin
    base_url = 'https://coinmarketcap.com/currencies/nxt/#markets'
    resp = urllib2.urlopen(base_url+'#markets')
    soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))
    exchanges = []
    for link in soup.find_all('a', href=True):
        if '/exchanges/' in link['href']:
            if link.split('/')[2] in ALLOWED_EXCHANGES:

    cur_url = 'https://coinmarketcap.com/'+'currencies/'+coin+'#social'
    base_url = 'https://coinmarketcap.com/currencies/nxt/#social'
    resp = urllib2.urlopen(base_url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))
    scripts = soup.find_all("script")
    for i in range(len(scripts)):
        cur_script = str(scripts[22].string)
        match = re.findall('https:\/\/www.reddit.com\/r\/\w+', cur_script)
        if match:
            social_url = match

    req = urllib2.Request(social_url+'/about.json')
    opener = urllib2.build_opener()
    f = opener.open(req)
    jason = json.loads(f.read())
    jason =


p = re.compile('https:\/\/www.reddit.com\/r\/\w+')
p = re.compile('(reddit)')
for script in soup.find_all("script"):
    if script:
        a = re.findall('https:\/\/www.reddit.com\/r\/\w+', scr[22].string)


#### Update Assets
# 1. Scape main page of CMC
# 2. Make list of coins
# for each coin :
## load page
## if #markets IN (SELECTED MARKETS)
## scrape social link for reddit
## append to list

### Grab Subscription Data
## go through list
## load about.json
## Save nb active subs

## Do some rendering somewhere