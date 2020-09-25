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

FILE_NAME_FORMAT = "Burlington_${0}_${1}.pdf"

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


def get_date_string(d):
    return d.strftime("%m/%d/%Y")


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


def element_click(element):
    return element.click()


def random_sleep(min_time=5, max_time=20):
    return time.sleep(random.randint(min_time, max_time))


def select_item_from_dropdown(element, option_name=""):
    for option in element.find_elements_by_tag_name('option'):
        if option.text.strip().upper() == option_name.upper():
            return element_click(option)
    return False


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

    string_date = input("Enter Date in the format : MM-DD-YYYY")
    to_date = get_to_date(string_date)
    from_date = get_from_date(to_date)

    access_to_site = False

    while not access_to_site:

        try:
            proxy = proxies.getProxy()
            opts = Options()
            opts.add_argument(
                "user-agent=[{}]".format(useragents.getUserAgent()))
            driver = webdriver.Chrome(
                desired_capabilities=get_proxy_capabilities(proxy), options=opts)

            driver.get(url)

            random_sleep()

            anchors = driver.find_elements_by_tag_name("a")

            for anchor in anchors:
                if anchor.get_attribute("title").lower() == "by document type".lower():
                    anchor.click()
                    break

            dropdown_element = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_ddlDocTypeTab2")

            select_item_from_dropdown(dropdown_element, option_name="DEED")

            # for option in dropdown_element.find_elements_by_tag_name("option"):
            #     if option.text.strip().lower() == "DEED".lower():
            #         option.click()

            from_date_element = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_txtFromTab2")

            to_date_element = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_txtToTab2")

            from_date_element.send_keys(get_date_string(from_date))

            to_date_element.send_keys(get_date_string(to_date))

            dropdown_element = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_ddlTotalRecTab2")

            select_item_from_dropdown(dropdown_element, option_name="2000")

            search_button_element = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_btnSearchTab2")

            element_click(search_button_element)

            random_sleep()

            view_button = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_dgdDeedMort_ctl03_btnView")

            element_click(view_button)

            random_sleep()

            outer_frame_element = driver.find_element(
                by="id", value="ctl00_ContentPlaceHolder1_ifrmElection")

            driver.switch_to.frame(outer_frame_element)

            random_sleep()

            while True:

                inner_frame_element_1 = driver.find_element_by_id(
                    "InstViewerHeadFrame")

                driver.switch_to.frame(inner_frame_element_1)

                inner_form_element = driver.find_element_by_id(
                    "frmNavigate")

                random_sleep()

                inner_table_element = driver.find_element_by_id("dgdDoc")

                for tr in inner_table_element.find_elements_by_tag_name("tr"):
                    td = tr.find_elements_by_tag_name("td")
                    if td[0].text.lower() == "type":
                        type_name = td[1].text.lower()
                    if td[0].text.lower() == "inst. number":
                        inst_number = td[1].text.lower()

                for each_file in os.listdir(os.path.join(os.path.expanduser("~"), "Downloads")):
                    if inst_number in each_file:
                        next_button = driver.find_element_by_id("btnNext")
                        element_click(next_button)
                        break

                display_image_button = driver.find_element_by_id(
                    "btnImage")

                element_click(display_image_button)

                driver.switch_to.parent_frame()

                inner_frame_element_2 = driver.find_element_by_id(
                    "InstViewerBodyFrame")

                driver.switch_to.frame(inner_frame_element_2)

                pdf_download_button_element = driver.find_element_by_id(
                    "Button_SaveImage")

                element_click(pdf_download_button_element)

                current_file_name = FILE_NAME_FORMAT.format(
                    type_name, inst_number)

                for each_file in os.listdir(os.path.join(os.path.expanduser("~"), "Downloads")):
                    if "oprs" in each_file.lower():
                        os.renames(os.path.join(os.path.join(os.path.expanduser("~"), "Downloads"), each_file), os.path.join(
                            os.path.join(os.path.expanduser("~"), "Downloads"), current_file_name))

                driver.switch_to.parent_frame()

            access_to_site = True

        except Exception as e:
            print(e.with_traceback())

        finally:
            driver.close()

    return True


if __name__ == "__main__":
    main()
