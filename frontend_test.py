import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import sys
import platform
import os

if platform.system() == 'Darwin':
    sys.path.insert(1, r'/Users/preben/Documents/GitHub/Screenr')
else:
    sys.path.insert(1, r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\Screenr')

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from backend.database import backend


app = dash.Dash(__name__, external_stylesheets=['/assets/main.css'])

# Read the CSV file
df = pd.read_csv('Stock_lists/stonks_list.csv')

# Preprocess the DataFrame to calculate scores
def calculate_score(df):
    score_df = pd.DataFrame()
    score_df['Ticker'] = df['Ticker']
    # Score EV/EBITDA (lower is better)
    score_df['EV/EBITDA_Score'] = (df['AM'].rank(ascending=True) / len(df)).round(2)
    # Score Return on Assets (higher is better)
    score_df['ROA_Score'] = (df['ROA'].rank(ascending=False) / len(df)).round(2)
    # Calculate Total Score
    score_df['Total_Score'] = 1 - ((score_df['EV/EBITDA_Score'] + score_df['ROA_Score']) / 2)  # Invert the ranking
    
    return score_df

# Calculate scores
score_df = calculate_score(df)
# Merge score_df with original dataframe
df = pd.merge(df, score_df, on='Ticker', how='left')

# Filter out rows with missing sector values
df = df.dropna(subset=['Sector'])

# Calculate average EV/EBITDA for each sector
avg_ev_ebitda_sector = df.groupby('Sector')['AM'].mean().round(3)
# Add the average EV/EBITDA to the DataFrame
df['Avg_EBITDA_Sector'] = df['Sector'].map(avg_ev_ebitda_sector)

# Calculate delta for each ticker
df['Delta_EBITDA'] = df['AM'] - df['Avg_EBITDA_Sector']

# Define page size
PAGE_SIZE = 20

# Define DataTable layout
app.layout = html.Div([
    html.Div("Screener", className="app-header"),
    html.Div([
        dash_table.DataTable(
            id='table-sorting-filtering',
            columns=[
                {'name': 'Ticker', 'id': 'Ticker', 'type': 'text', 'editable': False},
                {'name': 'Company', 'id': 'Company', 'type': 'text', 'editable': False},
                {'name': 'EV/EBITDA', 'id': 'AM', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': 'Return on Assets', 'id': 'ROA', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': 'Dividend', 'id': 'Dividend', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': '5YR CAGR', 'id': '5YR CAGR', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': '10YR CAGR', 'id': '10YR CAGR', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': '5YR FCF Growth', 'id': '5YR FCF Growth', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': '10YR FCF Growth', 'id': '10YR FCF Growth', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': '5YR Dividend CAGR', 'id': '5YR Dividend CAGR', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': '10YR Dividend CAGR', 'id': '10YR Dividend CAGR', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': 'Total Score', 'id': 'Total_Score', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': 'Delta_EBITDA', 'id': 'Delta_EBITDA', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': 'EV/EBITDA by Sector', 'id': 'Avg_EBITDA_Sector', 'type': 'numeric', 'editable': False, 'format': {'specifier': '.2f'}},
                {'name': 'Last Update', 'id': 'Last Update', 'type': 'datetime', 'editable': False},
                {'name': 'Sector', 'id': 'Sector', 'type': 'text', 'editable': False},
            ],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            filter_action='custom',
            filter_query='',
            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
            style_header={
                'backgroundColor': 'black',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'backgroundColor': 'rgb(10,10,10)',
                'color': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(40, 40, 40)',
                }
            ],
            style_filter={
                'backgroundColor': 'black',
                'color': 'white'
            },
        ),
        dcc.Graph(
            id='company-revenue-graph',
            style={'backgroundColor': 'rgb(10,10,10)'}  # Dark mode background
        ),
        dcc.Graph(
            id='company-dividends-graph',
            style={'backgroundColor': 'rgb(10,10,10)'}  # Dark mode background
        )
    ])
])

# Define filtering and sorting callback
@app.callback(
    Output('table-sorting-filtering', 'data'),
    Input('table-sorting-filtering', "page_current"),
    Input('table-sorting-filtering', "page_size"),
    Input('table-sorting-filtering', 'sort_by'),
    Input('table-sorting-filtering', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df.copy()
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if col_name in ['Ticker', 'Company']:
            if operator == 'contains':
                dff = dff[dff[col_name].str.contains(filter_value, case=False, na=False)]
            elif operator == 'eq':
                dff = dff[dff[col_name].str.lower() == filter_value.lower()]
        else:
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size

    return dff.iloc[page * size: (page + 1) * size].to_dict('records')
# Define a callback for cell click to update the graphs
@app.callback(
    [Output('company-revenue-graph', 'figure'),
     Output('company-dividends-graph', 'figure')],
    Input('table-sorting-filtering', 'active_cell'),
    State('table-sorting-filtering', 'data'))
def update_graph(active_cell, data):
    if active_cell:
        row = active_cell['row']
        ticker = data[row]['Ticker']
        
        # Call the revenue function to get revenue data and years
        revenue_data, revenue_years = backend.revenue(ticker)
        
        # Reverse the order of the revenue data and years to go from most recent to least recent
        revenue_data = revenue_data[::-1]
        revenue_years = revenue_years[::-1]
        
        # Call the dividends_paid function to get dividends data and years
        dividends, dividend_years = backend.dividends_paid(ticker)
        
        # Reverse the order of the dividend data and years to go from most recent to least recent
        dividends = dividends[::-1]
        dividend_years = dividend_years[::-1]
        
        # Calculate the number of years to display for revenue (up to 10 or the available data)
        num_years_revenue = min(10, len(revenue_years))
        
        # Calculate the number of years to display for dividends (up to 10 or the available data)
        num_years_dividends = min(10, len(dividend_years))
        
        # Create a new dataframe for revenue data
        revenue_df = pd.DataFrame({
            'Year': revenue_years[:num_years_revenue],
            'Revenue': revenue_data[:num_years_revenue]
        })
        
        # Create a new dataframe for dividends data
        dividends_df = pd.DataFrame({
            'Year': dividend_years[:num_years_dividends],
            'Dividends': dividends[:num_years_dividends]
        })
        
        # Create figure for revenue data
        revenue_fig = px.line(revenue_df, x='Year', y='Revenue', title=f'Revenue Data for {ticker}')
        revenue_fig.update_traces(line=dict(color='#2ca02c'))
        revenue_fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )
        
        # Create figure for dividends data
        dividends_fig = px.line(dividends_df, x='Year', y='Dividends', title=f'Dividends Data for {ticker}')
        dividends_fig.update_traces(line=dict(color='#2ca02c'))
        dividends_fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )
        
        return revenue_fig, dividends_fig

    return {}, {}





# Define helper function to split filter part
def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

# Define operators
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

if __name__ == '__main__':
    app.run_server(debug=True)
