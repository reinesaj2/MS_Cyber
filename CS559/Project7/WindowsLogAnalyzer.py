import xml.etree.ElementTree as ET
from collections import Counter
import logging
import os

class XMLWindowsLogAnalyzer:
    """
    This class analyzes converted .xml Windows log/event files.
    It computes the total number of events, the IDs of processes that generated the events,
    and tallies the number of ERROR and CRITICAL events.
    
    Author: ByteMeXpert
    Date: April 2024
    """
    
    def __init__(self, spectralPathway):
        """
        Initialize the XMLWindowsLogAnalyzer with the path to the .xml log file.
        
        Parameters:
            spectralPathway (str): Path to the .xml log file.
        """
        self.spectralPathway = spectralPathway
        self.processEventCounter = Counter()
        self.celestialEventTotal = 0
        self.errorEventAnomaly = 0  # Assuming Level 2 indicates ERROR events
        self.criticalEventAnomaly = 0  # Assuming Level 1 indicates CRITICAL events
        self.namespaceMap = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    
    def executeSpectralAnalysis(self):
        """
        Executes the analysis on the .xml log file, iterating over each event.
        """
        tree = ET.parse(self.spectralPathway)
        root = tree.getroot()
        for event in root.findall('ns:Event', self.namespaceMap):
            self.celestialEventTotal += 1
            self.processEventSpectrum(event)
    
    def processEventSpectrum(self, event):
        """
        Processes a single event element, extracting information and updating counters.
        
        Parameters:
            event (xml.etree.ElementTree.Element): An event element to analyze.
        """
        with open(self.file_path, 'r') as file:
            xml_content = file.read()
        events = ET.fromstring(xml_content)
        
        for event in events.findall('.//ns:Event', self.ns):
            self.total_events += 1
            level = event.find('.//ns:Level', self.ns)

            # Assuming non-namespaced ErrorCode element, adjust as necessary.
            error_code = event.find('.//ErrorCode')

            # Assuming the Level element text '2' indicates an ERROR
            if level is not None and level.text == '2':
                self.error_events += 1
            
            # Assuming Level '1' is CRITICAL
            elif level is not None and level.text == '1':
                self.critical_events += 1

            # Count an error if there's an ErrorCode element and its value is not '0x0'
            if error_code is not None and error_code.text != '0x0':
                self.error_events += 1
            
            execution = event.find('.//ns:Execution', self.ns)
            if execution is not None:
                process_id = execution.attrib.get('ProcessID')
                if process_id:
                    self.process_ids[process_id] += 1
    
    def generateSpectralReport(self):
        """
        Generates a formatted report of the analysis, suitable for inclusion in a final document.
        
        Returns:
            str: The formatted report string.
        """
        process_id_list = ', '.join(f"PID {pid}: {count}" for pid, count in self.processEventCounter.items())
        statistics = (
            f"Log File: {os.path.basename(self.spectralPathway)}\n"
            f"Total Events: {self.celestialEventTotal}\n"
            f"Error Events: {self.errorEventAnomaly}\n"
            f"Critical Events: {self.criticalEventAnomaly}\n"
            f"Process IDs: {process_id_list}\n"
        )
        return statistics

# Example usage:
analyzer = XMLWindowsLogAnalyzer('/home/reinesaj99/Desktop/DESKTOP-KUHNMLA_Setup_log.xml')
analyzer.executeSpectralAnalysis()
report = analyzer.generateSpectralReport()
print(report)
