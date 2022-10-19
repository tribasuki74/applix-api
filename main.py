from fastapi import FastAPI
import env_lab
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from model import Login
import psutil
import os

app = FastAPI()-

@app.get("/")
async def root():
    return {"message": "Applix-API version 1.0"}, 200

@app.get("/healthz")
async def healthz():
    return {"message": "Healthy", "status":True}, 200

@app.post("/login")
async def login(login: Login):
    token, status = get_login(login)
    if status:
        return {"token": token}, 200
    else:
        return {"message": "Login failed"}, 200

def get_login(login):
    # if (login.username == 'tribasuki') & (login.password == 'tribasuki123'):
    if checkUserExist(login): 
        token = get_token()
        return token, True
    else:
        return "", False

def checkUserExist(login):
    exist = False
    with open("data/users.csv") as data:
        Lines = data.readlines()
        for row in Lines:
            rows = row.split(";")
            print(rows[0], rows[1], rows[2], rows[3])
            if (login.username == rows[1]) & (login.password == rows[2]):
                exist = True
                break
    return exist
       
def get_token(host=env_lab.DNA_CENTER['host'],
              username=env_lab.DNA_CENTER['username'],
              password=env_lab.DNA_CENTER['password'],
              port=env_lab.DNA_CENTER['port']):
    """
    Use the REST API to log into an DNA_CENTER and retrieve a token
    """
    url = "https://{}:{}/dna/system/api/v1/auth/token".format(host,port)
    # Make Login request and return the response body
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), verify=False)
    token = response.json()["Token"]
    return token


@app.get("/stats")
async def statistic():
    stats = psutil.virtual_memory()  # returns a named tuple
    available = getattr(stats, 'available')
    ram_free = round(available / 1048576, 2)

    uptime = "XX:XX:XX:XX"
    pid = os.getpid()

    p = next((proc for proc in psutil.process_iter() if proc.pid == pid),None)
    prio = p.nice()

    proc = "X"
    data = {
        "ram_free": ram_free,
        "uptime": uptime,
        "api_pid": pid,
        "api_prio": prio,
        "total_proc": proc
    }
    return data, 200
