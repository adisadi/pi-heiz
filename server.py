#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import configparser
import datetime
import saia
import jsonstore
import os
import json


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        if self.path=="/":
            dataArray=jsonstore.load_json(os.path.join(basePath,'data.json'))
            data= dataArray[jsonstore.JSONROOT][-1:][0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            fin = open("index.html", encoding="utf-8")
            contents = fin.read()
            output = contents.format(**data)

            self.wfile.write(bytes(output, "utf-8"))
        elif self.path == '/data.json':
            dataArray=jsonstore.load_json(os.path.join(basePath,'data.json'))
            data=dataArray[jsonstore.JSONROOT]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(bytes(json.dumps(dataArray[jsonstore.JSONROOT]),"utf-8"))
        elif self.path=="/chart":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            fin = open("chart.html", encoding="utf-8")
            self.wfile.write(bytes(fin.read(), "utf-8"))

        else :
            self.send_error(404, "File Not Found {}".format(self.path))


serverPort = 8080

basePath = os.environ.get('PIHEIZ')
basePath= basePath if basePath is not None else os.getcwd() 

with HTTPServer(("", serverPort), MyServer) as httpd:
    print("serving at port", serverPort)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")
