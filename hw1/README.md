# CSCI 767 Assignment 1

Scraping NBA player statistics from [Basketball Reference](https://www.basketball-reference.com/) and [ESPN](https://www.espn.com/) for the 2023-34, 2024-25, and 2025-26 NBA seasons.

## Files

- `getHtml.py`: Script used to pull HTML information from the sites
    - ESPN could be done using a simple `requests.get`
    - Basketball Reference required JavaScript so needed to use a headless browser using `selenium`
- `convertToCsv.py`: Converts HTML files into CSV files for each site using `pandas`
- `reference.<year>.out.html`: HTML data for each year scraped from Basketball Reference
- `tableA.csv`: Compiled data scraped from Basketball Reference
- `espn.<year>.out.html`: HTML data for each year scraped from ESPN
- `tableB.csv`: Compiled data scraped from ESPN