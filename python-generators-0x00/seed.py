#!/usr/bin/python3
"""
seed.py - Setup ALX_prodev database, create table user_data, 
insert data from CSV, and stream rows using a generator.
"""

import mysql.connector
import csv
import uuid


# -------------------------
# Connect to MySQL server
# -------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # adjust if needed
            password="root"       # adjust if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# -------------------------
# Create database if missing
# -------------------------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()


# -------------------------
# Connect directly to ALX_prodev
# -------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # adjust if needed
            password="root",      # adjust if needed
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# -------------------------
# Create user_data table
# -------------------------
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


# -------------------------
# Insert data from CSV
# -------------------------
def insert_data(connection, csv_file):
    cursor = connection.cursor()

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]

            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))

    connection.commit()
    cursor.close()


# -------------------------
# Generator: Stream rows from DB
# -------------------------
def stream_rows(connection, batch_size=1):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
    cursor.close()
