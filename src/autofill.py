from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException

import time
import logging
import logging.handlers

import random

def log_setup():
    log_handler = logging.handlers.WatchedFileHandler('app.log')
    formatter = logging.Formatter(
        '%(asctime)s program_name [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

# log_setup()

def random_sleep():
    t = random.random() * 2
    time.sleep(t)
    return

def random_fast_sleep():
    t = random.random() * 0.67
    time.sleep(t)
    return

def main(account, password):
    try:
        # Driver Setup
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=chrome_options)
        # logging.info("Driver setup complete")

        driver.get('https://portal.nycu.edu.tw/#/login?redirect=%2F')

        # Locate the account and password input fields by their IDs and input the values
        account_input = driver.find_element(By.XPATH, "//input[@id='account']")
        password_input = driver.find_element(By.XPATH, "//input[@id='password']")

        account_input.send_keys(account)
        password_input.send_keys(password)

        submit_button = driver.find_element(By.XPATH, "//input[@class='login']")
        submit_button.click()
        # logging.info("Account/Password submitted")
        time.sleep(2)
        
        try:
            alert = driver.find_element(By.CLASS_NAME, "el-message--error")
            driver.quit()
            # logging.info("Login error, please check your accound and password")
            return "Login error, please check your accound and password"
        except NoSuchElementException:
            pass

        try:
            element = driver.find_element(By.XPATH, "//div[@class='el-message-box']")
            # logging.info("Authenticator detected, waiting for 30 seconds")
            time.sleep(30)
        except (NoSuchWindowException, NoSuchElementException):
            pass
        
        # logging.info("Authentication complete")
        random_sleep()

        driver.get('https://portal.nycu.edu.tw/#/redirect/cos')
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"idfrmSetPreceptor\"]/table/tbody/tr[5]/td/input")))
        random_sleep()
        button.click()
        # logging.info("Redirected to course system")
        
        random_sleep()
        driver.get('https://course.nycu.edu.tw/TeachPoll/index.asp')
        # logging.info("Redirected to TeachPoll/index.asp")

        elements_xpath = '//a[contains(@onclick, "SetfrmAction") and contains(text(), "填答問卷")]'
        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, elements_xpath)))
        # logging.info(f"Automation begins, detected elements: {len(elements)}")
        
        # Iterate over the elements and visit them
        for _ in range(len(elements)):
            random_fast_sleep()
            # logging.info("new link started")
            link_xpath = '//a[contains(@onclick, "SetfrmAction") and contains(text(), "填答問卷")]'
            submit_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, elements_xpath)))
            submit_button[0].click()
            extra_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="1"]') # 8個
            radio_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="5"]') # 3個
            addd_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="2"]') # 8個

            medium_elements = radio_elements + extra_elements[3:5] + [addd_elements[5]] + [extra_elements[6]] + [addd_elements[7]]
            # logging.info(medium_elements) 

            if len(radio_elements) <= 8:
                for element in medium_elements:
                    element.click()
                    random_fast_sleep()
            else:
                for element in radio_elements:
                    element.click()
                    random_fast_sleep()
                for element in extra_elements[-5:-3]+[addd_elements[-3]]+[extra_elements[-2]]+[addd_elements[-1]]:
                    element.click()
                    random_fast_sleep()

            random_sleep()
            # Find and click the button with type="button", value="送出", and onclick="chkdata();"
            button_xpath = '//input[@type="button" and @value="送出" and @onclick="chkdata();"]'
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            submit_button.click()
            random_fast_sleep()

            try:
                link_xpath = "//a[@href='index.asp']"
                link_path = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
                link_path.click()
            except:
                # logging.info("Couldn't find back link")
                driver.get('https://course.nycu.edu.tw/TeachPoll/index.asp')
                # logging.info("Link complete, redirecting to TeachPoll/index.asp")

        # Close the browser window
        driver.quit()
        # logging.info("Automation complete, quit driver")
        return "Automation complete, you can close the app now"

    except TimeoutException as e:
        # logging.warning(f"Connection time out: {str(e)}")
        return "Connection time out"
    
    except NoSuchElementException as e:
        # logging.warning(f"Element not found: {str(e)}")
        return "Element not found"
    
    except NoSuchWindowException as e:
        # logging.warning(f"No such window: target window already closed")
        return "No such window"
