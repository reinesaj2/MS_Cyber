import os
import re
from datetime import datetime

# Constants for pattern matching
KERNEL_TIMEKEEPING_PATTERN = (
    r'(Sep \d+ \d+:\d+:\d+) '  # Date and time
    r'([\w-]+) '  # Hostname
    r'kernel: '  # Kernel log indicator
    r'\[\d+\.\d+\] '  # Kernel time
    r'(.+)'  # The message
)
READ_BACK_DELAY_THRESHOLD = 500000  # Define the threshold for unusual delay in nanoseconds
CPU_REGISTER_STATE_PATTERN = r'RDX: .+ RSI: .+ RDI: .+'  # Regex pattern for CPU register state messages

def is_unusual_timekeeping_delay(message):
    """Check if the kernel timekeeping message contains a high read-back delay."""
    try:
        delay_part = message.split('read-back delay of ')[-1]
        delay_numbers = re.findall(r'\d+', delay_part)
        if delay_numbers:
            delay_value = int(delay_numbers[0])
            return delay_value > READ_BACK_DELAY_THRESHOLD
        else:
            return False
    except IndexError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def is_cpu_register_state_message(message):
    """Check if the message reports CPU register states."""
    return re.search(CPU_REGISTER_STATE_PATTERN, message) is not None

def parse_kernel_log_entry(entry):
    """Parse a single kernel log entry for Date, Hostname, and Message."""
    match = re.match(KERNEL_TIMEKEEPING_PATTERN, entry)
    if match:
        return {
            'date_time': match.group(1),
            'hostname': match.group(2),
            'message': match.group(3),
        }
    return None

def analyze_kernel_log_file(file_path):
    """Analyze a kernel log file for unusual timekeeping messages and CPU register state messages."""
    unusual_entries = []
    cpu_register_state_entries = []

    with open(file_path, 'r') as log_file:
        for line in log_file:
            log_entry = parse_kernel_log_entry(line)
            if log_entry:
                if is_unusual_timekeeping_delay(log_entry['message']):
                    unusual_entries.append(log_entry)
                elif is_cpu_register_state_message(log_entry['message']):
                    cpu_register_state_entries.append(log_entry)

    return unusual_entries, cpu_register_state_entries

# Main execution
if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)  # Determine the directory of the current script
    dir_path = os.path.join(script_dir, '')  # Compute the directory path

    log_files = [f for f in os.listdir(dir_path) if f.endswith('.log')]
    all_unusual_events = []
    all_cpu_state_events = []

    for log_file in log_files:
        log_file_path = os.path.join(dir_path, log_file)
        unusual_events, cpu_state_events = analyze_kernel_log_file(log_file_path)
        all_unusual_events.extend(unusual_events)
        all_cpu_state_events.extend(cpu_state_events)

    if all_unusual_events or all_cpu_state_events:
        output_file_path = os.path.join(dir_path, 'detected_events.txt')
        with open(output_file_path, 'w') as output_file:
            if all_unusual_events:
                output_file.write(f"Unusual timekeeping events detected: {len(all_unusual_events)} instances\n")
                for event in all_unusual_events:
                    output_file.write(str(event) + '\n')
            if all_cpu_state_events:
                output_file.write(f"CPU register state messages detected: {len(all_cpu_state_events)} instances\n")
                for event in all_cpu_state_events:
                    output_file.write(str(event) + '\n')
        print(f"Detected events saved to {output_file_path}")
    else:
        print("No unusual events detected.")
