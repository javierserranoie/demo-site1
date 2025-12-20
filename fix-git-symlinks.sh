#!/bin/bash
# Fix git symlink issues after folder rename

set -e

echo "Fixing git symlink/path issues..."

# Remove all files from git index (this doesn't delete them from disk)
git rm -r --cached . 2>/dev/null || true

# Re-add all files with current paths
git add .

# Normalize line endings and paths
git add --renormalize . 2>/dev/null || true

echo "Git index refreshed. Checking status..."
git status --short || echo "Status check completed"

echo "Done! Git should now recognize the new folder structure."
