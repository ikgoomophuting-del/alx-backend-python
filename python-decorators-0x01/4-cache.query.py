#!/usr/bin/env python3
import sqlite3
import functools

# in-memory cache
query_cache = {}

# decorator to manage database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# decorator to cache queries
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # extract query string (assume query is passed as kwarg or arg)
        query = kwargs.get("query")
        if query is None and len(args) > 1:
            query = args[1]  # conn is args[0], query should be args[1]
        
        if query in query_cache:
            print("⚡ Using cached result for query:", query)
            return query_cache[query]
        
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("✅ Query executed and cached:", query)
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example run
if __name__ == "__main__":
    # First call executes query
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("Users:", users)

    # Second call should use cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Users again (from cache):", users_again)
  
