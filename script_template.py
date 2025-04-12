from pwn import *
import requests
import json

def get_info(team_id, service, info1, info2):
    infos = []
    url = f"http://10.10.0.1:8081/flagIds?service={service}&team={team_id}"
    #info3 = "" #per altre eventuali
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            data = r.json()
            # Navigate into the nested structure
        if service not in data:
            print(f"[!] Servizio '{service}' non trovato in {url}")
            return infos

        team_data = data[service].get(str(team_id), {})
        if not team_data:
            print(f"[!] Nessun dato per il team {team_id} in {url}")
            return infos

        for round_num, entry in team_data.items():
        # Qui si usa 'round_num' come numero del round
            if entry and info1 in entry and info2 in entry:
                infos.append({
                    "round": round_num,  # usa la chiave come numero del round
                    "team": team_id,
                    info1: entry[info1],
                    info2: entry[info2]
                })
            else:
                print(f"[!] Entry senza {info1} o {info2}: {entry}")

    except Exception as e:
        print(f"[!] Error on round {round_num}: {e}")
    return infos

def get_info_specific_round(team_id, service, info1, info2):
    infos = []
    url = f"http://10.10.0.1:8081/flagIds?service={service}&team={team_id}"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            data = r.json()
            # Navigate into the nested structure
        if service not in data:
            print(f"[!] Servizio '{service}' non trovato in {url}")
            return infos

        team_data = data[service].get(str(team_id), {})
        if not team_data:
            print(f"[!] Nessun dato per il team {team_id} in {url}")
            return infos

        # Ordinare i round in ordine crescente (utilizzando le chiavi)
        sorted_rounds = sorted(team_data.keys(), key=int)

    # Se ci sono almeno due round, prendiamo il penultimo
        if len(sorted_rounds) >= 2:
            penultimate_round = sorted_rounds[-2]
            entry = team_data[penultimate_round]
            
            if entry and info1 in entry and info2 in entry:
                infos.append({
                    "round": penultimate_round,
                    "team": team_id,
                    info1: entry[info1],
                    info2: entry[info2]
                })
            else:
                print(f"[!] Entry senza {info1} o {2} per il penultimo round {penultimate_round}")

    except Exception as e:
        print(f"[!] Error on round {penultimate_round}: {e}")
    return infos

def exploit(ip, info1, info2):
    flag = ""
    #exploit qua
    
    return flag

# Example usage
if __name__ == "__main__":
    team_id = 0 #esempio di attacco
    results = get_info(team_id)
    print(results)
