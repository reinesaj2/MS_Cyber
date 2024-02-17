#!/bin/bash

# Set the author of the commits
AUTHOR="Abraham Reines <abraham.reines@gmail.com>"
DATE="$(date '+%Y-%m-%d %H:%M:%S')"

# Ensure script execution halts on the first error
set -e

# Initialize a new git repository if one doesn't exist
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    git init
fi

# Add all new and changed files to the git index
git add . --all --verbose

# Commit the changes with a timestamp
COMMIT_MESSAGE="School Commit $DATE"
git commit -m "$COMMIT_MESSAGE" || echo "No changes to commit."

# Find and remove all files that start with '._' from the working directory and the index
find . -name '._*' -exec git rm -f {} \;

# Commit the removal of '._*' files
git diff-index --quiet HEAD || git commit -m "Removing files starting with ._ $DATE"

# Add the remote repository if it doesn't exist
if ! git remote | grep -q origin; then
    git remote add origin https://github.com/reinesaj2/MS_Cyber.git
fi

# Ensure the local 'main' branch exists and track the remote 'main' branch
if ! git rev-parse --verify main > /dev/null 2>&1; then
    git branch main
fi
git fetch origin main
git branch --set-upstream-to=origin/main main

# Push the changes to the remote repository
git push -u origin main
