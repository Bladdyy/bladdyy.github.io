from bs4 import BeautifulSoup
import requests
from googlesearch import search


def create_subsite(name):
    if name == "Body Count":
        tempname = "Body Count (band)"
    else:
        tempname = name
    plus = tempname.replace(' ', '_')
    response = requests.get('https://en.wikipedia.org/wiki/' + plus)
    soup = BeautifulSoup(response.content, 'html.parser')
    photo = soup.findAll('img')[3].get('src')
    if name == "Metallica":
        photo = soup.findAll('img')[5].get('src')
    if photo == "//upload.wikimedia.org/wikipedia/en/thumb/9/94/Symbol_support_vote.svg/19px-Symbol_support_vote.svg.png":
        photo = soup.findAll('img')[4].get('src')
    if photo == "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png":
        photo = soup.findAll('img')[5].get('src')
    if photo == "//upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/20px-Cscr-featured.svg.png":
        photo = soup.findAll('img')[4].get('src')
    info = []
    for url in search(name + " band", stop=2):
        info.append(url)
    with open(name + ".md", "w", encoding="utf-8") as file:
        file.write("## " + name + "\n")
        file.write("#### Additional informations:\n")
        for url in info:
            file.write("[" + url +"](" + url + ")\n\n")
        file.write("#### Photo of the " + name + ":\n")
        file.write("![" + name + " photo](https:" + photo + ")\n")


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
