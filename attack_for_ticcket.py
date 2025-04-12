import requests
import time
from script_ticket import *


def send_attack(ip, team_id):
    flags = []
    for round in range(round_inf,round_inf+5):
        print(f"Attacco in corso a {ip}\n")  # per debug
        results = get_info(team_id, round)
        print(results)
        ctf_id = results[0]["ctf_id"] if results else None
        ticket_id = results[0]["ticket_id"] if results else None
        flag = exploit(ip, ctf_id, ticket_id)
        result = save_flag(flag)
    #flag = str(ip)
    return result


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
    team_ip = "10.60.64.1"
    teams = 81 #da modificare in base al numero di team
    round_inf = 0 #scrivere qua round minore
    while True:
        flags_found = 0
        for i in range(teams):
            ip = f"10.60.{i}.1"
            if ip == team_ip:
                continue
            try:
                print(f"Inizio attacco a {ip}")
                flag = send_attack(ip, i, round_inf)
                if flag:  # Se è stata trovata una flag
                    save_flag(flag)  # Scrive la flag nel file
                    flags_found += 1
            except Exception as e:
                print(f"[!] Errore durante l'attacco a {ip}: {e}")

        # Aggiungi una riga vuota per separare i round
        with open("CTF-Tools/flags.txt", "a") as f:
            f.write("\n\n")

        print(f"Giro completato. Trovate {flags_found} flag. Aspetto 120 secondi per il prossimo attacco...\n")
        time.sleep(120)
        round_inf += 1
