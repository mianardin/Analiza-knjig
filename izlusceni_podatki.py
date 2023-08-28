from bs4 import BeautifulSoup
import requests
import csv
from csv import writer
import os

try:
    seznam_podatkov = []
    for i in range(10):
        vir = requests.get('https://openlibrary.org/trending/daily?page=' + str(i + 1))
        vir.raise_for_status()

        soup = BeautifulSoup(vir.text, 'html.parser')
        
        knjige = soup.find('ul', class_="list-books").find_all("li")


        for knjiga in knjige:
            url = knjiga.find("a", class_="results")["href"]

            vir = requests.get("https://openlibrary.org" + url)
            vir.raise_for_status()

            soup = BeautifulSoup(vir.text, 'html.parser')

            naslov = soup.find("h1", class_="work-title").text.replace('\n', '').strip()

            avtorji = soup.find("h2", class_="edition-byline").text.replace('\n', '').strip()

            ocena = soup.find('li', class_="avg-ratings").find('span', itemprop="ratingValue").text.replace('\n', '').strip().replace(".", ",")

            st_strani_el = soup.find('span', class_="edition-pages")
            if st_strani_el:
                st_strani = st_strani_el.text
            else:
                st_strani = "not given"

            leto = soup.find('span', itemprop="datePublished").text.replace('\n', '').strip()[-4:]
                
            opis = soup.find('div', class_="book-description").p.text.replace('\n', '').strip()

            seznam_podatkov.append([naslov, avtorji, ocena, st_strani, leto, opis])

            html_filename =  naslov + ' - ' + avtorji + '.html'
            directory = "knjige"
            os.makedirs(directory, exist_ok=True)

            path = os.path.abspath(os.path.join(directory, html_filename))

            with open(path, 'w', encoding='utf-8') as html_file:
                html_file.write(str(soup))

        path = os.path.abspath('knjige.csv')
        with open(path, 'w', newline='', encoding ='utf8') as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow (['Naslov', 'Avtor', 'Ocena', 'Stevilo strani', 'Leto', 'Opis'])
            csv_writer.writerows(seznam_podatkov)
except Exception as e:
    print(e)