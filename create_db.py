import sqlite3
import csv
import os

def create_database():
    db_file = 'data.db'
    csv_file = 'movie.csv'
    
    # Remove existing db if it exists to ensure fresh start
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing {db_file}")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        score TEXT,
        categories TEXT,
        country TEXT,
        duration TEXT,
        release_date TEXT
    )
    '''
    cursor.execute(create_table_sql)
    print("Created table 'movies'")

    # Import data from CSV
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            to_db = [(i['title'], i['score'], i['categories'], i['country'], i['duration'], i['release_date']) for i in reader]
        
        cursor.executemany("INSERT INTO movies (title, score, categories, country, duration, release_date) VALUES (?, ?, ?, ?, ?, ?);", to_db)
        conn.commit()
        print(f"Imported {len(to_db)} rows into 'movies'")
    except FileNotFoundError:
        print(f"Error: {csv_file} not found")
    except Exception as e:
        print(f"Error importing data: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_database()
