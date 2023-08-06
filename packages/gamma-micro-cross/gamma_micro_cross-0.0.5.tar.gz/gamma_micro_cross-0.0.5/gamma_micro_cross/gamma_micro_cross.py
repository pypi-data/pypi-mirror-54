import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
import bs4

def README():
    print("Make sure that u have install package below:")
    print("requests,pandas,bs4")
    print("Two functions available in this package:")
    print("get_gamma_cross_forSigle(atom_number,energy)")
    print("get_gamma_cross_forRange(atom_number,energy_down,energy_up)")

url = "https://physics.nist.gov/cgi-bin/Xcom/xcom3_1"
headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Host" : "physics.nist.gov",
        "Referer" : "https://physics.nist.gov/cgi-bin/Xcom/xcom2"
    }
#the function below for get cross_section for special Energy,for exampel E=0.1MeV
def get_gamma_cross_forSingle(atom_number,energy_Mev):
    print("Please wait,loading data...")

    data = {
        "ZNum" : atom_number,
        "ZSym" : "",
        "OutOpt" : "PIC",
        "Graph6" : "on",
        "NumAdd" : "1",
        "Energies" : energy_Mev,
        "WindowXmin" : "",
        "WindowXmax" : "",
        "ResizeFlag" : "on"
    }
    response = requests.post(url = url,data=data)
    page_text = response.text
    #print(page_text)
    soup = BeautifulSoup(page_text,'lxml') 
    trs = soup.find_all('tr') 
    ulist = []
    for tr in trs: 
        ui = [] 
        for td in tr: 
            ui.append(td.string) 
        ulist.append(ui)
    print("Energy:{}".format(ulist[4][2]))
    print("Total Attenuation :{}".format(ulist[4][-2]))
    print("Scattering:{}".format(ulist[4][3]))
    print("Photoelectric Absorption:{}".format(ulist[4][5]))

def get_gamma_cross_forRange(atom_number,E_Down,E_Up):
    print("Please wait,loading data...")
    data = {
    "ZNum" : atom_number,
    "ZSym" : "",
    "OutOpt" : "PIC",
    "Graph6" : "on",
    "NumAdd" : "1",
    "Energies" : "",
    "Output" : "on",
    "WindowXmin" : E_Down,
    "WindowXmax" : E_Up,
    "ResizeFlag" : "on"
    }
    response = requests.post(url = url,data=data)
    page_text = response.text
    #print(page_text)
    soup = BeautifulSoup(page_text,'lxml') 
    trs = soup.find_all('tr') 
    ulist = []
    for tr in trs: 
        ui = [] 
        for td in tr: 
            ui.append(td.string) 
        ulist.append(ui)
    print("Energy/Mev|Total Attenuation|Scattering|Photoelectric Absorption")
    for i in range(4,len(ulist)):
        print(ulist[i][2],end="  ")
        print(ulist[i][-2],end="         ")
        print(ulist[i][3],end="  ")
        print(ulist[i][5])