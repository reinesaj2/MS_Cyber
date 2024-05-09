#!/bin/bash

# Set commit author and current date
AUTHOR="Abraham Reines <abraham.reines@gmail.com>"
DATE="$(date '+%Y-%m-%d %H:%M:%S')"

# Halt on any error
set -e

# Initialize Git LFS and repository if necessary
git lfs install
git rev-parse --is-inside-work-tree || git init

# Track specific large file types with Git LFS (e.g., for images)
# Uncomment and modify the following line as needed
# git lfs track "*.png"

# Add all changes and commit
git add . --all --verbose
COMMIT_MESSAGE="School Commit $DATE"
git commit -m "$COMMIT_MESSAGE" --author="$AUTHOR" || echo "No changes to commit."

# Add remote repository if it doesn't exist
git remote get-url origin || git remote add origin https://github.com/reinesaj2/MS_Cyber.git

# Ensure the 'main' branch is checked out and tracking the remote 'main'
git checkout main || git checkout -b main
git fetch origin main
git branch --set-upstream-to=origin/main main

# Optimize the local repository
git gc --aggressive --prune=now

# Push changes to the remote repository
git push -u origin main