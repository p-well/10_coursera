import requests
import pprint 
from lxml import objectify, etree


def get_courses_urls_list():
    xml_feed_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    try:
        coursera_xml = requests.get(xml_feed_url).content
    except requests.exceptions.ConnectionError as requests_error:
        print(requests_error)
    try:
        root = objectify.fromstring(coursera_xml)
        return [url_tag.loc.text for url_tag in root.getchildren()]
    except etree.XMLSyntaxError as etree_error:
        print(etree_error)

# def get_course_info(course_slug):
#     pass

# # def output_courses_info_to_xlsx(filepath):
# #     pass


if __name__ == '__main__':
    a = get_courses_urls_list()
    print(a)
