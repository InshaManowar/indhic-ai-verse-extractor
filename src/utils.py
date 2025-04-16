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
    Sanskrit verses typically consist of two lines with the verse index at the end
    of the second line.

    Args:
        lines (List[str]): Lines to process.

    Returns:
        List[Dict[str, str]]: List of dictionaries with verse content and index.
    """
    verses = []
    pending_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        if not line:
            continue
        
        # Check if this line contains a verse marker
        verse_content, verse_index = detect_verse_format(line)
        
        if verse_content is not None:
            # This line has a verse marker
            if pending_lines:
                # If we have a pending line, combine it with this line to form a complete verse
                complete_verse = [pending_lines[-1], verse_content]
                verses.append({
                    "verse": "\n".join(complete_verse),
                    "index": verse_index
                })
                pending_lines = []
            else:
                # If there's no pending line, just add this line as a verse
                verses.append({
                    "verse": verse_content,
                    "index": verse_index
                })
        else:
            # Line without a verse marker - store it as a pending line
            pending_lines.append(line)
            
            # But check if the next line has a verse marker
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line:  # Skip empty lines
                    next_content, next_index = detect_verse_format(next_line)
                    if next_content is not None:
                        # Next line has a marker, so together they form a verse
                        verses.append({
                            "verse": line + "\n" + next_content,
                            "index": next_index
                        })
                        i += 1  # Skip the next line since we've processed it
                        pending_lines = []
    
    # Handle any remaining pending lines (should be rare in well-formed input)
    if pending_lines and len(verses) > 0:
        # If we have an incomplete verse at the end, add it to the last verse
        last_verse = verses[-1]["verse"]
        verses[-1]["verse"] = last_verse + "\n" + "\n".join(pending_lines)
        
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