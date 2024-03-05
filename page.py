from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS


def create_subsite(name):
    info = DDGS().text(name + " band", region='wt-wt', safesearch='off', timelimit='y', max_results=3)
    photo = DDGS().images(
        keywords=name + " band",
        region="wt-wt",
        safesearch="off",
        size=None,
        color="Monochrome",
        type_image=None,
        layout=None,
        license_image=None,
        max_results=1
    )
    with open(name + ".md", "w", encoding="utf-8") as file:
        file.write("## " + name + "\n")
        file.write("#### Additional informations:\n")
        for temp in info:
            file.write("[" + temp['title'] +"](" + temp['href'] + ")\n\n")
        file.write("#### Photo of the " + name + ":\n")
        file.write("![" + name + " photo](" + photo[0]['image'] + ")\n")


def main_site():
    response = requests.get('https://pl.wikipedia.org/wiki/Nagroda_Grammy_w_kategorii_Best_Metal_Performance')
    soup = BeautifulSoup(response.content, 'html.parser')

    sentence = soup.find('p').text

    table = soup.select('table')[0]
    rows = table.findAll('td')[:93]
    cols = table.findAll('th')

    if len(cols) > 0:
        distinct_bands = set()
        for i in range(int(len(rows) / len(cols))):
            band = rows[1 + len(cols) * i].text
            if band[-1] == "\n":
                band = band[:-1]
            distinct_bands.add(band)
        for band in distinct_bands:
            create_subsite(band)
        colstring = "|"
        for i in range(len(cols)):
            msg = cols[i].text
            if msg[-1] == "\n":
                msg = msg[:-1]
            colstring = colstring + msg + " | "
        colstring = colstring + "\n|"
        for i in range(len(cols)):
            colstring = colstring + "---|"
        for i in range(len(rows)):
            if i % len(cols) == 0:
                colstring = colstring + "\n| " + rows[i].text[0:4] + " | "
            else:
                msg = rows[i].text
                if msg[-1] == '\n':
                    msg = msg[:-1]
                if i % len(cols) == 1:
                    colstring = colstring + "[" + msg + "](" + msg + ".md) | "
                else:
                    colstring = colstring + msg + " | "
        with open("index.md", "w", encoding='utf-8') as file:
            file.write("# Nagrody Grammy dla zespolów grajacych muzyke metalowa.\n")
            file.write(sentence + "\n")
            file.write("### Zdobywcy Grammy:\n")
            file.write(colstring)

main_site()