
import requests 

avrouters = 0
dsrouters = 0
attmp = 1
while attmp != 50:
    targets = '192.168.3.'+ str(attmp)
    attmp = attmp + 1
    url = 'http://' + targets + '/'
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        if r.status_code == 200:
            avrouters += 1
            print('Is running a Host on '+ url,'[+] status code : ',r.status_code)
    except Exception:
        dsrouters += 1
        print('Is not running a Host on '+ url,'[-] status not found')
print('Routers Avaliable: ',avrouters)  
print('Routers not found: ', dsrouters)  

        
