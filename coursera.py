import random 
import requests
from lxml import objectify, etree
from bs4 import BeautifulSoup


def get_courses_urls_list(amount):
    xml_feed_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    try:
        coursera_xml = requests.get(xml_feed_url).content
        coursera_xml.raise_for_status
    except requests.exceptions.ConnectionError as requests_error:
        print(requests_error)
    try:
        root = objectify.fromstring(coursera_xml)
        all_courses_urls = [url_tag.loc.text for url_tag in root.getchildren()]
        random_courses_urls = random.sample(all_courses_urls, amount)
        return random_courses_urls
    except etree.XMLSyntaxError, ValueError as parsing_error:
        print(parsing_error)

def get_course_page_html(course_page_url):
    try:
        course_page_html = requests.get(course_page_url)
        coursera_xml.raise_for_status
    except requests.exceptions.ConnectionError as error:
        print(error)
    course_page_html.encoding = 'utf-8'
    return course_page_html.text

def get_course_name(course_page_html):
    parsed_page = BeautifulSoup(course_page_html, html.parser)
    


# # def output_courses_info_to_xlsx(filepath):
# #     pass


if __name__ == '__main__':
    get_courses_urls_list()
