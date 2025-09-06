#!/usr/bin/python3
"""
Module: 3-avg_age
Objective: Compute average user age using a generator without loading all data into memory.
"""

import seed


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database.
    Yields:
        int: user age
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes average age using the stream_user_ages generator.
    Prints result in required format.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
