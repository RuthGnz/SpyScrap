#!/usr/bin/python
# coding: utf-8
# encoding=utf8
import sys
import datetime
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import os
from parsel import Selector
import urllib.parse
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.chrome.options import Options
import shutil
import requests
from io import BytesIO
import xml.etree.ElementTree as ET

def boe (text_to_search,initDate,outDate,pages,exact,verbose):
    if exact:
        text_to_search='"'+text_to_search+'"'
    pages=int(pages)
    chrome_options = Options()
    jsonData=[]
    chrome_options.add_argument("--headless")
    if initDate!=None and outDate!=None:
        url = 'https://www.boe.es/buscar/boe.php?campo%5B0%5D=ORI&dato%5B0%5D%5B1%5D=1&dato%5B0%5D%5B2%5D=2&dato%5B0%5D%5B3%5D=3&dato%5B0%5D%5B4%5D=4&dato%5B0%5D%5B5%5D=5&dato%5B0%5D%5BT%5D=T&operador%5B0%5D=and&campo%5B1%5D=TIT&dato%5B1%5D=&operador%5B1%5D=and&campo%5B2%5D=DEM&dato%5B2%5D=&operador%5B2%5D=and&campo%5B3%5D=DOC&dato%5B3%5D='+text_to_search+'&operador%5B3%5D=and&campo%5B4%5D=NBO&dato%5B4%5D=&operador%5B4%5D=and&campo%5B5%5D=NOF&dato%5B5%5D=&operador%5B5%5D=and&operador%5B6%5D=and&campo%5B6%5D=FPU&dato%5B6%5D%5B0%5D='+initDate+'&dato%5B6%5D%5B1%5D='+outDate+'&page_hits=50&sort_field%5B0%5D=fpu&sort_order%5B0%5D=desc&sort_field%5B1%5D=ori&sort_order%5B1%5D=asc&sort_field%5B2%5D=ref&sort_order%5B2%5D=asc&accion=Buscar'
    else:
        url ='https://www.boe.es/buscar/boe.php?campo%5B0%5D=ORI&dato%5B0%5D%5B1%5D=1&dato%5B0%5D%5B2%5D=2&dato%5B0%5D%5B3%5D=3&dato%5B0%5D%5B4%5D=4&dato%5B0%5D%5B5%5D=5&dato%5B0%5D%5BT%5D=T&operador%5B0%5D=and&campo%5B1%5D=TIT&dato%5B1%5D=&operador%5B1%5D=and&campo%5B2%5D=DEM&dato%5B2%5D=&operador%5B2%5D=and&campo%5B3%5D=DOC&dato%5B3%5D='+text_to_search+'&operador%5B3%5D=and&campo%5B4%5D=NBO&dato%5B4%5D=&operador%5B4%5D=and&campo%5B5%5D=NOF&dato%5B5%5D=&operador%5B5%5D=and&operador%5B6%5D=and&campo%5B6%5D=FPU&dato%5B6%5D%5B0%5D=&dato%5B6%5D%5B1%5D=&page_hits=50&sort_field%5B0%5D=fpu&sort_order%5B0%5D=desc&sort_field%5B1%5D=ori&sort_order%5B1%5D=asc&sort_field%5B2%5D=ref&sort_order%5B2%5D=asc&accion=Buscar'

    chrome_path = './chromedriver'
    driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

    driver.get(url)
    driver.implicitly_wait(20)
    links=[]
    for page in range(pages):
        elements=driver.find_elements_by_tag_name('li')
        for link in elements:
            li=link.get_attribute('class')
            if li=='resultado-busqueda':
                date=link.find_elements_by_tag_name('h4')[0].get_attribute('innerHTML').split(' ')[3]
                a=link.find_elements_by_tag_name('a')
                for i in a:
                    cl=i.get_attribute('class')
                    if cl=='resultado-busqueda-link-defecto':
                        href=i.get_attribute('href')
                        href=href.split('=')[1]
                        newUrl='https://www.boe.es/diario_boe/xml.php?id='+href
                        links.append(newUrl)
        nextPage=driver.find_elements_by_class_name('pagSig')
        if len(nextPage) == 0:
            break
        else:
            nextPage=nextPage[0]
            nextPageLink= nextPage.find_element_by_xpath('..').get_attribute('href')
            driver.get(nextPageLink)

    driver.quit()
    boe_data=[]
    for url in links:
        boe={}
        boe['url']=url
        remoteFile = urllib.request.urlopen(url).read()
        memoryFile = BytesIO(remoteFile)
        tree = ET.parse(memoryFile)
        root = tree.getroot()
        text=root.find('texto')
        tables=text.findall('table')
        results=[]
        for table in tables:
            is_important=False
            headings=[]
            content=[]
            thead=table.find('thead')
            if thead!=None:
                tr=thead.find('tr')
                th=tr.findall('th')
                if len(th)>0:
                    for t in th:
                        if t!=None:
                            data=t.text
                            if data!=None:
                                headings.append(data)
                                if 'nombre' in data.lower() or 'apellido' in data.lower() or 'dni' in data.lower() or 'd.n.i' in data.lower() or 'nif' in data.lower():
                                    is_important=True
                else:
                    td=tr.findall('td')
                    for t in td:
                        p=t.find('p')
                        if p!=None:
                            data=p.text
                            headings.append(data)
                            if 'nombre' in data.lower() or 'apellido' in data.lower() or 'dni' in data.lower() or 'd.n.i' in data.lower() or 'nif' in data.lower():
                                is_important=True
            else:
                tr=table.findall('tr')
                for i,tri in enumerate(tr):
                    td=tri.findall('td')
                    for tdi in td:
                        p=tdi.findall('p')
                        heading=""
                        for pi in p:
                            if pi.get('class')!=None:
                                if 'cabeza_tabla' in pi.get('class') :
                                    heading=heading+pi.text
                                    if 'nombre' in heading.lower() or 'apellido' in heading.lower() or 'dni' in heading.lower() or 'd.n.i' in heading.lower() or 'nif' in heading.lower():
                                        is_important=True
                            else:
                                if pi.text != None:
                                    data=pi.text
                                    if 'nombre' in data.lower() or 'apellido' in data.lower() or 'dni' in data.lower() or 'd.n.i' in data.lower() or 'nif' in data.lower():
                                        heading=heading+pi.text
                                        is_important=True
                                if i==2:
                                    break
                        if 'ANEXO' not in heading:
                            headings.append(heading)




            if is_important:
                tbody=table.find('tbody')
                if tbody!=None:
                    tr=tbody.findall('tr')
                else:
                    tr=table.findall('tr')
                for t in tr:
                    td=t.findall('td')

                    dataTable={}
                    for i,tdi in enumerate(td):
                        info=''
                        if tdi.text.strip()==None or tdi.text.strip()=="":
                            p=tdi.find('p')
                            if p!=None:
                                info=p.text
                        else:
                            info=tdi.text
                        if i>len(headings)-1:
                            dataTable[i]=info
                        else:
                            dataTable[headings[i]]=info
                    content.append(dataTable)
                results.append({'table':content,'headings':headings})

        boe['datatables']=results

        texto=[]
        if len(results)==0:
            p=text.findall('p')
            is_important_line=len(p)
            for i,pi in enumerate(p):
                if pi.text != None:
                    data=pi.text
                    if 'nombre' in data.lower() or 'apellido' in data.lower() or 'dni' in data.lower() or 'd.n.i' in data.lower() or 'nif' in data.lower():
                        is_important_line=i
                    if is_important_line<=i:
                        texto.append(pi.text)
            #try to search the text
        boe['texto']=texto
        boe_data.append(boe)



    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.isdir("data/boe"):
        os.mkdir( "data/boe" );
    path=os.path.join('data/boe',str(now) + '_boe_data.json')
    with open(path, 'w+') as outfile:
        json.dump(boe_data, outfile)
    if verbose:
        for i in boe_data:
            print(i["url"])
            print("--------------------")
            if i["datatables"]:
                print(i["datatables"])
            if i["texto"]:
                print(i["texto"])
    print("Results BOE in: " + str(path))
    response={'results':str(path)}
    return response