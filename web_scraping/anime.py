# -*- coding: utf-8 -*-
__author__ = "SirHades696"
__email__ = "djnonasrm@gmail.com"

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json

class Anime_Search:
    def __init__(self):
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
     
    def search_titles(self, anime, page = 1):
        """
        Busca cualquier titulo de anime disponible en la página de AnimeFLV

        Args:
            anime ([string]): Titulo del anime
            page (int, optional): Número de página para realizar la búsqueda. Defaults to 1.

        Returns:
            [dict]: Retorna un dict con los atributos de: Título, URL, Tipo, Valoración y Descripción
        """
        anime = anime.replace(" ", "+")
        url = "https://www3.animeflv.net/browse?q=" + anime + "&page=" + str(page)
        req = Request(url=url, headers = self.__headers) 
        url_open = urlopen(req).read() 
        html = BeautifulSoup(url_open, "html.parser")
        titles = html.find_all("article", {"class": "Anime alt B"})
        
        results = {}
        p = []
        if len(titles) == 0:
            return results, p
        else:
            pages = html.find_all("div", {"class": "NvCnAnm"})
            for page in pages:
                for i in page.find_all('a'):
                    if i.getText() != '«' and i.getText() != '»':
                        p.append(i.getText())
            url_base = r"https://www3.animeflv.net"
            for i, cont in enumerate(titles):
                href = url_base + cont.find('a', href=True).get('href')
                title = cont.find('h3').getText().replace("\"", "")
                type_a = cont.find_next('div', {'class': 'Description'}).getText().split("\n")[2].split(' ')[0]
                ranking = cont.find_next('div', {'class': 'Description'}).getText().split("\n")[2].split(' ')[1]
                desc = cont.find_next('div', {'class': 'Description'}).getText().split("\n")[3].replace("\"", "")
                if desc == "":
                    desc = "Sin descripción"                 
                results[str(i+1)] = {
                    'Title': title,
                    'URL' : href,
                    'Type': type_a,
                    'Ranking' : ranking,
                    'Description': desc
                }
        return results, p
    
    def search_episodes(self, url_title):  
        """Se encarga de buscar los episodios de un anime dado a tráves de su URL

        Args:
            url_title ([string]): URL del anime elegido

        Returns:
            [list]: Lista con los episodios encontrados a tráves de la URL, son retornados en orden ascendente.
        """
        req = Request(url=url_title, headers = self.__headers) 
        url_base = r"https://www3.animeflv.net/ver/"
        url_open = urlopen(req).read() 
        page = BeautifulSoup(url_open, "lxml")
        scripts = page.find_all('script')

        for script in scripts:
            if "var anime_info" in str(script):
                header1 = json.loads(str(script).split("=")[1].split(";\r\n    ")[0])
            
            if "var episodes" in str(script):
                
                header2 = json.loads(str(script).split("=")[2].split(";")[0])

        results = []
        for i in range(0,len(header2)):
            results.append(url_base + header1[2] + "-" +str(header2[i][0]))

        return results[::-1]
    
    def download_links(self, url_episode):
        """Busca todos los links disponibles del episodio seleccionado

        Args:
            url_episode ([string]): URL del episodio seleccionado.

        Returns:
            [list]: Lista con todos los links encontrados para ese episodio.
        """
        req = Request(url=url_episode, headers = self.__headers) 
        url_open = urlopen(req).read() 
        html = BeautifulSoup(url_open, "html.parser")
        data = html.find_all("a", {"class": "Button Sm fa-download"})
        fmt = html.find_all("table", {"class": "RTbl Dwnl"})
        
        formats = []
        for fm in fmt:
            for txt in fm.find_all('td'):
                if txt.get_text() == "SUB":
                    formats.append(txt.get_text())
                elif txt.get_text() == "LAT":
                    formats.append(txt.get_text())
        
        links = []
        for dat in data:
            links.append(dat.get('href'))
            
        return links, formats  
    
