import os
import requests
from bs4 import BeautifulSoup
import urllib3
import certifi
from urllib.parse import urljoin
from dotenv import dotenv_values

# Load the dotenv file
config = dotenv_values('.env')

# Get the URLs as a list
urls = config['URLS'].split(',')

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

# Function to process a URL: find links, follow them if they start with the base URL, and download PDFs
def process_url(base_url):
    # Send a GET request to the webpage
    response = requests.get(base_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <a> tags with href attributes
    links = soup.find_all('a', href=True)

    # Iterate over the links
    for link in links:
        href = link['href']
        
        # If the link starts with the base URL
        if href.startswith(base_url):
            # Follow the link and find PDFs
            pdf_response = requests.get(href)
            pdf_soup = BeautifulSoup(pdf_response.text, 'html.parser')
            pdf_links = pdf_soup.find_all('a', href=True)
            
            for pdf_link in pdf_links:
                pdf_href = pdf_link['href']
                if pdf_href.endswith('.pdf'):
                    # Construct the absolute URL if the link is relative
                    if not pdf_href.startswith('http'):
                        pdf_href = urljoin(href, pdf_href)
                    
                    # Extract the file name from the URL
                    file_name = pdf_href.split('/')[-1]
                    
                    # Create a directory named after the URL containing the PDFs
                    directory = href.replace('https://', '').replace('http://', '').replace('/', '_')
                    os.makedirs(directory, exist_ok=True)
                    
                    # Download the file
                    download_file(pdf_href, directory, file_name)
                    print(f"Downloaded: {file_name}")

# List of base URLs
base_urls = urls

# Process each base URL
for base_url in base_urls:
    process_url(base_url)
