#!/bin/bash

# Create a temporary directory to hold renamed files
temp_dir=$(mktemp -d)

# Initialize the counter
count=1

# Loop over files in the current directory
for file in *; do
	if [ -f "$file" ]; then
		# Extract the file extension
		ext="${file##*.}"
		# Rename and move the file to the temporary directory
		mv -- "$file" "$temp_dir/$count.$ext"
		count=$((count + 1))
	fi
done

# Move files back from the temporary directory to the current directory
mv -- "$temp_dir"/* .
# Remove the temporary directory
rmdir "$temp_dir"