# This script takes all of the combined census data from the file created by
# census_cleaner.py and splits it into simple tables for quick analysis.

import json
import csv
import os

class TableMaker(object):

    def open_json(self, data_json):
        # Opens JSON file and loads the data

        with open(data_json) as data_file:
            data = json.load(data_file)

            return data


    def population_table(self, data):
        # Creates a table of the total population of each ZIP code and its total
        # white population in order to determine whether white people increased their
        # share of the population in that area. Since gentrification is often
        # characterized as a process of white people displacing communities of color,
        # determining the white share of the population over time is relevant.

        writer = csv.writer(open('data/population.csv','wb'))
        header = ['year','zip_code','total_population','white_population']

        writer.writerow(header)

        for d in data:
            year = d.keys()[0]

            for i in range(1, len(d[year])):
                writer.writerow([year, d[year][i][7], d[year][i][1], d[year][i][2]])

    def household_income_table(self, data):
        # Creates a simple table of the median household income in every ZIP code.
        # Used to determine whether those with higher incomes have moved into
        # the area over time.

        writer = csv.writer(open('data/household_income.csv','wb'))
        header = ['year','zip_code','household_income']

        writer.writerow(header)

        for d in data:
            year = d.keys()[0]

            for i in range(1, len(d[year])):
                writer.writerow([year, d[year][i][7], d[year][i][3]])

    def rent_table(self, data):
        # Creates a table of both the median rent in every ZIP code and the
        # percentage of the household income that rent accounts for. One of the
        # defining features of a gentrifying neighborhood in increased rent expense,
        # caused by higher neighborhood desirability.

        writer = csv.writer(open('data/rent.csv','wb'))
        header = ['year','zip_code','median_rent','rent_percentage_of_household_income']

        writer.writerow(header)

        for d in data:
            year = d.keys()[0]

            for i in range(1, len(d[year])):
                writer.writerow([year, d[year][i][7], d[year][i][4], d[year][i][5]])

    def house_value_table(self, data):
        # Creates a simple table of the median house value of properties where
        # the owner lives in the residence.

        writer = csv.writer(open('data/house_value.csv','wb'))
        header = ['year','zip_code','median_house_value']

        writer.writerow(header)

        for d in data:
            year = d.keys()[0]

            for i in range(1, len(d[year])):
                writer.writerow([year, d[year][i][7], d[year][i][6]])


if __name__ == "__main__":

    # Initiates the class
    table_maker = TableMaker()

    data = table_maker.open_json("data/all_years_census.json")

    # Make the tables
    table_maker.population_table(data)
    table_maker.household_income_table(data)
    table_maker.rent_table(data)
    table_maker.house_value_table(data)
