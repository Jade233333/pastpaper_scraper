import os
import requests
from bs4 import BeautifulSoup
import urllib3
import certifi
from urllib.parse import urljoin
from dotenv import dotenv_values
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import random

# List of headers
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
]


# Load the dotenv file
config = dotenv_values('.env')

# Get the URLs as a list
urls = config['URLS'].split(',')

def download_file(url, directory, file_name):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    file_path = os.path.join(directory, file_name)  # Join the directory path and the file name
    with http.request('GET', url, preload_content=False) as response, open(file_path, 'wb') as out_file:
        total = int(response.headers.get('content-length', 0))
        with tqdm(total=total, unit='B', unit_scale=True, desc=file_name) as pbar:
            for chunk in response.stream(1024):
                out_file.write(chunk)
                pbar.update(len(chunk))
    response.release_conn()


def process_url(base_url):
    # Randomly select a User-Agent header
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    # Send a GET request to the webpage
    response = requests.get(base_url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <a> tags with href attributes
    links = soup.find_all('a', href=True)

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Iterate over the links
        for link in links:
            href = link['href']
            
            # If the link starts with the base URL
            if href.startswith(base_url):
                # Retry mechanism with a delay of 10 seconds
                while True:
                    try:
                        # Follow the link and find PDFs
                        # Update the headers for each request
                        headers = {
                            'User-Agent': random.choice(user_agents)
                        }
                        pdf_response = requests.get(href, headers=headers)
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
                                directory = href.replace('https://', '').replace('http://', '').replace('/', '_').replace('www.physicsandmathstutor.com_','')
                                os.makedirs(directory, exist_ok=True)
                                
                                # Submit the download task to the thread pool
                                executor.submit(download_file, pdf_href, directory, file_name)
                        
                        # Break the retry loop if the request is successful
                        break
                    except (requests.exceptions.RequestException,requests.exceptions.SSLError, urllib3.exceptions.SSLError):
                        print("Request failed. Retrying in 10 seconds...")
                        time.sleep(10)
                        
# List of base URLs
base_urls = urls

# Process each base URL
for base_url in base_urls:
    process_url(base_url)
