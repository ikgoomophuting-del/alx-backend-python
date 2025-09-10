#!/usr/bin/env python3
import time
import sqlite3
import functools

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


# decorator to retry on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            # if all attempts fail, raise the last exception
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example run
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print("✅ Users fetched:", users)
    except Exception as e:
        print(f"❌ All retries failed: {e}")
