from bs4 import BeautifulSoup
import urllib


url = 'https://www.ticketswap.nl/event/mano-le-tough-all-night-long-at-district-8-/e2d478bf-7586-4a09-8cb6-c0563ccf876d'
r = urllib.urlopen('https://www.ticketswap.nl/event/mano-le-tough-all-night-long-at-district-8-/e2d478bf-7586-4a09-8cb6-c0563ccf876d').read()
soup = BeautifulSoup(r, "html.parser")

print type(soup)

print soup.prettify()

available = soup.find_all("article", class_="listings-item")
available


r = urllib.urlopen('https://www.ticketswap.nl/event/nathan-fake-at-de-school/acf5d83f-c519-4bd6-a270-d75da89eda55').read()
soup = BeautifulSoup(r, "html.parser")

available = soup.find_all("article", class_="listings-item ")
# Unavailable listings listings-item  listings-item--not-for-sale
available

print soup.prettify()

r = urllib.urlopen('https://www.ticketswap.nl/event/white-lies/d71e18a0-ca8d-433f-946a-a2a0e10efb83').read()
soup = BeautifulSoup(r, "html.parser")

available = soup.find_all("article", class_="listings-item ")
available

# TODO:
# - Iterate through listings loaded in available (if more than one)
# - Iterate through metas and collect prices
# - Iterate through metas and collect quantities
# - Perform test, collect index of available that is best suited
# - collect href of suitable available.

metas = available[0].findAll('meta')

for meta in metas:
    if meta.get('itemprop') == "price":
        print meta.get('content')
