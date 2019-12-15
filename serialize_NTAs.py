import json
import numpy as np
import pandas as pd
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from shapely.geometry import shape, Point


path_nta = "data/Neighborhood Tabulation Areas.geojson"
path_311 = "data/311_Service_Requests_from_2010_to_Present_small.pkl"
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


# Apply to dataframe
def apply_to_df(df_chunks, js, print_params):
    df_chunks["NTA"] = df_chunks["Location"].apply(lambda x: get_nta(x, js, **print_params))
    return df_chunks
    print("finished chunk")


def convert(print_step=None):
    with open(path_ctc_legend) as fp_legend:
        ct_legend = json.load(fp_legend)
    with open(path_ctc) as fp_data:
        ct_data = json.load(fp_data)
    with open(path_nta) as fp:
        js = json.load(fp)

    df_source = pd.read_pickle(path_311)
    print(df_source.shape[0], "total NTAs")

    # Keep entries with Latitude and Longitude
    df = df_source[pd.notnull(df_source["Latitude"]) & pd.notnull(df_source["Longitude"])].copy()

    # Keep entries for relevant complaint type class
    df["Complaint Type Class Index"] = df["Complaint Type"].apply(lambda k: ct_data[k] if k in ct_data else -1)
    ct_legend_inv = {v:k for k, v in ct_legend.items()}
    df["Complaint Type Class"] = df["Complaint Type Class Index"].apply(lambda k: ct_legend_inv[k])

    print(df.shape[0], "filtered NTAs")
    
    # Create counter
    if print_step: ct = []
    print_params = dict(ct=[] if print_step else None, print_step=print_step)

    # Divide dataframe to chunks
    prs = 100 # define the number of processes
    chunk_size = int(df.shape[0]/prs)
    chunks = [df.iloc[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]
    
    # Process dataframes
    with ThreadPool(prs) as p:
        result = p.map(apply_to_df, chunks, js, print_params)

    # Concat all chunks
    df_reconstructed = pd.concat(result)

    print(df_reconstructed.shape)
    print(df_reconstructed["Complaint Type Class"].value_counts())

    df_reconstructed.to_pickle(path_output)

if __name__=="__main__":
    convert(print_step=1000)
    print(pd.read_pickle(path_output).head())