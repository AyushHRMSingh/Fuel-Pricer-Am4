# Airline Manager 4 Fuel Pricer

A Python-based fuel price monitoring tool for Airline Manager 4 (AM4) that automatically scrapes fuel and CO2 prices and sends Discord notifications when prices drop below configured thresholds.

## Features

- **Automated Price Monitoring**: Scrapes fuel and CO2 prices from AM4 Helper every 30 minutes
- **Discord Notifications**: Sends alerts when prices fall below your thresholds
- **Configurable Thresholds**: Set custom price alerts via environment variables
- **Headless Operation**: Runs in the background without GUI
- **Process Management**: Start, stop, and check status via shell scripts

## Setup

1. **Clone and navigate to the project**:
   ```bash
   git clone https://github.com/AyushHRMSingh/Fuel-Pricer-Am4.git
   cd fuel-pricer
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Discord webhook URL and desired thresholds
   ```

4. **Update your `.env` file**:
   ```env
   DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
   FUEL_PRICE_THRESHOLD=400
   CO2_PRICE_THRESHOLD=120
   ```

## Usage

**Start the fuel pricer**:
```bash
./run.sh start
```

**Check status**:
```bash
./run.sh status
```

**Stop the fuel pricer**:
```bash
./run.sh stop
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_WEBHOOK_URL` | Discord webhook for notifications | Required |
| `FUEL_PRICE_THRESHOLD` | Alert when fuel price drops below this value | 400 |
| `CO2_PRICE_THRESHOLD` | Alert when CO2 price drops below this value | 120 |

## How It Works

1. The scraper runs every 30 minutes (at :03 and :33 of each hour)
2. It fetches current fuel and CO2 prices from AM4 Helper
3. If prices fall below your configured thresholds, it sends a Discord notification
4. All activity is logged to `scraper.log`

## Requirements

- Python 3.7+
- Chrome/Chromium browser
- Internet connection
- Discord webhook URL

## Dependencies

See `requirements.txt` for the complete list of Python dependencies.

## Troubleshooting

- **Chrome driver issues**: The script automatically manages ChromeDriver via `webdriver-manager`
- **Permission errors**: Ensure `run.sh` and `setup.sh` are executable (`chmod +x *.sh`)
- **Missing prices**: Check `scraper.log` for detailed error messages
- **Discord notifications not working**: Verify your webhook URL in `.env`

## License

This project is for personal use with Airline Manager 4.
