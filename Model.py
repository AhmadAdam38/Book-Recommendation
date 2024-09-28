import requests
from bs4 import BeautifulSoup
import os

# Function to get HTML content of the website
def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve content from {url}")
        return None

# Function to download an image from a URL
def download_image(image_url, save_path):
    img_data = requests.get(image_url).content
    with open(save_path, 'wb') as img_file:
        img_file.write(img_data)

# Function to scrape books' titles and cover images
def scrape_books(url, save_dir):
    html = get_html(url)
    
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Finding all book sections
        books = soup.find_all('article', class_='product_pod')
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for book in books:
            # Extract book title
            title = book.h3.a['title']
            print(f"Title: {title}")

            # Extract image URL (relative path)
            image_rel_url = book.find('img')['src']
            image_url = f"http://books.toscrape.com/{image_rel_url}"
            
            print(f"Image URL: {image_url}")

            # Define save path for the image
            image_filename = os.path.join(save_dir, f"{title}.jpg")
            
            # Download the image
            download_image(image_url, image_filename)
            print(f"Image saved to {image_filename}")

# Define the URL of the website to scrape and the directory to save images
url = 'http://books.toscrape.com/'
save_directory = './book_images'

# Start scraping
scrape_books(url, save_directory)
