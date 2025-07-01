# tr-address-fetcher

A simple Python script to fetch and normalize Turkish address data (provinces, districts, neighborhoods, subdistricts, postcodes) from the official PTT website.

## Features

- Scrapes all Turkish provinces, districts, neighborhoods, and postcodes from https://postakodu.ptt.gov.tr/
- Outputs a normalized JSON file compatible with the [madkhix/tr-address](https://github.com/madkhix/tr-address) Laravel package
- Handles subdistrict (semt) parsing automatically

## Requirements

- Python 3.7+
- `requests` and `beautifulsoup4` libraries

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python fetch_tr_address_data.py
```

- This will generate a `tr-address-data.json` file in the current directory.

## Integration with Laravel Package

1. Copy the generated `tr-address-data.json` file to your Laravel project root (where `artisan` is located).
2. In your Laravel project, import the data:
   ```bash
   php artisan traddress:import tr-address-data.json
   ```

## License

MIT
