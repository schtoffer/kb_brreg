# Changelog

All notable changes to the BRREG API Lookup Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-10-24

### 🎯 Major Features Added
- **Intelligent Search Ranking**: Advanced text matching algorithm with relevance scoring
- **Visual Relevance Indicators**: 🎯 EXACT MATCH, ⭐ HIGH RELEVANCE, 📍 GOOD MATCH
- **Smart Result Sorting**: Most relevant results appear first instead of API order
- **Fuzzy Text Matching**: Uses difflib.SequenceMatcher for similarity scoring
- **Word Order Preservation**: Bonus scoring for maintaining query word sequence

### 🏗️ Architecture Improvements
- **TextMatcher Class**: Professional text matching and scoring algorithms
- **Enhanced OrganizationInfo**: Added relevance_score field with type safety
- **Improved Display Formatter**: Visual indicators and relevance score display
- **Better Error Handling**: More descriptive error messages and user guidance

### 🔧 Technical Enhancements
- **Type Safety**: Comprehensive type hints throughout codebase
- **Professional Documentation**: Detailed docstrings and inline comments
- **Modular Design**: Clear separation of concerns with single responsibility classes
- **Session Management**: Reusable HTTP sessions with proper headers

### 🎨 User Experience
- **Beautiful CLI Interface**: Modern emojis and professional formatting
- **Relevance Scoring**: Shows confidence scores for top matches
- **Better Help System**: Comprehensive examples and feature descriptions
- **Progress Indicators**: Clear feedback during API operations

### 🐛 Bug Fixes
- **Affiliate Association Issue**: Fixed problem where sub-entities appeared after main entities
- **Search Result Ordering**: Exact matches now appear first regardless of entity type
- **Address Formatting**: Improved handling of missing address data

### 📚 Documentation
- **Updated README**: Comprehensive feature documentation with examples
- **Usage Examples**: Added examples.py with practical use cases
- **Architecture Guide**: Detailed explanation of design patterns and components
- **API Documentation**: Clear endpoint documentation and error handling

## [1.0.0] - 2024-10-24

### Initial Release
- **Basic Organization Lookup**: Search by organization number
- **Name-based Search**: Search organizations by name
- **Dual API Support**: Query both enheter and underenheter endpoints
- **Command Line Interface**: Professional argument parsing
- **Error Handling**: Basic validation and error messages
- **Data Display**: Formatted output with organization details

---

### Legend
- 🎯 **Major Features**: Significant new functionality
- 🏗️ **Architecture**: Code structure and design improvements  
- 🔧 **Technical**: Under-the-hood improvements
- 🎨 **UX**: User experience enhancements
- 🐛 **Bug Fixes**: Issue resolutions
- 📚 **Documentation**: Documentation updates
