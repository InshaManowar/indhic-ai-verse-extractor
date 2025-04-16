"""
Configuration settings for the Ashtavakra Gita Verse Extractor.
"""

# Default URL for the text file
DEFAULT_URL = "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/sa_aSTAvakragItA.txt"

# Default output path
DEFAULT_OUTPUT_PATH = "verses.json"

# Regular expression for verse format
VERSE_PATTERN = r'(.*?)//\s*Avg_(\d+\.\d+)\s*$'

# Markers for identifying text sections
TEXT_START_MARKER = "# Text"
VERSE_REFERENCE_MARKER = "Avg_"

# Error messages
ERROR_NO_SOURCE = "Either text_content, url, or file_path must be provided"
ERROR_FETCH_URL = "Failed to fetch text from URL: {}"
ERROR_READ_FILE = "Failed to read file: {}" 