#!/bin/bash

# Ensure script execution halts on the first error
set -e

# Check if inside a Git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    git init
fi

# Function to append rule to .gitignore if it doesn't already exist
append_gitignore() {
    if ! grep -q "^$1\$" .gitignore 2>/dev/null; then
        echo "$1" >> .gitignore
    fi
}

# Add .gitignore rules
append_gitignore "git_backup/"
append_gitignore "._*"

# Add the .gitignore file and commit changes
git add .gitignore
git commit -m "Update .gitignore" || true # Proceed even if no changes

# Find and remove all files that start with '._'
find . -name '._*' -exec git rm -f {} \;

# Commit the removal of '._*' files
git commit -m "Removing files starting with ._ $(date '+%Y-%m-%d %H:%M:%S')"

# Check for any changes or new files
if git status --porcelain | grep -q "^??\|^ M"; then
    # Add all new and changed files to the git index, respecting .gitignore rules
    git add . --verbose
    # Commit the changes with a current timestamp message
    COMMIT_MESSAGE="School Commit $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MESSAGE"
else
    echo "No changes to commit."
fi

# Check if the remote is already added, only add if it isn't
if ! git remote | grep -q origin; then
    git remote add origin https://github.com/reinesaj2/MS_Cyber.git
fi

# Ensure the local branch exists before setting it to track the remote branch
if ! git rev-parse --verify main > /dev/null 2>&1; then
    git branch main
    git branch --set-upstream-to=origin/main main
fi

# Push the changes to the remote repository
git push -u origin main
