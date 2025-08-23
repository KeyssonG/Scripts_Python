import requests
import psycopg2
from faker import Faker
import random
import getpass
import time

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

URL = "http://localhost:8087/cadastrar/funcionario-cliente"
def get_departamentos(cursor, company_id):
    cursor.execute("SELECT departamento FROM departamentos WHERE company_id = %s", (company_id,))
    return [row[0] for row in cursor.fetchall()]
SEXO = ["M", "F"]

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
    company_id = input("Informe o company_id para buscar os departamentos: ").strip()
    departamentos = get_departamentos(cursor, company_id)
    if not departamentos:
        print("Nenhum departamento encontrado para o company_id informado.")
        conn.close()
        exit()
    faker = Faker('pt_BR')
    qtd_funcionarios = random.randint(5, 15)
    for _ in range(qtd_funcionarios):
        nome = faker.name()
        data_nascimento = faker.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d')
        telefone = faker.msisdn()[:11]
        email = faker.email()
        cpf = faker.cpf()
        endereco = faker.address().replace('\n', ', ')
        sexo = random.choice(SEXO)
        username = faker.user_name()
        departamento = random.choice(departamentos)
        payload = {
            "nome": nome,
            "dataNascimento": data_nascimento,
            "telefone": telefone,
            "email": email,
            "cpf": cpf,
            "endereco": endereco,
            "sexo": sexo,
            "username": username,
            "departamento": departamento
        }
        response = requests.post(URL, json=payload, headers=HEADERS)
        print(f"Funcionário: {nome} - Departamento: {departamento} - Status: {response.status_code}")
        time.sleep(2)  # Aguarda 2 segundos para processamento da proc
    conn.close()
