# 🏢 BRREG API Lookup Tool

> **Professional Norwegian Business Register Query Tool**

A beautifully crafted Python application for querying the Norwegian Business Register (Brønnøysundregisteret). Built with modern software engineering practices, type safety, and comprehensive error handling.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style: Professional](https://img.shields.io/badge/code%20style-professional-brightgreen.svg)]()

## ✨ Features

- **🔍 Dual Lookup Methods**: Search by organization number OR organization name
- **🏗️ Comprehensive Coverage**: Queries both main entities (`enheter`) and sub-entities (`underenheter`)
- **🎯 Affiliate Association Support**: Automatically handles subsidiary and affiliate lookups
- **🧠 Intelligent Search Ranking**: Advanced text matching with relevance scoring
  - 🎯 **EXACT MATCH** indicators for perfect matches
  - ⭐ **HIGH RELEVANCE** for very close matches  
  - 📍 **GOOD MATCH** for keyword matches
  - Smart sorting puts most relevant results first
- **📊 Rich Data Display**: Returns company name, address, organization form, and industry classification
- **🛡️ Type-Safe Architecture**: Built with dataclasses, enums, and comprehensive type hints
- **⚡ Professional Error Handling**: Graceful failure modes with helpful user guidance
- **🎨 Beautiful CLI Interface**: Modern command-line experience with emojis and formatting

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Search by Organization Number
```bash
python brreg_lookup.py -num <9-digit-org-number>
python brreg_lookup.py --number <9-digit-org-number>
```

### Search by Organization Name
```bash
python brreg_lookup.py -name "<organization_name>"
python brreg_lookup.py --name "<organization_name>"
```

## Examples

```bash
# Lookup by organization number
python brreg_lookup.py -num 923609016
python brreg_lookup.py -num 923554416

# Search by organization name
python brreg_lookup.py -name "EQUINOR ASA"
python brreg_lookup.py -name "FJORDKRAFT AS AVD SORTLAND"
python brreg_lookup.py -name "Telenor"
```

## Output Examples

### Organization Number Lookup
```
$ python brreg_lookup.py -num 923609016

============================================================
🔍 Looking up organization number: 923609016
--------------------------------------------------
Checking main entities: https://data.brreg.no/enhetsregisteret/api/enheter/923609016

✅ Organization found!
Type: Hovedenhet
Navn: EQUINOR ASA
Org.nr: 923609016
Adresse: Forusbeen 50, 4035 STAVANGER
Organisasjonsform: Allmennaksjeselskap
Næringskode: Utvinning av råolje
============================================================
```

### Organization Name Search with Intelligent Ranking
```
$ python brreg_lookup.py -name "FJORDKRAFT AS AVD SORTLAND"

======================================================================
🏢 BRREG API Lookup Tool v2.0.0
======================================================================
🔍 Searching for organizations matching: 'FJORDKRAFT AS AVD SORTLAND'
--------------------------------------------------
🔍 Searching main entities for: 'FJORDKRAFT AS AVD SORTLAND'
🔍 Searching sub-entities for: 'FJORDKRAFT AS AVD SORTLAND'

✅ Found 40 matching organization(s) (sorted by relevance):

--- Result 1 🎯 EXACT MATCH ---
Type: Underenhet
Navn: FJORDKRAFT AS AVD SORTLAND
Org.nr: 923554416
Adresse: c/o Fjordkraft AS, Postboks 3507 Fyllingsdalen, 5845 BERGEN
Organisasjonsform: Underenhet til næringsdrivende og offentlig forvaltning
Næringskode: Handel med elektrisitet
Relevance Score: 1.00

--- Result 2 ⭐ HIGH RELEVANCE ---
Type: Underenhet
Navn: FJORDKRAFT AS AVD OSLO
Org.nr: 923986731
Adresse: Postboks 178 Lilleaker, 0216 OSLO
Organisasjonsform: Underenhet til næringsdrivende og offentlig forvaltning
Relevance Score: 0.85

--- Result 3 📍 GOOD MATCH ---
Type: Underenhet
Navn: FJORDKRAFT AS AVD STAVANGER
Org.nr: 923986766
Adresse: c/o Fjordkraft AS, Postboks 3507 Fyllingsdalen, 5845 BERGEN
======================================================================
✅ Lookup completed successfully
```

## API Endpoints Used

- **Main entities**: `https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}`
- **Sub-entities**: `https://data.brreg.no/enhetsregisteret/api/underenheter/{orgnr}`

## Error Handling

- Validates 9-digit organization number format
- Handles API timeouts and connection errors
- Falls back to sub-entities if not found in main entities
- Provides clear error messages

## 🏗️ Architecture

This tool demonstrates professional Python development practices:

### **Core Components**

- **`BRREGClient`**: Professional API client with session management and error handling
- **`OrganizationInfo`**: Type-safe data class for organization information with relevance scoring
- **`Address`**: Structured address handling with intelligent formatting
- **`EntityType`**: Enum for type safety and clear entity classification
- **`TextMatcher`**: Advanced text matching and relevance scoring algorithm
- **`OrganizationDisplayFormatter`**: Separation of concerns for output formatting with relevance indicators
- **`InputValidator`**: Centralized validation logic with clear error messages

### **Design Patterns**

- **Single Responsibility Principle**: Each class has one clear purpose
- **Type Safety**: Comprehensive type hints throughout the codebase
- **Error Handling**: Graceful degradation with helpful user feedback
- **Separation of Concerns**: API logic, data models, and presentation are decoupled
- **Professional CLI**: Modern argument parsing with comprehensive help

### **Key Benefits for Developers**

- **Maintainable**: Clear class structure and separation of concerns
- **Extensible**: Easy to add new features or modify existing behavior
- **Testable**: Modular design enables comprehensive unit testing
- **Professional**: Follows Python best practices and modern conventions
- **Documented**: Comprehensive docstrings and type hints

This addresses the affiliate association lookup issue by checking both main entities and sub-entities (underenheter) endpoints while demonstrating enterprise-grade Python development practices.
