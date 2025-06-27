import plotly.graph_objects as go # type: ignore

def plotly_table(dataframe):
    header_color = "grey"
    row_even_color = "#f8fafd"
    row_odd_color = "#e1efff"

    # Create a table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + [f"<b>{str(col)[:10]}</b>" for col in dataframe.columns],
            line_color='darkslategray',
            fill_color=header_color,
            align=['left', 'center'],
            font=dict(color='white', size=15),
            height=35,
        ),
        cells=dict(
            values=[[f"<b>{i}</b>" for i in dataframe.index]] +
                   [dataframe[col].tolist() for col in dataframe.columns],
            align=['left', 'center'],
            line_color='darkslategray',
            font=dict(color='red', size=12),
            fill_color=row_even_color  # Note: Static color; for alternating rows, use a list.
        )
    )])

    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig
