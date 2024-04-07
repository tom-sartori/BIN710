import math
import pandas as pd


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the earth
    :param lat1: latitude of the first point
    :param lon1: longitude of the first point
    :param lat2: latitude of the second point
    :param lon2: longitude of the second point
    :return: the distance between the two points
    """
    R = 6371  # radius of the earth in km
    p = math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 2 * R * math.asin(math.sqrt(a))

def find_closest_measurements(points, measurements):
    """
    Find the closest measurements to a list of points
    :param points: a dataframe containing the points
    :param measurements: a dataframe containing the measurements
    :return: the closest measurements to the given point
    """
    closest_measurement_distance = pd.Series([float('inf')] * len(points))
    closest_measurement_climate = pd.Series([None] * len(points))
    for i, point in points.iterrows():
        for j, measurement in measurements.iterrows():
            distance = calculate_distance(point['Latitude'], point['Longitude'], measurement['Lat'], measurement['Lon'])
            if distance < closest_measurement_distance[i]:
                closest_measurement_distance[i] = distance
                closest_measurement_climate[i] = measurement['Cls']
        print(f'Point {i} done')
    return closest_measurement_climate

def add_climate_to_data(data_file, measurements_file):
    """
    Add climate information to the data
    :param data_file: the file containing the data
    :param measurements_file: the file containing the climate measurements
    :return: None
    """
    measurements = pd.read_csv(measurements_file)
    data = pd.read_csv(data_file)

    # Add columns 'Climate' to the data
    data['Climate'] = find_closest_measurements(data, measurements)
    data.to_csv(data_file.replace('.csv', '_with_climate.csv'), index=False)


if __name__ == '__main__':
    add_climate_to_data('data/data.csv', 'data/raw/climate.csv')

