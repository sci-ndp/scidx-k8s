#!/bin/bash

# Script to copy the example-secret.yaml template to pop-env-secret.yaml

SOURCE="template-secret.yaml"
DEST="pop-env-secret.yaml"

# Check if the source file exists
if [ ! -f "$SOURCE" ]; then
  echo "Error: $SOURCE not found. Please ensure the template file exists in the current directory."
  exit 1
fi

# Copy the file
cp "$SOURCE" "$DEST"

# Check if the copy was successful
if [ $? -eq 0 ]; then
  echo "Successfully copied $SOURCE to $DEST. Please edit $DEST with your environment variables."
else
  echo "Error: Failed to copy $SOURCE to $DEST."
  exit 1
fi