#!/bin/bash

# Change to the script's directory to ensure it runs from the correct location
cd "$(dirname "$0")"

# Script to start, stop, and check the status of the fuel pricer scraper

PIDFILE="scraper.pid"
LOGFILE="scraper.log"
VENV_DIR="venv"

# Function to show usage
usage() {
    echo "Usage: $0 {start|stop|status}"
    exit 1
}

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
    usage
fi

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

case "$1" in
    start)
        if [ -f $PIDFILE ]; then
            echo "Scraper is already running (PID: $(cat $PIDFILE))."
            exit 1
        fi
        echo "Starting scraper..."
        nohup python3 scraper.py > $LOGFILE 2>&1 &
        echo $! > $PIDFILE
        echo "Scraper started with PID $(cat $PIDFILE). Log file: $LOGFILE"
        ;;
    stop)
        if [ ! -f $PIDFILE ]; then
            echo "Scraper is not running."
            exit 1
        fi
        PID=$(cat $PIDFILE)
        echo "Stopping scraper (PID: $PID)..."
        kill $PID
        # Check if the process was killed
        if kill -0 $PID 2>/dev/null; then
            echo "Failed to stop scraper. Trying with kill -9."
            kill -9 $PID
        fi
        rm $PIDFILE
        echo "Scraper stopped."
        ;;
    status)
        if [ ! -f $PIDFILE ]; then
            echo "Scraper is not running."
            exit 1
        fi
        PID=$(cat $PIDFILE)
        if ps -p $PID > /dev/null; then
            echo "Scraper is running (PID: $PID)."
        else
            echo "Scraper is not running, but PID file exists."
            rm $PIDFILE
        fi
        ;;
    *)
        usage
        ;;
esac

exit 0
