
import os
import asyncio
import aiohttp
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import hashlib
import uuid
import json

# ===== Colors =====
w = "\033[1;00m"
g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
b = "\033[1;34m"
reset = "\033[0m"

# ===== Configuration =====
FIXED_URL = "https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=984a6b458027&gw_sn=H1T078800132C&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.142&mac=ca:51:aa:ff:b8:51&slot_num=33&nasip=192.168.1.161&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C016&chap_challenge=%5C135%5C061%5C367%5C376%5C225%5C324%5C217%5C041%5C213%5C145%5C002%5C251%5C074%5C104%5C267%5C152"
GITHUB_RAW_KEY_URL = "https://raw.githubusercontent.com/pdar6400-prog/fox/main/keys.txt"
LOCAL_DATA_FILE = ".data.json"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def Line():
    try:
        print(f"{y}-\033[1;00m" * os.get_terminal_size().columns)
    except:
        print(f"{y}-{w}" * 40)

def get_unique_id():
    data = {}
    if os.path.exists(LOCAL_DATA_FILE):
        try:
            with open(LOCAL_DATA_FILE, "r") as f:
                data = json.load(f)
        except: pass
    
    if "vip_id" not in data:
        short_id = str(uuid.uuid4().int)[:6]
        data["vip_id"] = f"VIP-{short_id}"
        with open(LOCAL_DATA_FILE, "w") as f:
            json.dump(data, f)
    return data["vip_id"]

def Logo():
    clear()
    vip_id = get_unique_id()
    # User requested Logo style (VIP)
    logo = f"""{b}
  ______   ________  ______   _______  
 /      \\ /        |/      \\ /       \\ 
/$$$$$$  |$$$$$$$$//$$$$$$  |$$$$$$$  |
$$ \\__$$/    $$ |  $$ |__$$ |$$ |__$$ |
$$      \\    $$ |  $$    $$ |$$    $$< 
 $$$$$$  |   $$ |  $$$$$$$$ |$$$$$$$  |
/  \\__$$ |   $$ |  $$ |  $$ |$$ |  $$ |
$$    $$/    $$ |  $$ |  $$ |$$ |  $$ |
 $$$$$$/     $$/   $$/   $$/ $$/   $$/ {w}
"""
    print(logo)
    Line()
    print(f"{w}[*] This tool is only for Ruijie Network Router")
    print(f"{b}[+] YOUR ID : {g}{vip_id}")
    print(f"{g}[*] VIP MEMBER Access")
    print(f"{g}[*] Telegram: @naymin126653 & @Leearma6")
    print(f"{g}[*] Channel: https://t.me/starlinkcodebypass")
    Line()

async def fetch_keys_from_github():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GITHUB_RAW_KEY_URL) as response:
                if response.status == 200:
                    keys_content = await response.text()
                    keys = [k.strip() for k in keys_content.split("\n") if k.strip()]
                    data = {}
                    if os.path.exists(LOCAL_DATA_FILE):
                        with open(LOCAL_DATA_FILE, "r") as f:
                            data = json.load(f)
                    data["valid_keys"] = keys
                    with open(LOCAL_DATA_FILE, "w") as f:
                        json.dump(data, f)
                    return True
    except: pass
    return False

def check_key_validity(user_key):
    if not os.path.exists(LOCAL_DATA_FILE): return False
    try:
        with open(LOCAL_DATA_FILE, "r") as f:
            data = json.load(f)
            return user_key in data.get("valid_keys", [])
    except: return False

async def auto_detect_network():
    print(f"{b}[*] Detecting network parameters...{reset}")
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    headers = {"User-Agent": "Mozilla/5.0 (Android 14) AppleWebKit/537.36"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(test_url, headers=headers, timeout=5, allow_redirects=False) as resp:
                if resp.status in (301, 302):
                    location = resp.headers.get("Location", "")
                    params = parse_qs(urlparse(location).query)
                    gw = params.get("gw_address") or params.get("nasip")
                    mac = params.get("mac") or params.get("umac")
                    return (gw[0] if gw else None, mac[0] if mac else None)
        except: pass
    return None, None

def open_portal(gw_ip, mac_addr):
    parsed = urlparse(FIXED_URL)
    params = parse_qs(parsed.query)
    if mac_addr: params["mac"] = [mac_addr]
    if gw_ip: 
        params["gw_address"] = [gw_ip]
        params["nasip"] = [gw_ip]
    new_query = urlencode({k: v[0] for k, v in params.items()})
    final_url = urlunparse(parsed._replace(query=new_query))
    try:
        os.system(f"xdg-open \"{final_url}\"")
        print(f"\n{g}[+] Opening portal... Done!{reset}")
    except: print(f"{r}[!] Failed to open browser.{reset}")

async def main():
    Logo()
    print(f"{b}[*] Checking for updates...{reset}")
    await fetch_keys_from_github()
    
    while True:
        user_key = input(f"{g}[?] Enter VIP Key: {reset}").strip()
        if not user_key:
            print(f"{y}[!] Please type your key before pressing Enter.{reset}")
            continue
        
        if check_key_validity(user_key):
            print(f"{g}[+] Key Valid!{reset}")
            break
        else:
            # Try updating from GitHub one more time
            print(f"{b}[*] Verifying with server...{reset}")
            if await fetch_keys_from_github():
                if check_key_validity(user_key):
                    print(f"{g}[+] Key Valid (Updated from Server)!{reset}")
                    break
            print(f"{r}[!] Invalid or Expired Key: '{user_key}'{reset}")
            print(f"{y}[*] Please check your key on GitHub: pdar6400-prog/fox{reset}")

    gw_ip, mac_addr = await auto_detect_network()
    if not gw_ip or not mac_addr:
        print(f"{y}[!] Detection failed. Manual entry required.{reset}")
        mac_addr = input(f"{g}[?] Enter MAC: {reset}").strip() or mac_addr
        gw_ip = input(f"{g}[?] Enter Gateway IP: {reset}").strip() or gw_ip
    
    if mac_addr and gw_ip:
        open_portal(gw_ip, mac_addr)
    else: print(f"{r}[!] Error: Missing parameters.{reset}")
    input(f"\n{reset}Press Enter to exit...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt: print("\n[!] Stopped.")
