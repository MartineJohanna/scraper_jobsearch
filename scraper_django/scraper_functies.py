# functies voor de scraper
def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")

# titel van de functie
def zoek_titel(div):
    titel = div.find(attrs={'class':'title'})
    if titel is not None:
        return titel.get_text()

# bedrijf van de vacature    
def zoek_bedrijf(div):
    bedrijf = div.find('span', attrs={'class':'company'})
    if bedrijf is not None:
        return bedrijf.get_text()
    else: 
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        return sec_try.get_text()

# locatie van de vacature
def zoek_locatie(div):
    locatie = div.find(attrs={'class':'location accessible-contrast-color-location'})
    if locatie is not None:
        return locatie.get_text()

# link naar de vacature
def zoek_link(div):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return a['href']

# text van de vacature 
def zoek_alles(html):
    spans = soup.findAll('div', attrs={'class': "jobsearch-jobDescriptionText"})
    for span in spans:
        return span.text.strip()
