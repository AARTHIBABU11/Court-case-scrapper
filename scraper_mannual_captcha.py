from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import base64
import time

URL = "https://hcmadras.tn.gov.in/filing_status.php"

def get_captcha_image(driver):
    wait = WebDriverWait(driver, 10)
    captcha_img = wait.until(EC.presence_of_element_located((By.ID, "status_captcha_img")))
    captcha_png = captcha_img.screenshot_as_png
    captcha_b64 = base64.b64encode(captcha_png).decode("utf-8")
    return captcha_b64

def scrape_filing_status(section, from_date, captcha_text):
    options = Options()
    # Disable headless during testing to see browser window
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    wait = WebDriverWait(driver, 20)

    # Wait for all fields to load
    wait.until(EC.presence_of_element_located((By.ID, "section")))
    wait.until(EC.presence_of_element_located((By.ID, "from_date")))
    wait.until(EC.presence_of_element_located((By.ID, "status_captcha")))
    wait.until(EC.presence_of_element_located((By.ID, "submit3")))

    # Select the section by value
    section_select = driver.find_element(By.ID, "section")
    for option in section_select.find_elements(By.TAG_NAME, "option"):
        if option.get_attribute("value") == section:
            option.click()
            break

    # Input the date
    from_date_input = driver.find_element(By.ID, "from_date")
    from_date_input.clear()
    from_date_input.send_keys(from_date)

    # Input the captcha text
    captcha_input = driver.find_element(By.ID, "status_captcha")
    captcha_input.clear()
    captcha_input.send_keys(captcha_text)

    # Submit the form
    submit_btn = driver.find_element(By.ID, "submit3")
    submit_btn.click()

    # Wait for either result table or error message
    try:
        # Wait for a div or table that contains results - update selector as per actual page
        wait.until(EC.presence_of_element_located((By.ID, "filingdt_results")))  # <-- example ID; replace if different

        # Grab the results container text
        results_element = driver.find_element(By.ID, "filingdt_results")
        results_text = results_element.text.strip()
        if not results_text:
            results_text = "No results found."
    except:
        # If no results container found, likely invalid captcha or no results
        results_text = "No results found or invalid captcha."

    driver.quit()
    return results_text

if __name__ == "__main__":
    section = "1"  # Judicial Section example
    from_date = "2023-01-01"
    captcha = input("Enter captcha from image: ")
    result = scrape_filing_status(section, from_date, captcha)
    print("Result:\n", result)
