#!/usr/bin/env python3
"""
BRREG API Lookup Tool - Usage Examples

This script demonstrates various ways to use the BRREG lookup tool.
Run this script to see example outputs and learn how to use the tool effectively.

Usage: python examples.py
"""

import subprocess
import sys
from typing import List


def run_example(description: str, command: List[str]) -> None:
    """Run an example command and display the results."""
    print("=" * 80)
    print(f"📋 EXAMPLE: {description}")
    print("=" * 80)
    print(f"Command: python {' '.join(command)}")
    print("-" * 80)
    
    try:
        result = subprocess.run(
            ["python"] + command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
    except Exception as e:
        print(f"❌ Error running example: {e}")
    
    print("\n" + "=" * 80 + "\n")


def main():
    """Run all examples."""
    print("🏢 BRREG API Lookup Tool - Usage Examples")
    print("This script demonstrates various usage patterns\n")
    
    examples = [
        (
            "Organization Number Lookup - Equinor ASA",
            ["brreg_lookup.py", "-num", "923609016"]
        ),
        (
            "Organization Number Lookup - Fjordkraft Sortland (Affiliate)",
            ["brreg_lookup.py", "-num", "923554416"]
        ),
        (
            "Exact Name Search - Perfect Match",
            ["brreg_lookup.py", "-name", "FJORDKRAFT AS AVD SORTLAND"]
        ),
        (
            "Broad Name Search - Multiple Results",
            ["brreg_lookup.py", "-name", "FJORDKRAFT"]
        ),
        (
            "Partial Name Search - Fuzzy Matching",
            ["brreg_lookup.py", "-name", "EQUINOR"]
        ),
        (
            "Help Command - Show Usage Information",
            ["brreg_lookup.py", "--help"]
        )
    ]
    
    for description, command in examples:
        run_example(description, command)
    
    print("🎉 All examples completed!")
    print("\n💡 Tips for developers:")
    print("- Use exact organization names for best results")
    print("- The tool automatically handles both main entities and sub-entities")
    print("- Results are sorted by relevance with visual indicators")
    print("- Perfect matches get 🎯 EXACT MATCH indicators")
    print("- The tool is designed to solve affiliate association lookup issues")


if __name__ == "__main__":
    main()
