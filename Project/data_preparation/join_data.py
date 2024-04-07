import pandas as pd


def join_data():
    """
    Join the data from the different files into one.
    :return: None
    """
    coordinates = pd.read_csv('data/cleaned/coordinates_cleaned.csv')
    covid_19_confirmed = pd.read_csv('data/cleaned/covid_19_confirmed_cleaned.csv')
    mean_temperature = pd.read_csv('data/cleaned/mean_temperature_cleaned.csv')
    total_pop = pd.read_csv('data/cleaned/total_pop_cleaned.csv')
    urban_pop = pd.read_csv('data/cleaned/urban_pop_cleaned.csv')
    mortality_rate = pd.read_csv('data/cleaned/mortality_rates_cleaned.csv')

    # Join the data
    # Drop 'Alpha-3 code'
    coordinates.drop('Alpha-3 code', axis=1, inplace=True)
    data = pd.merge(coordinates, urban_pop, on='Country', how='left', validate='one_to_one')
    # Rename '2020' to 'Urban Population'
    data.rename(columns={'2020': 'Urban Population'}, inplace=True)
    # Drop 'Country Code'
    data.drop('Country Code', axis=1, inplace=True)
    data = pd.merge(data, total_pop, on='Country', how='left', validate='one_to_one')
    # Rename '2020' to 'Total Population'
    data.rename(columns={'2020': 'Total Population'}, inplace=True)
    # Drop 'Country Code'
    data.drop('Country Code', axis=1, inplace=True)
    data = pd.merge(data, mortality_rate, on='Country', how='left', validate='one_to_one')
    
    data = pd.merge(data, mean_temperature, on='Country', how='left', validate='one_to_one')
    # Rename 'Temperature' to 'Mean Temperature'
    data.rename(columns={'Temperature': 'Mean Temperature'}, inplace=True)
    data = pd.merge(data, covid_19_confirmed, on='Country', how='left', validate='one_to_one')

    data.to_csv('data/data.csv', index=False)


if __name__ == '__main__':
    join_data()