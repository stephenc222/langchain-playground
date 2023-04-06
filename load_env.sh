#!/usr/bin/env bash

# Check if .env file exists
if [ -f .env ]; then
  # Read file and export variables
  export $(cat .env | xargs)
  echo "Environment variables from .env file loaded."
else
  echo "No .env file found."
fi
