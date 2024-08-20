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
    conn = get_db_connection()
    ratiosTTM = pd.read_sql_query('SELECT * FROM RatiosTTM', conn)
    assets = pd.read_sql_query('SELECT * FROM Assets', conn)
    conn.close()

    df = pd.merge(assets, ratiosTTM, on='symbol', how='left')
    df.rename(columns={'dividendYielTTM':'dividendYieldTTM'}, inplace=True)
    df.fillna(0, inplace=True)

    scoring_baseline = pd.read_csv(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\screenr_pub\backend\data\Baselines\baseline.csv')
    scoring_baseline['scoring_columns'] = scoring_baseline['scoring_columns'] + 'TTM'

    df_scored = scoring.calculate_score(df, np.array(scoring_baseline['scoring_columns']), np.array(scoring_baseline['booleans']))
    df_scored = df_scored.sort_values(by='score', ascending=False)

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    start = (page - 1) * per_page
    end = start + per_page

    df_scored_paginated = df_scored[start:end]

    scored_stocks_list = df_scored_paginated.to_dict(orient='records')
    return jsonify(scored_stocks_list)


@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM RatiosTTM').fetchall()
    conn.close()

    stocks_list = [dict(row) for row in stocks]
    return jsonify(stocks_list)

if __name__ == '__main__':
    app.run(debug=True)
