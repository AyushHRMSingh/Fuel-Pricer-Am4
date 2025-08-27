from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def scrape_fuel_prices():
    """
    Scrapes fuel prices from the specified URL.
    """
    url = "https://am4-helper.web.app/tabs/prices"
    
    # Set up headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Wait for the "current-hour" element to be present and contain text
        wait = WebDriverWait(driver, 20)
        current_hour_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "current-hour")))
        
        # Also wait for the text to be present in the element
        wait.until(lambda driver: current_hour_element.text.strip() != "")
        
        # Find the three text elements within the "current-hour" element
        # Assuming the three text elements are siblings or descendants
        # and we can find them by a common tag or class.
        # This part might need adjustment based on the actual HTML structure.
        
        # The data is directly within the element, separated by newlines.
        data = current_hour_element.text.split('\n')
        
        if len(data) >= 3:
            # Extract and print the text from the first three lines
            print(f"Time: {data[0]}")
            print(f"Fuel Price: {data[1]}")
            print(f"CO2 Price: {data[2]}")
            
            fuel_status = False
            co2_status = False

            if int(data[1]) < 400:
                fuel_status = True
            if int(data[2]) < 120:
                co2_status = True

            if fuel_status or co2_status:
                # Send a notification via webhook
                webhook_url = "YOUR_WEBHOOK_URL"
                message = ""
                if fuel_status:
                    message += f"Fuel price is low: {data[1]}\n"
                if co2_status:
                    message += f"CO2 price is low: {data[2]}\n" 
                payload = {"text": message}
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 200:
                    print("Notification sent successfully.")
        else:
            print("Could not find the three data elements.")
            # For debugging, print the whole current-hour element's text
            print("Content of current-hour element:")
            print(current_hour_element.text)

    finally:
        driver.quit()

# if __name__ == "__main__":
#     scrape_fuel_prices()


# have it run at the start of every half hour
import schedule
import time
schedule.every().hour.at(":03").do(scrape_fuel_prices)
schedule.every().hour.at(":33").do(scrape_fuel_prices)
while True:
    schedule.run_pending()
    time.sleep(1)
