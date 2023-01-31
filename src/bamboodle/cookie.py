import os
import re
import time
import sys
import requests
import pexpect

from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CLIOptions:
    domain = os.getenv('BAMBOOHR_DOMAIN', 'bamboohr.com')

options = CLIOptions()

UNIX_PASSWORD_STORE = "/usr/bin/pass"

def log(str):
    if options.verbose:
        print(str, file=sys.stderr)

def password_store_show(id):
    p = pexpect.spawn(UNIX_PASSWORD_STORE, ["show", id], encoding="utf-8")
    while True:
        match p.expect(['gpg:.*\r\n', 'Error:\s*(.*)\r\n', '(?<!otpauth://)(.*?)\r\n', pexpect.EOF]):
            case 0:
                log(p.after)
            case 1:
                 raise Exception(p.match.group(1))
            case 2:
                 return p.match.group(1)
            case _:
                 raise Exception("Unknown output " + p.before)

def login(driver, id):
    login_url = f"https://{options.domain}"
    log(f"Logging into {login_url}...")
    driver.get(login_url)
    login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "lemail"))
    )

    login.send_keys(id)
    login.send_keys(Keys.RETURN)
    log("Entered username")
    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    password.send_keys(password_store_show(f"{id}/{options.domain}"))
    password.send_keys(Keys.RETURN)
    log("Entered password")

    trust_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Yes, Trust this Browser')]"))
    )
    trust_button.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "MY_INFO"))
    )
    log("Clicked trust button")
    log("DONE")

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")

    return webdriver.Chrome("chromedriver", options=chrome_options)

def cookie_for(id):

    log(f"Hunting for cookies for {id}...")
    with get_driver() as driver:
        login(driver, id)

        cookies = { c['name'] : c['value'] for c in driver.get_cookies() if re.search(re.escape(options.domain), c["domain"])}
        log("Cookie is: \n")
        print(';'.join(f"{k}={v}" for k,v in cookies.items()))

def init_argparse() -> ArgumentParser:
    parser = ArgumentParser(
        prog="bamboodle",
        description="Login to bambooHR and print the auth cookies to stdout"
    )
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"{parser.prog} version 0.0.1")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="log progress to stderr")
    parser.add_argument("-d", "--domain",
                        help="The domain to use for the login, defaults to the value of the BAMBOOHR_DOMAIN environment variable, or bamboohr.com if not set")
    parser.add_argument("username")

    return parser

def main() -> None:
    parser = init_argparse()
    parser.parse_args(namespace=options)
    cookie_for(options.username)

if __name__ == "__main__":
    main()
