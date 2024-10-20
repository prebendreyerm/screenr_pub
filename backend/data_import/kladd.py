import sqlite3

def get_db_connection():
    conn = sqlite3.connect(r'backend\data\financial_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def fix_transactions():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Fetch all transactions
        cursor.execute('SELECT id, action, date FROM Transactions')
        transactions = cursor.fetchall()

        # Prepare updates with swapped action and date
        updates = []
        for transaction in transactions:
            id_ = transaction['id']
            action = transaction['action']
            date = transaction['date']
            updates.append((date, action, id_))

        # Update transactions with swapped values
        cursor.executemany('UPDATE Transactions SET action = ?, date = ? WHERE id = ?', updates)

        conn.commit()
        print("Transactions updated successfully.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    fix_transactions()
