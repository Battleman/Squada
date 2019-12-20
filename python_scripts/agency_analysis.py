import pandas as pd
from shapely.geometry import shape, Point
import json
import numpy as np

nta_geojson = "data/Neighborhood Tabulation Areas.geojson"
nta_id_field = "ntacode"
doe_geojson = "data/School Districts.geojson"
doe_id_field = "school_dist"
nypd_geojson = "data/Police Precincts.geojson"
nypd_id_field = "precinct"
fdny_geojson = "data/Fire Battalions.geojson"
fdny_id_field = "fire_bn"
dsny_geojson = "data/DSNY Districts.geojson"
dsny_id_field = "districtcode"

# districts and create polygons
def get_polygons(geojson_path, id_field):
    with open(geojson_path) as f:
        js = json.load(f)
        return [(feature["properties"][id_field], shape(feature["geometry"])) for feature in js["features"]]


def get_district(row, polygons):
    """Retrieves the district of a given location in NYC.
    Args:
        row: 311 request with associated metadata (e.g. location)
    Returns:
        String: code of the district the location is part of, or NaN if the location is not within a district
    """
    longitude = row["Longitude"]
    latitude = row["Latitude"]
    point = Point(longitude, latitude)
    for polygon in polygons:
        if polygon[1].contains(point):
            district_code = polygon[0]
            return district_code
    return np.nan


def get_population_per_district(agency, nta_pop_df, nta_polygons):
    polygons = get_polygons(agency[1], agency[2])
    agency[3].clear()
    for polygon in polygons:
        district_population = 0
        district_failed = False
        for nta_polygon in nta_polygons:
            try:
                district_population += (nta_polygon[1].intersection(polygon[1]).area /
                                        nta_polygon[1].area) * \
                                       nta_pop_df[nta_pop_df.index == nta_polygon[0]].values[0][
                                           0]
            except:
                print(f"failed for nta: {nta_polygon[0]} with district {polygon[0]}")
                district_failed = True
                break
        if district_failed:
            continue
        agency[3].append((polygon[0], district_population))
    return agency


def get_agencies_array(df_311):
    relevant_columns = ["Created Date", "Closed Date", "Agency",
                        "Complaint Type", "Latitude", "Longitude"]
    df_311 = df_311[relevant_columns]

    # split into agencies and use only those with present latitude and longitude
    df_311 = df_311[df_311["Latitude"].notnull() & df_311["Longitude"].notnull()]
    df_nypd = df_311[df_311["Agency"] == "NYPD"].drop(columns="Agency")
    df_dsny = df_311[df_311["Agency"] == "DSNY"].drop(columns="Agency")
    df_fdny = df_311[df_311["Agency"] == "FDNY"].drop(columns="Agency")
    df_doe = df_311[df_311["Agency"] == "DOE"].drop(columns="Agency")

    agencies = [(df_doe, doe_geojson, doe_id_field, []),
                (df_nypd, nypd_geojson, nypd_id_field, []),
                (df_dsny, dsny_geojson, dsny_id_field, []),
                (df_fdny, fdny_geojson, fdny_id_field, [])]

    all_agency_names = ["DOE", "NYPD", "DSNY", "FDNY"]
    for i, agency in enumerate(agencies):
        print(f"{all_agency_names[i]} has {len(agency[0])} entries")
    print("We realize that we few complaints from Fire Departments with specified location"
          "so we drop it. There are also not many such complaints to the department of education "
          "(~19k) and we also decide not to use if further.")

    agencies = [agencies[i] for i in [1, 2]]
    for agency in agencies:
        polygons = get_polygons(agency[1], agency[2])
        agency[0]["District"] = agency[0].apply(lambda x: get_district(x, polygons), axis=1)
    nta_pop_df = pd.read_csv(
        "data/New_York_City_Population_By_Neighborhood_Tabulation_Areas.csv")
    # the census is done every 10 years, so we have to depend on the 2010 data
    nta_pop_df = nta_pop_df[nta_pop_df["Year"] == 2010][["NTA Code", "Population"]].set_index(
        "NTA Code")

    # Get estimated population of each district.
    # We drop the three districts that have ill defined boundaries.
    nta_polygons = get_polygons(nta_geojson, nta_id_field)
    for agency in agencies:
        agency = get_population_per_district(agency, nta_pop_df, nta_polygons)

    # adding resolution time
    agencies_df = [agency[0] for agency in agencies]
    for i, agency in enumerate(agencies):
        time_diff = agencies_df[i]["Closed Date"] - agencies_df[i]["Created Date"]
        agencies_df[i]["Resolution Time (days)"] = time_diff.apply(
            lambda x: x.total_seconds() / (24 * 3600))

    for agency in agencies_df:
        agency.rename(columns={"Resolution Time": "Resolution Time (days)"}, inplace=True)

    return agencies




