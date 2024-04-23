import logging
from Evtx.Evtx import Evtx
from EventRecordWriter import EventRecordWriter

class EVTXConverter:
    """EVTX file to XML format."""
    def __init__(self, evtx_path, xml_path):
        self.evtx_path = evtx_path
        self.xml_path = xml_path

    def convert(self, encodings=('utf-8', 'utf-16-le')):
        """
        EVTX file to XML format using tested encodings:

        Args:
            encodings (tuple, optional): A tuple of encodings to be tried in order. ('utf-8', 'utf-16-le').

        Raises:
            Exception: If the conversion fails for all attempted encodings.

        Returns:
            None
        """
        for encoding in encodings:
            try:
                with Evtx(self.evtx_path) as evtx, open(self.xml_path, 'w', encoding=encoding) as xml_output:
                    writer = EventRecordWriter(evtx, xml_output)
                    writer.write_records(encoding)
                    logging.info(f"Successfully decoded {self.evtx_path} with {encoding}.")
                    return  # Exit after successful conversion
            except UnicodeDecodeError as error:
                logging.warning(f"Failed to decode {self.evtx_path} with {encoding}. Trying next... Error: {error}")

        # If all encodings fail, log an error
        logging.error(f"Failed to decode {self.evtx_path} with the encodings you thought would work")
        raise Exception(f"Conversion failed for these encodings")