from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


def get_decl_url(row: WebElement) -> None:
    a_tag = row.find_element(
        by=By.TAG_NAME,
        value='a'
    )
    url = a_tag.get_attribute('href')
    if __name__ == '__main__':
        work_files = '../work_files/tmp_urls.txt'
    else:
        work_files = 'work_files/tmp_urls.txt'
    with open(work_files, 'a') as file:
        file.write(url + '\n')


def get_rows_per_decl_page(browser: WebDriver) -> None:
    rows = browser.find_element(
        by=By.XPATH,
        value='/html/body/fgis-root/div/fgis-rds-declaration-table-view/div/div/div[1]/fgis-registry-table/fgis-h-table-with-components/fgis-handsontable-wrapper/div[1]/div/div/div/table/tbody'
    ).find_elements(
        by=By.TAG_NAME,
        value='tr'
    )
    assert len(rows) < 12
    rows = rows[1:]
    for row in rows:
        get_decl_url(row)
