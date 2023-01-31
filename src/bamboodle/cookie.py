import os
import re
import time
import sys
import requests
import pexpect

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


login_url = f"https://{os.getenv('BAMBOOHR_DOMAIN', 'bamboohr.com')}"

UNIX_PASSWORD_STORE = "/usr/bin/pass"


def password_store_show(id):
    p = pexpect.spawn(UNIX_PASSWORD_STORE, ["show", id], encoding="utf-8")
    while True:
        match p.expect(['gpg:.*\r\n', 'Error:\s*(.*)\r\n', '(?<!otpauth://)(.*?)\r\n', pexpect.EOF]):
            case 0:
                print(p.after, file=sys.stderr)
            case 1:
                 raise Exception(p.match.group(1))
            case 2:
                 return p.match.group(1)
            case _:
                 raise Exception("Unknown output " + p.before)

def login(driver, id):
    print(f"Logging into {login_url}...", file=sys.stderr)
    driver.get(login_url)
    login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "lemail"))
    )

    login.send_keys(id)
    login.send_keys(Keys.RETURN)
    print("Entered username", file=sys.stderr)
    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    password.send_keys(password_store_show(id+"/juxtpro.bamboohr.com"))
    password.send_keys(Keys.RETURN)
    print("Entered password", file=sys.stderr)
    trust_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Yes, Trust this Browser')]"))
    )
    trust_button.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "MY_INFO"))
    )
    print("Clicked trust button", file=sys.stderr)
    print("DONE", file=sys.stderr)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")

    return webdriver.Chrome("chromedriver", options=chrome_options)

def cookie_for(id):

    print(f"Hunting for cookies for {id}...", file=sys.stderr)
    with get_driver() as driver:
        login(driver, id)

        cookies = { c['name'] : c['value'] for c in driver.get_cookies() if re.search(r"juxtpro.bamboohr\.com", c["domain"])}
        print(';'.join(f"{k}={v}" for k,v in cookies.items()))

def main():
    if (len(sys.argv) == 2):
        cookie_for(sys.argv[1])
    else:
        print("Usage: bamboodle <username>", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
