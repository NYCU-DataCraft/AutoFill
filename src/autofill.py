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

def random_sleep(is_on=True):
    if is_on:
        t = random.random() * 2
        time.sleep(t)
    return

def random_fast_sleep(is_on=True):
    if is_on:
        t = random.random() * 0.67
        time.sleep(t)
    return

def main(account, password, mimic, custom_answers=None):
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
        random_fast_sleep()

        driver.get('https://portal.nycu.edu.tw/#/redirect/cos')
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"idfrmSetPreceptor\"]/table/tbody/tr[5]/td/input")))
        random_fast_sleep()
        button.click()
        # logging.info("Redirected to course system")
        
        random_fast_sleep()
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

            first_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="1"]') # 8個 非常不滿意 + 下五第一
            second_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="2"]') # 8個 滿意 + 下午第二
            third_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="3"]')
            fourth_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="4"]')
            fifth_elements = driver.find_elements(By.XPATH, '//input[@type="RADIO" and @value="5"]') # 3個 非常滿意

            default_elements = fifth_elements + first_elements[3:5] + [second_elements[5]] + [first_elements[6]] + [second_elements[7]]
            # logging.info(medium_elements) 
            
            if not custom_answers:
                if len(fifth_elements) <= 8:
                    for element in default_elements:
                        element.click()
                        random_fast_sleep(mimic)
                else:
                    for element in fifth_elements:
                        element.click()
                        random_fast_sleep(mimic)
                    for element in first_elements[-5:-3]+[second_elements[-3]]+[first_elements[-2]]+[second_elements[-1]]:
                        element.click()
                        random_fast_sleep(mimic)
            else:
                custom_elements = []
                query_table = {
                    "five_elements": {5:fifth_elements, 4:fourth_elements[:-2], 3:third_elements[:-5], 2:second_elements[:-5], 1:first_elements[:-5]}, # 5：非常滿意
                    "focus_level": {1:first_elements[-5], 2:second_elements[-5], 3:third_elements[-5]}, # 1：認真
                    "attendance": {1:first_elements[-4], 2:second_elements[-4], 3:third_elements[-4], 4:fourth_elements[-2]},
                    "study_span": {1:first_elements[-3], 2:second_elements[-3], 3:third_elements[-3]},
                    "expectation": {1:first_elements[-2], 2:second_elements[-2], 3:third_elements[-2]},
                    "difficulty": {1:first_elements[-1], 2:second_elements[-1], 3:third_elements[-1], 4:fourth_elements[-1]},
                }

                custom_elements += query_table["five_elements"][custom_answers[0]]
                custom_elements += [query_table["focus_level"][custom_answers[1]]]
                custom_elements += [query_table["attendance"][custom_answers[2]]]
                custom_elements += [query_table["study_span"][custom_answers[3]]]
                custom_elements += [query_table["expectation"][custom_answers[4]]]
                custom_elements += [query_table["difficulty"][custom_answers[5]]]

                for element in custom_elements:
                    element.click()
                    random_fast_sleep(mimic)

            random_sleep()
            # Find and click the button with type="button", value="送出", and onclick="chkdata();"
            button_xpath = '//input[@type="button" and @value="送出" and @onclick="chkdata();"]'
            try:
                submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                submit_button.click()
                random_fast_sleep()
            except:
                pass

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
