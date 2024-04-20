import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
import os
import concurrent.futures

class LogFileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.total_events = 0
        self.process_ids = set()
        self.error_count = 0
        self.critical_count = 0

    def analyze(self):
        with evtx.Evtx(self.file_path) as log:
            for record in log.records():
                try:
                    self.process_record(record.xml())
                except Exception as e:
                    # Log the error and continue with the next record
                    print(f"Error processing a record in {os.path.basename(self.file_path)}: {e}")

    def process_record(self, xml_content):
        xml_record = ET.fromstring(xml_content)
        self.total_events += 1
        for elem in xml_record.iter():
            if elem.tag.endswith('Level'):
                if elem.text == '2':  # ERROR
                    self.error_count += 1
                elif elem.text == '1':  # CRITICAL
                    self.critical_count += 1
            if elem.tag.endswith('Execution'):
                self.process_ids.add(elem.attrib.get('ProcessID'))

    def get_statistics(self):
        return {
            'file_name': os.path.basename(self.file_path),
            'Total Events': self.total_events,
            'Process IDs': self.process_ids,
            'Error Events': self.error_count,
            'Critical Events': self.critical_count
        }

def analyze_file(evtx_file):
    log_file_path = os.path.join(directory_path, evtx_file)
    analyzer = LogFileAnalyzer(log_file_path)
    analyzer.analyze()
    return analyzer.get_statistics()

directory_path = '/home/reinesaj99/Desktop/'
output_file_path = '/home/reinesaj99/Desktop/log_statistics.txt'
evtx_files = [f for f in os.listdir(directory_path) if f.endswith('.evtx')]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(analyze_file, evtx_file): evtx_file for evtx_file in evtx_files}
    results = []
    for future in concurrent.futures.as_completed(futures):
        evtx_file = futures[future]
        try:
            result = future.result()
            results.append(result)
        except Exception as exc:
            print(f'{evtx_file} generated an exception: {exc}')

with open(output_file_path, 'w') as output_file:
    for result in results:
        output_file.write(f"Stats for {result['file_name']}:\n")
        output_file.write(f"Total Events: {result['Total Events']}\n")
        output_file.write(f"Process IDs: {', '.join(map(str, result['Process IDs']))}\n")
        output_file.write(f"Error Events: {result['Error Events']}\n")
        output_file.write(f"Critical Events: {result['Critical Events']}\n\n")

print(f"Statistics for all .evtx files have been written to {output_file_path}")
