# Project Structure Documentation

Complete overview of the Video Text Blur Tool project structure and organization.

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [File Descriptions](#file-descriptions)
3. [Documentation Files](#documentation-files)
4. [Source Code Files](#source-code-files)
5. [Configuration Files](#configuration-files)
6. [Script Files](#script-files)
7. [File Dependencies](#file-dependencies)
8. [Development Workflow](#development-workflow)

---

## Directory Structure

```
video-text-blur/
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
│
├── blur_text_video.py            # Main application script
├── example_usage.py              # Usage examples
│
├── run_blur.sh                   # Convenience script
├── run_blur_interactive.sh       # Interactive mode script
│
├── Documentation/                # All documentation files
│   ├── README.md                 # Main project documentation
│   ├── QUICK_START.md            # Quick start guide
│   ├── USAGE_SUMMARY.md          # Usage summary
│   ├── UPDATED_FEATURES.md       # Feature documentation
│   ├── BLUR_WORDS_EXAMPLE.md     # Word blurring examples
│   │
│   ├── API_REFERENCE.md          # API documentation
│   ├── ARCHITECTURE.md           # Architecture documentation
│   ├── TECHNICAL_DOCUMENTATION.md # Technical details
│   ├── INSTALLATION.md           # Installation guide
│   ├── TROUBLESHOOTING.md        # Troubleshooting guide
│   ├── PERFORMANCE.md            # Performance optimization
│   │
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── CODE_OF_CONDUCT.md        # Code of conduct
│   ├── SECURITY.md               # Security policy
│   └── PROJECT_STRUCTURE.md      # This file
│
└── .EasyOCR/                     # OCR models (auto-created)
    └── model/                    # Downloaded models
```

---

## File Descriptions

### Core Application Files

#### `blur_text_video.py`
**Purpose**: Main application script  
**Type**: Python executable  
**Size**: ~309 lines  
**Key Components**:
- `VideoTextBlur` class
- CLI argument parsing
- Main processing logic
- Video I/O operations
- OCR integration
- Blur application

**Usage**:
```bash
python3 blur_text_video.py input.mp4 output.mp4 [OPTIONS]
```

**Key Functions**:
- `__init__()`: Initialize OCR and configuration
- `should_blur_text()`: Text matching logic
- `detect_text_regions()`: OCR text detection
- `blur_regions()`: Apply blur to regions
- `process_video()`: Main processing pipeline
- `main()`: CLI entry point

#### `example_usage.py`
**Purpose**: Code examples and usage patterns  
**Type**: Python script  
**Size**: ~120 lines  
**Contains**:
- Basic usage example
- Custom settings example
- Batch processing example
- Error handling example

**Usage**:
```bash
python3 example_usage.py
```

---

### Documentation Files

#### User Documentation

##### `README.md`
**Purpose**: Main project documentation  
**Audience**: All users  
**Contains**:
- Project overview
- Features list
- Installation instructions
- Basic usage
- Examples
- Troubleshooting basics

##### `QUICK_START.md`
**Purpose**: Fast onboarding guide  
**Audience**: New users  
**Contains**:
- Fastest way to use
- Common commands
- Quick tips
- Current features

##### `USAGE_SUMMARY.md`
**Purpose**: Quick reference for specific video  
**Audience**: End users  
**Contains**:
- Current video settings
- Quick commands
- Troubleshooting tips

##### `UPDATED_FEATURES.md`
**Purpose**: New features documentation  
**Audience**: Existing users  
**Contains**:
- Selective word blurring
- QuickTime compatibility
- Usage examples
- Technical details

##### `BLUR_WORDS_EXAMPLE.md`
**Purpose**: Word blurring examples  
**Audience**: Users needing selective blur  
**Contains**:
- Word matching examples
- Use cases
- Best practices

##### `STELLANTIS_RUN.md`
**Purpose**: Specific use case documentation  
**Audience**: Specific project users  
**Contains**:
- Project-specific instructions
- Custom configurations

#### Technical Documentation

##### `API_REFERENCE.md`
**Purpose**: Complete API documentation  
**Audience**: Developers  
**Contains**:
- Class documentation
- Method signatures
- Parameters and return values
- Code examples
- Type hints

##### `ARCHITECTURE.md`
**Purpose**: System architecture  
**Audience**: Developers, architects  
**Contains**:
- System overview
- Component architecture
- Data flow diagrams
- Technology stack
- Design patterns

##### `TECHNICAL_DOCUMENTATION.md`
**Purpose**: Comprehensive technical reference  
**Audience**: Advanced users, developers  
**Contains**:
- Detailed specifications
- Dependencies
- Changelog
- Performance benchmarks
- Appendices

##### `INSTALLATION.md`
**Purpose**: Detailed installation guide  
**Audience**: All users  
**Contains**:
- Platform-specific instructions
- Dependency installation
- Verification steps
- Troubleshooting installation

##### `TROUBLESHOOTING.md`
**Purpose**: Problem-solving guide  
**Audience**: All users  
**Contains**:
- Common issues and solutions
- Error messages
- Platform-specific issues
- Advanced troubleshooting

##### `PERFORMANCE.md`
**Purpose**: Performance optimization  
**Audience**: Users seeking better performance  
**Contains**:
- Optimization tips
- Hardware recommendations
- Configuration tuning
- Benchmarking

#### Community Documentation

##### `CONTRIBUTING.md`
**Purpose**: Contribution guidelines  
**Audience**: Contributors  
**Contains**:
- How to contribute
- Coding standards
- Pull request process
- Development setup

##### `CODE_OF_CONDUCT.md`
**Purpose**: Community standards  
**Audience**: All community members  
**Contains**:
- Expected behavior
- Unacceptable behavior
- Enforcement guidelines
- Reporting process

##### `SECURITY.md`
**Purpose**: Security policy  
**Audience**: Security researchers, users  
**Contains**:
- Vulnerability reporting
- Security features
- Best practices
- Known considerations

##### `PROJECT_STRUCTURE.md`
**Purpose**: Project organization  
**Audience**: Developers, contributors  
**Contains**:
- Directory structure
- File descriptions
- Dependencies
- Workflow

---

### Configuration Files

#### `requirements.txt`
**Purpose**: Python dependencies  
**Type**: pip requirements file  
**Contains**:
```txt
opencv-python>=4.8.0
opencv-contrib-python>=4.8.0
easyocr>=1.7.0
pytesseract>=0.3.10
ffmpeg-python>=0.2.0
numpy>=1.24.0
Pillow>=10.0.0
tqdm>=4.65.0
```

**Usage**:
```bash
pip install -r requirements.txt
```

#### `.gitignore`
**Purpose**: Git ignore rules  
**Type**: Git configuration  
**Contains**:
- Python cache files
- Virtual environments
- Video files
- OS-specific files
- IDE files
- OCR model cache

**Key Patterns**:
```
__pycache__/
*.pyc
venv/
*.mp4
*.mov
.DS_Store
.EasyOCR/
```

---

### Script Files

#### `run_blur.sh`
**Purpose**: Convenience script for specific video  
**Type**: Bash script  
**Executable**: Yes (`chmod +x`)  
**Contains**:
- Predefined input/output paths
- Default parameters
- User-friendly output

**Usage**:
```bash
./run_blur.sh
```

**Configuration**:
```bash
INPUT_VIDEO="2 - wx gov - creation Usecase.mp4"
OUTPUT_VIDEO="2 - wx gov - creation Usecase_BLURRED.mp4"
```

#### `run_blur_interactive.sh`
**Purpose**: Interactive mode launcher  
**Type**: Bash script  
**Executable**: Yes (`chmod +x`)  
**Contains**:
- Interactive prompts
- User input handling
- Parameter passing

**Usage**:
```bash
./run_blur_interactive.sh
```

---

## File Dependencies

### Dependency Graph

```
blur_text_video.py
├── Python 3.8+
├── opencv-python
├── easyocr
│   └── PyTorch
├── numpy
├── Pillow
├── tqdm
└── FFmpeg (external)

example_usage.py
└── blur_text_video.py

run_blur.sh
└── blur_text_video.py

run_blur_interactive.sh
└── blur_text_video.py

Documentation files
└── (no dependencies)
```

### Import Dependencies

```python
# blur_text_video.py imports
import cv2                    # opencv-python
import easyocr               # easyocr
import numpy as np           # numpy
from pathlib import Path     # stdlib
import argparse              # stdlib
from tqdm import tqdm        # tqdm
import sys                   # stdlib
import subprocess            # stdlib
```

---

## Development Workflow

### File Creation Order

1. **Core Application**
   - `blur_text_video.py` (main script)
   - `requirements.txt` (dependencies)

2. **Basic Documentation**
   - `Documentation/README.md` (overview)
   - `.gitignore` (version control)

3. **Usage Examples**
   - `example_usage.py` (code examples)
   - `run_blur.sh` (convenience script)

4. **User Guides**
   - `Documentation/QUICK_START.md`
   - `Documentation/USAGE_SUMMARY.md`
   - `Documentation/UPDATED_FEATURES.md`

5. **Technical Documentation**
   - `Documentation/API_REFERENCE.md`
   - `Documentation/ARCHITECTURE.md`
   - `Documentation/TECHNICAL_DOCUMENTATION.md`

6. **Support Documentation**
   - `Documentation/INSTALLATION.md`
   - `Documentation/TROUBLESHOOTING.md`
   - `Documentation/PERFORMANCE.md`

7. **Community Documentation**
   - `Documentation/CONTRIBUTING.md`
   - `Documentation/CODE_OF_CONDUCT.md`
   - `Documentation/SECURITY.md`

8. **Project Documentation**
   - `Documentation/PROJECT_STRUCTURE.md`

### File Modification Frequency

| File | Frequency | Reason |
|------|-----------|--------|
| `blur_text_video.py` | High | Feature development |
| `requirements.txt` | Medium | Dependency updates |
| `Documentation/README.md` | Medium | Feature additions |
| `Documentation/TECHNICAL_DOCUMENTATION.md` | Medium | Version updates |
| `Documentation/API_REFERENCE.md` | Medium | API changes |
| Documentation files | Low | Clarifications |
| Configuration files | Low | Rare changes |

---

## File Size Overview

| File | Approximate Size | Lines |
|------|-----------------|--------|
| `blur_text_video.py` | 10 KB | 309 |
| `example_usage.py` | 4 KB | 120 |
| `Documentation/README.md` | 7 KB | 174 |
| `Documentation/API_REFERENCE.md` | 22 KB | 545 |
| `Documentation/ARCHITECTURE.md` | 33 KB | 835 |
| `Documentation/TECHNICAL_DOCUMENTATION.md` | 16 KB | 410 |
| `Documentation/CONTRIBUTING.md` | 28 KB | 717 |
| `Documentation/CODE_OF_CONDUCT.md` | 12 KB | 298 |
| `Documentation/SECURITY.md` | 21 KB | 545 |
| `Documentation/INSTALLATION.md` | 26 KB | 673 |
| `Documentation/TROUBLESHOOTING.md` | 32 KB | 827 |
| `Documentation/PERFORMANCE.md` | 30 KB | 773 |
| Other docs | 2-5 KB each | 50-150 |

**Total Documentation**: ~250 KB  
**Total Code**: ~15 KB  
**Ratio**: 17:1 (documentation to code)

---

## File Relationships

### Documentation Hierarchy

```
Documentation/README.md (Entry point)
├── Documentation/QUICK_START.md (Quick reference)
├── Documentation/INSTALLATION.md (Setup)
│   └── Documentation/TROUBLESHOOTING.md (Problems)
├── Documentation/USAGE_SUMMARY.md (Usage)
│   ├── Documentation/UPDATED_FEATURES.md (Features)
│   └── Documentation/BLUR_WORDS_EXAMPLE.md (Examples)
├── Documentation/API_REFERENCE.md (API)
│   └── example_usage.py (Code examples)
├── Documentation/ARCHITECTURE.md (Design)
│   └── Documentation/TECHNICAL_DOCUMENTATION.md (Details)
├── Documentation/PERFORMANCE.md (Optimization)
├── Documentation/CONTRIBUTING.md (Development)
│   ├── Documentation/CODE_OF_CONDUCT.md (Community)
│   └── Documentation/SECURITY.md (Security)
└── Documentation/PROJECT_STRUCTURE.md (Organization)
```

### Cross-References

Files that reference each other:

- `Documentation/README.md` → All documentation files
- `Documentation/CONTRIBUTING.md` → `CODE_OF_CONDUCT.md`, `SECURITY.md`
- `Documentation/API_REFERENCE.md` → `example_usage.py`, `ARCHITECTURE.md`
- `Documentation/INSTALLATION.md` → `TROUBLESHOOTING.md`, `QUICK_START.md`
- `Documentation/TROUBLESHOOTING.md` → `INSTALLATION.md`, `PERFORMANCE.md`

---

## Maintenance Guidelines

### Regular Updates

**Monthly**:
- Update `requirements.txt` with latest versions
- Review and update `Documentation/TROUBLESHOOTING.md`
- Check `Documentation/README.md` for accuracy

**Per Release**:
- Update `Documentation/TECHNICAL_DOCUMENTATION.md` changelog
- Update version numbers
- Review all documentation for accuracy

**As Needed**:
- Update `Documentation/API_REFERENCE.md` when API changes
- Update `Documentation/ARCHITECTURE.md` when design changes
- Update `Documentation/CONTRIBUTING.md` when process changes

### Documentation Standards

1. **Markdown Format**: All documentation in Markdown
2. **Table of Contents**: Include in long documents
3. **Code Examples**: Use syntax highlighting
4. **Cross-References**: Link related documents
5. **Version Info**: Include version and date
6. **Consistent Style**: Follow same formatting

---

## Adding New Files

### Checklist for New Files

- [ ] Add to `.gitignore` if needed
- [ ] Update `Documentation/PROJECT_STRUCTURE.md`
- [ ] Add cross-references in related docs
- [ ] Include in `Documentation/README.md` if user-facing
- [ ] Add to appropriate section above
- [ ] Follow naming conventions
- [ ] Include file header/description

### Naming Conventions

- **Documentation**: `UPPERCASE_WITH_UNDERSCORES.md`
- **Scripts**: `lowercase_with_underscores.py`
- **Shell scripts**: `lowercase_with_underscores.sh`
- **Config files**: `lowercase` or `.lowercase`

---

## File Templates

### Documentation Template

```markdown
# Document Title

Brief description of the document.

---

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)

---

## Section 1

Content here...

---

**Document Version**: 1.0.0  
**Last Updated**: YYYY-MM-DD

---

**End of Document**
```

### Python Script Template

```python
#!/usr/bin/env python3
"""
Script Title
Brief description of what the script does
"""

import sys
# Other imports...

def main():
    """Main function"""
    pass

if __name__ == '__main__':
    main()
```

### Shell Script Template

```bash
#!/bin/bash
# Script Title
# Brief description

set -e  # Exit on error

echo "Starting..."

# Script logic here

echo "Done!"
```

---

## Version Control

### Git Workflow

```bash
# Main branch
main
├── feature/new-feature
├── fix/bug-fix
└── docs/documentation-update
```

### Commit Message Format

```
type(scope): subject

body

footer
```

**Types**: feat, fix, docs, style, refactor, test, chore

---

## Future Structure

### Planned Additions

```
video-text-blur/
├── tests/                    # Test suite
│   ├── test_blur.py
│   ├── test_ocr.py
│   └── test_integration.py
├── docs/                     # Documentation directory
│   ├── api/
│   ├── guides/
│   └── examples/
├── scripts/                  # Utility scripts
│   ├── benchmark.sh
│   └── setup.sh
├── docker/                   # Docker files
│   ├── Dockerfile
│   └── docker-compose.yml
└── .github/                  # GitHub specific
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

---

## Summary

### Key Files

**Must Read**:
1. `Documentation/README.md` - Start here
2. `Documentation/QUICK_START.md` - Get started quickly
3. `Documentation/INSTALLATION.md` - Setup instructions

**For Users**:
- `Documentation/USAGE_SUMMARY.md`
- `Documentation/TROUBLESHOOTING.md`
- `Documentation/PERFORMANCE.md`

**For Developers**:
- `Documentation/API_REFERENCE.md`
- `Documentation/ARCHITECTURE.md`
- `Documentation/CONTRIBUTING.md`

**For Contributors**:
- `Documentation/CONTRIBUTING.md`
- `Documentation/CODE_OF_CONDUCT.md`
- `Documentation/PROJECT_STRUCTURE.md`

---

**Document Version**: 1.0.0  
**Last Updated**: February 22, 2026

---

**End of Project Structure Documentation**