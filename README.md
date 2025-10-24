# BRREG API Lookup Tool

Simple Python script to lookup Norwegian organization information from Brønnøysundregisteret (BRREG) API.

## Features

- Looks up both main entities (`enheter`) and sub-entities (`underenheter`)
- Returns company name and address
- Handles both business address and postal address
- Shows additional info like organization form and industry code

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python brreg_lookup.py <9-digit-org-number>
```

## Examples

```bash
# Lookup Equinor ASA
python brreg_lookup.py 923609016

# Lookup any organization
python brreg_lookup.py 123456789
```

## Output Example

```
Looking up organization number: 923609016
--------------------------------------------------
Checking main entities: https://data.brreg.no/enhetsregisteret/api/enheter/923609016
✅ Organization found!
Type: Hovedenhet
Navn: EQUINOR ASA
Adresse: Forusbeen 50, 4035 STAVANGER
Organisasjonsform: Allmennaksjeselskap
Næringskode: Utvinning av råolje
--------------------------------------------------
Org.nr: 923609016
```

## API Endpoints Used

- **Main entities**: `https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}`
- **Sub-entities**: `https://data.brreg.no/enhetsregisteret/api/underenheter/{orgnr}`

## Error Handling

- Validates 9-digit organization number format
- Handles API timeouts and connection errors
- Falls back to sub-entities if not found in main entities
- Provides clear error messages

This addresses the affiliate association lookup issue by checking both main entities and sub-entities (underenheter) endpoints.
