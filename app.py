import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import os

# Inicializar la aplicación Dash con suppress_callback_exceptions
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Leer datos de películas
data_path = os.path.join(os.path.dirname(__file__), 'data/movies.csv')
if not os.path.exists(data_path):
    pd.DataFrame(columns=['title', 'rating']).to_csv(data_path, index=False)

# Aplicar Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dcc.Link("Home", href="/", className="nav-link")),
            dbc.NavItem(dcc.Link("Rankings", href="/rank", className="nav-link")),
        ],
        brand="Movie Ranking App",
        color="primary",
        dark=True,
    ),
    html.Div(id='page-content')
])

# Callback para actualizar el contenido de la página
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/rank':
        from pages.rank import create_rank_page
        return create_rank_page()
    else:
        from pages.home import create_home_page, register_callbacks
        register_callbacks(app)  # Registrar callbacks aquí
        return create_home_page(pd.read_csv(data_path))

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8000)
