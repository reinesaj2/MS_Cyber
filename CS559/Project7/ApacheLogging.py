import os
import re
from collections import defaultdict

# Author: Abraham Reines
# Date: April 22, 2024

# Determine directory of current script
script_dir = os.path.dirname(__file__)
# Compute directory path for logs
log_dir = os.path.join(script_dir, '')

# Define a function to parse log file
def analyze_log_file(log_file_path):
  """
  Parses given Apache log file and compiles statistics about IP addresses and number of events.
  
  Args:
    log_file_path (str): path to log file.
  
  Returns:
    dict: A dictionary with IP addresses as keys and a list of event counts as values.
  """
  ip_event_count = defaultdict(lambda: [0, 0])  # Dictionary to store IP: [individual file event count, total event count]
  total_events = 0
  
  # Regular expression to match IP addresses at start of log line
  ip_regex = re.compile(r'^(\d+\.\d+\.\d+\.\d+)')
  
  try:
    with open(log_file_path, 'r') as file:
      for line in file:
        ip_match = ip_regex.match(line)
        if ip_match:
          ip_address = ip_match.group(1)
          ip_event_count[ip_address][0] += 1
          total_events += 1
          
    # Update total event counts
    for ip in ip_event_count:
      ip_event_count[ip][1] = total_events
      
    return ip_event_count
  except FileNotFoundError:
    print(f"log file {log_file_path} was not found.")
    return {}

# Function to display results
def display_results(ip_event_count, log_file_path):
  """
  Displays results of log analysis in specified tabular format.
  Saves results to a text file with same name as log file.
  
  Args:
    ip_event_count (dict): dictionary containing IP event counts.
    log_file_path (str): path to log file.
  """
  result_file_path = log_file_path.replace('.7', '_results.txt')
  with open(result_file_path, 'w') as file:
    file.write("{:<20} {:<40} {:<15}\n".format('List of IP Addresses', '# of events in each log file respectively', 'Combined # of events'))
    for ip, counts in ip_event_count.items():
      file.write("{:<20} {:<40} {:<15}\n".format(ip, counts[0], counts[1]))
  print(f"Results saved to {result_file_path}")

# Path to log file
log_files = [file for file in os.listdir(log_dir) if file.endswith('.7')]
for log_file in log_files:
  log_file_path = os.path.join(log_dir, log_file)
  # Analyze log file and display results
  ip_event_counts = analyze_log_file(log_file_path)
  display_results(ip_event_counts, log_file_path)
