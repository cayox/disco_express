#!/bin/bash

# Define the target directory
TARGET_DIR="$HOME/disco_express"

# Check if the directory exists
if [ -d "$TARGET_DIR" ]; then
  # Delete all contents within the directory
  rm -rf "$TARGET_DIR"/*

  # Check if the delete command succeeded
  if [ $? -eq 0 ]; then
    echo "All contents of $TARGET_DIR have been deleted."
  else
    echo "Failed to delete contents of $TARGET_DIR."
    exit 1
  fi
else
  echo "Directory $TARGET_DIR does not exist."
  exit 1
fi
