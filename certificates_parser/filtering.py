import calendar
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


# operations with date (get and transform)
def transform_date(date: datetime.time) -> str:
    year = date.year
    month = str(date.month).rjust(2, '0')
    day = str(date.day).rjust(2, '0')
    return f'{day}.{month}.{year}'


def get_cur_date() -> str:
    date = datetime.now()
    return transform_date(date)


def get_next_month_date() -> str:
    date = datetime.now()
    days_in_month = calendar.monthrange(date.year, date.month)[1]
    date += timedelta(days=days_in_month)
    return transform_date(date)


# filter by date
def filter_by_start_date(browser: WebDriver) -> None:
    date = get_cur_date()
    browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rss-certificate-table-view/div/fgis-rss-certificate-advanced-search/div/div/div[2]/div/div[3]/fgis-calendar[1]/div/div/input'
    ).send_keys(date)


def filter_by_finish_date(browser: WebDriver) -> None:
    date = get_next_month_date()
    browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rss-certificate-table-view/div/fgis-rss-certificate-advanced-search/div/div/div[2]/div/div[3]/fgis-calendar[2]/div/div/input'
    ).send_keys(date)
    # browser.find_element(
    #     by=By.XPATH,
    #     value='/html/body/fgis-root/div/fgis-rss-certificate-table-view/div/fgis-rss-certificate-advanced-search/div/div/div[2]/div/div[3]/fgis-calendar[2]/div/div/input'
    # ).click()


def filter_by_date(browser: WebDriver) -> None:
    filter_by_start_date(browser)
    filter_by_finish_date(browser)


# filter by status
def click_activate_menu(browser: WebDriver) -> None:
    elem = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rss-certificate-table-view/div/fgis-rss-certificate-advanced-search/div/div/div[2]/div/div[4]/fgis-selectbox/div'
    )
    browser.execute_script("arguments[0].click();", elem)
    time.sleep(0.8)


def filter_by_status(browser: WebDriver) -> None:

    # choose types of certificates
    click_activate_menu(browser)
    recovery = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/fgis-select-dropdown/div/div/div[2]/fgis-virtual-list/div/div[2]/div[2]/fgis-virtual-list-item/li/div'
    )  # Возобновлен
    browser.execute_script("arguments[0].click();", recovery)

    click_activate_menu(browser)
    active = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/fgis-select-dropdown/div/div/div[2]/fgis-virtual-list/div/div[2]/div[3]/fgis-virtual-list-item/li/div'
    )  # Действует
    browser.execute_script("arguments[0].click();", active)

    click_activate_menu(browser)
    extended = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/fgis-select-dropdown/div/div/div[2]/fgis-virtual-list/div/div[2]/div[7]/fgis-virtual-list-item/li/div'
    )  # Продлен
    browser.execute_script("arguments[0].click();", extended)

