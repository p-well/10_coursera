import random
import argparse
import requests
from lxml import objectify, etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def fetch_page_content(url):
    return requests.get(url).content


def parse_xml_for_urls(xml_page_content):
    root = objectify.fromstring(xml_page_content)
    all_urls_list = [urltag.loc.text for urltag in root.getchildren()]
    return all_urls_list


def choose_random_urls(all_urls_list, amount):
    random_urls_list = random.sample(all_urls_list, amount)
    return random_urls_list


def parse_course_page_html(course_page_html):
    page_soup = BeautifulSoup(course_page_html, 'html.parser')
    return page_soup


def get_course_name(soup):
    try:
        return soup.find('h1', class_='title display-3-text').text
    except AttributeError:
        return None


def get_course_language(soup):
    try:
        return soup.find('div', class_='rc-Language').text
    except AttributeError:
        return None


def get_course_startdate(soup):
    try:
        start_date = soup.find('div', 'startdate').text
        temporary_date_list = start_date.split(' ')
        if temporary_date_list[0].lower().startswith('start'):
            del temporary_date_list[0]
            start_date = ' '.join(temporary_date_list)
        return start_date
    except AttributeError:
        return None


def get_course_duration(soup):
    try:
        return soup.find(
            'i',
            class_='cif-clock'
        ).parent.parent.contents[1].string
    except AttributeError:
        return None


def get_course_rating(soup):
    try:
        return soup.find(
            'div',
            class_='ratings-text bt3-visible-xs'
        ).contents[0].string
    except AttributeError:
        return None


def output_courses_info_to_xlsx(filename, all_courses_data):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Courses Information'
    header = [
        '№',
        'Course Name',
        'Language',
        'Start Date',
        'Duration',
        'Rating',
        'Link'
    ]
    worksheet.append(header)
    for course_data in all_courses_data:
        worksheet.append([
            course_data['№'],
            course_data['Course Name'],
            course_data['Language'],
            course_data['Start Date'],
            course_data['Duration'],
            course_data['Rating'],
            course_data['Link']
        ])
    workbook.save(filename)


def get_command_line_arguments():
    parser = argparse.ArgumentParser(prog='Coursera Crawler')
    parser.add_argument('--amount', type=int, default=20)
    parser.add_argument('--filename', type=str, default='cousera.xlsx')
    return parser.parse_args()


if __name__ == '__main__':
    all_courses_data = []
    arguments = get_command_line_arguments()
    print('\nCollecting coureses information...')
    xml_feed_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    xml_page_content = fetch_page_content(xml_feed_url)
    all_urls = parse_xml_for_urls(xml_page_content)
    random_urls = choose_random_urls(all_urls, arguments.amount)
    for number, url in enumerate(random_urls, start=1):
        course_page_html = fetch_page_content(url)
        page_soup = parse_course_page_html(course_page_html)
        course_data = {
            '№': number,
            'Course Name': get_course_name(page_soup),
            'Language': get_course_language(page_soup),
            'Start Date': get_course_startdate(page_soup),
            'Duration': get_course_duration(page_soup),
            'Rating': get_course_rating(page_soup),
            'Link': url
        }
        for key, value in course_data.items():
            if value is None:
                course_data[key] = 'No information'
        all_courses_data.append(course_data)
    output_courses_info_to_xlsx(arguments.filename, all_courses_data)
    print('\nDone! File "{}" created'.format(arguments.filename))
