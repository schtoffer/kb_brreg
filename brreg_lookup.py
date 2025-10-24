#!/usr/bin/env python3
"""
Simple BRREG API lookup script
Usage: python brreg_lookup.py <org_number>
Example: python brreg_lookup.py 123456789
"""

import sys
import requests
import json


def lookup_organization(org_number):
    """
    Lookup organization in BRREG API (both main entities and sub-entities)
    
    Args:
        org_number (str): 9-digit organization number
    
    Returns:
        dict: Organization data or None if not found
    """
    base_url = "https://data.brreg.no/enhetsregisteret/api"
    
    # Try main entities first
    main_url = f"{base_url}/enheter/{org_number}"
    print(f"Checking main entities: {main_url}")
    
    try:
        response = requests.get(main_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'type': 'hovedenhet',
                'data': data
            }
    except requests.RequestException as e:
        print(f"Error checking main entities: {e}")
    
    # Try sub-entities (underenheter) if not found in main
    sub_url = f"{base_url}/underenheter/{org_number}"
    print(f"Checking sub-entities: {sub_url}")
    
    try:
        response = requests.get(sub_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'type': 'underenhet',
                'data': data
            }
    except requests.RequestException as e:
        print(f"Error checking sub-entities: {e}")
    
    return None


def format_address(address_data):
    """Format address from BRREG API response"""
    if not address_data:
        return "Adresse ikke tilgjengelig"
    
    parts = []
    
    # Add street address
    if address_data.get('adresse'):
        for addr_line in address_data['adresse']:
            if addr_line:
                parts.append(addr_line)
    
    # Add postal code and place
    if address_data.get('postnummer'):
        postal_part = address_data['postnummer']
        if address_data.get('poststed'):
            postal_part += f" {address_data['poststed']}"
        parts.append(postal_part)
    
    return ", ".join(parts) if parts else "Adresse ikke tilgjengelig"


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python brreg_lookup.py <org_number>")
        print("Example: python brreg_lookup.py 123456789")
        sys.exit(1)
    
    org_number = sys.argv[1].strip()
    
    # Validate org number format
    if not org_number.isdigit() or len(org_number) != 9:
        print("Error: Organization number must be exactly 9 digits")
        sys.exit(1)
    
    print(f"Looking up organization number: {org_number}")
    print("-" * 50)
    
    # Lookup organization
    result = lookup_organization(org_number)
    
    if not result:
        print("❌ Organization not found in BRREG registry")
        sys.exit(1)
    
    org_data = result['data']
    org_type = result['type']
    
    # Extract information
    name = org_data.get('navn', 'Navn ikke tilgjengelig')
    
    # Get address (try forretningsadresse first, then postadresse)
    address = None
    if org_data.get('forretningsadresse'):
        address = format_address(org_data['forretningsadresse'])
    elif org_data.get('postadresse'):
        address = format_address(org_data['postadresse'])
    else:
        address = "Adresse ikke tilgjengelig"
    
    # Display results
    print("✅ Organization found!")
    print(f"Type: {org_type.capitalize()}")
    print(f"Navn: {name}")
    print(f"Adresse: {address}")
    
    # Additional info
    if org_data.get('organisasjonsform'):
        print(f"Organisasjonsform: {org_data['organisasjonsform'].get('beskrivelse', 'N/A')}")
    
    if org_data.get('naeringskode1'):
        print(f"Næringskode: {org_data['naeringskode1'].get('beskrivelse', 'N/A')}")
    
    print("-" * 50)
    print(f"Org.nr: {org_number}")


if __name__ == "__main__":
    main()
