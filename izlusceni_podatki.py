from bs4 import BeautifulSoup
import requests
import csv
from csv import writer
import os

seznam_podatkov = []
counter = 0
for i in range(8):
    vir = requests.get('https://openlibrary.org/trending/daily?page=' + str(i + 1))
    vir.raise_for_status()

    soup = BeautifulSoup(vir.text, 'html.parser')
    
    knjige = soup.find('ul', class_="list-books").find_all("li")


    for index, knjiga in enumerate(knjige):
        url = knjiga.find("a", class_="results")["href"]

        vir = requests.get("https://openlibrary.org" + url)
        vir.raise_for_status()

        soup = BeautifulSoup(vir.text, 'html.parser')

        naslov_el = soup.find("h1", class_="work-title")
        if naslov_el:
            naslov = naslov_el.text.replace('\n', '').strip().replace("?", "").replace(":", "")
        else:
            naslov = 'not given'

        avtorji_el = soup.find("h2", class_="edition-byline")
        if avtorji_el:
            avtorji = avtorji_el.text.replace('\n', '').strip()
        else:
            avtorji = 'not given'

        ocena_el = soup.find('li', class_="avg-ratings").find('span', itemprop="ratingValue")
        if ocena_el:
            ocena = ocena_el.text.replace('\n', '').strip().replace(".", ",")
        else:
            ocena = "not given"

        st_strani_el = soup.find('span', class_="edition-pages")
        if st_strani_el:
            st_strani = st_strani_el.text
        else:
            st_strani = "not given"

        leto_el = soup.find('span', itemprop="datePublished")
        if leto_el:
            leto = leto_el.text.replace('\n', '').strip()[-4:]
        else:
            leto = "not given"

        opis_el = soup.find('div', class_="book-description").p
        if opis_el:
            opis = opis_el.text.replace('\n', '').strip()
        else:
            opis = 'not given'

        seznam_podatkov.append([naslov, avtorji, ocena, st_strani, leto, opis])

        html_filename =  naslov + ' - ' + avtorji + '.html'
        directory = "knjige"
        os.makedirs(directory, exist_ok=True)

        path = os.path.abspath(os.path.join(directory, html_filename))

        with open(path, 'w', encoding='utf-8') as html_file:
            html_file.write(str(soup))
        
        counter += 1
        print(str(counter) + ") added: " + naslov + ' - ' + avtorji)

    path = os.path.abspath('knjige.csv')
    with open(path, 'w', newline='', encoding ='utf8') as f:
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow (['Naslov', 'Avtor', 'Ocena', 'Stevilo strani', 'Leto', 'Opis'])
        csv_writer.writerows(seznam_podatkov)