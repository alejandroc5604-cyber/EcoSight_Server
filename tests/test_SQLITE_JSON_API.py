#in this file, we are going to test the API endpoints for the http transfer

import requests
import random


def test_SetupDatabase(base_url):
    #testing the 
    endpoint = "/BuildDatabase"
    access = base_url + endpoint
    print(access)
    try:
        x = requests.get(access)
        print(x.text)
    except requests.exceptions.ConnectionError:
        print("Start Unicorn, or check the baseURL")


def test_ReturnJSONData(base_url):
    #testing the testReturnJSONData

    LIMIT = 100

    endpoint = "/ReturnJSONData"
    access = base_url + endpoint + f"?limit={LIMIT}"
    print(access)
    try:
        x = requests.get(access)
        print(x.text)
    except requests.exceptions.ConnectionError:
        print("Start Unicorn, or check the baseURL")


def test_AddToDatabase(base_url):
    #testing the 

    image_path = "data"
    latitude, longitude= -1.2864, 36.8172
    params = {
        "Type": random.choice(["plastic","metal","paper","glass"]),
        "confidence_score": random.randint(1, 10000) / 100,
        "image_path": image_path,
        "latitude": latitude,
        "longitude": longitude,
    }
    endpoint = base_url + "/AddToDatabase"
    
    try:
        x = requests.get(endpoint, params=params)
        print(x.text)
    except requests.exceptions.ConnectionError:
        print("Start Unicorn, or check the baseURL")




if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:8000"
    test_SetupDatabase(BASE_URL)
    for i in range(100):
        test_AddToDatabase(BASE_URL)
    test_ReturnJSONData(BASE_URL)