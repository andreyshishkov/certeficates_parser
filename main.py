import csv
from certificates_parser.cert_url_parser import parse_urls_cert
from certificates_parser.data_gathering import gather_cert_data

from declaration_parser.decl_url_parser import parse_urls_decl
from declaration_parser.decl_data_gathering import gather_decl_data


def main():
    with open('work_files/tmp_urls.txt', 'w') as file:
        pass
    parse_urls_cert()
    gather_cert_data()

    with open('work_files/tmp_urls.txt', 'w') as file:
        pass
    parse_urls_decl()
    gather_decl_data()

    with open('work_files/cert_data.csv', 'r', encoding='utf-8-sig') as cert_file:
        cert_reader = csv.reader(cert_file, delimiter=';')
        cert_data = [row for row in cert_reader]

    with open('work_files/decl_data.csv', 'r', encoding='utf-8-sig') as decl_file:
        decl_reader = csv.reader(decl_file, delimiter=';')
        decl_data = [row for row in decl_reader]

    headers = cert_data[0]
    with open('work_files/all_data.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        arr1 = cert_data[1:]
        arr1.extend(decl_data[1:])
        writer.writerow(headers)
        writer.writerows(arr1)


if __name__ == '__main__':
    main()
