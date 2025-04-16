# Ashtavakra Gita Verse Extractor

This project extracts verses from the Ashtavakra Gita text and outputs them in a structured JSON format. The source text is available at [https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/sa_aSTAvakragItA.txt](https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/sa_aSTAvakragItA.txt).

## Overview

The project extracts verses in the format:

```
na tvaṃ viprādiko varṇo nāśramī nākṣagocaraḥ 
asaṅgo 'si nirākāro viśvasākṣī sukhī bhava // Avg_1.5
```

And outputs them as JSON:

```json
{
  "verse": "na tvaṃ viprādiko varṇo nāśramī nākṣagocaraḥ\nasaṅgo 'si nirākāro viśvasākṣī sukhī bhava",
  "index": "1.5"
}
```

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone the repository:

```bash
[git clone https://github.com/yourusername/ashtavakra-gita-extractor.git](https://github.com/InshaManowar/indhic-ai-verse-extractor)
cd indhic-ai-verse-extractor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command-line interface

Run the extractor with default settings:

```bash
python -m src
```

This will fetch the text from the default URL and save the verses to `verses.json`.

You can specify a different URL or local file:

```bash
python -m src --url https://example.com/text.txt
python -m src --file path/to/local/file.txt
```

You can also specify a different output file:

```bash
python -m src --output my_verses.json
```

### Using as a library

```python
from src import VerseExtractor

# From URL
extractor = VerseExtractor(url="https://example.com/text.txt")

# From local file
extractor = VerseExtractor(file_path="path/to/local/file.txt")

# From text content
text_content = """
# Text

aṣṭāvakragītā

kathaṃ jñānam avāpto 'ti kathaṃ muktir bhaviṣyati 
vairāgyaṃ ca kathaṃ prāptam etad brūhi mama prabho // Avg_1.1
"""
extractor = VerseExtractor(text_content=text_content)

# Extract verses
verses = extractor.extract_verses()

# Extract and save to file
verses = extractor.save_to_json("output.json")
```

## Project Structure

```
└── src/
    ├── __init__.py      # Package initialization
    ├── __main__.py      # Module entry point
    ├── main.py          # Main VerseExtractor class
    ├── utils.py         # Utility functions
    └── config.py        # Configuration settings
```

## How It Works

1. **Text Retrieval**: The text is retrieved from a URL, local file, or provided as a string.
2. **Text Processing**: 
   - The text is split into lines
   - The actual content section is identified (after the header)
   - Lines are processed to extract verses and their indices
3. **Verse Extraction**:
   - Verses are identified by the pattern `// Avg_X.Y` at the end of lines
   - Multi-line verses are grouped together
   - Verses and their indices are collected into a structured format
4. **Output**: The extracted verses are output as JSON

## Edge Cases and Solutions

1. **Multi-line Verses**: 
   - The code handles verses that span multiple lines by tracking the current verse being processed and collecting lines until a new verse is encountered.

2. **Header Content**: 
   - The text file includes a header section that should be skipped. The code identifies the start of the actual content using the "# Text" marker or by finding the first verse if the marker is absent.

3. **Empty Lines**: 
   - Empty lines within and between verses are handled appropriately, with empty lines between verses being ignored and empty lines within verses preserved as part of the verse.

4. **Unicode Characters**: 
   - The text contains Unicode characters (Sanskrit diacritics). The code uses UTF-8 encoding for both reading the text and writing the JSON output to preserve these characters.

5. **Error Handling**:
   - The code includes robust error handling for failed URL fetches, file reading errors, and parsing issues.

