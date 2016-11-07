# This script takes data from the US Census 5-year American Community Survey,
# which, in this case, have been saved into two files, "2011.json" and "2014.json",
# and cross-references them against a list of zip codes that relate to the cities we are analyzing.

# The API calls that produced the data found in both of those JSON files are:
# - http://api.census.gov/data/2011/acs5?get=NAME,B01001_001E,B02001_002E,B19013_001E,B25064_001E,B25071_001E,B25077_001E&for=zip+code+tabulation+area:*
# - http://api.census.gov/data/2014/acs5?get=NAME,B01001_001E,B02001_002E,B19013_001E,B25064_001E,B25071_001E,B25077_001E&for=zip+code+tabulation+area:*

# The meanings of the census codes in the API call are:
# - 'B19013_001E' = 'Median household income'

# http://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml

# This comes from the ACS variable dictionary:
# http://api.census.gov/data/2013/acs5/variables.html

# 2011 is the earliest year where the API can tabulate results based on a
# ZIP code area, and 2014 is the last year of data, which is why they are used here.


import json
import csv
import os

class CensusCleaner(object):


    def open_json(self, data_json):
        # Opens JSON file and loads the data

        with open(data_json) as data_file:
            data = json.load(data_file)

            return data


    def open_csv(self, data_csv):
        # Opens JSON file and loads the data

        with open(data_csv) as data_file:
            data = csv.reader(data_file)

            return data

    def find_relevant_zips(self, all_zips, data):
        relevant_zips = []

        # Append the header data to the list
        writer = csv.writer(open('data/census/2014_cleaned.csv','wb'))
        header = ['Year','ZCTA5','Median household income']
        writer.writerow(header)

        # For every line in the data, check to see if the associated ZIP code is in the list
        # of ZIP codes being analyzed, and if it is, append the whole row to a list of "relevant ZIPs"
        for d in data:
            if d[1] in all_zips:
                print d[1]
                writer.writerow([ "2014", d[1], d[0]  ])

        # Return the list of relevant ZIP codes and their associated data
        return relevant_zips


    def find_relevant_zips_csv(self, all_zips, data_csv):
        relevant_zips = []

        writer = csv.writer(open('data/census/2000_cleaned.csv','wb'))
        header = ['Year','ZCTA5','Median household income']
        writer.writerow(header)

        with open(data_csv) as data_file:
            data = csv.reader(data_file)

            # For every line in the data, check to see if the associated ZIP code is in the list
            # of ZIP codes being analyzed, and if it is, append the whole row to a list of "relevant ZIPs"
            for d in data:
                if d[1] in all_zips:
                    print d[1], d[3]
                    writer.writerow([ "2000", d[1], d[3] ])


if __name__ == "__main__":

    # ZIP codes associated with San Francisco, Brooklyn, Portland, Austin and Oakland
    all_zips = ['94102','94103','94104','94105','94107','94108','94109','94110','94111',
                '94112','94114','94115','94116','94117','94118','94121','94122','94123',
                '94124','94127','94129','94130','94131','94132','94133','94134','94158',
                '11201','11204','11206','11208','11210','11212','11214','11216','11218',
                '11220','11222','11224','11226','11229','11231','11233','11235','11237',
                '11239','11203','11205','11207','11209','11211','11213','11215','11217',
                '11219','11221','11223','11225','11228','11230','11232','11234','11236',
                '11238','97034','97035','97080','97086','97201','97202','97203','97204',
                '97205','97206','97208','97209','97210','97211','97212','97213','97214',
                '97215','97216','97217','97218','97219','97220','97221','97222','97223',
                '97225','97227','97229','97230','97231','97232','97233','97236','97239',
                '97266','78610','78613','78617','78641','78652','78653','78660','78664',
                '78681','78701','78702','78703','78704','78705','78712','78717','78719',
                '78721','78722','78723','78724','78725','78726','78727','78728','78729',
                '78730','78731','78732','78733','78734','78735','78736','78737','78738',
                '78739','78741','78742','78744','78745','78746','78747','78748','78749',
                '78750','78751','78752','78753','78754','78756','78757','78758','78759',
                '94577','94601','94602','94603','94605','94606','94607','94608','94609',
                '94610','94611','94612','94613','94618','94619','94621','94704','94705']

    # Initiate the class
    cleaner = CensusCleaner()

    cleaner.find_relevant_zips_csv(all_zips, "data/census/2000.csv")

    json_data = cleaner.open_json("data/census/2014.json")
    cleaner.find_relevant_zips(all_zips, json_data)


    # ZIPS we have to throw output
    # 97239
    # 97208
    # 97086
    # 94613
    # 94158
    # 78712
