import os
import json
import time
import random
from datetime import date, datetime, timedelta

import useragents
import proxies

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys


__author__ = 'Gautham Kolluru'

JFN = "navigation_burlington.json"

FIND_ELEMENTS_BY = ["id", "tag_name", "xpath"]


def read_json(fn):
    with open(fn) as fp:
        # file info
        fi = json.load(fp)
    return fi


def get_random(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)


def get_to_date(string_date):
    return datetime.strptime(string_date, "%m-%d-%Y").date() if string_date else date.today()


def get_from_date(to_date):
    return to_date - timedelta(days=1)


def get_element(driver, by='', value=''):
    by = by.strip().lower()
    if by == "id":
        return driver.find_element_by_id(value)
    elif by == "name":
        return driver.find_element_by_name(value)
    elif by == "class_name":
        return driver.find_element_by_class_name(value)
    elif by == "tag_name":
        return driver.find_element_by_tag_name(value)


def get_elements(driver, by='', value=''):
    by = by.strip().lower()
    if by == "id":
        return driver.find_elements_by_id(value)
    elif by == "name":
        return driver.find_elements_by_name(value)
    elif by == "class_name":
        return driver.find_elements_by_class_name(value)
    elif by == "tag_name":
        return driver.find_elements_by_tag_name(value)


def switch_context(driver, element='', parent=False):
    if element:
        return driver.switch_to.frame(element)
    elif parent:
        return driver.switch_to.parent_frame()
    return driver.switch_to.default_content()


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
    jd = read_json(JFN)
    url = jd["url"]
    steps = jd["steps"]

    access_to_site = False

    while not access_to_site:

        proxy = proxies.getProxy()
        opts = Options()
        opts.add_argument(
            "user-agent=[{}]".format(useragents.getUserAgent()))
        driver = webdriver.Chrome(
            desired_capabilities=get_proxy_capabilities(proxy), options=opts)

        driver.get(url)

        for step in steps:
            for k in step.keys():
                for f in FIND_ELEMENTS_BY:
                    if k == f:
                        if "multiple" in step.keys():
                            if step["multiple"]:
                                element_collection = get_elements(
                                    driver=driver, by=k, value=step[k])
                                break
                        else:
                            element = get_element(
                                driver=driver, by=k, value=step[k])
                            break
            if element_collection:
                pass
            elif element:
                pass
    return True


main()
