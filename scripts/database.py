import psycopg2
import csv
import os

def store_jobs():
    try:
        conn = psycopg2.connect(
            dbname="airflow",
            user="airflow",
            password="airflow",
            host="postgres",
            port=5432,
        )
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_listings (
                id SERIAL PRIMARY KEY,
                title TEXT,
                company TEXT
            )
        """)

        # Check if the CSV exists
        csv_path = '/opt/airflow/datasets/jobs.csv'
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            return

        # Insert data into the database
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(
                    "INSERT INTO job_listings (title, company) VALUES (%s, %s)",
                    (row['title'], row['company'])
                )
                print(row['title'] + row['company'])

        conn.commit()
        print("Job data stored in database.")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
