#!/usr/bin/python3
"""
Module: 1-batch_users
Objective: Stream and process user data in batches using Python generators.
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from user_data table in batches.
    Args:
        batch_size (int): Number of rows to fetch per batch.
    Yields:
        list: A batch of rows from the user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # update if using another MySQL user
            password="root",   # update with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows  # yield a whole batch at once

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return


def batch_processing(batch_size):
    """
    Processes batches of users and yields only those older than 25.
    Args:
        batch_size (int): Number of rows to fetch per batch.
    Yields:
        tuple: A user row where age > 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            user_id, name, email, age = user
            if age > 25:
                yield user
      
