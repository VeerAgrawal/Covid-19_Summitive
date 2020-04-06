
#Libraries Needed
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests 
from bs4 import BeautifulSoup 
from prettytable import PrettyTable

#Indian ministry of health website for oficial coronavirus stats
url = 'https://www.mohfw.gov.in/' 

#This is getting the html content from the website
web_content = requests.get(url).content

#Using the library BeautifilSoup to parse the html content
soup = BeautifulSoup(web_content, "html.parser")

#Removing extra lines and spaces
extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 

#creating a list for stats
stats = []
#finding all of the rows in the table
all_rows = soup.find_all('tr')

#finding data cells and adding them to the list
for row in all_rows: 
    stat = extract_contents(row.find_all('td'))
    if len(stat) == 5: 
        stats.append(stat)

#Labeling the table and using the library pandas for processing it 
new_cols = ["no.", "States/UT","Confirmed","Recovered","Deceased"]
state_data = pd.DataFrame(data = stats, columns = new_cols)

#The data is in strings so converting it to Integers
state_data['Confirmed'] = state_data['Confirmed'].map(int)
state_data['Recovered'] = state_data['Recovered'].map(int)
state_data['Deceased']  = state_data['Deceased'].map(int)

#Using the library Prety table to represent the data
table = PrettyTable()
table.field_names = (new_cols)
for i in stats:
    table.add_row(i)
table.add_row(["","Total", 
               sum(state_data['Confirmed']), 
               sum(state_data['Recovered']), 
               sum(state_data['Deceased'])])
print(table)
