#!/usr/bin/env python3
"""
Enhanced Netcat: Encrypted, Multi-client, Cross-platform Netcat Clone

Features:
- TCP/UDP client & server (multi-client with threads)
- AES-256-CBC encrypted communication (pycryptodome)
- Interactive remote shell (with TTY support on Linux)
- File upload/download
- Cross-platform (Linux, Windows, macOS)
- Netcat-like CLI flags
- Graceful error handling
- Extensible, readable code

Author: Your Name
"""

import socket
import threading
import argparse
import sys
import os
import struct
import subprocess
import platform
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# --- ANSI COLOR CODES (Dark Royal Blue Theme) ---
DARK_ROYAL_BLUE = '\033[38;5;18m'    # Dark royal blue (primary)
ROYAL_BLUE = '\033[38;5;19m'         # Royal blue
BRIGHT_ROYAL = '\033[38;5;20m'       # Bright royal blue
LIGHT_ROYAL = '\033[38;5;27m'        # Light royal blue
YELLOW = '\033[38;5;226m'            # Yellow for highlights
GREEN = '\033[38;5;46m'              # Green for success
RED = '\033[38;5;196m'               # Red for warnings
BOLD = '\033[1m'
RESET = '\033[0m'

# --- 3D ASCII LOGO WITH USAGE ---
LOGO = f"""{DARK_ROYAL_BLUE}{BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   {DARK_ROYAL_BLUE}███████╗███╗   ██╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗{RESET}{DARK_ROYAL_BLUE}    ║
║   {DARK_ROYAL_BLUE}██╔════╝████╗  ██║██║  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗{RESET}{DARK_ROYAL_BLUE}   ║
║   {DARK_ROYAL_BLUE}█████╗  ██╔██╗ ██║███████║███████║██╔██╗ ██║██║     █████╗  ██║  ██║{RESET}{DARK_ROYAL_BLUE}   ║
║   {DARK_ROYAL_BLUE}██╔══╝  ██║╚██╗██║██╔══██║██╔══██║██║╚██╗██║██║     ██╔══╝  ██║  ██║{RESET}{DARK_ROYAL_BLUE}   ║
║   {DARK_ROYAL_BLUE}███████╗██║ ╚████║██║  ██║██║  ██║██║ ╚████║╚██████╗███████╗██████╔╝{RESET}{DARK_ROYAL_BLUE}   ║
║   {DARK_ROYAL_BLUE}╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝{RESET}{DARK_ROYAL_BLUE}    ║
║                                                                              ║
║        {DARK_ROYAL_BLUE}███╗   ██╗███████╗████████╗ ██████╗  █████╗ ████████╗{RESET}{DARK_ROYAL_BLUE}           ║
║        {DARK_ROYAL_BLUE}████╗  ██║██╔════╝╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝{RESET}{DARK_ROYAL_BLUE}           ║
║        {DARK_ROYAL_BLUE}██╔██╗ ██║█████╗     ██║   ██║      ███████║   ██║{RESET}{DARK_ROYAL_BLUE}              ║
║        {DARK_ROYAL_BLUE}██║╚██╗██║██╔══╝     ██║   ██║      ██╔══██║   ██║{RESET}{DARK_ROYAL_BLUE}              ║
║        {DARK_ROYAL_BLUE}██║ ╚████║███████╗   ██║   ╚██████╗ ██║  ██║   ██║{RESET}{DARK_ROYAL_BLUE}              ║
║        {DARK_ROYAL_BLUE}╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝{RESET}{DARK_ROYAL_BLUE}              ║
║                                                                              ║
║  {YELLOW}🔐 AES-256-CBC Encrypted{RESET} {GREEN}│{RESET} {YELLOW}🌐 Multi-Client Support{RESET} {GREEN}│{RESET} {YELLOW}💻 Cross-Platform{RESET}{DARK_ROYAL_BLUE}    ║
║  {RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}{DARK_ROYAL_BLUE}  ║
╚══════════════════════════════════════════════════════════════════════════════╝
{RESET}
{BRIGHT_ROYAL}┌─────────────────────── QUICK START COMMANDS ────────────────────────┐{RESET}
{LIGHT_ROYAL}│                                                                      │{RESET}
{LIGHT_ROYAL}│  {BOLD}SERVER MODE (Listen):{RESET}                                            {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│    {GREEN}▸{RESET} python enhanced_netcat.py {YELLOW}-l -p 4444{RESET}                       {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│                                                                      │{RESET}
{LIGHT_ROYAL}│  {BOLD}CLIENT MODE (Connect + Shell):{RESET}                                   {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│    {GREEN}▸{RESET} python enhanced_netcat.py {YELLOW}-t 192.168.1.10 -p 4444 --shell{RESET} {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│                                                                      │{RESET}
{LIGHT_ROYAL}│  {BOLD}FILE UPLOAD:{RESET}                                                     {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│    {GREEN}▸{RESET} python enhanced_netcat.py {YELLOW}-t IP -p PORT --upload file.txt{RESET}  {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│                                                                      │{RESET}
{LIGHT_ROYAL}│  {BOLD}FILE DOWNLOAD:{RESET}                                                   {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│    {GREEN}▸{RESET} python enhanced_netcat.py {YELLOW}-t IP -p PORT --download data.pdf{RESET} {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│                                                                      │{RESET}
{LIGHT_ROYAL}│  {BOLD}GET FULL HELP:{RESET}                                                   {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│    {GREEN}▸{RESET} python enhanced_netcat.py {YELLOW}--help{RESET}                              {LIGHT_ROYAL}│{RESET}
{LIGHT_ROYAL}│                                                                      │{RESET}
{BRIGHT_ROYAL}└──────────────────────────────────────────────────────────────────────┘{RESET}

{RED}⚠️  WARNING: For Educational and Authorized Testing Only!{RESET}
{LIGHT_ROYAL}═══════════════════════════════════════════════════════════════════════════{RESET}
"""

