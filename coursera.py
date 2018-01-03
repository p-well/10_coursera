import random
import argparse
import requests
from lxml import objectify, etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_xml_feed_page():
    xml_feed_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    try:
        xml_page_content = requests.get(xml_feed_url).content
    except requests.exceptions.ConnectionError:
        xml_page_content = None
    return xml_page_content


def parse_xml_and_choose_random_urls(xml_page_content, amount):
    try:
        root = objectify.fromstring(xml_page_content)
        all_courses_urls = [urltag.loc.text for urltag in root.getchildren()]
        random_courses_urls = random.sample(all_courses_urls, amount)
        return random_courses_urls
    except (etree.XMLSyntaxError, ValueError, UnboundLocalError):
        random_courses_urls = None


def get_course_page_soup(course_page_url):
    try:
        course_page_html = requests.get(course_page_url)
    except requests.exceptions.ConnectionError:
        course_page_html = None
    course_page_html.encoding = 'utf-8'
    soup_object = BeautifulSoup(course_page_html.text, 'html.parser')
    return soup_object


def get_course_name(soup):
    try:
        course_name = soup.find('h1', class_='title display-3-text').text
    except AttributeError:
        course_name = None
    return course_name


def get_course_language(soup):
    try:
        course_language = soup.find('div', class_='rc-Language').text
    except AttributeError:
        course_language = None
    return course_language


def get_course_startdate(soup):
    try:
        start_date = soup.find('div', 'startdate').text
        temporary_date_list = start_date.split(' ')
        if temporary_date_list[0].lower().startswith('start'):
            del temporary_date_list[0]
            start_date = ' '.join(temporary_date_list)
    except AttributeError:
        start_date = None
    return start_date


def get_course_duration(soup):
    try:
        duration = soup.find(
            'i',
            class_='cif-clock'
        ).parent.parent.contents[1].string
    except AttributeError:
        duration = None
    return duration


def get_course_rating(soup):
    try:
        rating = soup.find(
            'div',
            class_='ratings-text bt3-visible-xs'
        ).contents[0].string
    except AttributeError:
        rating = None
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
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    arguments = get_command_line_arguments()
    print('\nCollecting coureses information...')
    xml_page_content = get_xml_feed_page()
    urls_list = parse_xml_and_choose_random_urls(
        xml_page_content,
        arguments.amount
    )
    course_data = {}
    all_courses_data_list = []
    for number, url in enumerate(urls_list, start=1):
        soup = get_course_page_soup(url)
        course_data = {
            '№': number,
            'Course Name': get_course_name(soup),
            'Language': get_course_language(soup),
            'Start Date': get_course_startdate(soup),
            'Duration': get_course_startdate(soup),
            'Rating': get_course_rating(soup),
            'Link': url
        }
        all_courses_data_list.append(course_data)
    output_courses_info_to_xlsx(
        arguments.filename,
        all_courses_data_list
    )
    print('\nDone! File "{}" created'.format(arguments.filename))
