import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_missing_values_proportion(df_places: pd.DataFrame, column_name: str):
    df_amount = df_places['type'].value_counts().reset_index()
    df_na = pd.crosstab(df_places['type'], df_places[column_name].isna())
    df_na_relative = df_na.apply(lambda x: x / df_na.sum(axis=1)).reset_index()  # normalization

    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.2,
        subplot_titles=["Number of places", "Proportion of missing values"]
    )

    fig.add_trace(
        go.Bar(
            y=df_amount.iloc[:, 0],
            x=df_amount.iloc[:, 1],
            orientation='h',
            showlegend=False,
            name='amount'),
        row=1, col=1)

    for column in [True, False]:
        fig.add_trace(
            go.Bar(
                y=df_na_relative.iloc[:, 0],
                x=df_na_relative.loc[:, column],
                orientation='h',
                name=str(column)),
            row=1, col=2)

    fig.update_yaxes(tickmode='linear', showticklabels=True, title='place type')
    fig.update_xaxes(row=1, col=1, title='Number of places')
    fig.update_xaxes(row=1, col=2, title='Proportion of missing data (True = Missing Data)')
    fig.update_layout(barmode='stack', title_text="Missing values for [{}] column.".format(column_name))
    fig.show()
