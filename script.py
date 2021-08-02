from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import os
import logging
import json

# get config values
with open('config.json', 'r') as f:
    config = json.load(f)

logging.basicConfig(level=config['logging']['level'],
                    filename=config['logging']['file_name'], filemode='a',
                    format=config['logging']['message_format'],
                    datefmt=config['logging']['date_strftime_format'])


sleep_time = config['max_sleep_time_in_sec']
retry_count = config['retry_count']


def set_date(date, download_date):
    is_date_present = False
    for x in range(config['no_of_days_of_data_present']):
        date.click()
        for _ in range(x):
            date.send_keys(Keys.DOWN)
            time.sleep(sleep_time)
        date.send_keys(Keys.ENTER)
        time.sleep(sleep_time)
        date.send_keys(Keys.ENTER)
        time.sleep(sleep_time)
        if date.get_attribute('value') == download_date:
            is_date_present = True
            break
    return is_date_present


def download_data(download_date):
    # Creating a directory for saving downloaded files according to their date
    # Parent Directory path
    parent_dir = config['default_download_directory']
    # Path
    path = os.path.join(parent_dir, download_date)
    try:
        if not os.path.exists(os.path.dirname(path)):
            logging.info('Directory ' + path + ' created.')
            os.makedirs(os.path.dirname(path))
    except OSError as err:
        logging.error(err)
        if err.errno != errno.EEXIST:
            raise
        pass

    time.sleep(5)

    # setting default download directory as the above created directory
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': path}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=binary_path, options=options)

    for attempt in range(retry_count):
        try:
            driver.set_page_load_timeout(config['max_timeout_in_sec'])
            driver.get("https://www.sgx.com/research-education/derivatives")
            time.sleep(sleep_time)
        except TimeoutException as ex:
            logging.error('Exception has been thrown for loading the link: ' + str(ex))
            logging.info('Retry count: ' + str(++attempt))
            if attempt < retry_count - 1:
                continue
            else:
                logging.error('All attempts to retry failed for loading the link. Please check the logs for error.')
                raise
        break

    # Getting the type input box element
    for attempt in range(retry_count):
        try:
            type = WebDriverWait(driver, config['max_timeout_in_sec']).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                        "#page-container > template-base > div > div > section.col-xxs-12.col-md-9.template-widgets-section > div > sgx-widgets-wrapper > widget-research-and-reports-download:nth-child(4) > widget-reports-derivatives-tick-and-trade-cancellation > div > sgx-input-select:nth-child(1) > label > span.sgx-input-select-filter-wrapper > input")))
            time.sleep(sleep_time)
        except TimeoutException as ex:
            logging.error('Exception has been thrown for finding the type element: ' + str(ex))
            logging.info('Retry count: ' + str(++attempt))
            if attempt < retry_count - 1:
                continue
            else:
                logging.error(
                    'All attempts to retry failed for finding the type element. Please check the logs for error.')
                raise
        break

    # Getting the date input box element
    for attempt in range(retry_count):
        try:
            date = WebDriverWait(driver, config['max_timeout_in_sec']).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                        "#page-container > template-base > div > div > section.col-xxs-12.col-md-9.template-widgets-section > div > sgx-widgets-wrapper > widget-research-and-reports-download:nth-child(4) > widget-reports-derivatives-tick-and-trade-cancellation > div > sgx-input-select:nth-child(2) > label > span.sgx-input-select-filter-wrapper > input")))
            time.sleep(sleep_time)
        except TimeoutException as ex:
            logging.error('Exception has been thrown for finding the date element: ' + str(ex))
            logging.info('Retry count: ' + str(++attempt))
            if attempt < retry_count - 1:
                continue
            else:
                logging.error(
                    'All attempts to retry failed for finding the date element. Please check the logs for error.')
                raise
        break

    # Getting the download button element
    for attempt in range(retry_count):
        try:
            download_button = WebDriverWait(driver, config['max_timeout_in_sec']).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                                   "#page-container > template-base > div > div > section.col-xxs-12.col-md-9.template-widgets-section > div > sgx-widgets-wrapper > widget-research-and-reports-download:nth-child(4) > widget-reports-derivatives-tick-and-trade-cancellation > div > button")))
            time.sleep(sleep_time)
        except TimeoutException as ex:
            logging.error('Exception has been thrown for finding the download button element: ' + str(ex))
            logging.info('Retry count: ' + ++attempt)
            if attempt < retry_count - 1:
                continue
            else:
                logging.error(
                    'All attempts to retry failed for finding the download button element. Please check the logs for error.')
                raise
        break

    for x in range(config['no_of_file_types']):
        type.click()
        time.sleep(sleep_time)
        # select the file type
        for _ in range(x):
            type.send_keys(Keys.DOWN)
            time.sleep(sleep_time)
        type.send_keys(Keys.ENTER)
        time.sleep(sleep_time)
        type.send_keys(Keys.ENTER)
        if set_date(date, download_date):
            download_button.click()
            time.sleep(sleep_time)
            logging.info(type.get_attribute('value') + ' downloaded for date ' + download_date)
        else:
            print(type.get_attribute('value') + ' cannot be downloaded for date ' + download_date+'. Please try for last 5 days.')
            logging.info(type.get_attribute('value') + ' cannot be downloaded for date ' + download_date)

    driver.close()
