import plotly.graph_objects as go
import plotly
import matplotlib.pyplot as plt
import folium
import folium.plugins as plugins
import copy

def RGB_to_hex(RGB):
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def get_features(df_source, gj, df_area_key, df_year_key, gj_area_key, relevant_feature):
    df = df_source.copy()
    df.reset_index(inplace=True)
    features = []

    for year in range(2010, 2020):
        for feature in gj["features"]:
            ft = copy.deepcopy(feature)

            area = ft["properties"][gj_area_key]
            df_correct = df[(df[df_area_key] == area) & (df[df_year_key] == year)]

            q = float(df_correct.iloc[0][relevant_feature]\
                if df_correct.shape[0] > 0 else 0)

            color = RGB_to_hex((255*q, 0, 255*(1-q)))

            ft["properties"]["style"] = {
                "fillColor": str(color),
                'weight' : 1,
                'fillOpacity' : 0.66,
                'stroke': False
            }
            ft["properties"]["time"] = str(year)

            features.append(ft)
    return features


def map_features(features):
    m = folium.Map(location=(40.730610, -73.935242), zoom_start=10, tiles="Stamen Toner")

    plugins.TimestampedGeoJson(
        {'type': 'FeatureCollection',
        'features': features}
        , period='P1Y'
        , duration="P1Y"        
        , add_last_point=True
        , auto_play=False
        , loop=False
        , max_speed=0.5
        , loop_button=True
        , date_options='YYYY'
        , time_slider_drag_update=True
    ).add_to(m)

    return m

def calls_by_year(df_311_with_year):
    df_311_year = df_311_with_year.groupby("Year").count()["Unique Key"]
    barplot_text = df_311_year.values.round(-3) // 1000
    barplot_text = [str(val) + "k" for val in barplot_text]

    fig = go.Figure(
        data=go.Bar(x=df_311_year.keys(), y=df_311_year.values,
                    marker=dict(
                        color='rgb(250,128,114)',
                        line=dict(
                            color='rgb(8,48,107)',
                            width=1.5),
                    ),
                    text=barplot_text,
                    textposition='auto',
                    orientation='v',
                    opacity=0.6),
        layout_title_text="3-1-1 calls over time"
    )
    fig.update_layout(template="plotly_dark", yaxis_title="Number of calls", xaxis_title="Year",
                      xaxis_type="category")
    plot_filename = 'plots/calls_by_year.html'
    plotly.offline.plot(fig, filename=plot_filename)
    return plot_filename


def agency_complaint_resolution(agencies_df):
    agency_names = ["NYPD", "DSNY"]
    f, axes = plt.subplots(2, figsize=(16, 9))
    plt.subplots_adjust(bottom=0.05)
    for i in range(2):
        axes[i].set_yscale("log")
        agencies_df[i]["Resolution Time (days)"].hist(ax=axes[i], bins=100)
        axes[i].set_title(agency_names[i])
        axes[i].set_ylabel("number of complaints (log)")
        axes[i].set_xlabel("number of days")
    path = "plots/resolution_time_nypd_dsny.png"
    plt.savefig(path)
    return path
