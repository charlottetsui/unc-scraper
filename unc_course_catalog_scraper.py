from bs4 import BeautifulSoup
import requests
import csv

# 1st attempt at scraping UNC classes
# this one is not term specific, it scrapes all the courses from the UNC course catalog
# puts courses into a csv file -> use jsv.py to turn it into JSON data

url = "https://catalog.unc.edu/courses/comp/"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

# <div class="courseblock">
course_list = [] 
course_blocks = soup.find_all('div', class_="courseblock") # find_all courseblocks

for courses in course_blocks:

    # <span class="text detail-code margin--tiny text--semibold text--big"><strong>COMP 50.</strong></span>
    course_num_elem = courses.find('span', class_="text detail-code margin--tiny text--semibold text--big")
    course_num = course_num_elem.get_text(strip = True)
    
    # <span class="text detail-title margin--tiny text--semibold text--big"><strong>First-Year Seminar: Everyday Computing.</strong></span>
    course_name_elem = courses.find('span', class_="text detail-title margin--tiny text--semibold text--big")
    course_name = course_name_elem.get_text(strip = True)

    # <span class="text detail-hours margin--tiny text--semibold text--big"><strong>3 Credits.</strong></span>
    course_credits_elem = courses.find('span', class_="text detail-hours margin--tiny text--semibold text--big")
    course_credits = course_credits_elem.get_text(strip = True)
    
    # <p class="courseblockextra">
    course_description_elem = courses.find('p', class_="courseblockextra")
    course_description = course_description_elem.get_text(strip = True)

    # <span class="text detail-idea_action margin--default">
    course_ideas_elem = courses.find('span', class_="text detail-idea_action margin--default")
    if course_ideas_elem:
        course_ideas = course_ideas_elem.get_text(strip = True)
    else:
        course_ideas = "N/A"

    # <span class="text detail-making_connections margin--default">
    course_connections_elem = courses.find('span', class_="text detail-making_connections margin--default")
    if course_connections_elem:
        course_connections = course_connections_elem.get_text(strip = True)
    else:
        course_connections = "N/A"

    # <span class="text detail-requisites margin--default">
    course_requisites_elem = courses.find('span', class_="text detail-requisites margin--default")
    if course_requisites_elem:
        course_requisites = course_requisites_elem.get_text(strip = True)
    else:
        course_requisites = "N/A"

    course_list.append([course_num, course_name, course_credits, course_description, course_ideas, course_connections, course_requisites])

with open('unc_courses.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ["Course Number", "Course Name", "Course Credits", "Course Description", "Course Ideas", "Course Connections", "Course Requisites"]
    writer.writerow(header)
    writer.writerows(course_list)

csvfile.close()

print(course_list)