def show_logo():
    """Display the 3D ASCII logo with usage commands"""
    print(LOGO)

# --- CONFIGURABLE STATIC KEY (32 bytes for AES-256) ---
# For production, use a secure key exchange!
SECRET_KEY = b"this_is_a_very_secret_key_32byte"

# --- AES-256-CBC ENCRYPTION HELPERS ---

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    if pad_len > AES.block_size:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(data))
    return iv + ct

def decrypt(data, key):
    iv = data[:AES.block_size]
    ct = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct))

# --- NETWORK HELPERS ---

def send_encrypted(sock, data, key):
    enc = encrypt(data, key)
    sock.sendall(struct.pack(">I", len(enc)) + enc)

def recv_encrypted(sock, key):
    rawlen = recvall(sock, 4)
    if not rawlen:
        return None
    msglen = struct.unpack(">I", rawlen)[0]
    data = recvall(sock, msglen)
    if not data:
        return None
    return decrypt(data, key)

def recvall(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

# --- FILE TRANSFER HELPERS ---

def send_file(sock, filepath, key):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        send_encrypted(sock, b"FILE " + os.path.basename(filepath).encode() + b" " + str(len(data)).encode(), key)
        send_encrypted(sock, data, key)
    except Exception as e:
        send_encrypted(sock, f"ERROR {e}".encode(), key)

def recv_file(sock, key, filename, filesize):
    data = recv_encrypted(sock, key)
    if data and len(data) == int(filesize):
        with open(filename, "wb") as f:
            f.write(data)
        return True
    return False

# --- SHELL COMMAND EXECUTION ---

def run_command(cmd):
    try:
        if platform.system() == "Windows":
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, executable="/bin/bash")
        out, err = proc.communicate()
        return out + err
    except Exception as e:
        return str(e).encode()

# --- SERVER HANDLER ---

