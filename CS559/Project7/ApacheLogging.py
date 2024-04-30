import os
import re
from collections import defaultdict

# Author: Abraham Reines
# Date: April 22, 2024

# Determine directory of current script
Wheres_that_script = os.path.dirname(__file__)
# Compute directory path for logs
Dir_loc = os.path.join(Wheres_that_script, '')

# Define a function to parse log file
def analyze_s0me_logs(Wheres_those_logs):
  """
  Parses Apache log file; compiles statistics for IP addresses and number of events.
  
  Args:
    Wheres_those_logs (str): path to log file.
  
  Returns:
    dict: dictionary with IP addresses as keys and a list of event counts as values.
  """
  How_many_IPs = defaultdict(lambda: [0, 0])  # Dictionary to store IP
  total_events = 0
  
  # Regex match IP addresses
  RegexIPs = re.compile(r'^(\d+\.\d+\.\d+\.\d+)')
  
  try: 
    with open(Wheres_those_logs, 'r', encoding='ISO-8859-1') as file:
      for line in file:
        Found_match = RegexIPs.match(line)
        if Found_match:
          LocalizeIPs = Found_match.group(1)
          How_many_IPs[LocalizeIPs][0] += 1
          total_events += 1
          
    # Update total event counts
    for ip in How_many_IPs:
      How_many_IPs[ip][1] = total_events
      
    return How_many_IPs
  except FileNotFoundError:
    print(f"log file {Wheres_those_logs} was not found.")
    return {}

def Show_results(How_many_IPs, Wheres_those_logs):
  """
  Displays results of log analysis
  
  Args:
    How_many_IPs (dict): containing IP event counts.
    Wheres_those_logs (str): path to log file.
  """
  result_file_path = Wheres_those_logs.replace('.7', '_results.txt')
  with open(result_file_path, 'w') as file:
    file.write("{:<20} {:<40} {:<15}\n".format('List of IP Addresses', '# of events in each log file respectively', 'Combined # of events'))
    for ip, counts in How_many_IPs.items():
      file.write("{:<20} {:<40} {:<15}\n".format(ip, counts[0], counts[1]))
  print(f"Results saved to {result_file_path}")

# Path to log file
Files_with_logs = [file for file in os.listdir(Dir_loc) if file.endswith('.7')]
for log_file in Files_with_logs:
  Wheres_those_logs = os.path.join(Dir_loc, log_file)
  # Analyze log file and display results
  How_many_IPs = analyze_s0me_logs(Wheres_those_logs)
  Show_results(How_many_IPs, Wheres_those_logs)
  print("Done!")
