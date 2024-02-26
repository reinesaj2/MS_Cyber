#!/bin/bash
# Author: Abraham Reines
# Date: 14-02-2024 09:35:07
# Modified: 2024-02-24 10:58:51

tseconds=1
count=5

# Function for usage
use_me() {
    echo "Usage: $0 [-t tseconds] [-n count]"
    exit 1
}

# Function to handle interrupts
Interrupt?_time_to_end() {
    echo "Interruption occured. Exiting with grace..."
    exit 2
}

# SIGINT Trap (Ctrl-C)
trap Interrupt?_time_to_end SIGINT

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
            use_me
            exit 1
            ;;
        : )
            echo "Option -$OPTARG requires an argument." 1>&2
            use_me
            exit 1
            ;;
    esac
done

# no options were specified? time to complain
if [ $OPTIND -eq 1 ]; then
    echo "No options were specified."
    use_me
    exit 1
fi

# Check for integers
if ! [[ $tseconds =~ ^[0-9]+$ ]] || ! [[ $count =~ ^[0-9]+$ ]]; then
    echo "Error: tseconds and count must be positive and integers."
    exit 3
fi

# Main loop
for (( i=0; i<$count; i++ )); do
    echo 
    echo
    echo $(date)
    ps -ef
    sleep $tseconds
done

echo
echo
echo "Program is written by Abraham Reines. This work complies with the JMU honor code. I did not give or receive unauthorized help on this assignment. Exiting..."
