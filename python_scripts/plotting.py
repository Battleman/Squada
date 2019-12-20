import plotly.graph_objects as go
import plotly
import matplotlib.pyplot as plt


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
    plt.savefig("plots/resolution_time_nypd_dsny.png")
