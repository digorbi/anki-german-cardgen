#!/bin/bash

# Deploy script for Anki German Card Generator Plugin. Mac only.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Anki add-ons directory
ANKI_ADDONS_DIR="$HOME/Library/Application Support/Anki2/addons21/german_card"

echo -e "${YELLOW}Deploying German Card Generator Plugin...${NC}"

# Check if Anki add-ons directory exists
if [ ! -d "$ANKI_ADDONS_DIR" ]; then
    echo -e "${YELLOW}Creating Anki add-ons directory...${NC}"
    mkdir -p "$ANKI_ADDONS_DIR"
else
    echo -e "${YELLOW}Cleaning up existing files...${NC}"
    rm -rf "$ANKI_ADDONS_DIR"/*
fi

# Create core directory in addon
mkdir -p "$ANKI_ADDONS_DIR/core"

# Copy core files
echo -e "${YELLOW}Copying core files...${NC}"
cp core/*.py "$ANKI_ADDONS_DIR/core/"

# Copy plugin files (these go to the root of the addon)
echo -e "${YELLOW}Copying plugin files...${NC}"
cp plugin/*.py "$ANKI_ADDONS_DIR/"
cp plugin/*.json "$ANKI_ADDONS_DIR/"

# Copy vendor directory if it exists (bundled dependencies)
if [ -d "plugin/vendor" ]; then
    echo -e "${YELLOW}Copying bundled dependencies...${NC}"
    cp -r plugin/vendor "$ANKI_ADDONS_DIR/"
fi

# Copy prompts directory (prompt templates)
if [ -d "prompts" ]; then
    echo -e "${YELLOW}Copying prompts directory...${NC}"
    cp -r prompts "$ANKI_ADDONS_DIR/"
fi

echo -e "${GREEN}Plugin deployed successfully!${NC}"
echo -e "${YELLOW}Please restart Anki to load the updated plugin.${NC}" 