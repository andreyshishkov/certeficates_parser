from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import time

from declaration_parser.filtering import filter_by_date, filter_by_status
from declaration_parser.declr_url_gathering import get_rows_per_decl_page
ROOT_PATH = 'https://pub.fsa.gov.ru/rds/declaration'


def parse_urls_decl():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    with webdriver.Chrome(options=options) as browser:
        browser.get(ROOT_PATH)
        browser.maximize_window()
        browser.execute_script("document.body.style.zoom='70%'")
        time.sleep(2)

        filter_by_date(browser)
        filter_by_status(browser)
        activate_filters = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rds-declaration-table-view/div/fgis-rds-declaration-advanced-search/div/div/div[3]/button'
        )
        browser.execute_script("arguments[0].click();", activate_filters)
        time.sleep(3)

        next_page_elem = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rds-declaration-table-view/div/div/div[2]/fgis-table-paging/div/div[2]/div[2]/div/span[3]'
        )
        for _ in range(330):
            browser.execute_script("arguments[0].click();", next_page_elem)
            time.sleep(1.5)
            try:
                get_rows_per_decl_page(browser)
            except StaleElementReferenceException:
                time.sleep(3)
                get_rows_per_decl_page(browser)
            except:
                pass

        time.sleep(1)


if __name__ == '__main__':
    with open('../work_files/tmp_urls.txt', 'w') as file:
        pass
    parse_urls_decl()
