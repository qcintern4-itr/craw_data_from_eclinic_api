import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import config

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def get_token_and_cookies():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-logging")

    seleniumwire_options = {
        'verify_ssl': False
    }

    service = Service(log_path="NUL")  # "/dev/null" on Linux/Mac
    driver = webdriver.Chrome(service=service, options=chrome_options, seleniumwire_options=seleniumwire_options)

    try:
        driver.get("https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/login/newLogin.jsp")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "doctorID"))).send_keys(config.USERNAME)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nextStep"))).click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "passwordField"))).send_keys(config.PASSWORD)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Login"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "agreeBtn"))).click()
        print("Login successfully")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='providerLicense']//div[@class='modal-dialog']")))


        # get cookies
        cookies_list = driver.get_cookies()
        cookies = {
            cookie['name']: cookie['value']
            for cookie in cookies_list
            if cookie['name'] in ['JSESSIONID', 'ApplicationGatewayAffinityCORS', 'ApplicationGatewayAffinity',
                                  'SL_G_WPT_TO', 'SL_GWPT_Show_Hide_tmp', 'SL_wptGlobTipTmp']
        }

        # get token
        token = None
        for request in reversed(driver.requests):
            # check token with different name of token
            for header_name in ['x-csrf-token', 'X-CSRF-Token', 'X-Csrf-Token']:
                if header_name in request.headers and not token:
                    token = request.headers[header_name]
                    break
            if token:
                break

        # # if not found, check in response header
        # if not token:
        #     for request in reversed(driver.requests):
        #         if request.response:
        #             for header_name in ['x-csrf-token', 'X-CSRF-Token', 'X-Csrf-Token']:
        #                 if header_name in request.response.headers:
        #                     token = request.response.headers[header_name]
        #                     print(f"Token found from response header '{header_name}':", token)
        #                     # print(f"From URL: {request.url}")
        #                     break
        #             if token:
        #                 break

        # not found token
        if not token:
            print("Warning: No CSRF token found in any request!")

        return {
            "token": token,
            "cookies": cookies
        }

    finally:
        driver.quit()
