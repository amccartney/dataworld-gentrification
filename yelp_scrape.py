from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import csv
from passwords import *


auth = Oauth1Authenticator(
    consumer_key=YELP_CONSUMER_KEY,
    consumer_secret=YELP_CONSUMER_SECRET,
    token=YELP_TOKEN,
    token_secret=YELP_TOKEN_SECRET
)

client = Client(auth)

class YelpSearchScraper(object):

    def scrape_records(self, zip_code, category, offset):
        params = {
            'offset': offset,
            'category_filter': category
        }

        response = client.search(zip_code, **params)

        return response

    def write_csv(self, city, city_name):

        categories = [
            'vegan',
            'organic_stores',
            'juicebars',
            'kombucha',
            'coffee',
            'bikeparking',
            'climbing',
            'cyclingclasses',
            'barreclasses',
            'bootcamps',
            'gyms',
            'pilates',
            'yoga',
            'dog_parks',
            'skate_parks',
            'galleries',
            'musicvenues',
            'paintandsip',
            'bodyshops',
            'autopartssupplies',
            'autoloanproviders',
            'autocustomization',
            'carshares',
            'barbers',
            'blowoutservices',
            'hairstylists',
            'tattoo',
            'privateschools',
            'cheesetastingclasses',
            'winetasteclasses',
            'testprep',
            'breweries',
            'bubbletea',
            'empanadas',
            'distilleries',
            'coffeeroasteries',
            'intlgrocery',
            'healthmarkets',
            'cannabis_clinics',
            'doulas',
            'halfwayhouses',
            'cannabisreferrals',
            'oxygenbars',
            'publicart',
            'homelessshelters',
            'foodbanks',
            'bars',
            'beergardens',
            'mobileparks',
            'cafes',
            'breakfast_brunch',
            'mexican',
            'bespoke',
            'cannabisdispensaries',
            'discountstore',
            'vintage',
            'guns_and_ammo',
            'pawn',
            'bikes',
            'thrift_stores'
            ]

        writer = csv.writer(open(city_name + '.csv','wb'))
        header = ['genre','category','id']
        writer.writerow(header)

        for category in categories:
            for zip_code in city:

                print "Scraping " + category + " from " + str(zip_code)

                for offset in range (0,280,20):

                    response = self.scrape_records(zip_code, category, offset)

                    for business in response.businesses:
                        writer.writerow([ category, business.id.encode("utf-8") ])

if __name__ == "__main__":

    search_scraper = YelpSearchScraper()

    sf_zip_codes = [94102,94103,94104,94105,94107,94108,94109,94110,94111,94112,94114,94115,94116,94117,94118,94121,94122,94123,94124,94127,94129,94130,94131,94132,94133,94134,94158]
    bklyn_zip_codes = [11201,11204,11206,11208,11210,11212,11214,11216,11218,11220,11222,11224,11226,11229,11231,11233,11235,11237,11239,11203,11205,11207,11209,11211,11213,11215,11217,11219,11221,11223,11225,11228,11230,11232,11234,11236,11238]
    portland_zip_codes = [97034,97035,97080,97086,97201,97202,97203,97204,97205,97206,97208,97209,97210,97211,97212,97213,97214,97215,97216,97217,97218,97219,97220,97221,97222,97223,97225,97227,97229,97230,97231,97232,97233,97236,97239,97266]
    austin_zip_codes = [78610,78613,78617,78641,78652,78653,78660,78664,78681,78701,78702,78703,78704,78705,78712,78717,78719,78721,78722,78723,78724,78725,78726,78727,78728,78729,78730,78731,78732,78733,78734,78735,78736,78737,78738,78739,78741,78742,78744,78745,78746,78747,78748,78749,78750,78751,78752,78753,78754,78756,78757,78758,78759]
    oakland_zip_codes = [94577,94601,94602,94603,94605,94606,94607,94608,94609,94610,94611,94612,94613,94618,94619,94621,94704,94705]

    search_scraper.write_csv(sf_zip_codes, 'sanfrancisco')
    search_scraper.write_csv(bklyn_zip_codes, 'brooklyn')
    search_scraper.write_csv(portland_zip_codes, 'portland')
    search_scraper.write_csv(austin_zip_codes, 'austin')
    search_scraper.write_csv(oakland_zip_codes, 'oakland')
