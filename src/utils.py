"""
Utility functions for the Ashtavakra Gita Verse Extractor.
"""

import re
from typing import List, Dict, Optional, Tuple

# Handle imports for both direct script execution and package usage
try:
    # When running as a package
    from .config import VERSE_PATTERN, TEXT_START_MARKER, VERSE_REFERENCE_MARKER
except ImportError:
    # When running script directly
    from config import VERSE_PATTERN, TEXT_START_MARKER, VERSE_REFERENCE_MARKER


def detect_verse_format(line: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Detect if a line contains a verse with index and extract its parts.

    Args:
        line (str): The line to analyze.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing (verse_content, verse_index)
            or (None, None) if no verse is detected.
    """
    # Pattern to match verse lines with index like "// Avg_1.5"
    verse_pattern = re.compile(VERSE_PATTERN)
    match = verse_pattern.match(line.strip())
    
    if match:
        verse_content = match.group(1).strip()
        verse_index = match.group(2)
        return verse_content, verse_index
    
    return None, None


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text to ensure consistent formatting.

    Args:
        text (str): The text to normalize.

    Returns:
        str: Text with normalized whitespace.
    """
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def group_verse_lines(lines: List[str]) -> List[Dict[str, str]]:
    """
    Group lines into verses with their indices.

    Args:
        lines (List[str]): Lines to process.

    Returns:
        List[Dict[str, str]]: List of dictionaries with verse content and index.
    """
    verses = []
    current_verse_lines = []
    current_index = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        verse_content, verse_index = detect_verse_format(line)
        
        if verse_content is not None:
            # If we have collected lines from a previous verse, save it
            if current_verse_lines and current_index:
                verses.append({
                    "verse": "\n".join(current_verse_lines),
                    "index": current_index
                })
            
            # Start a new verse
            current_verse_lines = [verse_content]
            current_index = verse_index
        else:
            # Continue collecting lines for the current verse
            if current_verse_lines:  # Only append if we're collecting a verse
                current_verse_lines.append(line)
    
    # Add the last verse if there is one
    if current_verse_lines and current_index:
        verses.append({
            "verse": "\n".join(current_verse_lines),
            "index": current_index
        })
        
    return verses


def find_text_section(lines: List[str]) -> int:
    """
    Find the index where the main text section starts.

    Args:
        lines (List[str]): List of lines in the file.

    Returns:
        int: Index where the main text starts.
    """
    for i, line in enumerate(lines):
        if line.strip() == TEXT_START_MARKER:
            # Skip the "# Text" line and any blank lines after it
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            return i
    
    # If we can't find the "# Text" marker, try to find where the actual verses start
    for i, line in enumerate(lines):
        if VERSE_REFERENCE_MARKER in line:
            return i
            
    return 0  # Default to the beginning if we can't find a better starting point 