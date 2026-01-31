# Batch File Renamer

A batch file renaming tool with a complete graphical interface.

## Features

- Multiple Renaming Modes
  - Add prefix/suffix
  - Text replacement (with regex support)
  - Number sequence naming
  - Case conversion
  - Date/time naming
  
- File Management
  - Recursive directory processing
  - File type filtering
  - Real-time preview
  - Undo functionality
  
- User-Friendly GUI
  - Intuitive interface
  - Drag-and-drop support
  - Batch operations
  - Operation history

## Installation

```bash
# Clone the project
git clone https://github.com/FelistaYE/Batch-File-Renamer.git
cd Batch-File-Renamer

# Run the program
python run_i18n.py
```

## Usage

1. Launch the program and click "Select Directory" to choose the folder
2. Select files to rename in the left file list
3. Choose a renaming mode and set parameters on the right
4. Click "Preview" to see the renaming results
5. Click "Execute Rename" to apply changes after confirmation

## Renaming Modes

### Add Prefix/Suffix
- Add fixed text at the beginning or end of filename
- Example: `photo.jpg` → `vacation_photo.jpg`

### Text Replacement
- Replace specified text in filenames
- Supports regular expressions
- Example: `IMG_001.jpg` → `Photo_001.jpg`

### Number Sequence
- Rename files with sequential numbers
- Customizable starting number and digits
- Example: `file1.txt`, `file2.txt` → `001.txt`, `002.txt`

### Case Conversion
- Convert to uppercase, lowercase, or title case
- Example: `MyFile.TXT` → `myfile.txt`

### Date/Time
- Name files using modification or creation time
- Customizable date format
- Example: `document.pdf` → `20260131_143052.pdf`

## System Requirements

- Python 3.7+

## Notes

- Preview before renaming
- Program automatically handles filename conflicts
- Undo feature available for recent operations
- Backup important files before batch operations

## Other Language

- [中文文档](README_ZH.md)
