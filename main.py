import time
import json
from datetime import date, datetime, timedelta

import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

__author__ = 'Gautham Kolluru'

START_DATE = date.today()-timedelta(days=1)

URLS = [
    'https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentType',
]

PROXIES = []

# Json File Name
JFN = "navigation.json"


def read_json(fn):
    with open(fn) as fp:
        # file info
        fi = json.load(fp)
    return fi


def read_date_from_string(string_date):
    return datetime.strptime(string_date, "%m-%d-%Y").date()


def get_no_of_days(start_date, end_date):
    return (end_date - start_date).days


def historical_dates(start_date=START_DATE, end_date=date.today()):
    while get_no_of_days(start_date, end_date) > 0:
        if get_no_of_days(start_date, end_date) > 31:
            yield start_date, start_date + timedelta(days=31)
            start_date += timedelta(days=31)
        else:
            yield start_date, end_date
            start_date += timedelta(days=get_no_of_days(start_date, end_date))
    else:
        return False


def get_urls():
    for url in URLS:
        yield url


def get_driver():
    return webdriver.Chrome()


def select_from_dropdown(driver, dropdown_id="", dropdown_name="", option_name=""):
    if dropdown_id:
        dd = driver.find_element_by_id(dropdown_id)
    elif dropdown_name:
        dd = driver.find_element_by_name(dropdown_name)
    else:
        return False
    for option in dd.find_elements_by_tag_name('option'):
        if option.text.strip().upper() == option_name.upper():
            option.click()  # select() in earlier versions of webdriver
            time.sleep(5)
            return True
    return False


def sort_dict_values(d) -> list:
    return [v for k, v in sorted(d.items())]


def is_blocked(url, proxyDict={}):
    return 200 <= requests.get(url=url, proxies=proxyDict) < 300


def main():
    try:
        jd = read_json(JFN)
        if jd:
            urls = jd["urls"]
            proxies = jd["proxies"]
            steps = sort_dict_values(jd["steps"])

            for url in urls:

                # for proxy in proxies:
                #     if not is_blocked(proxy, url):
                #         break
                # else:
                #     raise("All Proxies Blocked!")

                driver = get_driver()
                driver.get(url)

                for step in steps:

                    if step["xpath"]:
                        step_xpath = step["xpath"]
                    elif step["id"]:
                        step_id = step["id"]
                    elif step["name"]:
                        step_name = step["name"]
                    print(step_name or step_xpath or step_id)

    except Exception as e:
        print(e)
    finally:
        driver.close()
    return True


main()
