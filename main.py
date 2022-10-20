from fastapi import FastAPI
import env_lab
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from model import Login, Customer
import psutil
import os
import time
from decode import DecodeToken
import json

app = FastAPI()

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
    ram_free = str(int(round(available / 1048576, 0)))

    totalSeconds = time.time() - psutil.boot_time()
    seconds = int(totalSeconds % 60);
    minutes = int((totalSeconds % 3600) / 60);
    hours = int((totalSeconds % 86400) / 3600);
    days = int((totalSeconds % (86400 * 30)) / 86400);

    uptime = "{:02d}:{:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds)
    pid = os.getpid()

    p = next((proc for proc in psutil.process_iter() if proc.pid == pid), None)
    prio = p.nice()
 
    proc = str(sum(1 for proc in psutil.process_iter()))
 
    data = {
        "ram_free": ram_free,
        "uptime": uptime,
        "api_pid": str(pid),
        "api_prio": prio,
        "total_proc": proc
    }
    return data, 200

@app.get("/whoami")
async def whoami(token: str):
    decode = DecodeToken.decode(token)
    response = {"username": decode['username'] }
    return response, 200

@app.put("/customers/")
async def addNewCustomer(customer: Customer):
    if checkUnique(customer):
        # save into customers.csv
        response = saveNewCustomer(customer)
        return response, 200
    else:
        return {"message": "HTTP Forbidden error" }, 403

def saveNewCustomer(customer):
    customers = []
    with open("data/customers.json") as data:
        json_data = data.read()
        customers = json.loads(json_data)
    customer = {
        "name": customer.name,
        "domain_prefix": customer.domain_prefix,
        "username": customer.username,
        "password": customer.password,
        "message": customer.message
    }
    customers.append(customer)
    with open("data/customers.json", "w") as fh: 
        json.dump(customers, fh, indent = 4)
    return customer

def checkUnique(customer):
    with open("data/customers.json") as data:
        json_data = data.read()
        customers = json.loads(json_data)
        print(customers)
        name = customer.name
        dp = customer.domain_prefix
        un = customer.username

        unique = True
        for cust in customers:
            if (name == cust['name']) | (dp == cust['domain_prefix']) | \
                (un == cust['username']):
                unique = False
                break
    return unique

@app.get("/network/devices/stats")
async def getDeviceStatistic(token: str, management_ip: str = ""):
    host = env_lab.DNA_CENTER['host']
    port = env_lab.DNA_CENTER['port']
    if management_ip == "":
        url = "https://{}:{}/api/v1/network-device".format(host,port)
    else:
        url = "https://{}:{}/api/v1/network-device?managementIpAddress={}" \
            .format(host,port,management_ip)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
    device_list = resp.json()["response"]
    devices = []
    if len(device_list) > 0:
        for deviceItem in device_list:
            print(deviceItem)
            deviceId = deviceItem["id"]
            interfaces = []
            # call interface based on device id
            url = "https://{}:{}/api/v1/interface?deviceId={}".format(host,port,deviceId)
            hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
            resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
            interface_info_list = resp.json()['response']
            for interfaceItem in interface_info_list:
                if "in-unicast-pkts" in interfaceItem:
                    pktsIn = interfaceItem["in-unicast-pkts"]
                else:
                    pktsIn = "None"
                if "out-unicast-pkts" in interfaceItem:
                    pktsOut = interfaceItem["out-unicast-pkts"]
                else:
                    pktsOut = "None"

                interface = {
                    "name": interfaceItem["portName"],
                    "mac": interfaceItem["macAddress"],
                    "ip": interfaceItem["ipv4Address"],
                    "pkts-in": pktsIn,
                    "pkts-out": pktsOut
                }
                interfaces.append(interface)
            device = {
                "hostname": deviceItem["hostname"],
                "management_ip": deviceItem["managementIpAddress"],
                "ios_version": deviceItem["softwareVersion"],
                "interfaces": interfaces
            }
            devices.append(device)
    else:
        response = {"mesage": "HTTP not found error"}
        return response, 200

    return {"devices": devices}, 200