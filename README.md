# LinkedIn Job Scraper

A lightweight web application that scrapes job listings from LinkedIn search results. Built with React, TypeScript, and Playwright.

## Features

- Scrape job listings from LinkedIn job search URLs
- Display results in a clean, sortable table
- View job details and apply directly through LinkedIn
- Modern, responsive UI built with Tailwind CSS

## Prerequisites

- [Bun](https://bun.sh/) (Latest version)
- A modern web browser

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd linkedin-scraper
```

2. Install dependencies:
```bash
bun install
```

3. Install Playwright browsers:
```bash
bunx playwright install chromium
```

## Development

To start the development server:

```bash
bun dev
```

The application will be available at `http://localhost:5173`.

## Usage

1. Navigate to LinkedIn and perform a job search
2. Copy the URL from your browser
3. Paste the URL into the application
4. Click "Scrape Jobs" to fetch the listings

## Project Structure

```
linkedin-scraper/
├── src/
│   ├── components/    # React components
│   ├── services/     # Scraping logic
│   ├── hooks/        # Custom React hooks
│   └── types/        # TypeScript type definitions
├── public/           # Static assets
└── tests/           # Test files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - see LICENSE file for details
# linked-in-html-to-cvs-parser
