#!/usr/bin/python3

import ldap3
import argparse
import time
from colorama import Fore, Style, init
from tqdm import tqdm

# Inicializa colorama
init(autoreset=True)

def is_valid_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def main():
    # Arguments
    parser = argparse.ArgumentParser(description="LDAP Connection Script")
    parser.add_argument('-i', '--ip', required=True, help="IP address of the LDAP server")
    parser.add_argument('-p', '--port', required=True, type=int, help="Port of the LDAP server")
    args = parser.parse_args()

    ipLdap = args.ip
    portLdap = args.port

    if not is_valid_ip(ipLdap):
        print(f"\n{Fore.RED}[ERROR] Invalid IP address.\n")
        return

    if not 1 <= portLdap <= 65535:
        print(f"\n{Fore.RED}[ERROR] Invalid port number. It must be between 1 and 65535.\n")
        return

    sslVar = portLdap == 636
    if sslVar:
        print(f"\n{Fore.GREEN}[INFO] Port {portLdap} uses SSL.\n")
    else:
        print(f"\n{Fore.YELLOW}[INFO] Port {portLdap} does not use SSL.\n")

    try:
        server = ldap3.Server(ipLdap, get_info=ldap3.ALL, port=portLdap, use_ssl=sslVar)
        connection = ldap3.Connection(server)

        if connection.bind():
            print(f"\n{Fore.GREEN}[SUCCESS] Connected successfully.\n")
            
            # Progess bar
            for _ in tqdm(range(100), desc="Loading Server Info", ncols=100, bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt}"):
                time.sleep(0.03)
            
            print(server.info)  # Output without colors
        else:
            print(f"\n{Fore.RED}[ERROR] Anonymous connections are not allowed.\n")

    except ldap3.core.exceptions.LDAPException as e:
        print(f"\n{Fore.RED}[ERROR] LDAP connection failed: {e}\n")

if __name__ == "__main__":
    main()
