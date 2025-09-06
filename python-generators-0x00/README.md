# Python Generators - ALX Project

## Description
This project demonstrates how to use **Python generators** to stream data from a MySQL database without loading everything into memory at once.

We set up a database `ALX_prodev`, create a table `user_data`, insert data from a CSV file, and implement a generator that streams rows one by one.

---

## Files
- **seed.py** → contains database setup and generator functions.
- **0-main.py** → test script that runs the setup and streams rows.
- **user_data.csv** → sample dataset used to populate the table.
- **README.md** → project documentation.

---

## Setup
1. Install requirements:
   ```bash
   pip install mysql-connector-python
   ```

2. Run the test script:

./0-main.py

3. Expected Output

connection successful
Table user_data created successfully
Database ALX_prodev is present

Streaming rows one by one:
('uuid1', 'Alice', 'alice@email.com', 23)
('uuid2', 'Bob', 'bob@email.com', 45)
...
