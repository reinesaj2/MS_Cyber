"""
This script is designed to hash customer passwords in the 'customers' table of the 'cs559dbsec' database.
It complies with the reqirements of section 4.6.3.    
Author: Abraham Reines
Modified: 2024-03-04 09:53:12
"""
import os
import bcrypt
import mysql.connector

def Is_there_a_database():
    """
    secure connection to database using mysql.connector
    """
    connection = mysql.connector.connect(
        host='127.0.0.1',
        database='cs559dbsec',
        user='root',
        password='C0d3Pyth0n>L8@N!te'
    )
    print("Securely connected to the database.")
    return connection, connection.cursor()

def Hash_to_columns(Cursor):
    """
    new column 'password_hash' in the 'customers' table
    """
    Cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.columns 
        WHERE table_schema = 'cs559dbsec' 
        AND table_name = 'customers' 
        AND column_name = 'password_hash';
    """)
    if Cursor.fetchone()[0] == 0:
        Cursor.execute("""
            ALTER TABLE customers 
            ADD COLUMN password_hash VARCHAR(60) AFTER password;
        """)
        print("password_hash column added to customers table.")

def Get_to_hashin(Cursor):
    """
    hashing existing plaintext passwords
    """
    Hash_to_columns(Cursor)
    Cursor.execute("""
        SELECT loginName, password 
        FROM customers 
        WHERE password_hash IS NULL OR password_hash = '';
    """)
    for loginName, OriginalPasswordword in Cursor:
        password_hash = bcrypt.hashpw(OriginalPasswordword.encode('utf-8'), bcrypt.gensalt())
        Cursor.execute("""
            UPDATE customers 
            SET password_hash = %s 
            WHERE loginName = %s;
        """, (password_hash, loginName))

def Lets_comply(Cursor):
    """
    Prints hashes of all customer passwords
    """
    Cursor.execute("""
        SELECT loginName, password_hash 
        FROM customers;
    """)
    print("Printing all hashed passwords:")
    for loginName, password_hash in Cursor:
        print(f"Login Name: {loginName} | Hash: {password_hash}")

def Secure_them_passwords():
    """
    Basically, the main function
    """
    DBConnection, Cursor = Is_there_a_database()
    try:
        Get_to_hashin(Cursor)
        DBConnection.commit()
        print("All customer password hashes updated successfully.")
        Lets_comply(Cursor)
    finally:
        if DBConnection.is_connected():
            Cursor.close()
            DBConnection.close()
            print("Database connection securely closed.")

if __name__ == "__main__":
    Secure_them_passwords()