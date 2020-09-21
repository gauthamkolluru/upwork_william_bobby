import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

__author__ = 'Gautham Kolluru'

URLS = [
    'https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentType',
]

PROXIES = []

# Json File Name
JFN = "navigation.json"


def read_json(fn=JFN):
    with open(fn) as fp:
        # file info
        fi = json.load(fp)
    return fi


def get_urls():
    for url in URLS:
        yield url


def get_driver():
    return webdriver.Chrome()


def dropdown_select(driver, dropdown_id="", dropdown_name="", option_name=""):
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


def sort_dict(d):
    return {k: v for k, v in sorted(d['steps'].items())}


def main():
    for url in get_urls():
        try:
            driver = get_driver()
            driver.get(url)
            # ji : json input
            ji = sort_dict(read_json()['steps'])
            for step in ji:
                dropdown_id = ""
                dropdown_name = ""
                option_name = ""
                if ji[step]['element'].lower().strip() == "dropdown":
                    if "id" in ji[step]:
                        dropdown_id = ji[step]['id']
                    elif "name" in ji[step]:
                        dropdown_name = ji[step]['name']
                    if "option" in ji[step]:
                        option_name = ji[step]['option']
                    dropdown_select(driver=driver, dropdown_id=dropdown_id,
                                    dropdown_name=dropdown_name, option_name=option_name)
        except Exception as e:
            print(e)
        finally:
            driver.close()
    return True


main()
