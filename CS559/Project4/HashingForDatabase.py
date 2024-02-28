import bcrypt
import psycopg2  # or another database adapter suitable for your DB

# Connect to your database
conn = psycopg2.connect('your_db_connection_string')
cursor = conn.cursor()

# Select all plaintext passwords
cursor.execute("SELECT customer_id, password FROM customers")
customers = cursor.fetchall()

# Update each customer with the hashed password
for customer_id, password in customers:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE customers SET password_hash = %s WHERE customer_id = %s", (hashed, customer_id))

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
