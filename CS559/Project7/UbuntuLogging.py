import re
import os
from collections import defaultdict
from tabulate import tabulate

# Determine the directory of the current script
script_dir = os.path.dirname(__file__)

# Log files to analyze
log_files = ['auth.log', 'kern.log', 'syslog']

# Regex pattern to capture the third "column" which may contain application names
app_name_pattern = re.compile(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+([\w-]+)(?:\[\d+\])?:')
# Function to analyze a single log file
def analyze_log_file(file_path):
    app_event_count = defaultdict(int)
    with open(file_path, 'r') as file:
        for line in file:
            match = app_name_pattern.match(line)
            if match:
                app_name = match.group(1)
                app_name = app_name.rstrip(':')
                app_event_count[app_name] += 1
    return app_event_count

# Analyze each log file and collect results
results = []
for log_file in log_files:
    file_path = os.path.join(script_dir, log_file)
    app_event_count = analyze_log_file(file_path)
    applications = ', '.join(sorted(app_event_count.keys()))
    events = ', '.join(str(app_event_count[app]) for app in sorted(app_event_count.keys()))
    results.append([log_file, applications, events])

# Save the results to a .txt file
output_file_path = '/home/reinesaj99/Desktop/UbuntuLoggingResults.txt'
with open(output_file_path, 'w') as output_file:
  for result in results:
    log_file = result[0]
    applications = result[1]
    events = result[2]
    output_file.write(f"{log_file}:\n") 
    output_file.write(f"-"*20+'\n')
    output_file.write(f"Number of events per app:\n")
    for app, event_count in zip(applications.split(', '), events.split(', ')):
      output_file.write(f"{app}: {event_count}\n")
    output_file.write('\n')

print(f"Results saved to {output_file_path}")
