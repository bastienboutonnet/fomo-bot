import urllib
import re
import json
import urllib2
import pandas
import logging
import os
import click

from bs4 import BeautifulSoup
from parameters import ALLOWED_EXCHANGES



logging.basicConfig(level=logging.INFO)

def load_and_append_data(new_data, filename, output=False):
    if os.path.isfile('./data/'+filename+'.json'):
        past_data = pandas.read_json('./data/{}.json'.format(filename),
                                     orient='records')
        bigger_df = pandas.concat([past_data, new_data])
        bigger_df.to_json('./data/{}.json'.format(filename),
                          orient='records')
        if output:
            return bigger_df
    else:
        new_data.to_json('./data/{}.json'.format(filename),
                         orient='records')
@click.command()
@click.option('--restrict_markets/--no-restrict_markets', default=False)
@click.argument('limit', type=int)
@click.argument('db_file', type=str)
def main(restrict_markets, limit, db_file):
    logging.info('Getting assets list')
    url = 'https://coinmarketcap.com/all/views/all/'

    logging.info('Loading coinmarket asset list')
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')

    logging.info('Looking for asset URLs')
    assets = soup.find_all("a", class_="currency-name-container")

    asset_list = []
    logging.info('Making URL list')
    for i in range(len(assets)):
       asset_list.append(assets[i]['href'])

    logging.info('Extracting asset names from URL')
    coins = []
    for i in range(len(asset_list   )):
        coins.append(asset_list[i].split('/')[2])


    subscriptions_data = pandas.DataFrame()

    logging.info('Iterating Over Coins')
    if limit > 0:
        coins = coins[0:limit]
    n_coins = len(coins)
    coins_counter = 0
    for coin in coins:
        social_url = []
        coins_counter += 1
        base_url = 'https://coinmarketcap.com/currencies/'+coin
        logging.info('Getting markets for: {}'.format(coin.upper()))
        logging.info('Progress {0}/{1} coins'.format(coins_counter, n_coins))
        # base_url = 'https://coinmarketcap.com/currencies/nxt/#markets'
        resp = urllib2.urlopen(base_url+'#markets')
        soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))

        counter = 0
        exchange_list = []
        for link in soup.find_all('a', href=True):
            # if counter == 0: # TODO move this to write restriction as I still wanna create a list of exchanges.
            if '/exchanges/' in link['href']:
                logging.info('{0} available on {1}'.format(coin.upper(), link['href'].split('/')[2])) # FIXME: potentially will make logging too busy.
                exchange_list.append(link['href'].split('/')[2])
                # if restrict_markets: # TODO Move this logic in the analyser part.
                    # if link['href'].split('/')[2] not in ALLOWED_EXCHANGES:
                        # pass
                    # else:
                if exchange_list:
                    if counter == 0:
                        logging.info('Looking for Reddit link for: {}'.format(coin.upper()))
                        # cur_url = 'https://coinmarketcap.com/'+'currencies/'+coin+'#social'
                        # base_url = 'https://coinmarketcap.com/currencies/nxt/#social'
                        resp = urllib2.urlopen(base_url+'#social')
                        soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))
                        scripts = soup.find_all("script")
                        for i in range(len(scripts)):
                            cur_script = str(scripts[i].string)
                            match = re.findall('https:\/\/www.reddit.com\/r\/\w+', cur_script)
                            if match:
                                logging.info('link found')
                                logging.info(str(match))
                                social_url = match
                                counter += 1
        if len(social_url) > 0:
            logging.info('Loading reddit subscription data')
            req = urllib2.Request(social_url[0]+'/about.json', headers={'User-Agent': 'Mozilla/5.0'})
            opener = urllib2.build_opener()
            try:
                f = opener.open(req)
                jason = json.loads(f.read())
                if jason:
                    if 'data' in jason:
                        if 'subscribers' in jason['data']:
                            logging.info('subscribers found')
                            # TODO: Create entry for "supported vs non supported exchange? keep a list of exchanges?
                            small_df = pandas.DataFrame({'asset': coin,
                                                         'report_ts': pandas.to_datetime('now'),
                                                         'subscriptions': [jason['data']['subscribers']],
                                                         'exchanges': [set(exchange_list)]})
                            subscriptions_data = subscriptions_data.append(small_df)
                        else:
                            logging.info('no subscription data found')
            except urllib2.HTTPError:
                logging.info('something FUCKED up with {}'.format(social_url))
                pass
        else:
            logging.info('not on allowed exchange or so')
    # save stuff
    logging.info('saving to db')
    load_and_append_data(subscriptions_data, db_file)

if __name__ == '__main__':
    main()
