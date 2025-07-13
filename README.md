
# Taiwan Stock Analysis Script

This script collects and processes Taiwan stock data using Python. It includes functions to fetch online CSVs, clean and convert them into DataFrames, and generate summary reports.

## Features

- Fetch stock data from online sources
- Parse CSV and HTML formats
- Convert data into pandas DataFrames
- Perform simple cleaning and transformation
- Display output and save to file

## Structure Overview

```python
import time
from datetime import datetime
import urllib.request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
```

## Key Functions

### `transform_date(date)`

A utility function to transform date formats.

## Usage

1. Run the script in a Python environment.
2. Ensure you have an internet connection for data fetching.
3. Output will be shown in the terminal or saved as CSV/DataFrame.

## Notes

- This is an educational script and may require modification for production use.
- Ensure all libraries are installed: `pandas`, `requests`, `bs4`.

## Author

Created by Jason Chen. Updated on July 2025.
