import plotly.express as px

def year_month_line_graph(df):
    month_group = (df.groupby(["year", "monthNo",  "monthName"], as_index=False)["salesAmount"]
                   .sum()
                   .sort_values(by=["year", "monthNo"], ascending=[False, True])
                   )

    fig_line = px.line(
        month_group,
        x="monthName",
        y="salesAmount",
        color="year",
        markers=True,
    )

    return fig_line