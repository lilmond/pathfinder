from urllib.parse import urlparse, urljoin
import threading
import argparse
import logging
import socket
import socks
import time
import ssl
import sys
import os

class Colors:
    RED = "\u001b[31;1m"
    GREEN = "\u001b[32;1m"
    YELLOW = "\u001b[33;1m"
    BLUE = "\u001b[34;1m"
    PURPLE = "\u001b[35;1m"
    CYAN = "\u001b[36;1m"
    RESET = "\u001b[0;0m"

BANNER = f"""{Colors.PURPLE}.__     , .  .___      .      
[__) _.-+-|_ [__ *._  _| _ ._.
|   (_] | [ )|   |[ )(_](/,[  
{Colors.RESET}"""

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def check_http(url: str, headers: dict = None, proxy: str = None, no_verify: bool = False):
    target_url = urlparse(url)

    if not target_url.port:
        if target_url.scheme == "https":
            port = 443
        else:
            port = 80
    else:
        port = target_url.port
    
    if proxy:
        logger.debug(f"Using proxy {proxy}...")
        sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_url = urlparse(proxy)
        proxy_type = getattr(socks, f"PROXY_TYPE_{proxy_url.scheme.upper()}")
        sock.set_proxy(proxy_type=proxy_type, addr=proxy_url.hostname, port=proxy_url.port)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if target_url.scheme == "https":
        ctx = ssl.create_default_context()
        if no_verify:
            logger.debug("Using no verify mode...")
            ctx.check_hostname = False
            ctx.verify_mode = ssl.VerifyMode.CERT_NONE
            sock = ctx.wrap_socket(sock=sock)
        else:
            sock = ctx.wrap_socket(sock=sock, server_hostname=target_url.hostname)

    logger.debug(f"Connecting to {Colors.BLUE}{target_url.hostname}:{port}{Colors.RESET}...")
    sock.connect((target_url.hostname, port))

    http_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #"accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "connection": "keep-alive",
        "dnt": "1",
        "host": f"{target_url.hostname}" + (f":{port}" if not port in [80, 443] else ""),
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    if headers:
        for header in headers:
            header_name, header_value = header.split(":", 1)
            header_name = header_name.strip()
            header_value = header_value.strip()

            http_headers[header_name] = header_value

    http_header = f"GET {target_url.path} HTTP/1.1\r\n"

    for header in http_headers:
        http_header += f"{header}: {http_headers[header]}\r\n"

    http_header += "\r\n"
    
    sock.send(http_header.encode())

    line1_response = b""

    while True:
        chunk = sock.recv(1)

        if not chunk:
            raise Exception("Connection closed unexpectedly.")
        
        line1_response += chunk
        
        if line1_response.endswith(b"\r\n"):
            break
    
    line1_response = line1_response.decode().strip()
    http_version, http_status_code = line1_response.split(" ", 1)
    
    if http_status_code.startswith("2"):
        color = Colors.GREEN
    else:
        color = Colors.RED

    logger.info(f"URL: {Colors.BLUE}{url}{Colors.RESET} | {color}{http_status_code}{Colors.RESET}")
        
def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform in ["linux", "linux2"]:
        os.system("clear")

def main():
    clear_console()

    print(BANNER)
    
    parser = argparse.ArgumentParser(description=f"A simple and fast web server path finder.")
    parser.add_argument("url", metavar="URL", type=str, help="Target URL.")
    parser.add_argument("-pf", "--paths-file", metavar="FILE", type=str, required=True, help="Path to URL path list file.")
    parser.add_argument("-t", "--threads", metavar="THREADS", type=int, default=10, help="This tool is multithreaded by default, the default threads is set to 10.")
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on debug mode.")
    parser.add_argument("-p", "--proxy", metavar="PROXY URL", type=str, help="Use proxy? If so, use this example's format: socks5://127.0.0.1:9050")
    parser.add_argument("-nv", "--no-verify", action="store_true", help="Turn SSL no verify mode on.")
    parser.add_argument("--header", action="append", help="Add a custom HTTP header, example: --header \"Authorization: TOKEN\"")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        with open(args.paths_file, "r") as file:
            path_list = file.read().splitlines()
            file.close()

        logger.info(f"Loaded {Colors.BLUE}{len(path_list)}{Colors.RESET} paths from {Colors.BLUE}{args.paths_file}{Colors.RESET}")
    except Exception as e:
        print(f"error: {e}")
        return
    
    logger.info(f"Checking (URL: {Colors.BLUE}{args.url}{Colors.RESET}) availability...")

    check_http(args.url, args.header, proxy=args.proxy, no_verify=args.no_verify)

    for path in path_list:
        url = urljoin(args.url, path)
        
        while True:
            if ((threading.active_count() - 1) >= args.threads):
                time.sleep(0.05)
                continue

            threading.Thread(target=check_http, args=[url, args.header, args.proxy, args.no_verify], daemon=True).start()
            break
    
    while True:
        if (threading.active_count() - 1) == 0:
            break
        time.sleep(0.1)

if __name__ == "__main__":
    main()
