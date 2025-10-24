#!/usr/bin/env python3
"""
BRREG API Lookup Tool

A professional Python tool for querying the Norwegian Business Register (Brønnøysundregisteret).
Supports both organization number lookups and name-based searches across main entities 
and sub-entities (affiliate associations).

Author: Christoffer Andersen
Version: 2.0.0
License: MIT
"""

import argparse
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union
import requests
from difflib import SequenceMatcher


# API Configuration Constants
BRREG_BASE_URL = "https://data.brreg.no/enhetsregisteret/api"
REQUEST_TIMEOUT = 10
MAX_SEARCH_RESULTS = 20

# Relevance Scoring Thresholds
EXACT_MATCH_THRESHOLD = 0.95
HIGH_RELEVANCE_THRESHOLD = 0.8
GOOD_MATCH_THRESHOLD = 0.6

# Text Matching Bonuses
WORD_SUBSET_BONUS = 0.2
WORD_ORDER_BONUS = 0.1

# Display Configuration
MAX_RESULTS_TO_SHOW_SCORES = 3


class EntityType(Enum):
    """Enumeration for different types of entities in BRREG."""
    HOVEDENHET = "hovedenhet"
    UNDERENHET = "underenhet"


@dataclass
class Address:
    """Data class representing an organization's address."""
    street_lines: List[str]
    postal_code: Optional[str] = None
    city: Optional[str] = None
    
    def format(self) -> str:
        """Format address for display."""
        if not self.street_lines and not self.postal_code:
            return "Adresse ikke tilgjengelig"
        
        parts = []
        
        # Add street address lines
        for line in self.street_lines:
            if line and line.strip():
                parts.append(line.strip())
        
        # Add postal code and city
        if self.postal_code:
            postal_part = self.postal_code
            if self.city:
                postal_part += f" {self.city}"
            parts.append(postal_part)
        
        return ", ".join(parts) if parts else "Adresse ikke tilgjengelig"


@dataclass
class OrganizationInfo:
    """Data class representing organization information from BRREG API."""
    name: str
    org_number: str
    entity_type: EntityType
    business_address: Optional[Address] = None
    postal_address: Optional[Address] = None
    organization_form: Optional[str] = None
    industry_code: Optional[str] = None
    relevance_score: float = 0.0
    
    @property
    def primary_address(self) -> Address:
        """Get the primary address (business address preferred, then postal)."""
        return self.business_address or self.postal_address or Address([])


