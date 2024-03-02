import os
import sqlite3
from datetime import datetime
import logging
import re

# Author: Reines Aj99
# Date: 2024-03-01

# Setup logging configuration
logging.basicConfig(level=logging.DEBUG, filename='query.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Compute the directory path for the database file
database_path = os.path.join(script_dir, 'database.db')

# Coordinates and timestamp from the USCG file
uscg_coordinates = (29.65144, -87.77464)  
uscg_time = "02/06/2023 03:29:28"

def detect_time_format(db_path):
    """
    Detect the time format used in the timestamp table of the database.
    
    Parameters:
    db_path (str): The file path to the SQLite database file.
    
    Returns:
    str: The detected time format string, or None if the format cannot be detected.
    """
    connection, navigator = establish_sqlite3_linkage(db_path)
    if connection is None or navigator is None:
        return None

    try:
        navigator.execute("SELECT recTime, recDate FROM timestamp LIMIT 1;")
        sample_time, sample_date = navigator.fetchone()
        # Use regular expression to check for MM/DD/YYYY format
        date_format = "%m/%d/%Y" if re.match(r'\d{2}/\d{2}/\d{4}', sample_date) else None
        # Use regular expression to check for HH:MM:SS format
        time_format = "%H:%M:%S" if re.match(r'\d{2}:\d{2}:\d{2}', sample_time) else None

        if date_format and time_format:
            return f"{date_format} {time_format}"
        else:
            logging.error("Unrecognized date or time format in timestamp table.")
            return None

    except sqlite3.Error as e:
        logging.error(f"An error occurred while detecting the time format: {e}")
        return None
    finally:
        connection.close()

def establish_sqlite3_linkage(db_path):
    """
    Establish a connection to the SQLite3 database.
    
    Parameters:
    db_path (str): The file path to the SQLite database file.
    
    Returns:
    tuple: A tuple containing the connection and cursor objects, respectively.
    """
    try:
        link = sqlite3.connect(db_path)
        return link, link.cursor()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while connecting to the database: {e}")
        return None, None

def extract_eligible_event_ids(db_path, geographic_point):
    """
    Extract the IDs and details of events that match the geographic criteria.
    
    Parameters:
    db_path (str): The file path to the SQLite database file.
    geographic_point (tuple): A tuple containing the latitude and longitude.
    """
    connection, navigator = establish_sqlite3_linkage(db_path)
    if connection is None or navigator is None:
        return

    try:
        # Formulate the SQL query with placeholders for parameters
        inquiry = """
        SELECT DISTINCT e.id,
               l.latitude,
               l.longitude,
               l.elevation,
               t.recTime AS RecordedTime,
               t.recDate AS RecordedDate,
               ao.transcript,
               ao.contentUrl,
               ao.description,
               ao.name AS AudioName,
               ao.encodingFormat
        FROM event e
        JOIN location l ON e.location_id = l.id
        JOIN timestamp t ON e.timestamp_id = t.id
        JOIN audio_object ao ON e.audio_object_id = ao.id
        WHERE ABS(l.latitude - ?) <= 0.1
          AND ABS(l.longitude - ?) <= 0.1;
        """

        # Prepare parameters for the SQL query
        parameters = (geographic_point[0], geographic_point[1])

        # Execute the SQL query with the provided parameters
        navigator.execute(inquiry, parameters)
        events_details = navigator.fetchall()

        # Output the IDs and details of valid events
        if events_details:
            logging.info(f"Identified event details: {events_details}")
            print("Identified event details:")
            for record in events_details:
                print(record)
        else:
            logging.info("No matching events found.")
            print("No matching events found.")

    except sqlite3.Error as error:
        logging.error(f"An error occurred during event details extraction: {error}")
        print(f"An error occurred during event details extraction: {error}")

    finally:
        # Clean-up the database connection
        connection.close()

# Invoke the function to detect the time format
detected_time_format = detect_time_format(database_path)

# Proceed only if a time format was successfully detected
if detected_time_format:
    # Invoke the function to extract eligible event IDs and details
    extract_eligible_event_ids(database_path, uscg_coordinates)
else:
    logging.error("Could not detect the time format. Aborting the event details extraction.")