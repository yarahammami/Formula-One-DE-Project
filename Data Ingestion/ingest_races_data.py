import requests
from bs4 import BeautifulSoup
import datetime
import psycopg2

def get_years(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sessions_years = []
        years = soup.find('ul', {'class': 'options'})
        for year in years:
            if year != "\n":
                sessions_years.append(year.text)
        return sessions_years
    return []

def scrape_website(url):
    years = get_years(url)
    all_data = []
    for year in years:
        if year == str(datetime.datetime.now().year):
            url = "https://pitwall.app/races"
        else:
            url = "https://pitwall.app/races/archive/" + year
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('tbody')
            if table:
                for row in table.find_all('tr'):
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    all_data.append((year, *cols))
            else:
                print(f"No table found for year {year}")
        else:
            print(f"Failed to retrieve the webpage for year {year}. Status code: {response.status_code}")
    return all_data

def get_postgresql_connection(username, password, host, port, dbname):
    try:
        connection = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        return connection
    except psycopg2.DatabaseError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# URL to scrape
url = 'https://pitwall.app/races'
scraped_data = scrape_website(url)

# Connection details
username = 'postgres'
password = 'database'
host = 'localhost'
port = '5432'
dbname = 'F1DB'

connection = get_postgresql_connection(username, password, host, port, dbname)

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS races (
                year INTEGER,
                date VARCHAR(50),
                race VARCHAR(100),
                circuit VARCHAR(100),
                winner VARCHAR(100),
                pole_position VARCHAR(100)
            )
        """)
        connection.commit()
        print("Table created successfully.")
    except psycopg2.DatabaseError as e:
        print(f"Error creating table: {e}")

def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO races (year, date, race, circuit, winner, pole_position) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.DatabaseError as e:
        print(f"Error inserting data: {e}")

if connection:
    # Create table (only need to run this once)
    create_table(connection)

    # Insert the scraped data
    insert_data(connection, scraped_data)


    # Close the connection
    connection.close()
else:
    print("Failed to establish connection to the database.")
