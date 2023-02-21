import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm


def get_finish_date(browser: WebDriver, url: str) -> str:
    cert_path = url + '/certificate'
    browser.get(cert_path)
    time.sleep(2)
    try:
        tag = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-certificate-certificate/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[3]/fgis-card-info-row[2]/div[2]/span'
        )
        result = tag.text
    except:
        result = '-'
    return result


def get_doc_type(browser: WebDriver, url: str) -> str:
    base_info_path = url + '/baseInfo'
    browser.get(base_info_path)
    time.sleep(2)
    try:
        tag = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-certificate-base-info/fgis-card-block/div/div[2]/div/fgis-card-info-row[2]/div[2]'
        )
        doc_type = tag.text

    except:
        doc_type = '-'
    return doc_type


# get personnel data
def get_fullname_organization(browser: WebDriver) -> str:
    try:
        org_name = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[3]/fgis-card-info-row[1]/div[2]/span'
        ).text

        pattern = re.compile('[«"]\w+?[»"]')
        short_name = pattern.findall(org_name)
        if short_name:
            org_name = short_name[-1]
    except:
        org_name = '-'
    return org_name


def get_fio(browser: WebDriver) -> str:
    # name
    try:
        name = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[4]/fgis-card-info-row[2]/div[2]/span'
        ).text
    except:
        name = ''

    # surname
    try:
        surname = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[4]/fgis-card-info-row[1]/div[2]/span'
        ).text
    except:
        surname = ''

    fio = ' '.join([surname, name])
    return fio if fio != ' ' else '-'


def get_address(browser: WebDriver) -> str:
    try:
        address = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[2]/div/div[2]/div/fgis-card-edit-row[1]/div[2]/fgis-field-complex-input-multi/div/div/span'
        ).text
    except:
        address = '-'

    return address


def get_phone(browser: WebDriver) -> str:
    try:
        phone = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[4]/div/div[2]/div/fgis-card-edit-row[1]/div[2]/fgis-field-complex-input-multi/div/div/span'
        ).text
    except:
        phone = '-'
    return phone


def get_email(browser: WebDriver) -> str:
    try:
        email = browser.find_element(
            by=By.XPATH,
            value='/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[4]/div/div[2]/div/fgis-card-edit-row[2]/div[2]/fgis-field-complex-input-multi/div/div/span'
        ).text
    except:
        email = '-'
    return email


def get_personnel_data(browser: WebDriver, url: str) -> list[str]:
    applicant_path = url + '/applicant'
    browser.get(applicant_path)
    time.sleep(2)

    org_name = get_fullname_organization(browser)
    fio = get_fio(browser)
    address = get_address(browser)
    phone = get_phone(browser)
    email = get_email(browser)

    return [org_name, fio, address, phone, email]


def get_data_from_url(browser: WebDriver, url) -> list[str]:
    finish_date = get_finish_date(browser, url)
    doc_type = get_doc_type(browser, url)
    personnel_data = get_personnel_data(browser, url)
    data = [finish_date, doc_type] + personnel_data
    return data


def gather_cert_data() -> None:
    options = webdriver.ChromeOptions()
    work_files_path = '../work_files' if __name__ == '__main__' else 'work_files'
    with webdriver.Chrome(options=options) as browser:
        browser.maximize_window()

        rows = []
        with open(work_files_path + '/tmp_urls.txt', 'r') as file:
            urls = file.read().strip('\n').split('\n')
            urls = list(set(urls))
            for url in tqdm(urls):
                row = get_data_from_url(browser, url)
                row[1] = f'Сертификат; {row[1]}'
                print(row)
                if row[-1] == '-' and row[-2] == '-':
                    continue
                rows.append(row)

    headers = [
        'Дата окончания',
        'Тип документа',
        'Наименование организации',
        'Имя руководителя',
        'Адрес организации',
        'Номер телефона',
        'Почта'
    ]
    with open(work_files_path + '/cert_data.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)
        writer.writerows(rows)


if __name__ == '__main__':
    gather_cert_data()
