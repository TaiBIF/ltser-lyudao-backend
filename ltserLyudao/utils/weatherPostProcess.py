import pandas
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


