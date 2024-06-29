import pytest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load test data from files
with open('tests/test_data/valid_data.json') as f:
    valid_data = json.load(f)
with open('tests/test_data/invalid_data.json') as f:
    invalid_data = json.load(f)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Initialize the WebDriver (use the path to your chromedriver if necessary)
    driver.get("https://www.edge196.com/contact")  # Navigate to the Contact Us page
    yield driver
    driver.quit()  # Quit the WebDriver after tests

def test_valid_form_submission(driver):
    for data in valid_data:
        fill_form(driver, data)
        submit_form(driver)
        wait = WebDriverWait(driver, 10)
        success_message = wait.until(EC.presence_of_element_located((By.ID, "success-message")))
        assert success_message.is_displayed()
        driver.refresh()

def test_invalid_form_submission(driver):
    for data in invalid_data:
        fill_form(driver, data)
        submit_form(driver)

        wait = WebDriverWait(driver, 10)
        error_message = wait.until(EC.presence_of_element_located((By.ID, "error-message")))
        assert error_message.is_displayed()
        driver.refresh()

def fill_form(driver, data):
    driver.find_element(By.NAME, "name").send_keys(data["name"])
    driver.find_element(By.NAME, "email").send_keys(data["email"])
    driver.find_element(By.NAME, "message").send_keys(data["message"])

def submit_form(driver):
    driver.find_element(By.NAME, "submit").send_keys(Keys.RETURN)
