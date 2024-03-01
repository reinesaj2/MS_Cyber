import mysql.connector
from mysql.connector import Error

# Replace the following variables with your actual details.
db_password = 'C0d3Pyth0n>L8@N!te'
db_host = '127.0.0.1'
db_name = 'cs559dbsec'

# Function to create a connection to the database
def create_db_connection(password, host, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            user='root',
            password=password,
            host=host,
            database=database
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

# Function to execute a query
def execute_query(connection, query, user):
    cursor = connection.cursor()
    try:
        for result in cursor.execute(query, multi=True):
            pass  # You need to iterate through the result even if you don't do anything with it
        connection.commit()
        print(f"Query successful for {user}")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()

# Connect to the database
connection = create_db_connection(db_password, db_host, db_name)

# Check if the connection was successful before proceeding
if connection is not None and connection.is_connected():
    # SQL commands to grant privileges
    backenduser_privileges = "GRANT ALL PRIVILEGES ON cs559dbsec.* TO 'backenduser'@'localhost';"
    webuser_select_privileges = "GRANT SELECT ON cs559dbsec.restrictedcustomers TO 'webuser'@'localhost';"
    webuser_insert_privileges = "GRANT INSERT ON cs559dbsec.queries TO 'webuser'@'localhost';"
    dbmanager_privileges = "GRANT ALL PRIVILEGES ON *.* TO 'dbmanager'@'localhost' WITH GRANT OPTION;"

    # Execute the queries one by one
    execute_query(connection, backenduser_privileges, "backenduser")
    execute_query(connection, webuser_select_privileges, "webuser for SELECT")
    execute_query(connection, webuser_insert_privileges, "webuser for INSERT")
    execute_query(connection, dbmanager_privileges, "dbmanager")

    # Close the connection
    connection.close()
else:
    print("Failed to connect to the database. Please check your credentials and ensure the MySQL service is running.")

