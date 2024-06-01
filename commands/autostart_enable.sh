#!/bin/bash

# Define the target file
DISABLED_FILE="$HOME/.config/autostart/disco_express.desktop.disabled"
TARGET_FILE="$HOME/.config/autostart/disco_express.desktop"

# Check if the disabled file exists
if [ -f "$DISABLED_FILE" ]; then
  # Rename the file to enable it again
  mv "$DISABLED_FILE" "$TARGET_FILE"

  # Check if the rename command succeeded
  if [ $? -eq 0 ]; then
    echo "AUTOSTART ENABLED"
  else
    echo "Failed to enable autostart"
    exit 1
  fi
else
  echo "File $DISABLED_FILE does not exist."
  exit 1
fi
