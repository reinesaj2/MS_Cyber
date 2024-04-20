import os
import logging
from concurrent.futures import ProcessPoolExecutor
from Evtx.Evtx import Evtx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("conversion.log"),  # Log to a file
        logging.StreamHandler()  # Log to standard output
    ]
)

def write_records(evtx, xml_output, encoding):
    """Writes the records from an EVTX file to an XML file with a specific encoding."""
    xml_output.write("<Events>\n")
    for record in evtx.records():
        try:
            xml_output.write(record.xml())
            xml_output.write("\n")
        except UnicodeDecodeError as e:
            logging.error(f"Encountered a UnicodeDecodeError with {encoding}: {e}")
            raise  # Re-raise to handle in the calling function
    xml_output.write("</Events>\n")

def convert_evtx_to_xml(evtx_path, xml_path):
    """Attempts to convert an EVTX file to an XML file using two different encodings."""
    try:
        with Evtx(evtx_path) as evtx, open(xml_path, 'w', encoding='utf-8') as xml_output:
            write_records(evtx, xml_output, 'utf-8')
            logging.info(f"Successfully decoded {os.path.basename(evtx_path)} with utf-8.")
    except UnicodeDecodeError as utf8_error:
        logging.warning(f"Failed utf-8 conversion for {os.path.basename(evtx_path)}. Trying utf-16-le...")
        try:
            with Evtx(evtx_path) as evtx, open(xml_path, 'w', encoding='utf-16-le') as xml_output:
                write_records(evtx, xml_output, 'utf-16-le')
                logging.info(f"Successfully decoded {os.path.basename(evtx_path)} with utf-16-le.")
        except UnicodeDecodeError as utf16_error:
            logging.error(f"Failed to decode {os.path.basename(evtx_path)} with both utf-8 and utf-16-le. Error details: utf-8: {utf8_error}, utf-16-le: {utf16_error}")

def worker(file_tuple):
    """Worker function to convert files passed as tuple pairs of paths."""
    convert_evtx_to_xml(*file_tuple)

def convert_files(script_dir):
    """Finds and converts all EVTX files in the specified directory to XML files."""
    files_to_convert = [(os.path.join(script_dir, filename), os.path.join(script_dir, f"{os.path.splitext(filename)[0]}.xml"))
                        for filename in os.listdir(script_dir) if filename.lower().endswith('.evtx')]
    
    with ProcessPoolExecutor() as executor:
        # Map the worker function to the files
        executor.map(worker, files_to_convert)

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    convert_files(script_dir)
    logging.info("All conversions completed.")
