# Made with <3 by Nekoraru22
# GitHub: 

import requests, re, os, zipfile
from bs4 import BeautifulSoup
from colorama import Fore
from selenium import webdriver

# Colors
##############################
green = Fore.LIGHTGREEN_EX
cyan = Fore.LIGHTCYAN_EX
white = Fore.LIGHTWHITE_EX
magenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.LIGHTYELLOW_EX
reset = Fore.RESET
##############################

# Functions
def download(url):
    print(f"{white}[{cyan}+{white}] {cyan}Downloading...{reset}")
    pre = re.findall(r"path=(.+)\/",url)[0]
    last_url = f"https://chromedriver.storage.googleapis.com/{pre}/chromedriver_win32.zip"
    # print(last_url)

    try: os.remove("chromedriver.exe")
    except: None

    r = requests.get(last_url, allow_redirects=True)
    with open('extract.zip', 'wb') as file:
        file.write(r.content)
        file.close()


    with zipfile.ZipFile("extract.zip", 'r') as zip_ref:
        zip_ref.extractall()

    try: os.remove("extract.zip")
    except: None

def get_update(actual_version, new_version):
    print(f"{white}[{green}+{white}] {green}New chromedriver update!{yellow}\n\tActual version: {white}{actual_version}{yellow}\n\tNew version: {white}{new_version}{reset}")

    r = requests.get('https://chromedriver.chromium.org/downloads')
    soup = BeautifulSoup(r.text, 'lxml')
    versions = soup.find_all('span', {'class','aw5Odc'})

    # with open("meow.txt", 'w+') as file:
    #     file.write(str(soup))
    #     file.close()

    for item in versions:
        version = item.findChildren("strong")
        if len(version) == 1:
            simple_version = re.findall(r"ChromeDriver ([0-9]+)", str(version))[0]
            
            if simple_version == new_version:
                url1 = item.findChildren("a")[0]["href"]
                download(url1)
                return

def get_version(error):
    new_version = re.findall(r"browser version is ([0-9]+)", str(error))
    actual_version = re.findall(r"Chrome version ([0-9]+)", str(error))
    get_update(actual_version[0], new_version[0])

def download_last():
    r = requests.get('https://chromedriver.chromium.org/downloads')
    soup = BeautifulSoup(r.text, 'lxml')
    versions = soup.find_all('span', {'class','aw5Odc'})
    
    for item in versions:
        version = item.findChildren("strong")
        if len(version) == 1:
            url1 = item.findChildren("a")[0]["href"]
            download(url1)
            break

# Start
try:
    browser = webdriver.Chrome(executable_path='./chromedriver')
except Exception as error:
    if "executable needs to be in PATH" in str(error):
        download_last()
        try:
            browser = webdriver.Chrome(executable_path='./chromedriver')
        except Exception as error:
            get_version(error)
    else:
        get_version(error)
    print(f"{white}[{green}+{white}] {green}Downloaded!{reset}")