"""
This script is designed to extract IDs and details of events.
Author: Abraham Reines
Date: 2024-03-01
Modified: 2024-03-04 09:53:12
"""

import os
import sqlite3
from datetime import datetime
import logging
import re

# logging configuration
logging.basicConfig(level=logging.DEBUG, filename='query.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
DBPath = os.path.join(script_dir, 'database.db')

# Coordinates and timestamp from the USCG file
USCGCoordinates = (29.65144, -87.77464)  
USCGTime = "02/06/2023 03:29:28"

def detect_Tformat(DBPath):
    """
    This function checks the first record in the timestamp table to determine the time format.
    This function was deemed necessary after many hours of debugging.
    """
    connection, navigator = Attach_yourself_SQLite(DBPath)
    if connection is None or navigator is None:
        return None

    try:
        navigator.execute("SELECT recTime, recDate FROM timestamp LIMIT 1;")
        Tsample, Dsample = navigator.fetchone()
        Dformat = "%m/%d/%Y" if re.match(r'\d{2}/\d{2}/\d{4}', Dsample) else None
        Tformat = "%H:%M:%S" if re.match(r'\d{2}:\d{2}:\d{2}', Tsample) else None

        if Dformat and Tformat:
            return f"{Dformat} {Tformat}"
        else:
            logging.error("Unrecognized date or time format in timestamp table.")
            return None

    except sqlite3.Error as e:
        logging.error(f"An error occurred while detecting the time format: {e}")
        return None
    finally:
        connection.close()

def Attach_yourself_SQLite(DBPath):
    """
    Connection to the SQLite3 database.
    """
    try:
        link = sqlite3.connect(DBPath)
        return link, link.cursor()
    except sqlite3.Error as e:
        logging.error(f"An error occurred connecting to the database: {e}")
        return None, None

def Find_those_eventIDs(DBPath, geography):
    """
    Extract the IDs and details of events which match the geography data.
    """
    connection, navigator = Attach_yourself_SQLite(DBPath)
    if connection is None or navigator is None:
        return

    try:
        # SQL query
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
        WHERE ABS(l.latitude - ?) <= 0.01
          AND ABS(l.longitude - ?) <= 0.01;
        """
        parameters = (geography[0], geography[1])

        # SQL query execution
        navigator.execute(inquiry, parameters)
        EDetails = navigator.fetchall()

        # log and print the results
        if EDetails:
            logging.info(f"Identified event details: {EDetails}")
            print("Identified event details:")
            for record in EDetails:
                print(record)
        else:
            logging.info("No matching events found.")
            print("No matching events found.")

    except sqlite3.Error as error:
        logging.error(f"An error occurred during extraction: {error}")
        print(f"An error occurred during extraction: {error}")

    finally:
        connection.close()

TimeDetection = detect_Tformat(DBPath)

if TimeDetection:
    # extract event IDs and details
    Find_those_eventIDs(DBPath, USCGCoordinates)
else:
    logging.error("Could not detect the time format. Aborting the event details extraction.")