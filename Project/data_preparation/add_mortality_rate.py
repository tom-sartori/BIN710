import pandas as pd


def add_mortality_rate(data_file, mr_file):
    """
    Add the mortality rate to the data file
    :param data_file: file with the data
    :param mr_file: file with the mortality rate
    :return: None
    """
    data = pd.read_csv(data_file)
    mr = pd.read_csv(mr_file)
    data = data.merge(mr, on='Country', how='left', validate='one_to_one')
    # Rearrange the columns
    col = data.columns.tolist()
    data = data[col[:5] + [col[-1]] + col[5:-1]]
    data.to_csv(data_file.replace('.csv', '_with_mortality_rate.csv'), index=False)


if __name__ == '__main__':
    add_mortality_rate('data/data.csv', 'data/cleaned/covid_19_mortality_rates_cleaned.csv')