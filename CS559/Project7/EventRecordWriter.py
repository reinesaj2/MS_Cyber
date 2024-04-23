import logging

class EventRecordWriter:
    """EVTX event records to XML file."""
    def __init__(self, evtx, xml_output):
        self.evtx = evtx
        self.xml_output = xml_output

    def write_records(self, encoding):
        """
        records from the evtx file to an XML file

        Args:
            encoding (str): The encoding for decoding the records.

        Returns:
            None
        """
        self.xml_output.write("<Events>\n")
        for record in self.evtx.records():
            try:
                self.xml_output.write(record.xml() + "\n")
            except UnicodeDecodeError as e:
                logging.error(f"Skipping a record due to a UnicodeDecodeError with {encoding}: {e}. Too bad. Record: {record.xml()}")
                continue  # Skip this record and continue 
        self.xml_output.write("</Events>\n")
