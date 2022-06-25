import re

import pandas as pd
import recordlinkage
from crawler.car_integration.car_integration.mapping import MANUFACTURER


def mapping_car_manufacturer(value: str):
    for key in MANUFACTURER.keys():
        for manufacturer in MANUFACTURER[key]:
            search_item = re.search(manufacturer, value.lower())
            if search_item:
                name_str = value[search_item.span()[0] :]
                word_list = name_str.split(" ")
                car_name = word_list[0:3]
                return " ".join(car_name)
    return value.lower()


def record_linking(df):
    indexer = recordlinkage.Index()
    indexer.block(["fuel", "manufacturer", "mfg", "seat", "status", "origin"])
    candidate_links = indexer.index(df)
    # print(len(candidate_links))
    compare_cl = recordlinkage.Compare()
    compare_cl.exact("color", "color", missing_value=1.0, label="color")
    compare_cl.string(
        "drive",
        "drive",
        method="jarowinkler",
        missing_value=1.0,
        threshold=0.95,
        label="drive",
    )
    compare_cl.string(
        "engine",
        "engine",
        method="jarowinkler",
        missing_value=1.0,
        threshold=0.95,
        label="engine",
    )
    compare_cl.exact("fuel", "fuel", missing_value=1.0, label="fuel")
    compare_cl.exact(
        "interior_color", "interior_color", missing_value=1.0, label="interior_color"
    )
    compare_cl.exact(
        "manufacturer", "manufacturer", missing_value=1.0, label="manufacturer"
    )
    compare_cl.numeric("mfg", "mfg", missing_value=1.0, label="mfg")
    compare_cl.string(
        "name",
        "name",
        method="jarowinkler",
        missing_value=1.0,
        threshold=0.95,
        label="name",
    )
    compare_cl.exact("origin", "origin", missing_value=1.0, label="origin")
    compare_cl.numeric("price", "price", missing_value=1.0, label="price")
    compare_cl.numeric("seat", "seat", missing_value=1.0, label="seat")
    compare_cl.exact("status", "status", missing_value=1.0, label="status")
    compare_cl.string(
        "transmission",
        "transmission",
        method="jarowinkler",
        missing_value=1.0,
        threshold=0.95,
        label="transmission",
    )
    compare_cl.string(
        "type",
        "type",
        method="jarowinkler",
        missing_value=1.0,
        threshold=0.95,
        label="type",
    )
    features = compare_cl.compute(candidate_links, df)
    return features


def connected_tuples(pairs):
    lists_by_element = {}

    def make_new_list_for(x, y):
        lists_by_element[x] = lists_by_element[y] = [x, y]

    def add_element_to_list(lst, el):
        lst.append(el)
        lists_by_element[el] = lst

    def merge_lists(lst1, lst2):
        merged_list = lst1 + lst2
        for el in merged_list:
            lists_by_element[el] = merged_list

    for x, y in pairs:
        xList = lists_by_element.get(x)
        yList = lists_by_element.get(y)

        if not xList and not yList:
            make_new_list_for(x, y)

        if xList and not yList:
            add_element_to_list(xList, y)

        if yList and not xList:
            add_element_to_list(yList, x)

        if xList and yList and xList != yList:
            merge_lists(xList, yList)

    return set(tuple(l) for l in lists_by_element.values())


df = pd.read_csv("data/truncated_data.csv")
# print(df)
lower_value_columns = [
    "color",
    "drive",
    "fuel",
    "interior_color",
    "name",
    "origin",
    "transmission",
    "type",
]
for column in lower_value_columns:
    df[column] = df[column].str.lower()

df.loc[df["origin"] == "việt nam", "origin"] = "trong nước"
df.loc[df["origin"] == "lắp ráp trong nước", "origin"] = "trong nước"
df.loc[df["origin"].isna(), "origin"] = "khác"
df.loc[
    (df["origin"] != "trong nước") & (df["origin"] != "khác"), "origin"
] = "nhập khẩu"


list_name = df["name"].to_list()
year_re = "\d{4}"
new_list_name = []
for name in list_name:
    if isinstance(name, float):
        continue
    new_name = mapping_car_manufacturer(name)
    year = re.search(year_re, new_name)
    if year:
        year = year.group()
        new_name = re.sub(year, "", new_name)
    new_list_name.append(new_name)

df["name"] = pd.DataFrame(new_list_name)
features = record_linking(df)
matches = features[(features.sum(axis=1) > 13) & (features.name == 1)].sort_index(
    ascending=True
)
# print(matches)
duplicate_list = []
for index in matches.index:
    duplicate_list.append(index)
connected_records_list = sorted(connected_tuples(duplicate_list))
remove_records = [record[1:] for record in connected_records_list]
remove_records = [i for sub in remove_records for i in sub]
# print(remove_records)
df_drop = df.drop(remove_records, axis=0, inplace=False)
# print(df_drop.reset_index(drop = True))
df_drop.to_csv("data/final_data.csv", index=False)
