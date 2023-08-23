import os
import requests
import traceback

knjige_directory = 'podatki'

def download_url_to_string(url):
    try:
        page_content = requests.get(url)
        if page_content.status_code == 200:
            return page_content.text
        else:
            raise ValueError(f"Čudna koda: {page_content.status_code}")
    except Exception:
        print(f"Prišlo je do spodnje napake:\n{traceback.format_exc()}")

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    html_strani = download_url_to_string(page)
    save_string_to_file(html_strani, directory, filename)

def url(index):
    return 'https://openlibrary.org/trending/daily?page='.format(index)
def name(index):
    return 'knjige{}'.format(index)

for i in range(0,10):
    save_frontpage(url(i), knjige_directory, name(i)) 

def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()