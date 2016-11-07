import csv
import json
import sys
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


class YelpBusinessScraper(object):
    def __init__(self, yelp_config):
        self.auth = Oauth1Authenticator(
            consumer_key=yelp_config['consumer_key'],
            consumer_secret=yelp_config['consumer_secret'],
            token=yelp_config['token'],
            token_secret=yelp_config['token_secret']
        )
        self.client = Client(self.auth)
        self.reader = csv.DictReader
        self.db = []

    def read_csv(self, csv_name):
        with open(csv_name) as csvfile:
            csv_file = self.reader(csvfile)
            for row in csv_file:
                self.get_yelp_business(row)
            self.write_json("data/businesses.json")

    def write_json(self, json_name):
        with open(json_name, "w+") as outfile:
            print "Done!"
            print "Wrote to %s businesses to %s" % (len(self.db), outfile)
            json.dumps(self.db, outfile)

    def get_yelp_business(self, row):
        business_id = row['business_id']
        response = self.client.get_business(business_id)
        print response.business.name
        self.get_response_info(response)

    def get_response_info(self, response):
        response.business.neighborhoods = self.get_neighborhoods(response)
        response.business.categories = self.get_categories(response)
        response.business.address = self.get_address(response)
        business_json = self.get_business_json(response)
        self.db.append(business_json)

    def get_neighborhoods(self, response):
        output = ["", ""]
        neighborhoods = response.business.location.neighborhoods
        if neighborhoods is not None:
            output[0] = neighborhoods[0]
            if len(neighborhoods) > 1:
                output[1] = neighborhoods[1]
        return output

    def get_categories(self, response):
        output = ["", ""]
        categories = response.business.categories
        if categories is not None:
            output[0] = categories[0][1]
            if len(categories) > 1:
                output[1] = categories[1][1]
        return output

    def get_address(self, response):
        output = ""
        addresses = response.business.location.address
        if addresses is not None:
            output = addresses[0]
        return output

    def get_business_json(self, response):
        business = response.business
        output = {
            'name':         business.name,
            'is_closed':    business.is_closed,
            'business_id':  business.id.encode("utf-8"),
            'address':      business.address,
            'city':         business.location.city,
            'zip_code':     business.location.postal_code,
            'coordinates':  {
                'longitude':    business.location.coordinate.longitude,
                'latitude':     business.location.coordinate.latitude
            },
            'neighborhoods': {
                'neighborhood_1': business.neighborhoods[0],
                'neighborhood_2': business.neighborhoods[1],
            },
            'categories': {
                'category_1': business.categories[0],
                'category_2': business.categories[1]
            },
        }
        return output


if __name__ == "__main__":

    auth = Oauth1Authenticator(
        consumer_key=YELP_CONSUMER_KEY,
        consumer_secret=YELP_CONSUMER_SECRET,
        token=YELP_TOKEN,
        token_secret=YELP_TOKEN_SECRET
    )

    csv_name = 'data/all.csv'
    business_scraper = YelpBusinessScraper(auth)
    business_scraper.read_csv(csv_name)
    # data = earch_scraper.parse_response(response)
