from bs4 import BeautifulSoup
import requests
import csv
from csv import writer
import os

try:
    for i in range(1):
        vir = requests.get('https://openlibrary.org/trending/daily?page=' + str(i + 1))
        vir.raise_for_status()

        soup = BeautifulSoup(vir.text, 'html.parser')
        
        knjige = soup.find('ul', class_="list-books").find_all("li")

        seznam_podatkov = []

        for knjiga in knjige:
            url = knjiga.find("a", class_="results")["href"]

            vir = requests.get("https://openlibrary.org" + url)
            vir.raise_for_status()

            soup = BeautifulSoup(vir.text, 'html.parser')

            naslov = soup.find("h1", class_="work-title").text.replace('\n', '').strip()
            print(naslov)

            avtorji_neloceno = soup.find("h2", class_="edition-byline").text.replace('\n', '')
                
            def nov_avtorji(niz, za_odstranit, za_menjat, nova_stvar):
                nov_niz = niz.replace(za_odstranit,"").replace(za_menjat, nova_stvar)
                return nov_niz
                
            avtorji = nov_avtorji(avtorji_neloceno, 'by ', ' and', ',').strip()

            ocena = soup.find('li', class_="avg-ratings").find('span', itemprop="ratingValue").text.replace('\n', '').strip().replace(".", ",")

            st_strani_el = soup.find('span', class_="edition-pages")
            if st_strani_el:
                st_strani = st_strani_el.text
            else:
                st_strani = "not given"
            print(st_strani)

            leto = soup.find('span', itemprop="datePublished").text.replace('\n', '').strip()[-4:]

            def nov_datum(niz):
                if ',' in niz:
                    niz_seznam = niz.split(',')
                    if len(niz_seznam) > 1:
                        return niz_seznam[1]
                else:
                    return niz
                
            opis = soup.find('div', class_="book-description").p.text.replace('\n', '').strip()

            seznam_podatkov.append([naslov, avtorji, ocena, leto, opis])

            html_filename =  naslov + ' - ' + avtorji + '.html'
            directory = "knjige"
            os.makedirs(directory, exist_ok=True)
            path = os.path.abspath(os.path.join(directory, html_filename))

            with open(path, 'w', encoding='utf-8') as html_file:
                html_file.write(str(soup))

        path = os.path.abspath('knjige.csv')
        with open(path, 'w', newline='', encoding ='utf8') as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow (['Naslov', 'Avtor', 'Ocena', 'Leto', 'Opis'])
            csv_writer.writerows(seznam_podatkov)
except Exception as e:
    print(e)