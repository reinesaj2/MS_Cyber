"""
This script is used to grant privileges to the users of the database. 
Author: Abraham Reines
Modified: 2024-03-04 09:53:12
"""
import mysql.connector
from mysql.connector import Error

DBPassword = 'C0d3Pyth0n>L8@N!te'
DBHost = '127.0.0.1'
DBName = 'cs559dbsec'

# create a connection to database
def Lets_connect(password, host, database):
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

# execute a query
def Lets_execute(connection, query, user):
    cursor = connection.cursor()
    try:
        for result in cursor.execute(query, multi=True):
            pass  
        connection.commit()
        print(f"Query successful for {user}")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()

# Connect to the database
connection = Lets_connect(DBPassword, DBHost, DBName)

if connection is not None and connection.is_connected():
    # SQL commands to grant privileges
    backenduser_needs_privileges = "GRANT ALL PRIVILEGES ON cs559dbsec.* TO 'backenduser'@'localhost';"
    webuser_select_privileges = "GRANT SELECT ON cs559dbsec.restrictedcustomers TO 'webuser'@'localhost';"
    webuser_insert_privileges = "GRANT INSERT ON cs559dbsec.queries TO 'webuser'@'localhost';"
    dbmanager_needs_privileges = "GRANT ALL PRIVILEGES ON *.* TO 'dbmanager'@'localhost' WITH GRANT OPTION;"

    # Execute the queries
    Lets_execute(connection, backenduser_needs_privileges, "backenduser")
    Lets_execute(connection, webuser_select_privileges, "webuser for SELECT")
    Lets_execute(connection, webuser_insert_privileges, "webuser for INSERT")
    Lets_execute(connection, dbmanager_needs_privileges, "dbmanager")

    # Close the connection
    connection.close()
else:
    print("Failed to connect to the database.")

