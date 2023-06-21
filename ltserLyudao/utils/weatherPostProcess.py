import pandas
import os
import pandas as pd
import csv
import codecs

input_file = './weather_utf8.csv'



"""import chardet

with open(input_file, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    original_encoding = result['encoding']

print(original_encoding)
"""

data = pd.read_csv(input_file, encoding='utf-8')
data.insert(0, "id", range(1, len(data) + 1))
data['eventDate'] = pd.to_datetime(data['eventDate'])
data['eventDate'] = data['eventDate'].dt.strftime("%Y-%m-%d %H:%M:%S")
data.to_csv('weather_post_process.csv', index=False, encoding='utf-8')

