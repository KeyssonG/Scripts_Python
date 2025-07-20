import requests
import time
import random
import uuid

url = "http://localhost:8085/register"

def generate_random_data():
    name = f"Empresa {random.randint(1, 1000)}"
    email = f"contato{random.randint(1, 1000)}@empresa.com"
    cnpj = str(random.randint(10000000000000, 99999999999999))
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = f"Senha#{random.randint(1000, 9999)}"
    return {
        "name": name,
        "email": email,
        "cnpj": cnpj,
        "username": username,
        "password": password
    }


while True:
    data = generate_random_data()

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"Requisição bem-sucedida: {response.json()}")
        else:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")

time.sleep(60) 