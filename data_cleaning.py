import datetime
import re
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly


path_311 = "data/311_Service_Requests_from_2010_to_Present.csv"
path_nta = "data/Neighborhood Tabulation Areas.geojson"
path_nta_population = "data/New_York_City_Population_By_Neighborhood_Tabulation_Areas.csv"

df_311 = pd.read_csv(path_311)
df_311.set_index("Unique Key")
# We drop the State Plane coordinates as they are just a different format of the coordinates present in Latitude and Longitude.
df_311.drop(columns=["X Coordinate (State Plane)", "Y Coordinate (State Plane)"], inplace=True)
# We drop the "Location" column as it is just the Latitude and Longitude columns combined.
df_311.drop(columns="Location", inplace=True)

# We realize that some of the complaint types are incorrct. Many of such entries categories appear only once in the dataset. 
# We drop those entries as we cannot interpret such complaints.
invalid_complaints = list(df_311["Complaint Type"].value_counts(ascending=True)[
    df_311["Complaint Type"].value_counts(ascending=True) == 1].index)
df_311 = df_311[~df_311["Complaint Type"].isin(invalid_complaints)]

unique_created_dates = df_311["Created Date"].unique()
unique_closed_dates = df_311["Closed Date"].unique()
unique_closed_dates = list(pd.DataFrame(unique_closed_dates)[0].dropna())

# We will verify if the fields with dates have proper formatting. This still does not guarantee that they are logically correct, 
# that is in some expected range, but tells us whether or not we would be able to parse them.
txt='01/17/2026 10:12:35 PM'

# MMDDYYYY 1
re1='((?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1}))[-:\\/.](?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'
# White Space 1
re2='( )'	
# HourMinuteSec
re3='((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'

rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)

def try_matching(txt):
    m = rg.search(str(txt))
    if not m:
        print("NOT A MATCH!")
        print(txt)
        return 1
    return 0

# There is one entry among closed dates that is in the third millenium. We assume time travel is impossible, 
# so the complaint couldn't have been closed in the future. Dropping the entry with it.
df_311 = df_311[df_311["Closed Date"] != "03/30/3027 12:00:00 AM"]

df_311["Created Date"] = pd.to_datetime(df_311["Created Date"])
df_311["Closed Date"] = pd.to_datetime(df_311["Closed Date"])

# Clearly there is something wrong with the values of ticket closed date. There are entries that have the dates set in 1900s:
# We assume that those which do not have "Status" set to closed should not have the "Closed Date" set in the first place as the only
# other status present among them is "Pending". Thus we set their "Closed Date" to NaN. We remove the entries which had the status closed and "Closed date" set before 2010.
df_311.drop(df_311[(df_311["Closed Date"] < datetime.datetime(2010, 1, 1)) & (df_311["Status"] == "Closed")].index, inplace=True)

# One of the issues we have spotted is the fact that there are entries with "Closed Date" before "Created Date". 
# We assume this might be a way of dealing with complaints submitted for the problems that were already resolved.
# Those may be also plain mistakes. We decide to drop all such rows.
df_311.drop(df_311[df_311["Closed Date"] < df_311["Created Date"]].index, inplace=True)

# We also decide to remove the rows that have "Closed Date" after today. 
# This is because one expects the tickets with "Closed Date" present to be actually closed already. There is few such cases, so it should not pose a problem.
df_311.drop(df_311[df_311["Closed Date"] > datetime.datetime.today()].index, inplace=True)

# We won't use "Due date" and "Modified date"
df_311.drop(columns=["Resolution Action Updated Date", "Due Date"], inplace=True)

# We note that many of the columns can take only one of a small set of possible values. We cast them to "category" type to save space
# and make computation faster
category_columns = ["Agency", "Agency Name", "Complaint Type", "Descriptor", "Location Type",
                    "Community Board", "Address Type", "City", "Landmark", "Facility Type", "Status",
                    "Resolution Description", "Borough", "Open Data Channel Type", "Park Facility Name",
                    "Park Borough", "Vehicle Type", "Taxi Company Borough", "Bridge Highway Direction", "Road Ramp"]
df_311[category_columns] = df_311[category_columns].astype("category")
df_311.to_pickle("data/311_Service_Requests_from_2010_to_Present_cleaned.pkl")
