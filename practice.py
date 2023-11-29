import requests
from bs4 import BeautifulSoup
import certifi
import urllib3
from urllib.parse import urljoin
import os

# Function to download a file
def download_file(url, directory, file_name):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    file_path = os.path.join(directory, file_name)  # Join the directory path and the file name
    with http.request('GET', url, preload_content=False) as response, open(file_path, 'wb') as out_file:
        while True:
            data = response.read(1024)
            if not data:
                break
            out_file.write(data)
    response.release_conn()

# Function to download a file
def download_file(url, file_name):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    with http.request('GET', url, preload_content=False) as response, open(file_name, 'wb') as out_file:
        while True:
            data = response.read(1024)
            if not data:
                break
            out_file.write(data)
    response.release_conn()

# URL of the webpage to scrape
url = 'https://www.physicsandmathstutor.com/biology-revision/igcse-cie/characteristics-and-classification-of-living-organisms/'

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the <a> tags with href attributes
links = soup.find_all('a', href=True)

# Specify your directory here
directory = 'directory'

# Iterate over the links and download PDF files
for link in links:
    href = link['href']
    if href.endswith('.pdf'):
        # Construct the absolute URL if the link is relative
        if not href.startswith('http'):
            href = urljoin(url, href)
        
        # Extract the file name from the URL
        file_name = href.split('/')[-1]
        
        # Download the file
        download_file(href, directory, file_name)
        print(f"Downloaded: {file_name}")

