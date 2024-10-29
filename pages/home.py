from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd

def create_home_page(movies_df):
    return html.Div([
        html.H1("Welcome to the Movie Ranking App"),
        html.Div("Here you can rank movies you've seen with your family."),
        
        # Dropdown to select existing movies
        html.Div([
            html.H2("Select a Movie"),
            dcc.Dropdown(
                id='movie-dropdown',
                options=[{'label': title, 'value': title} for title in movies_df['title']],
                placeholder="Select a movie",
            ),
            html.Button("Submit", id='select-button', n_clicks=0),
            html.Div(id='selected-output')
        ]),
        
        # Section to add a new movie
        html.Div([
            html.H2("Add a New Movie"),
            dcc.Input(id='new-movie-title', type='text', placeholder="Enter movie title"),
            dcc.Input(id='new-movie-rating', type='number', placeholder="Enter movie rating (1-10)", min=1, max=10),
            html.Button("Add Movie", id='add-button', n_clicks=0),
            html.Div(id='add-output')
        ])
    ])

def register_callbacks(app):
    @app.callback(
        Output('selected-output', 'children'),
        Input('select-button', 'n_clicks'),
        Input('movie-dropdown', 'value')
    )
    def update_output(n_clicks, selected_movie):
        if n_clicks > 0 and selected_movie:
            return f"You have selected: {selected_movie}"
        return "Please select a movie."

    @app.callback(
        Output('add-output', 'children'),
        Input('add-button', 'n_clicks'),
        State('new-movie-title', 'value'),
        State('new-movie-rating', 'value'),
        prevent_initial_call=True
    )
    def add_movie(n_clicks, title, rating):
        if n_clicks > 0 and title and rating is not None:
            # Load existing movies
            data_path = 'data/movies.csv'  # Ensure this path is correct
            movies_df = pd.read_csv(data_path)

            # Add new movie to DataFrame
            new_movie = pd.DataFrame({'title': [title], 'rating': [rating]})
            movies_df = pd.concat([movies_df, new_movie], ignore_index=True)
            movies_df.to_csv(data_path, index=False)  # Save to CSV

            return f"Added movie: {title} with rating: {rating}"
        return "Please enter a movie title and rating."
