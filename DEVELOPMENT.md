# Development Guide

This guide helps developers understand, modify, and extend the BRREG API Lookup Tool.

## 🏗️ Architecture Overview

### Core Classes

```
BRREGClient
├── Session management and HTTP requests
├── API endpoint handling (enheter/underenheter)
├── Response parsing and error handling
└── Relevance scoring integration

TextMatcher
├── Advanced text similarity algorithms
├── Relevance score calculation
├── Word order preservation detection
└── Fuzzy matching with difflib

OrganizationInfo (DataClass)
├── Type-safe data structure
├── Address handling (business/postal)
├── Relevance scoring
└── Entity type classification

OrganizationDisplayFormatter
├── Result presentation logic
├── Relevance indicator display
├── Consistent formatting
└── User-friendly output
```

### Data Flow

```
User Input → InputValidator → BRREGClient → API Request
                                    ↓
TextMatcher ← OrganizationInfo ← API Response
     ↓
Relevance Scoring → Sort Results → DisplayFormatter → User Output
```

## 🔧 Key Design Decisions

### 1. **Separation of Concerns**
- **API Logic**: Isolated in `BRREGClient`
- **Data Models**: Clean dataclasses with type hints
- **Text Processing**: Dedicated `TextMatcher` class
- **Presentation**: Separate `DisplayFormatter`

### 2. **Type Safety**
```python
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

# All functions have comprehensive type hints
def search_by_name(self, name: str) -> List[OrganizationInfo]:
```

### 3. **Error Handling Strategy**
- **Graceful Degradation**: Continue operation when possible
- **User-Friendly Messages**: Clear, actionable error descriptions
- **Comprehensive Logging**: Detailed error information for debugging

### 4. **Intelligent Ranking Algorithm**
```python
# Scoring hierarchy:
1.0   - Exact match
0.95  - Substring containment  
0.9   - Reverse containment
0.x   - Fuzzy similarity + bonuses
+0.2  - All query words present
+0.1  - Word order preserved
```

## 🚀 Adding New Features

### Adding a New Search Filter

1. **Extend OrganizationInfo**:
```python
@dataclass
class OrganizationInfo:
    # ... existing fields
    municipality: Optional[str] = None  # New field
```

2. **Update API Parsing**:
```python
def _parse_organization_data(self, data: Dict, ...):
    municipality = data.get('kommune', {}).get('kommunenavn')
    return OrganizationInfo(..., municipality=municipality)
```

3. **Add CLI Argument**:
```python
parser.add_argument('--municipality', help='Filter by municipality')
```

### Adding New Relevance Factors

1. **Extend TextMatcher**:
```python
@staticmethod
def _calculate_location_bonus(query: str, org_info: OrganizationInfo) -> float:
    # Custom scoring logic
    return bonus_score
```

2. **Integrate into Main Scoring**:
```python
def calculate_relevance_score(query: str, org_info: OrganizationInfo) -> float:
    base_score = # ... existing logic
    location_bonus = TextMatcher._calculate_location_bonus(query, org_info)
    return min(base_score + location_bonus, 1.0)
```

## 🧪 Testing Strategy

### Unit Tests Structure
```
tests/
├── test_brreg_client.py      # API client tests
├── test_text_matcher.py      # Text matching algorithm tests
├── test_data_models.py       # Data class validation tests
├── test_display_formatter.py # Output formatting tests
└── test_integration.py       # End-to-end tests
```

### Example Test Cases
```python
def test_exact_match_scoring():
    score = TextMatcher.calculate_relevance_score(
        "FJORDKRAFT AS", "FJORDKRAFT AS"
    )
    assert score == 1.0

def test_substring_match_scoring():
    score = TextMatcher.calculate_relevance_score(
        "FJORDKRAFT", "FJORDKRAFT AS AVD OSLO"
    )
    assert score == 0.95
```

## 🔍 Debugging Tips

### Enable Verbose Logging
```python
# Add to BRREGClient.__init__
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```python
# Test text matching in isolation
from brreg_lookup import TextMatcher
score = TextMatcher.calculate_relevance_score("query", "organization name")
print(f"Relevance score: {score}")
```

### API Response Inspection
```python
# Add temporary debugging in _parse_organization_data
print(f"Raw API data: {json.dumps(data, indent=2, ensure_ascii=False)}")
```

## 📈 Performance Considerations

### Current Optimizations
- **Session Reuse**: Single HTTP session for all requests
- **Efficient Sorting**: Single sort operation with compound key
- **Lazy Evaluation**: Only calculate scores when needed

### Potential Improvements
- **Caching**: Cache API responses for repeated queries
- **Async Requests**: Parallel API calls for better performance
- **Result Pagination**: Handle large result sets efficiently

## 🤝 Contributing Guidelines

### Code Style
- **Type Hints**: All functions must have type annotations
- **Docstrings**: Google-style docstrings for all public methods
- **Error Handling**: Comprehensive exception handling
- **Naming**: Descriptive variable and method names

### Commit Message Format
```
feat: add intelligent search ranking algorithm
fix: resolve affiliate association ordering issue
docs: update README with new features
refactor: improve text matching performance
```

### Pull Request Checklist
- [ ] All tests pass
- [ ] Type hints added
- [ ] Documentation updated
- [ ] Examples work correctly
- [ ] CHANGELOG.md updated

## 🔧 Development Setup

```bash
# Clone and setup
git clone <repository>
cd kb_brreg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run examples
python examples.py

# Check code style
python -m flake8 brreg_lookup.py
python -m mypy brreg_lookup.py
```

## 📚 Additional Resources

- **BRREG API Documentation**: https://data.brreg.no/enhetsregisteret/api/docs/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **Dataclasses Guide**: https://docs.python.org/3/library/dataclasses.html
- **Argparse Documentation**: https://docs.python.org/3/library/argparse.html
