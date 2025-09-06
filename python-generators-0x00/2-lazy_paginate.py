#!/usr/bin/python3
"""
Module: 2-lazy_paginate
Objective: Implement a lazy pagination generator that fetches user data page by page.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from user_data.
    Args:
        page_size (int): number of rows per page.
        offset (int): starting point in table.
    Returns:
        list of dicts: rows from user_data.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches users page by page.
    Args:
        page_size (int): number of rows per page.
    Yields:
        list of dicts: a page of users.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
