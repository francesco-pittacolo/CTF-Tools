import requests
import time
from info_from_flagID import *

team_ip = "10.60.64.1" #da modificare in base al team
submitter_ip = "http://10.81.64.9:5000/submit" #scrivere qua ip del submitter
teams = 81 #da modificare in base al numero di team
service = "" # servizio
service_attribute_1 = "" # primo argomento flagID
service_attribute_2 = "" # secondo argomento flagID

#scrivere l'exploit qua, ritorna singola flag. arg1 e arg2 sono i valori recuperati da flagID, nomi modificabili 
def exploit(ip, arg1, arg2):
    flag = ""
    #exploit qua
    
    return flag

#per mandare attacco, modificare solo service, service_attribute_1 e service_attribute_2
def send_attack(ip, team_id):
    print(f"Attacco in corso a {ip}\n")
    #position = 3 #posizione per ottenere round specifico (da 0 a 3), opzionale
    results = get_info(team_id, service, service_attribute_1, service_attribute_2) #per tutti i round in flagID, ritorna una lista di dizionari
    #results = get_info_specific_round(team_id, service, service_attribute_1, service_attribute_2, position) #per avere un round specifico
    print(results) # debug opzionale

    for i in range(0, 4):
        if not results[i]: # check se è vuoto
            continue

        arg1 = results[i][service_attribute_1]
        arg2 = results[i][service_attribute_2]

        flag = exploit(ip, arg1, arg2)
        #save = save_flag(flag) #per eventuale salvataggio in locale della flag
        data = {'flag': flag}
        response = requests.post(submitter_ip, data=data)

        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

    return

#funzione per salvare le flag su un file, ma non serve più
def save_flag(flag):
    try:
        with open("CTF-Tools/flags.txt", "a") as f:
            f.write(flag + "\n")
        print(f"Flag salvata: {flag}\n")
        return 1
    except Exception as e:
        print(f"[!] Errore durante il salvataggio della flag: {e}\n")
        return 0

if __name__ == "__main__":
    while True:
        flags_found = 0
        for i in range(teams):
            ip = f"10.60.{i}.1"
            if ip == team_ip:
                continue
            try:
                print(f"Inizio attacco a {ip}")
                flag = send_attack(ip, i)
                if flag:  # Se è stata trovata una flag
                    flags_found += 1
            except Exception as e:
                print(f"[!] Errore durante l'attacco a {ip}: {e}")

        print(f"Giro completato. Trovate {flags_found} flag. Aspetto 120 secondi per il prossimo attacco...\n")
        time.sleep(120) #da modificare a seconda delle necessità
