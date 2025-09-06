#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")
        cursor.close()

        # ✅ Stream rows using generator
        print("\nStreaming rows one by one:")
        for row in seed.stream_rows(connection):
            print(row)


  #!/usr/bin/python3
stream = __import__('0-stream_users').stream_users

for i, row in enumerate(stream()):
    print(row)
    if i == 4:  # just show first 5 rows
        break
    
