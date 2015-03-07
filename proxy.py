#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import socket
import urllib

cache = {}


class miServidor (webapp.webApp):
    def parse(self, request):
        url = request.split()[1][1:].split('/')[0]
        try:
            peticion = request.split()[1][1:].split('/')[1]
        except IndexError:
            peticion = None
        cabeceras = request.split('\r\n', 1)[1]

        return (url, cabeceras, peticion)

    def process(self, parsedRequest):
        miurl = "http://" + socket.gethostname() + ":1234/" + parsedRequest[0]
        url = "http://" + parsedRequest[0]
        urlshtml = ("<a href= '" + url + "'>Pagina original</a></br>" +
                   "<a href= '" + miurl + "'>Recargar</a></br>" +
                   "<a href= '" + miurl + "/cache'>Cache</a></br>" +
                   "<a href= '" + miurl + "/cabeceras1'>Cabeceras 1</a></br>" +
                   "<a href= '" + miurl + "/cabeceras2'>Cabeceras 2</a></br>" +
                   "<a href= '" + miurl + "/cabeceras3'>Cabeceras 3</a></br>" +
                   "<a href= '" + miurl + "/cabeceras4'>Cabeceras 4</a></br>")

        try:
            f = urllib.urlopen(url)
        except IOError:
            html = ("<html><body><p>Pagina no encontrada</p></html></body>")
            return ("400 Not Found", hmtl)

        if parsedRequest[2] == "cabeceras1":
            html = ("<html><body>" + urlshtml +
                    "<p>Cabeceras recibidas del navegador:</p>" +
                    parsedRequest[1] + "</html></body>")
        elif parsedRequest[2] == "cabeceras2":
            html = ("<html><body>" + urlshtml +
                    "<p>Cabeceras enviadas al servidor " + url + ":</p>" +
                    "</html></body>")
        elif parsedRequest[2] == "cabeceras3":
            cabecera3 = f.info()
            print cabecera3
            html = ("<html><body>" + urlshtml +
                    "<p>Cabeceras recibidas del servidor " + url + ":</p>" +
                    str(cabecera3) + "</html></body>")
        elif parsedRequest[2] == "cabeceras4":
            html = ("<html><body>" + urlshtml +
                    "<p>No se envian cabeceras al navegador:" +
                    "</p></html></body>")
        elif parsedRequest[2] == "cache":
            try:
                html = cache[url]
            except KeyError:
                html = ("<html><body><p>Pagina no encontrada</p>" +
                        "</html></body>")
                return ("400 Not Found", hmtl)
        else:
            f = urllib.urlopen(url)
            html = f.read()
            cache[url] = html
            posicion = html.find('<body')
            posicion = html.find('>', posicion)
            html = (html[:posicion + 1] + urlshtml +
                    "</br></br>" + html[(posicion + 1):])

        return ("200 OK", html)


if __name__ == "__main__":
    serv = miServidor(socket.gethostname(), 1234)
