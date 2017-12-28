import re
import random 
import requests
from lxml import objectify, etree
from bs4 import BeautifulSoup


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
    print(course_name)
    return course_name

def get_course_language(parsed_page):
    try:
        course_language = parsed_page.find('div', class_='rc-Language').text
    except AttributeError:
        course_language = None
    print(course_language)
    return course_language

def get_course_startdate(parsed_page):
    try:
        start_date = parsed_page.find('div', 'startdate').text
        temporary_date_list = start_date.split(' ')
        if temporary_date_list[0].lower().startswith('start'):
            del temporary_date_list[0]
            start_date = ' '.join(temporary_date_list)
        print(type(start_date))
    except AttributeError:
        start_date = None
    print(start_date)
    return start_date


def get_course_duration(parsed_page):
    try:
        duration = parsed_page.find('i', class_='cif-clock').parent.parent.contents[1].string
    except AttributeError:
        duration = None
    print(duration)
    return duration
        
        
# # def output_courses_info_to_xlsx(filepath):
# #     pass


if __name__ == '__main__':
    urls_list = get_courses_urls_list(5)
    parsed_page = get_and_parse_course_page_html(urls_list[0])
    course_name = get_course_name(parsed_page)
    course_language = get_course_language(parsed_page)
    start_date = get_course_startdate(parsed_page)
    duration = get_course_duration(parsed_page)
    #print(course_name, course_language, start_date)
