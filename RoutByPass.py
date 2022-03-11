
from inspect import trace
from operator import index
import requests, time, signal, sys
import contextlib

attmp = 1
avrouters = 0
dsrouters = 0
target = input("Please enter the Target or Targets: ")

if int(target[10]) == 0:
    index = list(target)
    index[10] =""
    target = "".join(index)
    limit = int(input("introduzca la cantidad de ip a escanear (0 - 255): "))
else:
    attmp = int(target[10])
    limit = attmp
    
print("\n Scaning...\n")
time.sleep(2)
validip = []

while attmp <= limit:   
    if  limit == attmp: 
        ip = target
    else:
        ip = target + str(attmp)    
    attmp = attmp + 1
    url = 'http://' + ip + '/'
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        if r.status_code == 200:
            avrouters += 1
            validip.append(url)
            print('[+] Login for Web Admin Panel Found on '+ url,'[+] status code : ',r.status_code)
    except Exception:
        dsrouters += 1
        print('[+] Login for Web Admin Panel Not Found on '+ url,'[-] status not found')
time.sleep(1)

su_name = input("\nIntroduzca un nombre para el archivo de reporte: ")
print("Printing scan results.. \n")
time.sleep(3)

file_path = su_name + '.txt'
with open(file_path, "w") as o:
    with contextlib.redirect_stdout(o):
        print("Valid IP: ", validip)
        print('Hosts Avaliable: ',avrouters)  
        print('Hosts not found: ', dsrouters) 

print('Hosts Avaliable: ',avrouters)  
print('Hosts not found: ', dsrouters)  

        

