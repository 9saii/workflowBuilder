import sqlite3

def add_description_column():
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()
    try:
        cursor.execute('ALTER TABLE workflows ADD COLUMN description TEXT')
        conn.commit()
        print("Column 'description' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_description_column()
