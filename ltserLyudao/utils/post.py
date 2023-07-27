# import pandas as pd
#
# data = pd.read_csv("fish/fish_diversity_2023_Srping_post_process.csv")
#
# unique_locationIDs = data['locationID'].unique()
#
# for id in unique_locationIDs:
#     print(id)

"""import json

# 所有的 site 點
sites = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 19, 20, 21, 22, 25, 26, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 49, 50, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65, 67, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 118, 119, 120, 121, 123, 124, 125, 128, 129, 130, 131, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158]

# 生成 JSON 物件列表
json_objects = [{"site": str(site), "items": ["plant"]} for site in sites]

# 將列表轉換為 JSON
json_data = json.dumps(json_objects, indent=4)

# 將 JSON 數據寫入文件
with open("output.json", "w") as f:
    f.write(json_data)

print("JSON file has been written.")"""


import json

# 你的資料
data = [
    {
      "site": "A1",
      "items": ["weather"]
    },
    {
      "site": "CK",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "DBS",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "GG",
      "items": ["sea-temperature","coral-rec", "fish-div"]
    },
    {
      "site": "GW",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "NL",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "SL",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "WQG",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "YZH",
      "items": ["sea-temperature", "coral-rec", "zoobenthos", "bird-net-sound", "fish-div"]
    },
    {
      "site": "ZP",
      "items": ["sea-temperature", "coral-rec", "fish-div"]
    },
    {
      "site": "DMM",
      "items": ["zoobenthos"]
    },
    {
      "site": "BS",
      "items": ["bird-net-sound"]
    },
    {
      "site": "GST",
      "items": ["bird-net-sound"]
    },
    {
      "site": "LH",
      "items": ["bird-net-sound"]
    },
    {
      "site": "KZY",
      "items": ["fish-div"]
    }
]

# 將資料轉換為 JSON
json_data = json.dumps(data, indent=4)

# 打印 JSON
print(json_data)

# 檢查 site 是否有重複
sites = [item['site'] for item in data]
if len(sites) != len(set(sites)):
    print("Some sites are duplicated.")
else:
    print("All sites are unique.")

