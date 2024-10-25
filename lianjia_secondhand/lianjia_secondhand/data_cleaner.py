import re

def clean_data(item):
    cleaned_title = re.sub(r'\s+', ' ', item['title']) if item['title'] else ''
    cleaned_price = re.sub(r'\s+', ' ', item['price']) if item['price'] else ''
    cleaned_area = re.sub(r'\s+', ' ', item['area']) if item['area'] else ''
    cleaned_location = re.sub(r'\s+', ' ', item['location']) if item['location'] else ''

    return cleaned_title, cleaned_price, cleaned_area, cleaned_location