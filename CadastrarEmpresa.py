import requests
import time
import random
import uuid

url = "http://localhost:8085/register"

def generate_random_data():

    # Listas mais diversificadas para gerar nomes aleatórios
    prefixos = [
        "Comercial", "Empresa", "Grupo", "Indústria", "Tecnologia", "Serviços", "Soluções", "Corporação",
        "Consultoria", "Distribuidora", "Importadora", "Exportadora", "Matriz", "Holding", "Companhia",
        "Organização", "Instituto", "Central", "União", "Federação", "Associação", "Cooperativa"
    ]
    
    sufixos = [
        "Brasil", "Nacional", "Internacional", "Global", "Premium", "Express", "Digital", "Systems", "Tech", "Plus",
        "Solutions", "Corporation", "Enterprises", "Industries", "Commerce", "Trading", "Logistics", "Advanced",
        "Innovation", "Excellence", "Quality", "Professional", "Master", "Elite", "Prime", "Royal", "Supreme",
        "Ultimate", "Mega", "Super", "Ultra", "Max", "Pro", "Smart", "Fast", "Direct", "Secure"
    ]
    
    # Nomes próprios para adicionar variedade
    nomes_proprios = [
        "Alpha", "Beta", "Gamma", "Delta", "Omega", "Sigma", "Phoenix", "Titan", "Atlas", "Apollo",
        "Zeus", "Mercury", "Jupiter", "Saturn", "Venus", "Mars", "Neptune", "Orion", "Centauro",
        "Pegasus", "Hercules", "Athena", "Minerva", "Victoria", "Aurora", "Luna", "Stella"
    ]
    
    # Gerar nome aleatório usando diferentes combinações
    tipo_nome = random.randint(1, 4)
    
    if tipo_nome == 1:
        # Prefixo + Sufixo
        name = f"{random.choice(prefixos)} {random.choice(sufixos)}"
    elif tipo_nome == 2:
        # Nome próprio + Sufixo
        name = f"{random.choice(nomes_proprios)} {random.choice(sufixos)}"
    elif tipo_nome == 3:
        # Prefixo + Nome próprio
        name = f"{random.choice(prefixos)} {random.choice(nomes_proprios)}"
    else:
        # Nome próprio simples
        name = f"{random.choice(nomes_proprios)} {random.choice(['Corp', 'Inc', 'Ltd', 'S.A.', 'Ltda'])}"
    
    # Criar e-mail baseado no nome da empresa
    email_base = name.lower().replace(" ", "").replace("ç", "c").replace("õ", "o").replace(".", "")
    email = f"{email_base}@empresa.com"
    
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

    time.sleep(1) 