def handle_client(conn, addr, args):
    print(f"[+] Connection from {addr}")
    try:
        while True:
            data = recv_encrypted(conn, SECRET_KEY)
            if not data:
                break
            if data.startswith(b"SHELL"):
                send_encrypted(conn, b"Shell ready. Type commands.", SECRET_KEY)
                while True:
                    cmd = recv_encrypted(conn, SECRET_KEY)
                    if not cmd or cmd.strip() in [b"exit", b"quit"]:
                        break
                    output = run_command(cmd.decode())
                    send_encrypted(conn, output, SECRET_KEY)
            elif data.startswith(b"UPLOAD"):
                _, filename, filesize = data.decode().split()
                if recv_file(conn, SECRET_KEY, filename, filesize):
                    send_encrypted(conn, b"Upload complete.", SECRET_KEY)
                else:
                    send_encrypted(conn, b"Upload failed.", SECRET_KEY)
            elif data.startswith(b"DOWNLOAD"):
                _, filename = data.decode().split()
                send_file(conn, filename, SECRET_KEY)
            else:
                # Echo mode
                send_encrypted(conn, b"OK: " + data, SECRET_KEY)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected {addr}")

def server(args):
    proto = socket.SOCK_DGRAM if args.u else socket.SOCK_STREAM
    s = socket.socket(socket.AF_INET, proto)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((args.t, args.p))
    if not args.u:
        s.listen(5)
        print(f"[+] Listening on {args.t}:{args.p} (TCP)")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, args), daemon=True).start()
    else:
        print(f"[+] Listening on {args.t}:{args.p} (UDP)")
        while True:
            data, addr = s.recvfrom(65535)
            # For UDP, no encryption for simplicity, but can be added
            print(f"[UDP] {addr}: {data.decode()}")

# --- CLIENT ---

def client(args):
    proto = socket.SOCK_DGRAM if args.u else socket.SOCK_STREAM
    s = socket.socket(socket.AF_INET, proto)
    if not args.u:
        s.connect((args.t, args.p))
    else:
        # UDP: no connect, just sendto/recvfrom
        pass

    def send_recv(msg):
        send_encrypted(s, msg.encode(), SECRET_KEY)
        resp = recv_encrypted(s, SECRET_KEY)
        if resp:
            print(resp.decode(errors="ignore"))

    try:
        if args.shell:
            send_encrypted(s, b"SHELL", SECRET_KEY)
            print(recv_encrypted(s, SECRET_KEY).decode())
            while True:
                cmd = input("Shell> ")
                if cmd.strip() in ["exit", "quit"]:
                    break
                send_encrypted(s, cmd.encode(), SECRET_KEY)
                output = recv_encrypted(s, SECRET_KEY)
                print(output.decode(errors="ignore"))
        elif args.upload:
            send_encrypted(s, f"UPLOAD {os.path.basename(args.upload)} {os.path.getsize(args.upload)}".encode(), SECRET_KEY)
            with open(args.upload, "rb") as f:
                send_encrypted(s, f.read(), SECRET_KEY)
            print(recv_encrypted(s, SECRET_KEY).decode())
        elif args.download:
            send_encrypted(s, f"DOWNLOAD {args.download}".encode(), SECRET_KEY)
            meta = recv_encrypted(s, SECRET_KEY)
            if meta and meta.startswith(b"FILE"):
                _, filename, filesize = meta.decode().split()
                if recv_file(s, SECRET_KEY, filename, filesize):
                    print("Download complete.")
                else:
                    print("Download failed.")
            else:
                print(meta.decode())
        else:
            # Simple chat/echo
            while True:
                msg = input("> ")
                if not msg:
                    break
                send_recv(msg)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        s.close()

# --- ARGUMENT PARSING ---

def main():
    # Display the 3D ASCII logo with commands on startup
    show_logo()
    
    parser = argparse.ArgumentParser(
        description=f"{ROYAL_BLUE}Enhanced Netcat - Encrypted Multi-Client Netcat Clone{RESET}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True
    )
    parser.add_argument("-l", action="store_true", help="Listen mode (server)")
    parser.add_argument("-t", metavar="TARGET", default="0.0.0.0", help="Target IP (default: 0.0.0.0)")
    parser.add_argument("-p", metavar="PORT", type=int, required=True, help="Port (required)")
    parser.add_argument("-u", action="store_true", help="UDP mode (default: TCP)")
    parser.add_argument("--shell", action="store_true", help="Interactive shell (client mode)")
    parser.add_argument("--upload", metavar="FILE", help="Upload file to server")
    parser.add_argument("--download", metavar="FILE", help="Download file from server")
    args = parser.parse_args()

    if args.l:
        server(args)
    else:
        client(args)

if __name__ == "__main__":
    main()
