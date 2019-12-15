import json
import numpy as np
import pandas as pd
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from shapely.geometry import shape, Point


path_nta = "data/Neighborhood Tabulation Areas.geojson"
path_311 = "data/311_samples.pkl"  # data/311_samples.pkl --- data/311_selected_columns.pkl
path_ctc_legend = "complaint_type_cls_legend.json"
path_ctc = "complaint_type_cls.json"
path_output = "NTA_and_CTC_output.pkl"

with open(path_nta) as fp:
    js = json.load(fp)


def get_nta(row):
    longitude = row["Longitude"]
    latitude = row["Latitude"]
    point = Point(longitude, latitude)
    for feature in js["features"]:
        polygon = shape(feature["geometry"])
        if polygon.contains(point):
            nta_code = feature["properties"]["ntacode"]
            return nta_code        
    return np.nan


# Apply to dataframe
def apply_to_df(df_chunks):
    df_chunks["NTA"] = df_chunks.apply(get_nta, axis=1)
    print("finished chunk")
    return df_chunks


def convert():
    with open(path_ctc_legend) as fp_legend:
        ct_legend = json.load(fp_legend)
    with open(path_ctc) as fp_data:
        ct_data = json.load(fp_data)

    start_time = time.time()

    df_source = pd.read_pickle(path_311)
    print(df_source.shape[0], "total complaints")

    # Keep entries with Latitude and Longitude
    df = df_source[pd.notnull(df_source["Latitude"]) & pd.notnull(df_source["Longitude"])].copy()
    df = df.set_index("Unique Key")

    # Keep entries for relevant complaint type class
    df["Complaint Type Class Index"] = df["Complaint Type"].apply(lambda k: ct_data[k] if k in ct_data else -1)
    ct_legend_inv = {v:k for k, v in ct_legend.items()}
    df["Complaint Type Class"] = df["Complaint Type Class Index"].apply(lambda k: ct_legend_inv[k])

    print(df.shape[0], "filtered complaints")

    # Add NTA column
    df["NTA"] = np.nan

    # Divide dataframe to chunks
    prs = 100 # define the number of processes
    chunk_size = int(df.shape[0]/prs)
    chunks = [df.loc[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]
    
    # Process dataframes
    with ThreadPool(prs) as p:
        result = p.map(apply_to_df, chunks)

    # Concat all chunks
    df_reconstructed = pd.concat(result)

    end_time = time.time()
    print("Took {:.3f} seconds to process {} complaints".format(time.time() - start_time, df_reconstructed.shape[0]))

    print(df_reconstructed.shape)
    print(df_reconstructed["Complaint Type Class"].value_counts())

    df_reconstructed.to_pickle(path_output)


if __name__=="__main__":
    convert()
    print(pd.read_pickle(path_output).head())