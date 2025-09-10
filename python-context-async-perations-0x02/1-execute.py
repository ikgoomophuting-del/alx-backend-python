#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """Custom context manager to execute a query and return results"""

    def __init__(self, query, params=None, db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else []
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # open connection and execute query
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # commit if no exception, rollback otherwise
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(query, (25,)) as results:
        print("Users older than 25:", results)
      
