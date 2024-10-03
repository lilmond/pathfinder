# pathfinder
A simple, fast and reliable HTTP web server path finder written in Python.

# Installation
Linux
```
git clone https://github.com/lilmond/pathfinder
cd pathfinder
pip install -r requirements.txt
```

# Usage help
```
python pathfinder.py --help
```
```
.__     , .  .___      .
[__) _.-+-|_ [__ *._  _| _ ._.
|   (_] | [ )|   |[ )(_](/,[

usage: pathfinder.py [-h] -pf FILE [-t THREADS] [-d] [-p PROXY URL] [-nv] [--header HEADER] URL

A simple and fast web server path finder.

positional arguments:
  URL                   Target URL.

options:
  -h, --help            show this help message and exit
  -pf FILE, --paths-file FILE
                        Path to URL path list file.
  -t THREADS, --threads THREADS
                        This tool is multithreaded by default, the default threads is set to 10.
  -d, --debug           Turn on debug mode.
  -p PROXY URL, --proxy PROXY URL
                        Use proxy? If so, use this example's format: socks5://127.0.0.1:9050
  -nv, --no-verify      Turn SSL no verify mode on.
  --header HEADER       Add a custom HTTP header, example: --header "Authorization: TOKEN"
```

# Usage
```
python pathfinder.py https://www.roblox.com/ -pf pathlist\pathlist2.txt
```
```
.__     , .  .___      .
[__) _.-+-|_ [__ *._  _| _ ._.
|   (_] | [ )|   |[ )(_](/,[

[10-03-2024 13:27:47][INFO] Loaded 3 paths from pathlist\pathlist2.txt
[10-03-2024 13:27:47][INFO] Checking (URL: https://www.roblox.com/) availability...
[10-03-2024 13:27:48][INFO] URL: https://www.roblox.com/ | HTTP/1.1 200 OK
[10-03-2024 13:27:48][INFO] URL: https://www.roblox.com/admin | HTTP/1.1 404 Not Found
[10-03-2024 13:27:48][INFO] URL: https://www.roblox.com/test | HTTP/1.1 404 Not Found
[10-03-2024 13:27:48][INFO] URL: https://www.roblox.com/login | HTTP/1.1 200 OK
```

# Usage with Tor proxy and debug mode on.
```
python pathfinder.py https://www.roblox.com/ -pf pathlist\pathlist2.txt -p socks5://127.0.0.1:9050 -d
```
```
.__     , .  .___      .
[__) _.-+-|_ [__ *._  _| _ ._.
|   (_] | [ )|   |[ )(_](/,[

[10-03-2024 13:30:57][INFO] Loaded 3 paths from pathlist\pathlist2.txt
[10-03-2024 13:30:57][INFO] Checking (URL: https://www.roblox.com/) availability...
[10-03-2024 13:30:57][DEBUG] Using proxy socks5://127.0.0.1:9050...
[10-03-2024 13:30:57][DEBUG] Connecting to www.roblox.com:443...
[10-03-2024 13:30:58][INFO] URL: https://www.roblox.com/ | HTTP/1.1 200 OK
[10-03-2024 13:30:58][DEBUG] Using proxy socks5://127.0.0.1:9050...
[10-03-2024 13:30:58][DEBUG] Using proxy socks5://127.0.0.1:9050...
[10-03-2024 13:30:58][DEBUG] Using proxy socks5://127.0.0.1:9050...
[10-03-2024 13:30:58][DEBUG] Connecting to www.roblox.com:443...
[10-03-2024 13:30:58][DEBUG] Connecting to www.roblox.com:443...
[10-03-2024 13:30:58][DEBUG] Connecting to www.roblox.com:443...
[10-03-2024 13:30:58][INFO] URL: https://www.roblox.com/admin | HTTP/1.1 404 Not Found
[10-03-2024 13:30:58][INFO] URL: https://www.roblox.com/test | HTTP/1.1 404 Not Found
[10-03-2024 13:30:58][INFO] URL: https://www.roblox.com/login | HTTP/1.1 200 OK
```