class TextMatcher:
    """
    Utility class for intelligent text matching and relevance scoring.
    
    This class implements advanced text matching algorithms to rank search results
    by relevance, ensuring that exact matches appear first and similar matches
    are properly scored.
    
    The scoring algorithm considers:
    - Exact matches (score: 1.0)
    - Substring containment (score: 0.95)
    - Fuzzy string similarity using difflib.SequenceMatcher
    - Word subset matching (bonus: +0.2)
    - Word order preservation (bonus: +0.1)
    """
    
    @staticmethod
    def calculate_relevance_score(query: str, organization_name: str) -> float:
        """Calculate relevance score between query and organization name.
        
        Args:
            query: The search query
            organization_name: The organization name to compare against
            
        Returns:
            Relevance score between 0.0 and 1.0 (higher is more relevant)
        """
        query_clean = TextMatcher._normalize_text(query)
        name_clean = TextMatcher._normalize_text(organization_name)
        
        # Exact match gets highest score
        if query_clean == name_clean:
            return 1.0
        
        # Check if query is contained in name (case insensitive)
        if query_clean in name_clean:
            return 0.95
        
        # Check if name contains query
        if name_clean in query_clean:
            return 0.9
        
        # Use sequence matcher for fuzzy matching
        similarity = SequenceMatcher(None, query_clean, name_clean).ratio()
        
        # Boost score if all words in query appear in name
        query_words = set(query_clean.split())
        name_words = set(name_clean.split())
        
        if query_words.issubset(name_words):
            similarity += WORD_SUBSET_BONUS  # Boost for containing all words
        
        # Boost score for word order preservation
        if TextMatcher._preserves_word_order(query_clean, name_clean):
            similarity += WORD_ORDER_BONUS
        
        return min(similarity, 1.0)  # Cap at 1.0
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Normalize text for comparison by converting to lowercase and stripping whitespace.
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text string
        """
        return text.lower().strip()
    
    @staticmethod
    def _preserves_word_order(query: str, name: str) -> bool:
        """
        Check if the word order from query is preserved in the organization name.
        
        This method checks if all words from the query appear in the same order
        within the organization name, which indicates a more relevant match.
        
        Args:
            query: The search query
            name: The organization name
            
        Returns:
            True if word order is preserved, False otherwise
        """
        query_words = query.split()
        name_words = name.split()
        
        query_index = 0
        for word in name_words:
            if query_index < len(query_words) and word == query_words[query_index]:
                query_index += 1
        
        return query_index == len(query_words)


class BRREGClient:
    """Professional client for interacting with the BRREG API."""
    
    def __init__(self, base_url: str = BRREG_BASE_URL, timeout: int = REQUEST_TIMEOUT):
        """Initialize the BRREG client.
        
        Args:
            base_url: Base URL for the BRREG API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BRREG-Lookup-Tool/2.0.0',
            'Accept': 'application/json'
        })
    
    def lookup_by_number(self, org_number: str) -> Optional[OrganizationInfo]:
        """Lookup organization by organization number.
        
        Args:
            org_number: 9-digit organization number
            
        Returns:
            OrganizationInfo if found, None otherwise
        """
        # Try main entities first
        main_url = f"{self.base_url}/enheter/{org_number}"
        print(f"🔍 Checking main entities: {main_url}")
        
        try:
            response = self.session.get(main_url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return self._parse_organization_data(data, EntityType.HOVEDENHET)
        except requests.RequestException as e:
            print(f"⚠️  Error checking main entities: {e}")
        
        # Try sub-entities if not found in main
        sub_url = f"{self.base_url}/underenheter/{org_number}"
        print(f"🔍 Checking sub-entities: {sub_url}")
        
        try:
            response = self.session.get(sub_url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return self._parse_organization_data(data, EntityType.UNDERENHET)
        except requests.RequestException as e:
            print(f"⚠️  Error checking sub-entities: {e}")
        
        return None
    
    def search_by_name(self, name: str) -> List[OrganizationInfo]:
        """Search organizations by name with intelligent relevance ranking.
        
        Args:
            name: Organization name to search for
            
        Returns:
            List of matching OrganizationInfo objects sorted by relevance
        """
        results = []
        
        # Search main entities
        print(f"🔍 Searching main entities for: '{name}'")
        main_results = self._search_endpoint("enheter", name)
        for data in main_results:
            org_info = self._parse_organization_data(data, EntityType.HOVEDENHET, name)
            if org_info:
                results.append(org_info)
        
        # Search sub-entities
        print(f"🔍 Searching sub-entities for: '{name}'")
        sub_results = self._search_endpoint("underenheter", name)
        for data in sub_results:
            org_info = self._parse_organization_data(data, EntityType.UNDERENHET, name)
            if org_info:
                results.append(org_info)
        
        # Sort by relevance score (highest first), then by entity type preference
        results.sort(key=lambda x: (x.relevance_score, x.entity_type == EntityType.HOVEDENHET), reverse=True)
        
        return results
    
    def _search_endpoint(self, endpoint: str, name: str) -> List[Dict]:
        """Search a specific endpoint for organizations by name."""
        try:
            url = f"{self.base_url}/{endpoint}"
            params = {'navn': name, 'size': MAX_SEARCH_RESULTS}
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return data.get('_embedded', {}).get(endpoint, [])
        except requests.RequestException as e:
            print(f"⚠️  Error searching {endpoint}: {e}")
        
        return []
    
    def _parse_organization_data(self, data: Dict, entity_type: EntityType, query: Optional[str] = None) -> Optional[OrganizationInfo]:
        """Parse raw API data into OrganizationInfo object."""
        try:
            # Extract basic information
            name = data.get('navn', 'Navn ikke tilgjengelig')
            org_number = data.get('organisasjonsnummer', 'N/A')
            
            # Calculate relevance score if query is provided
            relevance_score = 0.0
            if query:
                relevance_score = TextMatcher.calculate_relevance_score(query, name)
            
            # Parse addresses
            business_address = self._parse_address(data.get('forretningsadresse'))
            postal_address = self._parse_address(data.get('postadresse'))
            
            # Extract additional information
            org_form = None
            if data.get('organisasjonsform'):
                org_form = data['organisasjonsform'].get('beskrivelse')
            
            industry_code = None
            if data.get('naeringskode1'):
                industry_code = data['naeringskode1'].get('beskrivelse')
            
            return OrganizationInfo(
                name=name,
                org_number=org_number,
                entity_type=entity_type,
                business_address=business_address,
                postal_address=postal_address,
                organization_form=org_form,
                industry_code=industry_code,
                relevance_score=relevance_score
            )
        except Exception as e:
            print(f"⚠️  Error parsing organization data: {e}")
            return None
    
    def _parse_address(self, address_data: Optional[Dict]) -> Optional[Address]:
        """Parse address data from API response."""
        if not address_data:
            return None
        
        street_lines = address_data.get('adresse', [])
        postal_code = address_data.get('postnummer')
        city = address_data.get('poststed')
        
        return Address(
            street_lines=street_lines or [],
            postal_code=postal_code,
            city=city
        )


class OrganizationDisplayFormatter:
    """Professional formatter for displaying organization information."""
    
    @staticmethod
    def display_single_result(org_info: OrganizationInfo) -> None:
        """Display a single organization result."""
        print("\n✅ Organization found!")
        OrganizationDisplayFormatter._display_organization_details(org_info)
    
    @staticmethod
    def display_multiple_results(results: List[OrganizationInfo]) -> None:
        """Display multiple organization results sorted by relevance."""
        print(f"\n✅ Found {len(results)} matching organization(s) (sorted by relevance):")
        
        for i, org_info in enumerate(results):
            relevance_indicator = ""
            if org_info.relevance_score >= EXACT_MATCH_THRESHOLD:
                relevance_indicator = " 🎯 EXACT MATCH"
            elif org_info.relevance_score >= HIGH_RELEVANCE_THRESHOLD:
                relevance_indicator = " ⭐ HIGH RELEVANCE"
            elif org_info.relevance_score >= GOOD_MATCH_THRESHOLD:
                relevance_indicator = " 📍 GOOD MATCH"
            
            print(f"\n--- Result {i + 1}{relevance_indicator} ---")
            OrganizationDisplayFormatter._display_organization_details(org_info)
            
            # Show relevance score for top results or high-relevance matches
            if i < MAX_RESULTS_TO_SHOW_SCORES or org_info.relevance_score >= HIGH_RELEVANCE_THRESHOLD:
                print(f"Relevance Score: {org_info.relevance_score:.2f}")
        
        if len(results) > 5:
            print(f"\n💡 Showing first {len(results)} results. The most relevant matches are listed first.")
    
    @staticmethod
    def _display_organization_details(org_info: OrganizationInfo) -> None:
        """Display detailed organization information."""
        print(f"Type: {org_info.entity_type.value.capitalize()}")
        print(f"Navn: {org_info.name}")
        print(f"Org.nr: {org_info.org_number}")
        print(f"Adresse: {org_info.primary_address.format()}")
        
        if org_info.organization_form:
            print(f"Organisasjonsform: {org_info.organization_form}")
        
        if org_info.industry_code:
            print(f"Næringskode: {org_info.industry_code}")


class InputValidator:
    """Validator for user input."""
    
    @staticmethod
    def validate_org_number(org_number: str) -> bool:
        """Validate organization number format.
        
        Args:
            org_number: Organization number to validate
            
        Returns:
            True if valid, False otherwise
        """
        return org_number.isdigit() and len(org_number) == 9
    
    @staticmethod
    def validate_organization_name(name: str) -> bool:
        """Validate organization name.
        
        Args:
            name: Organization name to validate
            
        Returns:
            True if valid, False otherwise
        """
        return len(name.strip()) >= 3


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command line argument parser."""
    parser = argparse.ArgumentParser(
        description='🏢 BRREG API Lookup Tool - Professional Norwegian Business Register Query Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
📋 Examples:
  python brreg_lookup.py -num 923554416
  python brreg_lookup.py -name "FJORDKRAFT AS AVD SORTLAND"
  python brreg_lookup.py --number 923609016
  python brreg_lookup.py --name "EQUINOR ASA"

🔍 Features:
  • Searches both main entities (enheter) and sub-entities (underenheter)
  • Handles affiliate associations automatically
  • Professional data formatting and error handling
  • Type-safe implementation with comprehensive validation
        '''
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-num', '--number',
        help='9-digit organization number for direct lookup',
        metavar='ORG_NUMBER'
    )
    group.add_argument(
        '-name', '--name',
        help='Organization name for search (minimum 3 characters)',
        metavar='ORG_NAME'
    )
    
    return parser


def main() -> None:
    """Main application entry point with professional error handling."""
    try:
        # Parse command line arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Initialize BRREG client
        client = BRREGClient()
        formatter = OrganizationDisplayFormatter()
        
        print("=" * 70)
        print("🏢 BRREG API Lookup Tool v2.0.0")
        print("=" * 70)
        
        if args.number:
            # Organization number lookup
            org_number = args.number.strip()
            
            if not InputValidator.validate_org_number(org_number):
                print("❌ Error: Organization number must be exactly 9 digits")
                sys.exit(1)
            
            print(f"🔍 Looking up organization number: {org_number}")
            print("-" * 50)
            
            result = client.lookup_by_number(org_number)
            
            if not result:
                print("❌ Organization not found in BRREG registry")
                print("💡 Tip: Verify the organization number or try searching by name")
                sys.exit(1)
            
            formatter.display_single_result(result)
            
        elif args.name:
            # Organization name search
            org_name = args.name.strip()
            
            if not InputValidator.validate_organization_name(org_name):
                print("❌ Error: Organization name must be at least 3 characters")
                sys.exit(1)
            
            print(f"🔍 Searching for organizations matching: '{org_name}'")
            print("-" * 50)
            
            results = client.search_by_name(org_name)
            
            if not results:
                print("❌ No organizations found matching the search criteria")
                print("💡 Tip: Try a broader search term or check spelling")
                sys.exit(1)
            
            formatter.display_multiple_results(results)
        
        print("\n" + "=" * 70)
        print("✅ Lookup completed successfully")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
        print("💡 Please check your internet connection and try again")
        sys.exit(1)


if __name__ == "__main__":
    main()
