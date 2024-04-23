import os
import logging
from concurrent.futures import ProcessPoolExecutor
from EVTXConverter import EVTXConverter

def setup_logging():
    """global logging setup"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("conversion.log"),
            logging.StreamHandler()
        ]
    )

class ConversionManager:
    """conversion process of multiple EVTX files concurrently"""
    def __init__(self, directory):
        self.directory = directory

    def convert_files(self):
            """
            Converts all .evtx files in the relative directory to .xml format.

            Returns:
                None
            """
            files_to_convert = [
                (os.path.join(self.directory, f), os.path.join(self.directory, f"{os.path.splitext(f)[0]}.xml"))
                for f in os.listdir(self.directory) if f.lower().endswith('.evtx')
            ]

            with ProcessPoolExecutor() as executor:
                executor.map(self.worker, files_to_convert)

    @staticmethod
    def worker(file_tuple):
        """
        Process the file tuple using the EVTXConverter: 

        Args:
            file_tuple (tuple): A tuple containing the file information.

        Raises:
            Exception: If there is an error processing the file.

        Returns:
            None
        """
        try:
            converter = EVTXConverter(*file_tuple)
            converter.convert()
        except Exception as e:
            logging.error(f"Error processing {file_tuple[0]}: {e}")

if __name__ == "__main__":
    setup_logging()
    manager = ConversionManager(os.path.dirname(os.path.realpath(__file__)))
    manager.convert_files()
    logging.info("All conversions completed.")
