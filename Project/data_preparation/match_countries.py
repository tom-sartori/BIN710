import difflib
import pandas as pd
import numpy as np


def match_countries(countries, possible_matches):
    """
    Match countries to possible matches
    :param countries: list of countries
    :param possible_matches: list of possible matches
    :return: dictionary with countries as keys and their best match as value
    """
    matches = {}
    for country in countries:
        match = difflib.get_close_matches(country, possible_matches, n=1, cutoff=0.8)
        if match:
            matches[country] = match[0]
        else:
            matches[country] = None
            print(f'No match found for {country}')
    return matches

def delete_unmatched(from_file, to_files):
    """
    Delete rows from a file that are not in the matches of all the to_files.
    :param from_file: file to delete rows from
    :param to_files: list of files to match with
    :return: None
    """
    data = pd.read_csv(from_file)
    countries = data['Country'].unique()
    matches_nb = {c: 0 for c in countries}
    for to_file in to_files:
        to_data = pd.read_csv(to_file)
        matches = match_countries(countries, to_data['Country'].unique())
        for country, match in matches.items():
            if match:
                matches_nb[country] += 1
    print(matches_nb)
    to_delete = [c for c, m in matches_nb.items() if m != len(to_files)]
    print(to_delete)
    for c in to_delete:
        data = data[data['Country'] != c]
    data.to_csv(from_file.replace('.csv', '_cleaned.csv'), index=False)

def select_matched(countries, files):
    """
    Select the rows of the files that are matched with the countries and replace the country names with the matches.
    :param countries: list of countries
    :param files: list of files
    :return: list of dataframes
    """
    for file_ in files:
        data = pd.read_csv(file_)
        possibles_countries = data['Country'].unique()
        matches = match_countries(countries, possibles_countries)
        data = data[data['Country'].isin(matches.values())]
        reversed_matches = {v: k for k, v in matches.items()}
        data['Country'] = data['Country'].map(reversed_matches)
        data.to_csv(file_.replace('.csv', '_cleaned.csv'), index=False)


if __name__ == '__main__':
    covid_data = pd.read_csv('data/data.csv')
    countries = covid_data['Country'].unique()
    # pop_data = pd.read_csv('data/mean_temperature.csv')
    # possible_matches = pop_data['Country'].unique()

    # matches = match_countries(countries, possible_matches)
    # for country, match in matches.items():
    #     print(f'{country} -> {match}')
    # print(len([m for m in matches.values() if m]))

    # delete_unmatched('data/raw/covid_19_confirmed_merged.csv', ['data/total_pop.csv', 'data/urban_pop.csv', 'data/mean_temperature.csv', 'data/coordinates.csv'])

    select_matched(countries, ['data/raw/covid_19_mortality_rates.csv'])

    # nb_occ = {c: 0 for c in countries}
    # for file_ in ['data/total_pop_cleaned.csv', 'data/urban_pop_cleaned.csv', 'data/mean_temperature_cleaned.csv', 'data/coordinates_cleaned.csv']:
    #     data = pd.read_csv(file_)
    #     for c in countries:
    #         if c in data['Country'].values:
    #             nb_occ[c] += 1
    # for c, n in nb_occ.items():
    #     if n != 4:
    #         print(c, n)