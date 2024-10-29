from dash import html
import pandas as pd
import os

def create_rank_page():
    # Leer datos más recientes del archivo CSV
    data_path = os.path.join(os.path.dirname(__file__), '../data/movies.csv')
    df = pd.read_csv(data_path)

    layout = html.Div([
        html.H2("Movie Rankings"),
        html.Table([
            html.Thead(
                html.Tr([html.Th("Title"), html.Th("Average Rating"), html.Th("Number of Votes")])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(movie),
                    html.Td(round(df[df['title'] == movie]['rating'].mean(), 2)),
                    html.Td(df[df['title'] == movie].shape[0])
                ]) for movie in df['title'].unique()
            ])
        ])
    ])
    return layout
