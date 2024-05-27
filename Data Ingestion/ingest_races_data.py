import requests
from bs4 import BeautifulSoup
import datetime
import oracledb

# def get_years(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         #print(soup)
#         sessions_years = []
#         years = soup.find('ul',{'class':'options'})
#         for year in years:
#             if year != "\n":
#                 sessions_years.append(year.text)
#         return sessions_years
        

# def scrape_website(url):
#     years = get_years(url)
#     for year in years:
#         if year == datetime.datetime.now().year:
#             url = "https://pitwall.app/races"
#         else:
#             url = "https://pitwall.app/races/archive/"+year
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             #print(soup)
#             data = []
#             table = soup.find('tbody')
#             for row in table.find_all('tr'):  
#                 cols = row.find_all('td')
#                 cols = [col.text.strip() for col in cols]
#                 data.append(cols)
#             print(data)
#         else:
#             print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
#             return []



def get_oracle_connection(username, password, dsn):
    try:
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error connecting to Oracle: {e}")
        return None


# # URL to scrape
# url = 'https://pitwall.app/races'
# scraped_data = scrape_website(url)

# Connection details
username = 'sys'
password = 'database'
dsn = 'localhost:1530/orcl.lan' 

connection = get_oracle_connection(username, password, dsn)

# def create_table(connection):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("""
#             CREATE TABLE races (
#                 year INTEGER,
#                 date DATE,
#                 race VARCHAR2(100),
#                 circuit VARCHAR2(100),
#                 winner VARCHAR2(100),
#                 pole_position VARCHAR2(100), 
#             )
#         """)

#         connection.commit()
#         print("Table created successfully.")
#     except oracledb.DatabaseError as e:
#         print(f"Error creating table: {e}")

# def insert_data(connection, data):
#     try:
#         cursor = connection.cursor()
#         insert_query = """
#             INSERT INTO races (year, date, race, circuit, winner, pole_position) VALUES ()
#         """
#         cursor.executemany(insert_query, data)
#         connection.commit()
#         print("Data inserted successfully.")
#     except oracledb.DatabaseError as e:
#         print(f"Error inserting data: {e}")

# # Create table (only need to run this once)
# create_table(connection)

# # Insert the scraped data
# insert_data(connection, scraped_data)




#print(scraped_data)
