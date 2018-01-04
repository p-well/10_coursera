# Coursera Dump

This is web crawler for  collecting information about educational courses presented at [Coursera.org](https://www.coursera.org/). <br />

The script randomly choose any specified number of courses from [Coursera xml feed](https://www.coursera.org/sitemap~www~courses.xml) and parse XML using 
[lxml](https://pypi.python.org/pypi/lxml) library <br /> to retrieve URLs list. <br />

Then script goes to the each course webpage, parse it with [BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4) and put parsed data into Excel table using [Openpyxl](https://pypi.python.org/pypi/openpyxl) library.


Script retrieves the following data about course:

- Course name
- Course language
- Closest date of start
- Duration
- Average stars

Pavel Kadantsev, 2017. <br/>
p.a.kadantsev@gmail.com


# Installation

Python 3.5 should be already installed. <br />
Clone this repo on your machnine and install dependencies using ```pip install -r requirements.txt``` in CLI. <br />
It is recommended to use virtual environment.


# Usage

To execute the script run the command ```python coursera.py <arguments>``` in your OS console/terminal.

User needs to specify amount of courses and name of output Excel file - see example below.
Excel file will be saved in script directory.

Script executing without specifying of the arguments leads to script running with default values - amount: 20, filename: "coursera.xlsx".

# Example of Scripts Launch

<pre>
<b>>python coursera.py --amount 20 --filename coursera_output.xlsx</b>

Collecting coureses information...

Done! File "coursera_output.xlsx" created
</pre>


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
