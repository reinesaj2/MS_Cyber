#!/bin/bash

# Set the author of the commits
AUTHOR="Abraham Reines abraham.reines@gmail.com"
DATE="$(date '+%Y-%m-%d %H:%M:%S')"

# Ensure script execution halts on the first error
set -e

# Check if inside a Git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    git init
fi

# Function to append rule to .gitignore if it doesn't already exist
# append_gitignore() {
#     if ! grep -q "^$1\$" .gitignore 2>/dev/null; then
#         echo "$1" >> .gitignore
#     fi
# }

# Add .gitignore rules
#append_gitignore "git_backup/"
#append_gitignore "._*"

# Add the .gitignore file
#git add .gitignore

# Commit the .gitignore changes if there are any
#it diff-index --quiet HEAD || git commit -m "Update .gitignore $DATE" --author "$AUTHOR"

# Add all new and changed files to the git index, respecting .gitignore rules
git add . --all --verbose

# Stage all changes including new, modified, and deleted files
git add -A --verbose

# Commit the changes with a current timestamp message
COMMIT_MESSAGE="School Commit $DATE"
git diff-index --quiet HEAD || git commit -m "$COMMIT_MESSAGE"

# Check if the remote is already added, only add if it isn't
if ! git remote | grep -q origin; then
    git remote add origin https://github.com/reinesaj2/MS_Cyber.git
fi

# Ensure the local branch exists and is tracking the remote branch
if ! git rev-parse --verify main > /dev/null 2>&1; then
    git branch main
fi
git fetch origin main
git branch --set-upstream-to=origin/main main

# Push the changes to the remote repository
git push -u origin main

# Find and remove all files that start with '._' and stage the removal
find . -name '._*' -exec git rm --cached {} \;

# Stage all changes forcibly, including untracked and ignored files
git add --force .

# Commit the removal of '._*' files if there are any
git diff-index --quiet HEAD || git commit -m "Removing files starting with ._ $DATE"

# Push the changes to the remote repository
git push -u origin main
