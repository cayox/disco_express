#!/bin/bash

# Define the target file
TARGET_FILE="$HOME/.config/autostart/disco_express.desktop"
DISABLED_FILE="$HOME/.config/autostart/disco_express.desktop.disabled"

# Check if the file exists
if [ -f "$TARGET_FILE" ]; then
  # Rename the file to disable it
  mv "$TARGET_FILE" "$DISABLED_FILE"

  # Check if the rename command succeeded
  if [ $? -eq 0 ]; then
    echo "AUTOSTART DISABLED"
  else
    echo "Failed to disable autostart"
    exit 1
  fi
else
  echo "File $TARGET_FILE does not exist."
  exit 1
fi
