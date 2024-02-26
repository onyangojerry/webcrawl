# Python Web Crawler README

## Overview

This Python script is a web crawler designed to start from a specified educational institution's homepage (typically an `.edu` domain) and search through web pages to find and collect valid URLs. It uses a breadth-first or depth-first search approach to explore links, filtering to keep only those that belong to educational institutions. The script is designed to handle errors gracefully and avoid visiting the same URL multiple times.

## Features

- **URL Validation**: Checks if URLs belong to educational institutions by looking for the `.edu` domain.
- **Full URL Checks**: Verifies if a link is a complete URL starting with `http://` or `https://`.
- **Link Collection**: Retrieves all valid links from a given webpage.
- **Customizable Search Depth**: Allows specification of the maximum number of links to collect.
- **Error Handling**: Gracefully handles and ignores inaccessible URLs.

## Requirements

- Python 3.x
- An internet connection

## Setup

No additional Python packages are required beyond the standard library. Simply download the script to your local machine.

## Usage

Before running the script, ensure you have the necessary permissions and understand the ethical considerations of web crawling.

1. **Input the Institution Name**: When prompted, enter the name of the educational institution without the `.edu` part. The script constructs the starting URL based on this input.
   
   Example: If the institution's website is `http://example.edu`, you should input `example`.

2. **Specify Search Parameters**: Choose between a breadth-first search (BFS) or depth-first search (DFS) approach by initializing the `to_visit` variable with either a `Queue()` or `Stack()` class instance, respectively.

3. **Set the Maximum Number of Links**: Determine how many links you wish to collect.

4. **Run the Script**: Execute the script. It will collect links and print them to the console as it crawls.

5. **Output**: The script optionally writes the collected links to a specified output file.

## Example

```python
from stackqueue import Queue  # or Stack for DFS

start_url = "http://example.edu"
to_visit = Queue()  # Use Stack() for DFS
max_links = 100
output_name = "collected_links.txt"

write_institution_urls(start_url, to_visit, max_links, output_name)
```

## Ethical Considerations

- Ensure you have permission to crawl the website.
- Respect `robots.txt` files to avoid crawling disallowed areas.
- Be mindful of the server load; maintain a reasonable request rate.

## Contributing

Contributions to improve the script or extend its capabilities are welcome. Please adhere to standard coding practices and document any changes.

---
