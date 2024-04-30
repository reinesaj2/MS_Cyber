import re
import os
from collections import defaultdict
from tabulate import tabulate

# Determine the directory of the current script
Wheres_the_script = os.path.dirname(__file__)

# Log files to analyze
log_files = ['auth.log', 'kern.log', 'syslog']

# Regex pattern to capture the third "column" which may contain application names
Reg_for_apps = re.compile(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+([\w-]+)(?:\[\d+\])?:')
# Function to analyze a single log file
def analyze_these_logs(file_loc):
    how_many_events = defaultdict(int)
    with open(file_loc, 'r') as file:
        for line in file:
            match = Reg_for_apps.match(line)
            if match:
                app_name = match.group(1)
                app_name = app_name.rstrip(':')
                how_many_events[app_name] += 1
    return how_many_events

# Analyze each log file and collect results
results = []
for log_file in log_files:
    file_loc = os.path.join(Wheres_the_script, log_file)
    how_many_events = analyze_these_logs(file_loc)
    applications = ', '.join(sorted(how_many_events.keys()))
    events = ', '.join(str(how_many_events[app]) for app in sorted(how_many_events.keys()))
    results.append([log_file, applications, events])

# Save the results to a .txt file
output_file_loc = os.path.join(Wheres_the_script, 'UbuntuLoggingResults.txt')
with open(output_file_loc, 'w') as output_file:
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

print(f"Results saved to {output_file_loc}")
