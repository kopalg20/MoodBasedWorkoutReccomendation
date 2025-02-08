from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Test function for the suggestion page
def test_suggestions_page():
    try:
        # Navigate to the form page
        driver.get("http://127.0.0.1:5000/")  # Replace with your local URL

        # Fill the form with test data
        driver.find_element(By.NAME, "age").send_keys("25")
        driver.find_element(By.NAME, "gender").send_keys("female")
        driver.find_element(By.NAME, "fitness").send_keys("beginner")
        driver.find_element(By.NAME, "mood").send_keys("happy")
        driver.find_element(By.NAME, "motivation").send_keys("high")
        driver.find_element(By.NAME, "connectedness").send_keys("moderate")
        driver.find_element(By.NAME, "energy").send_keys("medium")
        driver.find_element(By.NAME, "sleep").send_keys("good")
        driver.find_element(By.NAME, "interest").send_keys("fitness")
        driver.find_element(By.NAME, "time").send_keys("morning")

        # Submit the form
        driver.find_element(By.TAG_NAME, "button").click()

        # Wait for the page to load
        time.sleep(3)

        # Verify the suggestions page loaded
        page_source = driver.page_source

        # Check if the suggestions are present in the page source
        if "Suggested Workout" in page_source and "Suggested Meditation" in page_source and "Suggested Yoga" in page_source:
            print("Test passed: Suggestions are displayed.")
        else:
            print("Test failed: Suggestions are not displayed correctly.")

    finally:
        # Close the browser
        driver.quit()

# Run the test
test_suggestions_page()


