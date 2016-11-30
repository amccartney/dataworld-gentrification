# This takes each business from the original list of businesses created by the
# yelp_scrape.py script and pulls its business profile from the Yelp API.

# @geraldarthur contributed major help to this script

import csv
import json
import sys
from passwords import *
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
        self.outfile = open('data/yelp/businesses.csv', "w+")
        self.db = []

    def read_csv(self, csv_filename):
        with open(csv_filename) as csvfile:
            self.init_write_csv("data/yelp/businesses.csv")
            csv_file = self.reader(csvfile)
            for row in csv_file:
                try:
                    self.get_yelp_business(row)
                except:
                    print "Failed to get records for " + row['business_id']
            self.outfile.close()
            print "Done!"
            # print "Wrote to %s businesses to %s" % (len(self.db), outfile)

    def init_write_csv(self, csv_filename):
        fieldnames = [
            'name',
            'is_closed',
            'business_id',
            'address',
            'city',
            'zip_code',
            'longitude',
            'latitude',
            'neighborhood_1',
            'neighborhood_2',
            'category_1',
            'category_2'
        ]
        self.writer = csv.DictWriter(self.outfile, fieldnames=fieldnames)
        self.writer.writeheader()


    def get_yelp_business(self, row):
        business_id = row['business_id']
        response = self.client.get_business(business_id)
        # print response.business.name
        self.get_response_info(response)

    def get_response_info(self, response):
        response.business.neighborhoods = self.get_neighborhoods(response)
        response.business.categories = self.get_categories(response)
        response.business.address = self.get_address(response)
        business_dict = self.get_business_dict(response)
        self.writer.writerow(business_dict)

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
            try:
                output = addresses[0]
            except:
                output = addresses
        return output

    def get_business_dict(self, response):
        business = response.business

        try:
            if business.location.coordinate.latitude:
                latitude = business.location.coordinate.latitude
        except:
            latitude = None

        try:
            if business.location.coordinate.longitude:
                longitude = business.location.coordinate.longitude
        except:
            longitude = None

        output = {
            'name':           business.name,
            'is_closed':      business.is_closed,
            'business_id':    business.id.encode("utf-8"),
            'address':        business.address,
            'city':           business.location.city,
            'zip_code':       business.location.postal_code,
            'longitude':      longitude,
            'latitude':       latitude,
            'neighborhood_1': business.neighborhoods[0],
            'neighborhood_2': business.neighborhoods[1],
            'category_1':     business.categories[0],
            'category_2':     business.categories[1]
        }
        return output


if __name__ == "__main__":

    auth = {
        'consumer_key': YELP_CONSUMER_KEY,
        'consumer_secret': YELP_CONSUMER_SECRET,
        'token': YELP_TOKEN,
        'token_secret': YELP_TOKEN_SECRET
    }
    csv_name = 'data/yelp/all.csv'
    business_scraper = YelpBusinessScraper(auth)
    business_scraper.read_csv(csv_name)
