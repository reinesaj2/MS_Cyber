#!/bin/bash
# Author: Abraham Reines
# Date: 14-02-2024 09:35:07

tseconds=1
count=5

# Function for usage
show_usage() {
    echo "Usage: $0 [-t tseconds] [-n count]"
    exit 1
}

# Function to handle interrupts
handle_interrupt() {
    echo "Interruption occured. Exiting with grace..."
    exit 2
}

# SIGINT Trap (Ctrl-C)
trap handle_interrupt SIGINT

# Parsing 
while getopts ":t:n:" opt; do
    case ${opt} in
        t )
            tseconds=$OPTARG
            ;;
        n )
            count=$OPTARG
            ;;
        \? )
            echo "Invalid Option: -$OPTARG" 1>&2
            show_usage
            ;;
        : )
            echo "Option -$OPTARG requires an argument." 1>&2
            show_usage
            ;;
    esac
done

# Check for integers
if ! [[ $tseconds =~ ^[0-9]+$ ]] || ! [[ $count =~ ^[0-9]+$ ]]; then
    echo "Error: tseconds and count must be positive and integers."
    exit 3
fi

# Main loop
for (( i=0; i<$count; i++ )); do
    echo $(date)
    ps -ef
    sleep $tseconds
done

echo
echo
echo "Program is written by Abraham Reines. This work complies with the JMU honor code. I did not give or receive unauthorized help on this assignment. Exiting..."
