import requests
import psycopg2
from faker import Faker
import random
import requests
import psycopg2
from faker import Faker
import random
import getpass

def get_database_config():
    print("=" * 60)
    print("CONFIGURAÇÃO DO BANCO POSTGRESQL")
    print("Por segurança, todos os dados serão ocultados durante a digitação")
    print("=" * 60)
    host_input = getpass.getpass("Host do banco (pressione Enter para localhost): ").strip()
    host = host_input if host_input else 'localhost'
    port_input = getpass.getpass("Porta do banco (pressione Enter para 5432): ").strip()
    port = port_input if port_input else '5432'
    database = getpass.getpass("Nome do banco de dados: ").strip()
    user = getpass.getpass("Nome de usuário: ").strip()
    password = getpass.getpass("Senha: ")
    if not database or not user:
        print("Nome do banco e usuário são obrigatórios!")
        return None
    confirm = input("\nConfirmar configuração? (s/N): ").strip().lower()
    if confirm not in ['s', 'sim', 'y', 'yes']:
        print("Configuração cancelada!")
        return None
    return {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }

URL = "http://localhost:8086/administracao/departamento"
faker = Faker('pt_BR')
TIPOS_DEPARTAMENTOS = [
    "Recursos Humanos", "Financeiro", "Marketing", "Vendas", "TI", "Logística", "Jurídico", "Operações", "Compras", "Pesquisa e Desenvolvimento"
]
# Gera e cadastra departamentos aleatórios
if __name__ == "__main__":
    db_config = get_database_config()
    if not db_config:
        exit()
    token = getpass.getpass("Token Bearer para autenticação: ").strip()
    HEADERS = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    conn = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    qtd_departamentos = random.randint(5, 15)
    for _ in range(qtd_departamentos):
        nome_departamento = faker.word().capitalize()
        if random.random() < 0.5:
            nome_departamento = random.choice(TIPOS_DEPARTAMENTOS)
        payload = {
            "nomeDepartamento": nome_departamento
        }
        response = requests.post(URL, json=payload, headers=HEADERS)
        print(f"Departamento: {nome_departamento} - Status: {response.status_code}")
    conn.close()
qtd_departamentos = random.randint(5, 15)
for _ in range(qtd_departamentos):
    nome_departamento = faker.word().capitalize()
    if random.random() < 0.5:
        nome_departamento = random.choice(TIPOS_DEPARTAMENTOS)
    payload = {
        "nomeDepartamento": nome_departamento
    }
    response = requests.post(URL, json=payload, headers=HEADERS)
    print(f"Departamento: {nome_departamento} - Status: {response.status_code}")

conn.close()
