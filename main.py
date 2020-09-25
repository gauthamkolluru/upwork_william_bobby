import time
import json
from datetime import date, datetime, timedelta

import random

# import requests
# import urllib
import useragents
import proxies

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys


__author__ = 'Gautham Kolluru'

START_DATE = date.today()-timedelta(days=1)


# Json File Name
JFN = "navigation.json"
# JFN = "navigation1.json"


def read_json(fn):
    with open(fn) as fp:
        # file info
        fi = json.load(fp)
    return fi


def read_date_from_string(string_date):
    return datetime.strptime(string_date, "%m-%d-%Y").date()


def get_no_of_days(start_date, end_date):
    return (end_date - start_date).days


def get_dates(start_date=START_DATE, end_date=date.today()):
    while get_no_of_days(start_date, end_date) > 31:
        yield start_date, start_date + timedelta(days=31)
        start_date += timedelta(days=31)
    yield start_date, end_date


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


def finding_element(driver, name):
    return driver.find_element_by_name(name)


def select_value(el, value):
    for option in el.find_elements_by_tag_name('option'):
        if option.text.strip().lower() == value.lower():
            option.click()  # select() in earlier versions of webdriver
            time.sleep(5)
            return True
    return False


def write_value(el, value):
    el.clear()
    el.send_keys(value)
    return True


def click_button(el):
    return el.click()


def get_element(driver, name="", element_id="", tag_name="", type_name="", class_name="", xpath="", multiple=False):
    if multiple:
        if name:
            return driver.find_elements_by_name(name)
        elif class_name:
            return driver.find_elements_by_class_name(class_name)
        elif element_id:
            return driver.find_elements_by_id(element_id)
        elif tag_name:
            return driver.find_elements_by_tag_name(tag_name)
        elif xpath:
            return driver.find_elements_by_xpath(xpath)

    else:
        if name:
            return driver.find_element_by_name(name)
        elif class_name:
            return driver.find_element_by_class_name(class_name)
        elif element_id:
            return driver.find_element_by_id(element_id)
        elif tag_name:
            return driver.find_element_by_tag_name(tag_name)
        elif xpath:
            return driver.find_element_by_xpath(xpath)
    return False


def set_value(driver, name="", element_id="", tag_name="", type_name="", class_name="", xpath="", value="", multiple=False, additional_specifier=""):
    el = get_element(driver,
                     name=name,
                     element_id=element_id,
                     tag_name=tag_name,
                     type_name=type_name,
                     class_name=class_name,
                     xpath=xpath,
                     multiple=multiple,
                     )

    print(el.tag_name)
    print(el.text)

    if "select" in el.tag_name.lower():
        return select_value(el, value)

    elif "input" in el.tag_name.lower():
        for start_date, end_date in get_dates():
            break
        print(start_date, end_date)
        if additional_specifier:
            if additional_specifier == "from day":
                value = start_date.day
            elif additional_specifier == "from month":
                value = start_date.month
            elif additional_specifier == "from year":
                value = start_date.year
            elif additional_specifier == "to day":
                value = end_date.day
            elif additional_specifier == "to month":
                value = end_date.month
            elif additional_specifier == "to year":
                value = end_date.year
        return write_value(el, value)

    elif "button" in el.tag_name.lower():
        return click_button(el)

    time.sleep(5)

    return True


def sort_dict_values(d) -> list:
    return [v for k, v in sorted(d.items())]


def get_proxy_capabilities(proxy):
    p = Proxy()
    p.proxy_type = ProxyType.MANUAL
    p.http_proxy = proxy
    capabilities = webdriver.DesiredCapabilities.CHROME
    return p.add_to_capabilities(capabilities)


def get_driver(capabilities=None):
    return webdriver.Chrome(desired_capabilities=capabilities)


def main():
    try:
        jd = read_json(JFN)
        if jd:
            url = jd["url"]
            steps = sort_dict_values(jd["steps"])

            access_to_site = False

            i = 0

            while not access_to_site:
                proxy = proxies.getProxy()
                opts = Options()
                opts.add_argument(
                    "user-agent=[{}]".format(useragents.getUserAgent()))
                driver = webdriver.Chrome(
                    desired_capabilities=get_proxy_capabilities(proxy), options=opts)
                driver.get(url)
                if 'notice' not in driver.title.strip().lower():
                    access_to_site = True
                else:
                    print("i = ", i)
                    driver.close()
                if i > 99:
                    break
                i += 1

            print("access to site", access_to_site)
            print("proxy : ", proxy)

            exit(0)

            # driver = get_driver()
            driver.get(url)

            print(driver.title)

            for step in steps:

                set_value(
                    driver=driver,
                    name=step["name"],
                    element_id=step["element_id"],
                    tag_name=step["tag_name"],
                    type_name=step["type_name"],
                    class_name=step["class_name"],
                    xpath=step["xpath"],
                    value=step["value"],
                    multiple=step["multiple"]
                )

    except Exception as e:
        print(e, e.with_traceback())
    finally:
        driver.close()
    return True


main()

# def is_blocked(url, proxyDict={}):
#     print("checking proxy in 'is_blocked' ", proxyDict)
#     print(url, proxyDict, 200 <= requests.get(
#         url=url, proxies=proxyDict).status_code < 300)
#     return 200 <= requests.get(url=url, proxies=proxyDict).status_code < 300
