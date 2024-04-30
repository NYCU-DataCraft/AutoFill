from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=chrome_options)
time.sleep(40)

# Get the initial window handle
initial_window_handle = driver.current_window_handle

# Switch to the new tab
for window_handle in driver.window_handles:
    if window_handle != initial_window_handle:
        driver.switch_to.window(window_handle)
        break
# Find and click every <a> element with text "填答問卷"
# Wait for all elements with the specified attributes to be present on the new tab

driver.get('https://course.nycu.edu.tw/TeachPoll/index.asp')

elements_xpath = '//a[contains(@onclick, "SetfrmAction") and contains(text(), "填答問卷")]'
elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, elements_xpath)))

# Iterate over the elements and visit them
for _ in range(len(elements)):
    link_xpath = '//a[contains(@onclick, "SetfrmAction") and contains(text(), "填答問卷")]'
    submit_button = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, elements_xpath)))
    submit_button[0].click()
    extra_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="1"]')
    radio_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="5"]')
    for extra_element in extra_elements:
        extra_element.click()
    for radio_element in radio_elements:
        radio_element.click()
    time.sleep(1)
    # Find and click the button with type="button", value="送出", and onclick="chkdata();"
    # Locate the button by its attributes
    button_xpath = '//input[@type="button" and @value="送出" and @onclick="chkdata();"]'
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    submit_button.click()
    print("submitted")
    # Wait for a while to ensure the page loads after submitting the form (you may need to adjust the time)
    time.sleep(1)

    # Find and click the link with href="index.asp"
    driver.get('https://course.nycu.edu.tw/TeachPoll/index.asp')


# Close the browser window
driver.quit()
