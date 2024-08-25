#!/bin/bash

# Define your CS531 environment and directory
CS531_ENV="/Volumes/StorageAJR/MS_Cyber/CS531/CS531"
CS531_DIR="/Volumes/StorageAJR/MS_Cyber/CS531"

# Function to deactivate any active Conda environment
deactivate_conda_env() {
    if [[ -n "$CONDA_DEFAULT_ENV" ]]; then
        echo "Deactivating Conda environment: $CONDA_DEFAULT_ENV"
        conda deactivate
        hash -r
    fi
}

# Function to deactivate any active virtualenv environment
deactivate_virtualenv() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "Deactivating virtualenv: $VIRTUAL_ENV"
        deactivate
        hash -r
    fi
}

# Main function to manage environment switching
switch_to_cs531_env() {
    echo "Current directory: $PWD"
    if [[ "$PWD" == $CS531_DIR* ]]; then
        echo "Current directory is within CS531 directory."
        # Deactivate any currently active environments
        deactivate_conda_env
        deactivate_virtualenv
        # Activate the CS531 environment
        echo "Activating CS531 environment..."
        source "$CS531_ENV/bin/activate"
        echo "CS531 environment activated."
    else
        echo "Current directory is NOT within CS531 directory."
    fi
}

# Execute the environment switch
switch_to_cs531_env