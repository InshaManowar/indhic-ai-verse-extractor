#!/usr/bin/env python3
"""
Ashtavakra Gita Verse Extractor

This script extracts verses from the Ashtavakra Gita text file and outputs them
in a structured JSON format.
"""

import argparse
import json
import re
import requests
import sys
import os
from typing import Dict, List, Optional, Tuple

# Handle imports for both direct script execution and package usage
try:
    # When running as a package
    from .config import DEFAULT_URL, DEFAULT_OUTPUT_PATH, ERROR_NO_SOURCE, ERROR_FETCH_URL, ERROR_READ_FILE
    from .utils import detect_verse_format, normalize_whitespace, group_verse_lines, find_text_section
except ImportError:
    # When running script directly
    from config import DEFAULT_URL, DEFAULT_OUTPUT_PATH, ERROR_NO_SOURCE, ERROR_FETCH_URL, ERROR_READ_FILE
    from utils import detect_verse_format, normalize_whitespace, group_verse_lines, find_text_section


class VerseExtractor:
    """Class to extract verses from the Ashtavakra Gita text."""

    def __init__(self, text_content: Optional[str] = None, url: Optional[str] = None, file_path: Optional[str] = None):
        """
        Initialize the extractor with text content, URL, or file path.

        Args:
            text_content (str, optional): The text content to parse.
            url (str, optional): URL to fetch the text from.
            file_path (str, optional): Path to a local text file.
        """
        if text_content:
            self.text_content = text_content
        elif url:
            self.text_content = self._fetch_text(url)
        elif file_path:
            self.text_content = self._read_file(file_path)
        else:
            raise ValueError(ERROR_NO_SOURCE)

    def _fetch_text(self, url: str) -> str:
        """
        Fetch text content from a URL.

        Args:
            url (str): URL to fetch text from.

        Returns:
            str: The text content.

        Raises:
            Exception: If fetch fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(ERROR_FETCH_URL.format(e))

    def _read_file(self, file_path: str) -> str:
        """
        Read text content from a file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: The text content.

        Raises:
            Exception: If file reading fails.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(ERROR_READ_FILE.format(e))

    def extract_verses(self) -> List[Dict[str, str]]:
        """
        Extract verses from the text content.

        Returns:
            List[Dict[str, str]]: List of dictionaries with verse content and index.
        """
        # Split the text content into lines
        lines = self.text_content.split('\n')
        
        # Skip header content and find where the actual text starts
        text_start_index = find_text_section(lines)
        text_lines = lines[text_start_index:]
        
        # Group the lines into verses
        verses = group_verse_lines(text_lines)
        
        return verses

    def save_to_json(self, output_path: str) -> List[Dict[str, str]]:
        """
        Extract verses and save them to a JSON file.

        Args:
            output_path (str): Path to save the JSON output.
            
        Returns:
            List[Dict[str, str]]: The extracted verses.
        """
        verses = self.extract_verses()
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(verses, f, ensure_ascii=False, indent=2)
            
        return verses


def main():
    """Run the verse extraction process."""
    parser = argparse.ArgumentParser(description='Extract verses from Ashtavakra Gita.')
    parser.add_argument('--url', default=DEFAULT_URL,
                        help='URL of the text file')
    parser.add_argument('--file', help='Path to a local text file')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_PATH,
                        help='Output JSON file path')
    
    args = parser.parse_args()
    
    try:
        if args.file:
            extractor = VerseExtractor(file_path=args.file)
        else:
            extractor = VerseExtractor(url=args.url)
            
        verses = extractor.save_to_json(args.output)
        
        print(f"Successfully extracted {len(verses)} verses to {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main() 