# Yelp gentrification data scripts

A series of scripts used to pull and clean the data used for the Data World Yelp Gentrification project. In order to use these scripts as intended, you will need virtualenv and virtualenvwrapper.

1. `git clone https://github.com/amccartney/dataworld-gentrification.git`
2. `cd dataworld-gentrification`
3. `mkvirtualenv yelp`
4. `pip install -r requirements.txt`

Then the order the scripts should be run in:

1. yelp_scrape.py
2. business_scrape.py
3. Make this API call: http://api.census.gov/data/2014/acs5?get=B19013_001E&for=zip+code+tabulation+area
4. census_cleaner.py
5. table_maker.py
