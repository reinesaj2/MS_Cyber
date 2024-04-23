import os

import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
import concurrent.futures

# Author: Abraham Reines
# Date: April 22, 2024

class WinHacked:
  def __init__(self, file_path):
    self.file_path = file_path
    self.suspicious_events = {
      '4625': [],
      '4624': [],
      '4720': [],
      '4672': [],
      '4728': [],
      '7022': [],
      '7023': [],
      '7031': [],
      '7034': [],
      '1102': []
    }

  def analyze(self):
    with evtx.Evtx(self.file_path) as log:
      with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for record in log.records():
          try:
            future = executor.submit(self.process_record, record.xml())
            futures.append(future)
          except Exception as e:
            print(f"Error submitting task: {e}")
        
        for future in concurrent.futures.as_completed(futures):
          try:
            event_id, event_data = future.result()
            if event_id in self.suspicious_events:
              self.suspicious_events[event_id].append(event_data)
          except Exception as e:
            print(f"Error processing record: {e}")

  def process_record(self, xml_content):
    xml_record = ET.fromstring(xml_content)
    event_data = {}
    
    for elem in xml_record.iter():
      if elem.tag.endswith('EventID'):
        event_id = elem.text
      if elem.tag.endswith('TimeCreated'):
        event_data['TimeCreated'] = elem.attrib.get('SystemTime')
      if elem.tag.endswith('IpAddress'):
        event_data['IpAddress'] = elem.text
      if elem.tag.endswith('TargetUserName'):
        event_data['TargetUserName'] = elem.text

    return event_id, event_data

  def report_suspicious_events(self):
    for event_id, events in self.suspicious_events.items():
      if events:
        print(f"Event ID {event_id} has {len(events)} occurrences.")
        # Add any specific output or logging you want here for each event
        file_name = f"events_{event_id}.txt"
        with open(file_name, 'w') as file:
          for event in events:
            file.write(str(event) + '\n')
        print(f"Saved {len(events)} occurrences of Event ID {event_id} to {file_name}")


# Determine directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Compute directory path for logs
evtx_directory = os.path.join(script_dir, '')
# Example usage
for filename in os.listdir(evtx_directory):
  if filename.endswith('.evtx'):
    log_file_path = os.path.join(evtx_directory, filename)
    analyzer = WinHacked(log_file_path)
    analyzer.analyze()
    analyzer.report_suspicious_events()
