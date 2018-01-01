import random
import argparse
import requests
from lxml import objectify, etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def fetch_random_courses_urls_list(amount):
    xml_feed_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    try:
        coursera_xml = requests.get(xml_feed_url)
        coursera_xml.raise_for_status
        coursera_xml_content = coursera_xml.content
    except requests.exceptions.ConnectionError:
        coursera_xml.content = None
    try:
        root = objectify.fromstring(coursera_xml_content)
        all_courses_urls = [urltag.loc.text for urltag in root.getchildren()]
        random_courses_urls = random.sample(all_courses_urls, amount)
        return random_courses_urls
    except (etree.XMLSyntaxError, ValueError, UnboundLocalError):
        random_courses_urls = None


def fetch_course_page_soup(course_page_url):
    try:
        course_page_html = requests.get(course_page_url)
    except requests.exceptions.ConnectionError:
        course_page_html = None
    course_page_html.encoding = 'utf-8'
    soup_object = BeautifulSoup(course_page_html.text, 'html.parser')
    return soup_object


def fetch_course_name(soup):
    try:
        course_name = soup.find('h1', class_='title display-3-text').text
    except AttributeError:
        course_name = None
    return course_name


def fetch_course_language(soup):
    try:
        course_language = soup.find('div', class_='rc-Language').text
    except AttributeError:
        course_language = 'No information'
    return course_language


def fetch_course_startdate(soup):
    try:
        start_date = soup.find('div', 'startdate').text
        temporary_date_list = start_date.split(' ')
        if temporary_date_list[0].lower().startswith('start'):
            del temporary_date_list[0]
            start_date = ' '.join(temporary_date_list)
    except AttributeError:
        start_date = 'No information'
    return start_date


def fetch_course_duration(soup):
    try:
        duration = soup.find(
            'i',
            class_='cif-clock'
        ).parent.parent.contents[1].string
    except AttributeError:
        duration = 'No information'
    return duration


def fetch_course_rating(soup):
    try:
        rating = soup.find(
            'div',
            class_='ratings-text bt3-visible-xs'
        ).contents[0].string
    except AttributeError:
        rating = 'No information'
    return rating


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
    namespace = parser.parse_args()
    return namespace


if __name__ == '__main__':
    namespace = get_command_line_arguments()
    all_courses_data_list = []
    print('\nCollecting coureses information...')
    urls_list = fetch_random_courses_urls_list(namespace.amount)
    course_data = {}
    for number, url in enumerate(urls_list, start=1):
        soup = fetch_course_page_soup(url)
        course_data = {
            '№': number,
            'Course Name': fetch_course_name(soup),
            'Language': fetch_course_language(soup),
            'Start Date': fetch_course_startdate(soup),
            'Duration': fetch_course_startdate(soup),
            'Rating': fetch_course_rating(soup),
            'Link': url
        }
        all_courses_data_list.append(course_data)
    output_courses_info_to_xlsx(namespace.filename, all_courses_data_list)
    print('\nDone! File "{}" created'.format(namespace.filename))
