import csv
import json

csv_file_path = 'unc_courses.csv'
json_file_path = 'unc_courses.json'

courses = []

with open(csv_file_path, mode = 'r', newline = '') as csvfile:
    csvReader = csv.DictReader(csvfile)
    for row in csvReader:
        courses.append(row)

with open(json_file_path, mode = 'w') as jsonfile:
    json.dump(courses, jsonfile, indent=4)