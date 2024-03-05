"""
Author: ByteMeXpert
Date: 2024-03-04

Spy utility program for tracking system processes based on specific patterns,
interval, and count.
"""

import sys
import time
import re
import psutil
import signal
import os
from datetime import datetime

# Determine the directory of the current script
script_dir = os.path.dirname(__file__)
temp_file_path = os.path.join(script_dir, 'spy_temp.txt')

def handle_interrupt(signum, frame):
    """Clean up temporary files on interrupt and exit gracefully."""
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    sys.exit("\nInterrupt received. Exiting spy and cleaning up temporary files.")

# Register the signal handler for interrupt (Ctrl-C)
signal.signal(signal.SIGINT, handle_interrupt)

def parse_arguments():
    """Parse command line arguments."""
    patterns = []
    interval = 1
    count = 5
    args = sys.argv[1:]

    if '-t' in args:
        try:
            interval_index = args.index('-t')
            interval = int(args[interval_index + 1])
            args.pop(interval_index)
            args.pop(interval_index)
        except (ValueError, IndexError):
            print("Invalid interval specification. Usage: spy [list of patterns] [-t seconds] [-n count]")
            sys.exit(1)

    if '-n' in args:
        try:
            count_index = args.index('-n')
            count = int(args[count_index + 1])
            args.pop(count_index)
            args.pop(count_index)
        except (ValueError, IndexError):
            print("Invalid count specification. Usage: spy [list of patterns] [-t seconds] [-n count]")
            sys.exit(1)

    patterns = args
    return patterns, interval, count

def scan_processes(patterns):
    """Scan current processes and filter them based on the given patterns."""
    process_list = []
    for proc in psutil.process_iter(['pid', 'username', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'])
            if any(re.search(pattern, cmdline) for pattern in patterns) or not patterns:
                process_list.append(f"{proc.info['username']} {proc.info['pid']} {cmdline}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list

def compare_and_log(old_list, new_list):
    """Compare two process lists, log differences, and update the temporary file."""
    started = set(new_list) - set(old_list)
    ended = set(old_list) - set(new_list)

    with open(temp_file_path, 'w') as temp_file:
        for proc in new_list:
            temp_file.write(proc + '\n')

    return started, ended

def main():
    patterns, interval, count = parse_arguments()

    # Compile patterns for efficiency
    patterns = [re.compile(pattern) for pattern in patterns]

    if os.path.exists(temp_file_path):
        with open(temp_file_path, 'r') as temp_file:
            old_process_list = temp_file.read().splitlines()
    else:
        old_process_list = []

    for _ in range(count):
        new_process_list = scan_processes(patterns)
        started, ended = compare_and_log(old_process_list, new_process_list)

        print(datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y"))
        for proc in started:
            print(f"Started: {proc}")
        for proc in ended:
            print(f"Ended: {proc}")

        if not started and not ended:
            print("No process changes detected.")

        old_process_list = new_process_list
        time.sleep(interval)

if __name__ == "__main__":
    main()
