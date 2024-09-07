import pandas as pd
import sqlite3


conn = sqlite3.connect(r'backend\data\financial_data.db')
df = pd.read_sql_query('SELECT * FROM KeyMetricsTTM', conn)



# # Connect to the SQLite database (replace 'your_database.db' with your database name)
# conn = sqlite3.connect(r'backend\data\financial_data.db')

# # Create a cursor object
# cursor = conn.cursor()

# # Execute the query to list all tables
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# # Fetch all results and print
# tables = cursor.fetchall()
# for table in tables:
#     print(table[0])

# # # Commit the changes
# # conn.commit()

# # Close the connection
# conn.close()

