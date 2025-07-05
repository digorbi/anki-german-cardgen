#!/usr/bin/env python3
"""
Bundle script for German Card Anki addon.
This script copies all required dependencies into the addon directory.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def bundle_dependencies():
    """Bundle dependencies into the addon directory."""
    print("Bundling dependencies for German Card addon...")
    
    # Get paths
    project_root = Path(__file__).parent.parent
    addon_dir = project_root / "plugin"
    vendor_dir = addon_dir / "vendor"
    
    # Clean vendor directory if it exists
    if vendor_dir.exists():
        print(f"Cleaning existing vendor directory: {vendor_dir}")
        shutil.rmtree(vendor_dir)
    vendor_dir.mkdir(exist_ok=True)
    
    # Read dependencies from central file
    deps_file = project_root / "requirements.txt"
    if not deps_file.exists():
        print(f"✗ Dependencies file not found: {deps_file}")
        return False
    
    print("Installing dependencies to vendor directory (including sub-dependencies)...")
    
    # Install dependencies to vendor directory (with sub-dependencies)
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--target", str(vendor_dir),
            "-r", str(deps_file)
        ])
        print("✓ Dependencies installed to vendor directory")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    
    # Create __init__.py in vendor directory
    vendor_init = vendor_dir / "__init__.py"
    vendor_init.write_text("# Vendor directory for bundled dependencies\n")
    
    print(f"✓ Bundle created at: {vendor_dir}")
    return True

if __name__ == "__main__":
    bundle_dependencies() 