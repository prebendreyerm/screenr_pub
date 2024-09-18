from flask import Flask, jsonify, request
import sqlite3
import pandas as pd
from analysis import scoring
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\screenr_pub\backend\data\financial_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/stocks/scores', methods=['GET'])
def get_scored_stocks():
    try:
        # Get query parameters for columns, strategy, pagination, sorting
        selected_columns = request.args.getlist('columns')
        strategy = request.args.get('strategy', 'baseline')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        sort_by = request.args.get('sort_by', 'score')
        sort_order = request.args.get('sort_order', 'desc')
        name_search = request.args.get('name_search', '').lower()
        symbol_search = request.args.get('symbol_search', '').lower()
        sector_search = request.args.get('sector_search', '').lower()

        # Connect to the database
        conn = get_db_connection()
        ratiosTTM = pd.read_sql_query('SELECT * FROM RatiosTTM', conn)
        assets = pd.read_sql_query('SELECT * FROM Assets', conn)
        conn.close()

        # Merge dataframes
        df = pd.merge(assets, ratiosTTM, on='symbol', how='left')
        df.rename(columns={'dividendYielTTM':'dividendYieldTTM'}, inplace=True)
        df.fillna(0, inplace=True)

        # Load the appropriate baseline strategy
        baseline_file = f'C:\\Users\\Preben\\OneDrive\\Dokumenter\\GitHub\\screenr_pub\\backend\\data\\Baselines\\{strategy}.csv'
        scoring_baseline = pd.read_csv(baseline_file)
        scoring_baseline['scoring_columns'] = scoring_baseline['scoring_columns'] + 'TTM'

        # Calculate scores
        df_scored = scoring.calculate_score(df, np.array(scoring_baseline['scoring_columns']), np.array(scoring_baseline['booleans']))

        # Applying search
        if name_search:
            df_scored = df_scored[df_scored['name'].str.lower().str.contains(name_search)]
        if symbol_search:
            df_scored = df_scored[df_scored['symbol'].str.lower().str.contains(symbol_search)]
        if sector_search:
            df_scored = df_scored[df_scored['sector'].str.lower().str.contains(sector_search)]

        # Apply sorting
        sort_by = sort_by if sort_by in df_scored.columns else 'score'
        sort_order = True if sort_order == 'asc' else False
        df_scored = df_scored.sort_values(by=sort_by, ascending=sort_order)

        # Apply pagination
        start = (page - 1) * limit
        end = start + limit
        df_scored_paginated = df_scored.iloc[start:end]

        # Convert DataFrame to a list of dictionaries
        scored_stocks_list = df_scored_paginated.to_dict(orient='records')

        return jsonify({
            'data': scored_stocks_list,
            'page': page,
            'limit': limit,
            'total': len(df_scored)
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    try:
        conn = get_db_connection()
        stocks = conn.execute('SELECT * FROM RatiosTTM').fetchall()
        conn.close()

        stocks_list = [dict(row) for row in stocks]
        return jsonify(stocks_list)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
