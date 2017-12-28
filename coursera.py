import re
import random 
import requests
from lxml import objectify, etree
from bs4 import BeautifulSoup
from openpyxl import Workbook

def get_courses_urls_list(amount):
    xml_feed_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    try:
        coursera_xml = requests.get(xml_feed_url)
        coursera_xml.raise_for_status
        coursera_xml_content = coursera_xml.content
    except requests.exceptions.ConnectionError as requests_error:
        print(requests_error)
    try:
        root = objectify.fromstring(coursera_xml_content)
        all_courses_urls = [url_tag.loc.text for url_tag in root.getchildren()]
        random_courses_urls = random.sample(all_courses_urls, amount)
        #print(random_courses_urls)
        return random_courses_urls
    except (etree.XMLSyntaxError,
            ValueError, 
            UnboundLocalError) as parsing_error:
        print(parsing_error)

        
def get_and_parse_course_page_html(course_page_url):
    try:
        course_page_html = requests.get(course_page_url)
#        coursera_xml.raise_for_status
    except requests.exceptions.ConnectionError as error:
        print(error)
    course_page_html.encoding = 'utf-8'
    parsed_page = BeautifulSoup(course_page_html.text, 'html.parser')
    return parsed_page


def get_course_name(parsed_page):
    try:
        course_name = parsed_page.find('h1', class_='title display-3-text').text
    except AttributeError:
        course_name = None
    print('Name:', course_name)
    return course_name


def get_course_language(parsed_page):
    try:
        course_language = parsed_page.find('div', class_='rc-Language').text
    except AttributeError:
        course_language = 'No information'
    print(course_language)
    return course_language


def get_course_startdate(parsed_page):
    try:
        start_date = parsed_page.find('div', 'startdate').text
        temporary_date_list = start_date.split(' ')
        if temporary_date_list[0].lower().startswith('start'):
            del temporary_date_list[0]
            start_date = ' '.join(temporary_date_list)
    except AttributeError:
        start_date = 'No information'
    print(start_date)
    return start_date


def get_course_duration(parsed_page):
    try:
        duration = parsed_page.find('i', class_='cif-clock').parent.parent.contents[1].string
    except AttributeError:
        duration = 'No information'
    print(duration)
    return duration


def get_course_rating(parsed_page):
    try:
        rating = parsed_page.find('div', class_='ratings-text bt3-visible-xs').contents[0].string
    except AttributeError:
        rating = 'No information'
    print(rating)
    return rating


def output_courses_info_to_xlsx(all_courses_data):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Courses Information'
    header = ['№','Course Name', 'Language', 'Start Date', 'Duration', 'Rating', 'Link']
    worksheet.append(header)
    for course_data in all_courses_data:
        worksheet.append(course_data)
    workbook.save('coursera_info.xlsx')


if __name__ == '__main__':
    all_courses_data_list = []
    urls_list = get_courses_urls_list(5)
    for number,url in enumerate(urls_list, start=1):
        course_data = []
        parsed_page = get_and_parse_course_page_html(url)
        course_data.append(number)
        course_data.append(get_course_name(parsed_page))
        course_data.append(get_course_language(parsed_page))
        course_data.append(get_course_startdate(parsed_page))
        course_data.append(get_course_duration(parsed_page))
        course_data.append(get_course_rating(parsed_page))
        course_data.append(url)
        all_courses_data_list.append(course_data)
    output_courses_info_to_xlsx(all_courses_data_list)
