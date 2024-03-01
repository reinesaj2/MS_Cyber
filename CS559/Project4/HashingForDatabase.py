import os
import bcrypt
import mysql.connector

# Determine the directory of the current script
script_dir = os.path.dirname(__file__)
# Compute the directory path
dir_path = os.path.join(script_dir, '')

def connect_to_database():
    """
    Establishes a connection to the database and returns the connection and cursor.
    Author: ByteMeXpert
    Date: 2024-02-28
    """
    conn = mysql.connector.connect(
        host='127.0.0.1',
        database='cs559dbsec',
        user='webuser',
        password='N3wStr0ng!Passw0rd'
    )
    print("Connected to the database.")
    return conn, conn.cursor()

def check_and_alter_table_to_add_password_hash(cursor):
    """
    Checks for the existence of the password_hash column and adds it if it does not exist.
    Author: ByteMeXpert
    Date: 2024-02-28
    """
    try:
        # Check if the password_hash column already exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.columns 
            WHERE table_schema = 'cs559dbsec' 
            AND table_name = 'customers' 
            AND column_name = 'password_hash';
        """)
        if cursor.fetchone()[0] == 0:
            # If the password_hash column does not exist, add it
            cursor.execute("""
                ALTER TABLE customers 
                ADD password_hash VARCHAR(60);
            """)
            print("Added password_hash column to customers table.")
        else:
            print("password_hash column already exists in customers table.")
    except mysql.connector.Error as err:
        print("Error occurred: {}".format(err))

def update_customer_password_hashes(cursor):
    """
    Hashes plaintext passwords stored in the customers table and updates the table with the hashed passwords.
    Author: ByteMeXpert
    Date: 2024-02-28
    """
    try:
        # Add password_hash column to the customers table
        check_and_alter_table_to_add_password_hash(cursor)

        # Select customer IDs and plaintext passwords
        cursor.execute("SELECT loginName, password FROM customers WHERE password_hash IS NULL OR password_hash = ''")
        customers = cursor.fetchall()
        if customers:
            print(f"Updating password hashes for {len(customers)} customers.")

        # Hash each password and update the database
        for loginName, password in customers:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE customers SET password_hash = %s WHERE loginName = %s", (hashed, loginName))
            print(f"Updated password hash for customer: {loginName}")

        if not customers:
            print("No customers to update.")

    except mysql.connector.Error as err:
        print("Error occurred: {}".format(err))

def main():
    """
    The main execution method for the script.
    Author: ByteMeXpert
    Date: 2024-02-28
    """
    conn, cursor = connect_to_database()
    try:
        update_customer_password_hashes(cursor)
        conn.commit()
        print("All password hashes updated successfully.")
    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
