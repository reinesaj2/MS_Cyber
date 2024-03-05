#!/bin/bash

# Author: ByteMeXpert
# Date: 2024-03-04

# Usage: spy [list of patterns] [-t secs] [-n count]

# Default values
interval=1
count=5
patterns=()
temp_file="spy_temp.txt"

# Function to display usage
usage() {
    echo "Usage: $0 [list of patterns] [-t seconds] [-n count]"
    exit 1
}

# Function to handle interrupts (Ctrl-C)
cleanup() {
    echo
    echo "Cleaning up temporary files..."
    rm -f "$temp_file"
    exit
}

trap cleanup INT

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t) interval="$2"; shift ;;
        -n) count="$2"; shift ;;
        -*) echo "Unknown option: $1"; usage ;;
        *) patterns+=("$1") ;;
    esac
    shift
done

if [[ -z "$interval" || -z "$count" ]]; then
    usage
fi

if ! [[ "$interval" =~ ^[0-9]+$ ]] || ! [[ "$count" =~ ^[0-9]+$ ]]; then
    echo "Interval and count must be integers."
    usage
fi

# Main loop
for ((i=0; i<count; i++)); do
    # Adjusted to use 'args' instead of 'cmd' for wider compatibility
    current_processes=$(ps -eo user,pid,args | grep -v grep | grep -v $0)
    if [ ${#patterns[@]} -gt 0 ]; then
        filtered_processes=$(echo "$current_processes" | grep -E "$(IFS=\|; echo "${patterns[*]}")")
    else
        filtered_processes="$current_processes"
    fi

    if [ -f "$temp_file" ]; then
        # Compare current processes with the last scan
        started=$(comm -13 <(sort "$temp_file") <(echo "$filtered_processes" | sort))
        ended=$(comm -23 <(sort "$temp_file") <(echo "$filtered_processes" | sort))
        
        echo "$(date):"
        if [ ! -z "$started" ]; then
            echo "Started:"
            echo "$started"
        fi
        if [ ! -z "$ended" ]; then
            echo "Ended:"
            echo "$ended"
        fi
        if [ -z "$started" ] && [ -z "$ended" ]; then
            echo "No process changes detected."
        fi
    else
        echo "$(date):"
        echo "Initial scan. Monitoring started."
    fi

    echo "$filtered_processes" > "$temp_file"
    
    sleep "$interval"
done

# Cleanup on exit
rm -f "$temp_file"
