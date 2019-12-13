
import numpy as np
import pandas as pd
import json
from shapely.geometry import shape, Point


path_nta = "data/Neighborhood Tabulation Areas.geojson"
path_311 = "data/extract.csv"
path_ctc_legend = "complaint_type_cls_legend.json"
path_ctc = "complaint_type_cls.json"
path_output = "NTA_and_CTC_output.pickle"

def get_nta(location, js, *, ct=None, print_step=None):
    location = eval(location)
    latitude = location[0]
    longitude = location[1]
    point = Point(longitude, latitude)
    for feature in js["features"]:
        polygon = shape(feature["geometry"])
        if polygon.contains(point):
            nta_code = feature["properties"]["ntacode"]
            if print_step: ct += [1]
            if ct and len(ct) % print_step == 0: print("Got", len(ct), "NTAs.")
            return nta_code        
    return np.nan

def convert(selected_ctcs, *, print_step=None):
    with open(path_ctc_legend) as fp_legend:
        ct_legend = json.load(fp_legend)
    with open(path_ctc) as fp_data:
        ct_data = json.load(fp_data)
    with open(path_nta) as fp:
        js = json.load(fp)

    df_source = pd.read_csv(path_311)
    print(df_source.shape[0], "total NTAs")

    # Keep entries with Latitude and Longitude
    df = df_source[pd.notnull(df_source["Latitude"]) & pd.notnull(df_source["Longitude"])].copy()

    # Keep entries for relevant complaint type class
    df["Complaint Type Class Index"] = df["Complaint Type"].apply(lambda k: ct_data[k])
    ct_legend_inv = {v:k for k, v in ct_legend.items()}
    df["Complaint Type Class"] = df["Complaint Type Class Index"].apply(lambda k: ct_legend_inv[k])
    df = df[df["Complaint Type Class"].isin(selected_ctcs)]

    print(df.shape[0], "filtered NTAs")
    
    # Create counter
    if print_step: ct = []
    print_params = dict(ct=[] if print_step else None, print_step=print_step)
    df["NTA"] = df["Location"].apply(lambda x: get_nta(x, js, **print_params))

    print(df.shape)
    print(df["Complaint Type Class"].value_counts())

    df.to_pickle(path_output)

if __name__=="__main__":
    convert(["noise annoyance", "pest"], print_step=1000)
    print(pd.read_pickle(path_output).head())