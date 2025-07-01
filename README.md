# Turkish Address and Postal Code Scraper

This project scrapes Turkish address data (City > District > Quarter > Neighborhood > Postal Code) from postakodu.web.tr and outputs the results as a structured JSON file.

## Features

- Robust scraping with retry and error logging for all HTTP requests (city, district, quarter, neighborhood, and postal code levels).
- Each scraping function will retry up to 3 times in case of connection errors or timeouts.
- If all retries fail, the problematic URL and error message are logged to a dedicated log file for each level:
  - `failed_city_links.txt`
  - `failed_district_links.txt`
  - `failed_quarters.txt`
  - `failed_neighborhoods.txt`
  - `failed_postcodes.txt`
- Output is a hierarchical JSON file: `tr-address-data.json`.

## Requirements

- Python 3.7+
- `requests` and `beautifulsoup4` libraries

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Run the script:
   ```bash
   python fetch_tr_address_data.py
   ```
3. The results will be saved to `tr-address-data.json`.
4. If any addresses or postal codes could not be fetched, check the corresponding log files for details.

## Error Handling

- The script automatically retries failed requests up to 3 times.
- If a request fails after all retries, the URL and error are logged in the appropriate log file.
- You can review these log files and re-run the script or manually check the problematic URLs if needed.

## Output

- The output file `tr-address-data.json` contains the full address hierarchy:
  ```json
  [
    {
      "name": "Istanbul",
      "districts": [
        {
          "name": "Kadikoy",
          "quarters": [
            {
              "name": "Fenerbahce",
              "neighborhoods": [
                {
                  "name": "Fenerbahce Mahallesi",
                  "postcode": "34726"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
  ```

## Notes

- Please use responsibly and avoid overloading the source website.
- If you encounter many errors, consider increasing the delay between requests or using a different network connection.

## Integration with Laravel Package

1. Copy the generated `tr-address-data.json` file to your Laravel project root (where `artisan` is located).
2. In your Laravel project, import the data:
   ```bash
   php artisan traddress:import tr-address-data.json
   ```

## License

MIT
