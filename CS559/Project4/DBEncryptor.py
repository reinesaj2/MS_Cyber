"""
This script is designed to encrypt sensitive data in the 'customers' table of the 'cs559dbsec' database.
Author: Abraham Reines
Modified: 2024-03-04 10:32:10
"""

import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

DBPassword = 'C0d3Pyth0n>L8@N!te'
DBHost = '127.0.0.1'
DBName = 'cs559dbsec'

# create a connection to the database
def We_should_connect(password, host, database):
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

# alter the table and encrypt data
def Encryption_is_necessary(connection, ciphers):
    try:
        cursor = connection.cursor()

        # Alter table to use BLOB...
        altering_table = """
        ALTER TABLE customers 
            MODIFY ssn BLOB,
            MODIFY creditCardNumber BLOB;
        """
        cursor.execute(altering_table)
        print("Table structure altered to accommodate encrypted data.")

        which_query = "SELECT loginName, ssn, creditCardNumber FROM customers;"
        cursor.execute(which_query)
        customers = cursor.fetchall()
        
        # Encrypt existing data...
        for loginName, ssn, creditCardNumber in customers:
            SSNEncrypted = ciphers.encrypt(ssn if isinstance(ssn, bytes) else ssn.encode())
            CCNEncrypted = ciphers.encrypt(creditCardNumber if isinstance(creditCardNumber, bytes) else creditCardNumber.encode())
            update_query = """
            UPDATE customers 
            SET ssn = %s, creditCardNumber = %s WHERE loginName = %s;
            """
            cursor.execute(update_query, (SSNEncrypted, CCNEncrypted, loginName))
            print(f"loginName: {loginName}, Encrypted SSN: {SSNEncrypted}, Encrypted Credit Card: {CCNEncrypted}")

        connection.commit()
        cursor.close()
        print("Encryption of data completed and printed.")
    except Error as err:
        print(f"Error: '{err}'")

if __name__ == "__main__":
    conn = We_should_connect(DBPassword, DBHost, DBName)
    
    key = Fernet.generate_key()
    ciphers = Fernet(key) #NOTE: in a professional setting, this key should be stored securely and not hardcoded in the script

    if conn is not None:
        Encryption_is_necessary(conn, ciphers)
        conn.close()
