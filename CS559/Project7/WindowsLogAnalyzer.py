import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
import os
import concurrent.futures

class LogFileAnalyzer:
    """
    Class for analyzing Windows log files.

    Attributes:
        Wheres_our_file (str): Path to log file.
        How_many_events (int): Total number of events in log file.
        ProcessIDs (set): Set of unique process IDs found in log file.
        Errors (int): Number of error events in log file.
        Criticals (int): Number of critical events in log file.
    """

    def __init__(self, Wheres_our_file):
        self.Wheres_our_file = Wheres_our_file
        self.How_many_events = 0
        self.ProcessIDs = set()
        self.Errors = 0
        self.Criticals = 0

    def analyze(self):
        """
        Analyzes log file and processes record.

        This method reads the log file using the `evtx` library and processes each record.
        """
        with evtx.Evtx(self.Wheres_our_file) as log:
            for record in log.records():
                try:
                    self.process_these_records(record.xml())
                except Exception as e:
                    # Log error and continue with the next record
                    print(f"Error processing record in {os.path.basename(self.Wheres_our_file)}: {e}")

    def process_these_records(self, xml_content):
        """
        Processes XML of log records.

        Args:
            xml_content (str): XML content of the log record.

        This method extracts information from the XML and updates the class attributes.
        """
        XML_records = ET.fromstring(xml_content)
        self.How_many_events += 1
        for elem in XML_records.iter():
            if elem.tag.endswith('Level'):
                if elem.text == '2':  # ERROR
                    self.Errors += 1
                elif elem.text == '1':  # CRITICAL
                    self.Criticals += 1
            if elem.tag.endswith('Execution'):
                self.ProcessIDs.add(elem.attrib.get('ProcessID'))

    def get_s0me_stats(self):
        """
        Returns some statistics about the log file.

        Returns:
            dict: A dictionary containing the following statistics:
                - 'file_name': Name of the log file.
                - 'Total Events': Total number of events in the log file.
                - 'Process IDs': Set of unique process IDs found in the log file.
                - 'Error Events': Number of error events in the log file.
                - 'Critical Events': Number of critical events in the log file.
        """
        return {
            'file_name': os.path.basename(self.Wheres_our_file),
            'Total Events': self.How_many_events,
            'Process IDs': self.ProcessIDs,
            'Error Events': self.Errors,
            'Critical Events': self.Criticals
        }

def analyze_this(evtx_file):
    log_Wheres_our_file = os.path.join(Absolute_path, evtx_file)
    analyzer = LogFileAnalyzer(log_Wheres_our_file)
    analyzer.analyze()
    return analyzer.get_s0me_stats()

Absolute_path = '/home/reinesaj99/Desktop/'
S0me_stats = '/home/reinesaj99/Desktop/log_statistics.txt'
EVTXFiles = [f for f in os.listdir(Absolute_path) if f.endswith('.evtx')]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(analyze_this, evtx_file): evtx_file for evtx_file in EVTXFiles}
    results = []
    for future in concurrent.futures.as_completed(futures):
        evtx_file = futures[future]
        try:
            result = future.result()
            results.append(result)
        except Exception as exc:
            print(f'{evtx_file} generated an exception: {exc}')

with open(S0me_stats, 'w') as This_came_out:
    for result in results:
        This_came_out.write(f"Stats for {result['file_name']}:\n")
        This_came_out.write(f"Total Events: {result['Total Events']}\n")
        This_came_out.write(f"Process IDs: {', '.join(map(str, result['Process IDs']))}\n")
        This_came_out.write(f"Error Events: {result['Error Events']}\n")
        This_came_out.write(f"Critical Events: {result['Critical Events']}\n\n")

print(f"Statistics for .evtx filesm written to {S0me_stats}")