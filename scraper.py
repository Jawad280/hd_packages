from bs4 import BeautifulSoup
import urllib3

def source_code_generator(url):
    # Create a PoolManager instance
    http = urllib3.PoolManager()
    # Send a GET request to the URL
    response = http.request('GET', url)
    # Read the HTML content from the response
    source_code = response.data.decode('utf-8')
    return source_code

def get_package(url):
    source_code = source_code_generator(url=url)
    soup = BeautifulSoup(source_code, 'html.parser')

    package_name = soup.find(class_='package-layout__product-title').string
    price = soup.find(class_='package-price-extended__pdp-page').string
    shop_name = soup.find(class_='description-location__card-name').string
    location = soup.find(class_='description-location__card-address').string

    # RATING
    rating = soup.find(class_='package-reviews__section-review')
    if rating:
        rating = rating.find('div', class_='star-rating').text.strip()
    else:
        rating = 'No Rating'

    # FAQ
    faq = []
    faq_items = soup.find_all(class_='questions-package__item')
    for item in faq_items:
        question = item.find('h3', class_='questions-package__question__text').text.strip()
        answer = item.find('div', class_='questions-package__answer__text').text.strip()
        
        faq.append({question: answer})

    # PACKAGE DETAILS
    package_details = []

    # Extract all the headers and their corresponding contents
    sections = soup.find_all('div', class_='package-details-accordion--item')

    for section in sections:
        # Extract the header
        header = section.find('h2', class_='package-details-accordion--title')

        # Extract the content within each section
        content = section.find('div', class_='panel-body')
        if content:
            test = content.get_text(separator='\n').strip()

        package_details.append({header.text.strip(): content.get_text(separator='\n').strip()})

    # Category Url
    category_tags = soup.find('div', class_='breadcrumbs')
    category_url = ''

    # Find all <a> tags within the breadcrumbs
    links = category_tags.find_all('a')

    # Extract the href attribute from the last <a> tag
    if links:
        category_tag = links[-1]['href']
        category_url = f'https://hdmall.co.th{category_tag}'

    return {
        "package_name": package_name,
        "price": price,
        "shop_name": shop_name,
        "location": location,
        "rating": rating,
        "faq": faq,
        "package_details": package_details,
        "category_url": category_url
    }