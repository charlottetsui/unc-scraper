from bs4 import BeautifulSoup
import requests
import pandas as pd

# 2nd attempt to scrape UNC courses
# this one can be adjusted to scrape term specific courses

url = 'https://reports.unc.edu/class-search/?subject=DATA&term=2025+Spring'

page = requests.get(url)

soup = BeautifulSoup(page.text, features = 'lxml')

table = soup.find('table', class_ = 'table table-sm table-hover tableau-like')
header = soup.find_all('th')

excluded_headers = {"Same As", "Available Seats"}
header_titles = [titles.text.strip() for titles in header if titles.text.strip() not in excluded_headers]

df = pd.DataFrame(columns = header_titles)

row_list = []

column_data = table.find_all('tr')


first_row_data = column_data[1].find_all('td') 
first_row = [data.text.strip() for data in first_row_data]
first_row.pop(2)
first_row.pop(len(first_row) - 1)
row_list.append(first_row)

i = 1
for row in column_data[2:]:
    row_data = row.find_all('td')
    indv_row_data = [data.text.strip() for data in row_data]
    indv_row_data.pop(len(indv_row_data) - 1)

    if len(indv_row_data) == 11:
        indv_row_data[0] = row_list[i - 1][1]
    if len(indv_row_data) == 12:
        indv_row_data.pop(1)
    
    indv_row_data.insert(0, 'DATA') # change name with respective course name

    row_list.append(indv_row_data)
                    
    length = len(df)
    df.loc[length] = indv_row_data
    i += 1

json_data = df.to_json(orient='records')

with open('data_courses.json', 'w') as f:
    f.write(json_data)
