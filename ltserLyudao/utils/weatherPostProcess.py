import os
import pandas as pd
import csv
import codecs
import numpy as np

"""
input_file = './weather_utf8.csv'
data = pd.read_csv(input_file, encoding='utf-8')
data.insert(0, "id", range(1, len(data) + 1))
data['eventDate'] = pd.to_datetime(data['eventDate'])
data['eventDate'] = data['eventDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
data.to_csv('weather_post_process.csv', index=False, encoding='utf-8')
"""

"""
folder_path = 'seaTemperature'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        df.replace(['', pd.NA, np.nan], np.nan, inplace=True)
        df.insert(0, "id", range(1, len(df) + 1))
        df['measurementDeterminedDate'] = pd.to_datetime(df['measurementDeterminedDate'])
        df['measurementDeterminedDate'] = df['measurementDeterminedDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(f"{file_name}_post_process.csv", index=False, encoding='utf-8')
"""

"""
input_file = './plant.csv'
data = pd.read_csv(input_file, encoding='utf-8')
data.insert(0, "id", range(1, len(data) + 1))
data['eventDate'] = pd.to_datetime(data['eventDate'])
data['eventDate'] = data['eventDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
data['measurementDeterminedDate'] = pd.to_datetime(data['measurementDeterminedDate'])
data['measurementDeterminedDate'] = data['measurementDeterminedDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
data.to_csv('plant_post_process.csv', index=False, encoding='utf-8')
"""

"""
folder_path = 'birdNetSound'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        #df.replace(['', pd.NA, np.nan], np.nan, inplace=True)
        df.insert(0, "id", range(1, len(df) + 1))
        df['measurementDeterminedDate'] = pd.to_datetime(df['measurementDeterminedDate'])
        df['measurementDeterminedDate'] = df['measurementDeterminedDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(f"{file_name}_post_process.csv", index=False, encoding='utf-8')
"""

"""input_file = './fish_diversity_2023_Spring.csv'
data = pd.read_csv(input_file, encoding='utf-8')
data.insert(0, "id", range(1, len(data) + 1))
data['eventDate'] = pd.to_datetime(data['eventDate'])
data['eventDate'] = data['eventDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
data.to_csv('fish_diversity_2023_Srping_post_process.csv', index=False, encoding='utf-8')"""

"""
input_file = './zoobenthos.csv'
data = pd.read_csv(input_file, encoding='utf-8')
data = data.rename(columns={'class': 'class_name'})
data.insert(0, "id", range(1, len(data) + 1))
data['eventDate'] = pd.to_datetime(data['eventDate'], format="%Y-%m-%d")
data['eventDate'] = data['eventDate'].dt.strftime("%Y-%m-%d")
data.to_csv('zoobenthos_post_process.csv', index=False, encoding='utf-8')
"""

"""folder_path = 'terreSound'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        #df.replace(['', pd.NA, np.nan], np.nan, inplace=True)
        df.insert(0, "id", range(1, len(df) + 1))
        df['measurementDeterminedDate'] = pd.to_datetime(df['measurementDeterminedDate'])
        df['measurementDeterminedDate'] = df['measurementDeterminedDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(f"{file_name}_post_process.csv", index=False, encoding='utf-8')"""

"""
input_file = './water/ltser-lyudao-water-202303-up.csv'
data = pd.read_csv(input_file, encoding='utf-8')
#data = data.rename(columns={'class': 'class_name'})
data.insert(0, "id", range(1, len(data) + 1))
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d")
data['time'] = data['time'].dt.strftime("%Y-%m-%d")
data.to_csv('water_post_process.csv', index=False, encoding='utf-8')
"""
"""
input_file = './habitat/habitat.csv'
data = pd.read_csv(input_file, encoding='utf-8')
#data = data.rename(columns={'class': 'class_name'})
data.insert(0, "id", range(1, len(data) + 1))
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d")
data['time'] = data['time'].dt.strftime("%Y-%m-%d")
data.to_csv('habitat_post_process.csv', index=False, encoding='utf-8')"""

"""input_file = './coralcomm/coralcomm.csv'
data = pd.read_csv(input_file, encoding='utf-8')
#data = data.rename(columns={'class': 'class_name'})
data.insert(0, "id", range(1, len(data) + 1))
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d")
data['time'] = data['time'].dt.strftime("%Y-%m-%d")
data.to_csv('coralcomm_post_process.csv', index=False, encoding='utf-8')"""

input_file = "./recreational fishery/RecreationalMay31.csv"
data = pd.read_csv(input_file, encoding='utf-8')
data['time'] = pd.to_datetime(data['time'])
data['time'] = data['time'].dt.strftime("%Y-%m-%d %H:%M:%S")
data.to_csv('RecreationalMay31_post_process.csv', index=False, encoding='utf-8')