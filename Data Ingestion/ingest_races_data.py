import requests
from bs4 import BeautifulSoup
import datetime
#import cx_Oracle

def get_years(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        sessions_years = []
        years = soup.find('ul',{'class':'options'})
        for year in years:
            if year != "\n":
                sessions_years.append(year.text)
        return sessions_years
        

def scrape_website(url):
    years = get_years(url)
    for year in years:
        if year == datetime.datetime.now().year:
            url = "https://pitwall.app/races"
        else:
            url = "https://pitwall.app/races/archive/"+year
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(soup)
            data = []
            table = soup.find('tbody')
            for row in table.find_all('tr'):  
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                data.append(cols)
            print(data)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return []

# def get_oracle_connection(username, password, dsn):
#     try:
#         connection = cx_Oracle.connect(username, password, dsn)
#         return connection
#     except cx_Oracle.DatabaseError as e:
#         print(f"Error connecting to Oracle: {e}")
#         return None

# def create_table(connection):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("""
#             CREATE TABLE scraped_data (
#                 col1 VARCHAR2(100),
#                 col2 VARCHAR2(100),
#                 col3 VARCHAR2(100)
#                 -- Add more columns as needed
#             )
#         """)
#         connection.commit()
#         print("Table created successfully.")
#     except cx_Oracle.DatabaseError as e:
#         print(f"Error creating table: {e}")

# def insert_data(connection, data):
#     try:
#         cursor = connection.cursor()
#         insert_query = """
#             INSERT INTO scraped_data (col1, col2, col3) VALUES (:1, :2, :3)
#         """
#         cursor.executemany(insert_query, data)
#         connection.commit()
#         print("Data inserted successfully.")
#     except cx_Oracle.DatabaseError as e:
#         print(f"Error inserting data: {e}")

# URL to scrape
url = 'https://pitwall.app/races'
scraped_data = scrape_website(url)
#print(scraped_data)
# # Oracle connection details
# username = 'your_username'
# password = 'your_password'
# dsn = 'your_dsn'  # e.g., 'localhost:1521/xe'

# # Connect to Oracle and insert data
# connection = get_oracle_connection(username, password, dsn)
# if connection:
#     create_table(connection)
#     insert_data(connection, scraped_data)
#     connection.close()
