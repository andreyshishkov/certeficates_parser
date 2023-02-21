import calendar
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from certificates_parser.filtering import get_cur_date, get_next_month_date


def filter_by_start_date(browser: WebDriver) -> None:
    date = get_cur_date()
    browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rds-declaration-table-view/div/fgis-rds-declaration-advanced-search/div/div/div[2]/div/fgis-date-range[2]/div/fgis-calendar[1]/div/div/input'
    ).send_keys(date)


def filter_by_finish_date(browser: WebDriver) -> None:
    date = get_next_month_date()
    browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rds-declaration-table-view/div/fgis-rds-declaration-advanced-search/div/div/div[2]/div/fgis-date-range[2]/div/fgis-calendar[2]/div/div/input'
    ).send_keys(date)


def filter_by_date(browser: WebDriver) -> None:
    filter_by_start_date(browser)
    filter_by_finish_date(browser)


def click_activate_menu(browser: WebDriver) -> None:
    elem = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rds-declaration-table-view/div/fgis-rds-declaration-advanced-search/div/div/div[2]/div/div[2]/fgis-selectbox/div/div/div[1]'
    )
    browser.execute_script("arguments[0].click();", elem)
    time.sleep(0.8)


def filter_by_status(browser: WebDriver) -> None:

    # choose types of declarations
    click_activate_menu(browser)
    active = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/fgis-select-dropdown/div/div/div[2]/fgis-virtual-list/div/div[2]/div[2]/fgis-virtual-list-item/li/div'
    )  # Действует
    browser.execute_script("arguments[0].click();", active)

    click_activate_menu(browser)
    recovery = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/fgis-select-dropdown/div/div/div[2]/fgis-virtual-list/div/div[2]/div[5]/fgis-virtual-list-item/li/div'
    )  # Возобновлен
    browser.execute_script("arguments[0].click();", recovery)
