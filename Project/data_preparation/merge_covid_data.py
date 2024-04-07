import pandas


def group_covid_data():
    world = pandas.read_csv('data/raw/covid_19_confirmed.csv')
    us = pandas.read_csv('data/raw/covid_19_confirmed_US.csv')
    # group by first column and sum the rest
    world = world.groupby('Country/Region').sum()
    us = us.groupby('iso3').sum()
    # export to csv
    world.to_csv('data/covid_19_confirmed.csv')
    us.to_csv('data/covid_19_confirmed_US.csv')


if __name__ == '__main__':
    group_covid_data()
