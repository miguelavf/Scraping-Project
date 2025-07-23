# Web Scraping Project

This project is a web scraper designed to extract contact information from the AVF-WFV website. It retrieves email addresses for team coaches and other staff members and saves them to a JSON file.

## Features

- Scrapes multiple team pages to gather contact information.
- Extracts email addresses that are protected by image-based obfuscation.
- Rotates user-agents to minimize the risk of being blocked.
- Saves the extracted data in a structured JSON format.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the scraper and generate the `data.json` file, execute the following command:

```bash
python app.py
```

The script will print its progress to the console and create a `data.json` file in the project's root directory with the scraped data.
